from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .core import collect_memory_records

MAX_QUERY_CHARS = 500
MAX_PACK_RECORDS = 20
DEFAULT_PACK_RECORDS = 8
TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9_.-]*")
SECRET_RE = re.compile(
    r"-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----"
    r"|\bsk-(ant|proj)-[A-Za-z0-9_-]{20,}"
    r"|\bghp_[A-Za-z0-9]{20,}"
    r"|\bgithub_pat_[A-Za-z0-9_]{20,}"
    r"|\bAKIA[0-9A-Z]{16}\b"
    r"|(?i:\b(api[_-]?key|token|secret|password)\s*=\s*['\"]?"
    r"(?!your|example|changeme|redacted|none)[A-Za-z0-9_\-]{12,})"
)
STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "our",
    "the",
    "to",
    "we",
    "what",
    "when",
    "with",
}


def build_context_pack(root: Path, query: str, limit: int = DEFAULT_PACK_RECORDS) -> dict[str, Any]:
    """Return a compact, pointer-only memory packet for a task query."""
    root = root.resolve()
    clean_query = _clean_query(query)
    safe_limit = _clean_limit(limit)
    terms = _query_terms(clean_query)

    records = collect_memory_records(root)
    ranked = sorted(
        (
            {
                "id": f"R{index}",
                "score": _score_record(record, terms),
                "path": record["path"],
                "title": record["title"],
                "type": record.get("type", ""),
                "status": record.get("status", ""),
                "tags": record.get("tags", []),
                "valid_from": record.get("valid_from", ""),
                "valid_to": record.get("valid_to", ""),
                "source_bytes": _source_size(root, record),
            }
            for index, record in enumerate(records)
        ),
        key=lambda item: (-item["score"], _status_rank(str(item["status"])), str(item["path"])),
    )
    selected = [
        {**record, "id": f"R{index}"}
        for index, record in enumerate(record for record in ranked if record["score"] > 0)
    ][:safe_limit]

    payload = {
        "schema_version": "FCP/1",
        "query": clean_query,
        "mode": "pointer-only",
        "record_count": len(records),
        "returned": len(selected),
        "source_bytes_if_loaded": sum(int(record["source_bytes"]) for record in selected),
        "corpus_source_bytes": sum(int(record["source_bytes"]) for record in ranked),
        "records": selected,
        "instructions": [
            "Use this packet as an index, not as source text.",
            "Read only the listed files that are needed for the task.",
            "When exact wording matters, open the source path before deciding.",
            "Never store or repeat secrets in memory packets.",
        ],
    }
    return add_context_pack_measurement(payload)


def render_context_pack(payload: dict[str, Any]) -> str:
    """Render a Forge Context Packet in the compact FCP/1 text format."""
    measurement = payload.get("measurement") if isinstance(payload.get("measurement"), dict) else {}
    lines = [
        "FCP/1",
        f"Q={_compact(payload.get('query', ''))}",
        "MODE=PTR",
        "LOSSLESS=BY_REFERENCE",
        f"RECORDS={payload.get('returned', 0)}/{payload.get('record_count', 0)}",
        "MEASURE=UTF8_BYTES;TOKEN_EST=BYTES/4",
        f"FCP_BYTES={measurement.get('packet_bytes', 0)}",
        f"SELECTED_SRC_BYTES={measurement.get('selected_source_bytes', payload.get('source_bytes_if_loaded', 0))}",
        f"ALL_MEMORY_BYTES={measurement.get('corpus_source_bytes', payload.get('corpus_source_bytes', 0))}",
        f"SAVE_SELECTED={measurement.get('savings_vs_selected_percent', 'NA')}%",
        f"SAVE_ALL={measurement.get('savings_vs_corpus_percent', 'NA')}%",
        "RULE=READ_LISTED_SOURCE_ONLY_WHEN_NEEDED",
        "LEGEND=R|S=score|T=type|ST=status|G=tags|P=path|H=heading",
    ]
    for index, record in enumerate(payload.get("records", [])):
        tags = ",".join(str(tag) for tag in record.get("tags", []))
        record_id = _compact(record.get("id") or f"R{index}")
        lines.append(
            f"{record_id}|S={record.get('score', 0)}"
            f"|T={_compact(record.get('type', ''))}"
            f"|ST={_compact(record.get('status', ''))}"
            f"|G={_compact(tags)}"
            f"|P={_compact(record.get('path', ''))}"
            f"|H={_compact(record.get('title', ''))}"
        )
    if not payload.get("records"):
        lines.append("NO_MATCH=Use discovery search before loading broad memory.")
    lines.append("END")
    return "\n".join(lines) + "\n"


def add_context_pack_measurement(payload: dict[str, Any]) -> dict[str, Any]:
    """Add byte and approximate token measurements to an FCP payload."""
    measured = dict(payload)
    measured["measurement"] = _build_measurement(measured, packet_bytes=0)
    previous_packet_bytes = -1
    for _ in range(8):
        packet_bytes = len(render_context_pack(measured).encode("utf-8"))
        measured["measurement"] = _build_measurement(measured, packet_bytes=packet_bytes)
        if packet_bytes == previous_packet_bytes:
            break
        previous_packet_bytes = packet_bytes
    return measured


def _clean_query(query: str) -> str:
    clean = " ".join(str(query or "").split())
    if not clean:
        raise ValueError("Context pack query cannot be empty")
    if len(clean) > MAX_QUERY_CHARS:
        raise ValueError(f"Context pack query must be {MAX_QUERY_CHARS} characters or fewer")
    if SECRET_RE.search(clean):
        raise ValueError("Context pack query appears to contain a secret")
    return clean


def _build_measurement(payload: dict[str, Any], packet_bytes: int) -> dict[str, Any]:
    selected_source_bytes = int(payload.get("source_bytes_if_loaded") or 0)
    corpus_source_bytes = int(payload.get("corpus_source_bytes") or 0)
    return {
        "basis": "selected_source_files_and_all_indexed_memory_files",
        "method": "utf8_bytes_measured_from_rendered_fcp",
        "token_estimate": "bytes_divided_by_4_approximation",
        "packet_bytes": packet_bytes,
        "packet_est_tokens": _estimate_tokens(packet_bytes),
        "selected_source_bytes": selected_source_bytes,
        "selected_source_est_tokens": _estimate_tokens(selected_source_bytes),
        "corpus_source_bytes": corpus_source_bytes,
        "corpus_source_est_tokens": _estimate_tokens(corpus_source_bytes),
        "savings_vs_selected_bytes": selected_source_bytes - packet_bytes,
        "savings_vs_selected_percent": _savings_percent(selected_source_bytes, packet_bytes),
        "savings_vs_corpus_bytes": corpus_source_bytes - packet_bytes,
        "savings_vs_corpus_percent": _savings_percent(corpus_source_bytes, packet_bytes),
    }


def _estimate_tokens(byte_count: int) -> int:
    if byte_count <= 0:
        return 0
    return max(1, round(byte_count / 4))


def _savings_percent(source_bytes: int, packet_bytes: int) -> str:
    if source_bytes <= 0:
        return "NA"
    return f"{((source_bytes - packet_bytes) / source_bytes) * 100:.1f}"


def _clean_limit(limit: int) -> int:
    try:
        value = int(limit)
    except (TypeError, ValueError):
        raise ValueError("Context pack limit must be a number") from None
    if value < 1:
        raise ValueError("Context pack limit must be at least 1")
    return min(value, MAX_PACK_RECORDS)


def _query_terms(query: str) -> set[str]:
    return {term for term in TOKEN_RE.findall(query.lower()) if term not in STOP_WORDS and len(term) > 1}


def _score_record(record: dict[str, Any], terms: set[str]) -> int:
    if not terms:
        return 0
    title = _token_text(record.get("title", ""))
    tags = _token_text(" ".join(str(tag) for tag in record.get("tags", [])))
    path = _token_text(record.get("path", ""))
    record_type = _token_text(record.get("type", ""))
    status = _token_text(record.get("status", ""))

    score = 0
    for term in terms:
        if term in title:
            score += 8
        if term in tags:
            score += 6
        if term in path:
            score += 4
        if term in record_type:
            score += 3
        if term in status:
            score += 1
    if str(record.get("status", "")).lower() == "current":
        score += 1
    return score


def _token_text(value: Any) -> set[str]:
    return set(TOKEN_RE.findall(str(value or "").lower()))


def _status_rank(status: str) -> int:
    return {"current": 0, "draft": 1, "superseded": 3}.get(status.lower(), 2)


def _source_size(root: Path, record: dict[str, Any]) -> int:
    path = root / str(record.get("path", ""))
    try:
        if path.is_file() and not path.is_symlink():
            return path.stat().st_size
    except OSError:
        return 0
    return 0


def _compact(value: Any, max_chars: int = 120) -> str:
    text = " ".join(str(value or "").split())
    text = text.replace("|", "/")
    text = text.encode("ascii", "ignore").decode("ascii")
    if len(text) > max_chars:
        text = text[: max_chars - 3].rstrip() + "..."
    return text
