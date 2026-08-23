from __future__ import annotations

import hashlib
import os
import re
import stat
from dataclasses import dataclass
from pathlib import Path
from typing import Any


SAFE_KEY_RE = re.compile(r"^[A-Z][A-Z0-9_]{1,79}$")
SAFE_ENV_FILE_NAMES = {".env.example"}
BLOCKED_ENV_FILE_NAMES = {".env", ".env.local", ".envrc", "secrets.env", "secret.env"}


@dataclass(frozen=True)
class SecretsCheck:
    external_path: Path
    exists: bool
    repo_env_files: list[Path]
    keys: list[str]
    warnings: list[str]

    def as_dict(self, root: Path) -> dict[str, Any]:
        return {
            "external_location": "outside_repository",
            "exists": self.exists,
            "repo_env_files": [str(path.relative_to(root)) for path in self.repo_env_files],
            "keys": self.keys,
            "warnings": self.warnings,
        }


def external_secrets_path(root: Path) -> Path:
    """Return the per-repository secrets file path outside the repository."""
    root = root.resolve()
    config_home = _forgeloop_config_home()
    repo_hash = hashlib.sha256(str(root).encode("utf-8")).hexdigest()[:12]
    repo_slug = _safe_slug(root.name or "repository")
    return config_home / "secrets" / f"{repo_slug}-{repo_hash}.env"


def init_external_secrets(root: Path, force: bool = False) -> Path:
    """Create the external secrets file from .env.example without overwriting values."""
    root = root.resolve()
    env_example = root / ".env.example"
    if not env_example.is_file():
        raise FileNotFoundError(".env.example is required before initialising external secrets")

    target = external_secrets_path(root)
    if target.resolve() == target.resolve().parent:
        raise ValueError("Invalid external secrets path")
    if _path_is_inside(target, root):
        raise ValueError("External secrets path resolved inside the repository")
    if _has_symlink_ancestor(target.parent):
        raise ValueError("Refusing to write secrets inside a symlinked folder")
    # Path.exists() is false for dangling symlinks on some platforms. Check the
    # link itself before opening the target so a local link cannot redirect a
    # secrets write outside the intended configuration location.
    if target.is_symlink():
        raise ValueError("Refusing to write secrets through a symlink")
    if target.exists() and not target.is_file():
        raise ValueError("External secrets path must be a regular file")
    if target.exists() and not force:
        return target

    keys = parse_env_keys(env_example.read_text(encoding="utf-8"))
    if not keys:
        raise ValueError(".env.example does not define any keys")

    lines = [
        "# ForgeLoop external secrets file",
        "# This file is outside the repository and must not be committed.",
        "# Fill in values locally. Keep blanks for secrets you do not use.",
        "",
    ]
    for key in keys:
        lines.append(f"{key}=")
    text = "\n".join(lines).rstrip() + "\n"

    target.parent.mkdir(parents=True, exist_ok=True)
    if _has_symlink_ancestor(target.parent):
        raise ValueError("Refusing to write secrets inside a symlinked folder")
    flags = os.O_WRONLY | os.O_CREAT
    if not force:
        flags |= os.O_EXCL
    else:
        flags |= os.O_TRUNC
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(target, flags, 0o600)
    with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    _restrict_file_permissions(target)
    return target


def check_secrets(root: Path) -> SecretsCheck:
    root = root.resolve()
    external_path = external_secrets_path(root)
    repo_env_files = find_repo_env_files(root)
    keys: list[str] = []
    warnings: list[str] = []

    if external_path.is_symlink():
        warnings.append("External secrets file is a symlink.")
    elif external_path.exists():
        if not external_path.is_file():
            warnings.append("External secrets path is not a regular file.")
        else:
            text = external_path.read_text(encoding="utf-8", errors="replace")
            keys = parse_env_keys(text)
            invalid = [key for key in keys if not SAFE_KEY_RE.fullmatch(key)]
            if invalid:
                warnings.append(f"Invalid secret key names: {', '.join(invalid)}")
            mode_warning = _permission_warning(external_path)
            if mode_warning:
                warnings.append(mode_warning)
    else:
        warnings.append("External secrets file does not exist yet.")

    exists = external_path.is_file() and not external_path.is_symlink()
    return SecretsCheck(external_path, exists, repo_env_files, keys, warnings)


def parse_env_keys(text: str) -> list[str]:
    keys: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _value = line.split("=", 1)
        key = key.strip()
        if key and key not in keys:
            keys.append(key)
    return keys


def find_repo_env_files(root: Path) -> list[Path]:
    root = root.resolve()
    matches: list[Path] = []
    for current_root, dirs, files in os.walk(root):
        dirs[:] = [
            name
            for name in dirs
            if name not in {".git", "__pycache__", ".pytest_cache", "node_modules", "dist", "build", ".opencli"}
        ]
        for file_name in files:
            lower_name = file_name.lower()
            path = Path(current_root) / file_name
            if file_name in SAFE_ENV_FILE_NAMES:
                continue
            if (
                lower_name in BLOCKED_ENV_FILE_NAMES
                or lower_name.startswith(".env.")
                or lower_name.endswith(".env")
            ):
                matches.append(path)
    return sorted(matches)


def _forgeloop_config_home() -> Path:
    override = os.environ.get("FORGELOOP_CONFIG_HOME")
    if override:
        return Path(override).expanduser().resolve()

    if os.name == "nt":
        base = os.environ.get("APPDATA")
        if base:
            return Path(base) / "ForgeLoop"
        return Path.home() / "AppData" / "Roaming" / "ForgeLoop"

    if sys_platform := os.environ.get("XDG_CONFIG_HOME"):
        return Path(sys_platform).expanduser() / "forgeloop"

    if os.uname().sysname == "Darwin":
        return Path.home() / "Library" / "Application Support" / "ForgeLoop"

    return Path.home() / ".config" / "forgeloop"


def _safe_slug(value: str) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-._").lower()
    return slug[:60] or "repository"


def _path_is_inside(path: Path, root: Path) -> bool:
    resolved_path = path.resolve()
    resolved_root = root.resolve()
    return resolved_path == resolved_root or resolved_root in resolved_path.parents


def _has_symlink_ancestor(path: Path) -> bool:
    current = path
    while current != current.parent:
        if current.exists() and current.is_symlink():
            return True
        current = current.parent
    return False


def _restrict_file_permissions(path: Path) -> None:
    try:
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
    except OSError:
        pass


def _permission_warning(path: Path) -> str:
    if os.name == "nt":
        return ""
    mode = stat.S_IMODE(path.stat().st_mode)
    if mode & (stat.S_IRWXG | stat.S_IRWXO):
        return "External secrets file is readable or writable by group/other users."
    return ""
