from __future__ import annotations

import os
import stat
import tempfile
from dataclasses import dataclass
from pathlib import Path, PurePosixPath, PureWindowsPath
from typing import Any

from .setup import ALL_SUPPORTED_ID, SUPPORTED_TOOLS

MAX_PROFILE_FILE_BYTES = 1_000_000


@dataclass(frozen=True)
class AdoptionEntry:
    path: str
    action: str
    reason: str = ""


@dataclass(frozen=True)
class AdoptionReport:
    tool_id: str
    tool_label: str
    dry_run: bool
    entries: list[AdoptionEntry]

    @property
    def conflicts(self) -> list[AdoptionEntry]:
        return [entry for entry in self.entries if entry.action == "conflict"]

    def as_dict(self) -> dict[str, Any]:
        return {
            "tool": self.tool_id,
            "label": self.tool_label,
            "dry_run": self.dry_run,
            "entries": [
                {"path": entry.path, "action": entry.action, "reason": entry.reason}
                for entry in self.entries
            ],
        }


def adopt_into_repo(
    source_root: Path,
    destination_root: Path,
    tool_id: str,
    *,
    apply: bool = False,
) -> AdoptionReport:
    source_root = source_root.resolve(strict=True)
    destination_root = destination_root.resolve(strict=True)
    if not source_root.is_dir():
        raise ValueError("ForgeLoop source root must be a directory")
    if not destination_root.is_dir():
        raise ValueError("Destination must be an existing directory")
    if source_root == destination_root:
        raise ValueError("Destination must be a different repository from the ForgeLoop source")
    if source_root in destination_root.parents:
        raise ValueError("Destination cannot be inside the ForgeLoop source repository")

    label, relative_paths = _profile_paths(tool_id)
    contents = {
        relative: _read_source_file(source_root, relative)
        for relative in relative_paths
    }
    entries = _plan_entries(destination_root, contents)
    if not apply:
        return AdoptionReport(tool_id, label, True, entries)

    created_files: list[tuple[Path, bytes]] = []
    created_directories: list[Path] = []
    results: dict[str, AdoptionEntry] = {entry.path: entry for entry in entries}
    try:
        for relative in relative_paths:
            if results[relative].action != "create":
                continue
            target = destination_root.joinpath(*PurePosixPath(relative).parts)
            _create_parent_directories(destination_root, relative, created_directories)
            if _create_file_exclusive(target, contents[relative]):
                created_files.append((target, contents[relative]))
                results[relative] = AdoptionEntry(relative, "created")
            elif (
                target.is_file()
                and not _is_link_like(target)
                and target.stat().st_size <= MAX_PROFILE_FILE_BYTES
                and target.read_bytes() == contents[relative]
            ):
                results[relative] = AdoptionEntry(relative, "unchanged", "created concurrently with identical content")
            else:
                results[relative] = AdoptionEntry(relative, "conflict", "destination appeared during installation; preserved")
    except Exception as exc:
        rollback_errors = _rollback(created_files, created_directories)
        if rollback_errors:
            raise OSError(
                "adoption failed and rollback was incomplete: " + "; ".join(rollback_errors)
            ) from exc
        raise

    return AdoptionReport(
        tool_id,
        label,
        False,
        [results[relative] for relative in relative_paths],
    )


def format_adoption_report(report: AdoptionReport) -> str:
    lines = [f"ForgeLoop adoption: {report.tool_label}"]
    counts = {action: 0 for action in ("create", "created", "unchanged", "conflict")}
    for entry in report.entries:
        counts[entry.action] = counts.get(entry.action, 0) + 1
    lines.extend(
        [
            f"Files to add: {counts['create']}",
            f"Files added: {counts['created']}",
            f"Already matching: {counts['unchanged']}",
            f"Conflicts preserved: {counts['conflict']}",
        ]
    )
    for entry in report.entries:
        if entry.action in {"create", "created"}:
            lines.append(f"{'Would add' if report.dry_run else 'Added'}: {entry.path}")
        elif entry.action == "conflict":
            lines.append(f"Conflict: {entry.path} ({entry.reason})")
    if report.dry_run:
        lines.append("Preview only. Re-run with --apply to add missing files.")
    else:
        lines.append("Existing files were never overwritten. Review the destination diff before committing.")
    return "\n".join(lines)


def _profile_paths(tool_id: str) -> tuple[str, list[str]]:
    if tool_id == ALL_SUPPORTED_ID:
        profiles = SUPPORTED_TOOLS
        label = "All supported tools"
    else:
        profiles = [profile for profile in SUPPORTED_TOOLS if profile["id"] == tool_id]
        if not profiles:
            raise ValueError(f"Unknown tool profile: {tool_id}")
        label = str(profiles[0]["label"])

    paths: list[str] = []
    for profile in profiles:
        for raw_path in profile["entry_files"]:
            relative = _validated_relative_path(str(raw_path))
            if relative not in paths:
                paths.append(relative)
    return label, paths


def _validated_relative_path(raw_path: str) -> str:
    path = PurePosixPath(raw_path)
    windows_path = PureWindowsPath(raw_path)
    if (
        not raw_path
        or "\\" in raw_path
        or "\x00" in raw_path
        or any(part in {"", ".", ".."} for part in raw_path.split("/"))
        or path.is_absolute()
        or windows_path.is_absolute()
        or windows_path.drive
    ):
        raise ValueError(f"Unsafe ForgeLoop profile path: {raw_path!r}")
    return path.as_posix()


def _read_source_file(source_root: Path, relative: str) -> bytes:
    path = source_root.joinpath(*PurePosixPath(relative).parts)
    _reject_symlink_components(source_root, relative)
    if not path.is_file():
        raise ValueError(f"ForgeLoop profile file is missing: {relative}")
    content = path.read_bytes()
    if len(content) > MAX_PROFILE_FILE_BYTES:
        raise ValueError(f"ForgeLoop profile file exceeds the size limit: {relative}")
    return content


def _plan_entries(destination_root: Path, contents: dict[str, bytes]) -> list[AdoptionEntry]:
    entries: list[AdoptionEntry] = []
    for relative, source_content in contents.items():
        path = destination_root.joinpath(*PurePosixPath(relative).parts)
        _reject_symlink_components(destination_root, relative)
        blocked_parent = _non_directory_parent(destination_root, relative)
        if blocked_parent:
            entries.append(AdoptionEntry(relative, "conflict", f"parent is not a directory: {blocked_parent}"))
        elif not path.exists():
            entries.append(AdoptionEntry(relative, "create"))
        elif not path.is_file():
            entries.append(AdoptionEntry(relative, "conflict", "destination is not a regular file"))
        elif path.stat().st_size > MAX_PROFILE_FILE_BYTES:
            entries.append(AdoptionEntry(relative, "conflict", "destination file exceeds the comparison size limit"))
        elif path.read_bytes() == source_content:
            entries.append(AdoptionEntry(relative, "unchanged"))
        else:
            entries.append(AdoptionEntry(relative, "conflict", "different file already exists; preserved"))
    return entries


def _reject_symlink_components(root: Path, relative: str) -> None:
    current = root
    for part in PurePosixPath(relative).parts:
        current = current / part
        if _is_link_like(current):
            raise ValueError(f"Refusing to follow symlink in profile path: {relative}")


def _non_directory_parent(root: Path, relative: str) -> str | None:
    current = root
    parts = PurePosixPath(relative).parts[:-1]
    for part in parts:
        current = current / part
        if current.exists() and not current.is_dir():
            return current.relative_to(root).as_posix()
    return None


def _create_parent_directories(root: Path, relative: str, created: list[Path]) -> None:
    current = root
    for part in PurePosixPath(relative).parts[:-1]:
        current = current / part
        if _is_link_like(current):
            raise ValueError(f"Refusing to write through symlink: {current.relative_to(root).as_posix()}")
        if current.exists():
            if not current.is_dir():
                raise ValueError(f"Cannot create profile file below non-directory: {current.relative_to(root).as_posix()}")
            continue
        try:
            current.mkdir()
            created.append(current)
        except FileExistsError:
            if _is_link_like(current) or not current.is_dir():
                raise ValueError(f"Unsafe directory appeared during installation: {current.relative_to(root).as_posix()}")


def _create_file_exclusive(path: Path, content: bytes) -> bool:
    temp_path: Path | None = None
    created = False
    try:
        with tempfile.NamedTemporaryFile(dir=path.parent, prefix=".forgeloop-", delete=False) as temporary:
            temp_path = Path(temporary.name)
            temporary.write(content)
            temporary.flush()
            os.fsync(temporary.fileno())
        os.chmod(temp_path, 0o644)
        try:
            os.link(temp_path, path)
        except FileExistsError:
            return False
        created = True
        return True
    finally:
        if temp_path is not None:
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                if created and not _is_link_like(path) and path.is_file() and path.read_bytes() == content:
                    path.unlink(missing_ok=True)
                raise


def _rollback(created_files: list[tuple[Path, bytes]], created_directories: list[Path]) -> list[str]:
    errors: list[str] = []
    for path, expected_content in reversed(created_files):
        try:
            if _is_link_like(path):
                errors.append(f"created path became a symlink: {path.name}")
            elif path.is_file():
                if path.read_bytes() == expected_content:
                    path.unlink()
                else:
                    errors.append(f"created file changed before rollback: {path.name}")
        except OSError as exc:
            errors.append(f"could not remove {path.name}: {exc}")
    for directory in reversed(created_directories):
        try:
            directory.rmdir()
        except OSError:
            pass
    return errors


def _is_link_like(path: Path) -> bool:
    if path.is_symlink():
        return True
    is_junction = getattr(path, "is_junction", None)
    if callable(is_junction) and is_junction():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except OSError:
        return False
    reparse_flag = getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400)
    return bool(attributes & reparse_flag)


def adoption_source_root() -> Path:
    return Path(__file__).resolve().parents[1]
