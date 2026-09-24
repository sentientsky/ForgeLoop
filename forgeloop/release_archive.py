from __future__ import annotations

import argparse
from pathlib import Path, PurePosixPath
from zipfile import BadZipFile, ZipFile

LOCAL_ONLY_NAMES = {
    ".env",
    ".envrc",
    ".forgeloop.local.json",
    ".git-credentials",
    ".netrc",
    ".npmrc",
    ".pypirc",
    "settings.local.json",
    "secrets.env",
    "secret.env",
    "credentials",
    "credentials.json",
    "service-account.json",
    "token.json",
    "id_rsa",
    "id_dsa",
    "id_ecdsa",
    "id_ed25519",
    "id_ed25519_sk",
    "id_ecdsa_sk",
}
LOCAL_ONLY_SUFFIXES = {".pem", ".p12", ".pfx"}


def forbidden_source_paths(archive_path: Path) -> list[str]:
    try:
        with ZipFile(archive_path) as archive:
            names = archive.namelist()
    except (BadZipFile, OSError):
        raise ValueError("Could not read the source ZIP archive.") from None

    forbidden = []
    for name in names:
        path = PurePosixPath(name)
        if name.endswith("/"):
            continue
        lowered_name = path.name.casefold()
        is_env_file = (
            (lowered_name.startswith(".env.") and lowered_name != ".env.example")
            or lowered_name.endswith(".env")
        )
        if (
            lowered_name in LOCAL_ONLY_NAMES
            or is_env_file
            or path.suffix.casefold() in LOCAL_ONLY_SUFFIXES
        ):
            forbidden.append(path.as_posix())
    return forbidden


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Reject local-only secrets files in a ForgeLoop source archive.")
    parser.add_argument("archive", type=Path, help="source ZIP archive to inspect")
    args = parser.parse_args(argv)
    try:
        forbidden = forbidden_source_paths(args.archive)
    except ValueError as exc:
        parser.error(str(exc))
    if forbidden:
        print(f"Source archive contains {len(forbidden)} local-only file(s). Remove them before release.")
        return 1
    print("Source archive safety check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
