from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .context import DEFAULT_PACK_RECORDS, build_context_pack, render_context_pack
from .core import MAX_FILE_BYTES, collect_memory_records

TOOL_TOKEN_PROFILES = {
    "claude-code": {
        "label": "Claude Code",
        "method": "provider_api_required",
        "notes": "Claude token counts are model-specific. ForgeLoop does not call provider APIs by default.",
    },
    "codex": {
        "label": "Codex",
        "method": "tiktoken_o200k_optional",
        "notes": "Uses tiktoken o200k_base when installed. Falls back to measured bytes divided by 4.",
    },
    "cursor": {
        "label": "Cursor",
        "method": "model_dependent",
        "notes": "Cursor can use different models, so there is no single exact local tokenizer.",
    },
    "github-copilot": {
        "label": "GitHub Copilot",
        "method": "model_dependent",
        "notes": "Copilot can route across models, so counts are treated as estimates.",
    },
    "gemini": {
        "label": "Gemini CLI / Gemini Code Assist",
        "method": "provider_api_required",
        "notes": "Gemini exact counts require a model-specific provider countTokens call.",
    },
    "windsurf": {
        "label": "Windsurf",
        "method": "model_dependent",
        "notes": "Windsurf supports multiple models, so counts are treated as estimates.",
    },
    "cline-roo": {
        "label": "Cline / Roo Code",
        "method": "model_dependent",
        "notes": "Cline and Roo can use different providers, so counts are treated as estimates.",
    },
    "jetbrains-ai": {
        "label": "JetBrains AI",
        "method": "model_dependent",
        "notes": "JetBrains AI can use provider-specific models, so counts are treated as estimates.",
    },
    "kiro": {
        "label": "Kiro",
        "method": "model_dependent",
        "notes": "Kiro model routing can vary, so counts are treated as estimates.",
    },
    "opencode": {
        "label": "OpenCode",
        "method": "model_dependent",
        "notes": "OpenCode is provider-configurable, so counts are treated as estimates.",
    },
    "aider": {
        "label": "Aider",
        "method": "model_dependent",
        "notes": "Aider is provider-configurable, so counts are treated as estimates.",
    },
}


@dataclass(frozen=True)
class TokenCount:
    tokens: int
    exact: bool
    method: str


def supported_token_tools() -> list[str]:
    return list(TOOL_TOKEN_PROFILES)


def build_token_report(
    root: Path,
    query: str,
    limit: int = DEFAULT_PACK_RECORDS,
    tool_id: str | None = None,
) -> dict[str, Any]:
    """Measure a rendered FCP packet against source memory for one or more tools."""
    root = root.resolve()
    packet = build_context_pack(root, query, limit=limit)
    packet_text = render_context_pack(packet)
    selected_text = _selected_source_text(root, packet)
    corpus_text = _corpus_source_text(root)
    requested_tools = _requested_tools(tool_id)

    tool_reports = [
        _tool_report(tool, packet_text, selected_text, corpus_text)
        for tool in requested_tools
    ]
    return {
        "schema_version": 1,
        "query": packet["query"],
        "packet_bytes": len(packet_text.encode("utf-8")),
        "selected_source_bytes": len(selected_text.encode("utf-8")),
        "corpus_source_bytes": len(corpus_text.encode("utf-8")),
        "returned_records": packet["returned"],
        "record_count": packet["record_count"],
        "tool_reports": tool_reports,
        "warnings": [
            "Exact token counts are only reported when a matching local tokenizer is available.",
            "Provider API token counters are not called by default, so secrets stay outside ForgeLoop.",
            "For public claims, cite the exact command, tool profile, and exact flag from this report.",
        ],
    }


def format_token_report(report: dict[str, Any]) -> str:
    lines = [
        "ForgeLoop token report:",
        f"- Query: {report['query']}",
        f"- Records: {report['returned_records']}/{report['record_count']}",
        f"- Packet bytes: {report['packet_bytes']}",
        f"- Selected source bytes: {report['selected_source_bytes']}",
        f"- Corpus source bytes: {report['corpus_source_bytes']}",
        "",
        "Tool profiles:",
    ]
    for item in report["tool_reports"]:
        exact = "exact" if item["exact"] else "estimate"
        lines.append(
            f"- {item['label']}: packet {item['packet_tokens']} tokens, "
            f"selected {item['selected_source_tokens']} tokens, "
            f"save selected {item['savings_vs_selected_percent']}% ({exact}, {item['method']})"
        )
    lines.append("")
    lines.append("Warnings:")
    lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines)


def _tool_report(tool_id: str, packet_text: str, selected_text: str, corpus_text: str) -> dict[str, Any]:
    profile = TOOL_TOKEN_PROFILES[tool_id]
    packet = _count_for_profile(tool_id, packet_text)
    selected = _count_for_profile(tool_id, selected_text)
    corpus = _count_for_profile(tool_id, corpus_text)
    exact = packet.exact and selected.exact and corpus.exact
    return {
        "tool": tool_id,
        "label": profile["label"],
        "exact": exact,
        "method": packet.method,
        "packet_tokens": packet.tokens,
        "selected_source_tokens": selected.tokens,
        "corpus_source_tokens": corpus.tokens,
        "savings_vs_selected_tokens": selected.tokens - packet.tokens,
        "savings_vs_selected_percent": _savings_percent(selected.tokens, packet.tokens),
        "savings_vs_corpus_tokens": corpus.tokens - packet.tokens,
        "savings_vs_corpus_percent": _savings_percent(corpus.tokens, packet.tokens),
        "notes": profile["notes"],
    }


def _count_for_profile(tool_id: str, text: str) -> TokenCount:
    method = TOOL_TOKEN_PROFILES[tool_id]["method"]
    if method == "tiktoken_o200k_optional":
        count = _count_with_tiktoken(text)
        if count is not None:
            return TokenCount(count, True, "tiktoken:o200k_base")
    return TokenCount(_estimate_tokens(text), False, "utf8_bytes_divided_by_4")


def _count_with_tiktoken(text: str) -> int | None:
    try:
        import tiktoken  # type: ignore[import-not-found]
        encoding = tiktoken.get_encoding("o200k_base")
        return len(encoding.encode(text))
    except (ImportError, LookupError, OSError, ValueError):
        return None


def _estimate_tokens(text: str) -> int:
    byte_count = len(text.encode("utf-8"))
    if byte_count <= 0:
        return 0
    return max(1, round(byte_count / 4))


def _savings_percent(source_tokens: int, packet_tokens: int) -> str:
    if source_tokens <= 0:
        return "NA"
    return f"{((source_tokens - packet_tokens) / source_tokens) * 100:.1f}"


def _selected_source_text(root: Path, packet: dict[str, Any]) -> str:
    chunks = []
    for record in packet.get("records", []):
        chunks.append(_read_memory_file(root, str(record.get("path", ""))))
    return "\n".join(chunk for chunk in chunks if chunk)


def _corpus_source_text(root: Path) -> str:
    chunks = []
    for record in collect_memory_records(root):
        chunks.append(_read_memory_file(root, str(record.get("path", ""))))
    return "\n".join(chunk for chunk in chunks if chunk)


def _read_memory_file(root: Path, relative_path: str) -> str:
    path = (root / relative_path).resolve()
    if path != root and root not in path.parents:
        return ""
    try:
        if not path.is_file() or path.is_symlink() or path.stat().st_size > MAX_FILE_BYTES:
            return ""
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _requested_tools(tool_id: str | None) -> list[str]:
    if not tool_id or tool_id == "all-supported":
        return supported_token_tools()
    selected = tool_id.strip().lower()
    if selected not in TOOL_TOKEN_PROFILES:
        allowed = ", ".join(supported_token_tools() + ["all-supported"])
        raise ValueError(f"Unsupported token tool '{tool_id}'. Allowed tools: {allowed}")
    return [selected]
