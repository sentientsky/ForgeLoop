from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
import venv
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description="Test a built ForgeLoop wheel outside the source checkout.")
    parser.add_argument("dist", type=Path, help="folder containing exactly one wheel")
    parser.add_argument("repo", type=Path, help="ForgeLoop repository to validate")
    args = parser.parse_args()

    wheels = sorted(args.dist.resolve().glob("*.whl"))
    if len(wheels) != 1:
        parser.error(f"expected exactly one wheel in {args.dist}, found {len(wheels)}")

    repo = args.repo.resolve()
    with tempfile.TemporaryDirectory(prefix="forgeloop-wheel-smoke-") as tmp:
        temp_root = Path(tmp)
        environment = temp_root / ".venv"
        venv.EnvBuilder(with_pip=True, clear=True).create(environment)
        python = environment / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        clean_env = os.environ.copy()
        clean_env.pop("PYTHONPATH", None)
        clean_env.pop("PYTHONHOME", None)
        clean_env["PYTHONNOUSERSITE"] = "1"

        _run(
            python,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            "--no-deps",
            str(wheels[0]),
            cwd=temp_root,
            env=clean_env,
        )
        _run(python, "-m", "forgeloop", "--help", cwd=temp_root, env=clean_env)
        _run(python, "-m", "forgeloop", "intro", "--plain", "--no-tagline", cwd=temp_root, env=clean_env)
        _run(python, "-m", "forgeloop", "validate", str(repo), cwd=temp_root, env=clean_env)

    print(f"Wheel smoke test passed: {wheels[0].name}")
    return 0


def _run(python: Path, *args: str, cwd: Path, env: dict[str, str]) -> None:
    subprocess.run([str(python), *args], check=True, cwd=cwd, env=env)


if __name__ == "__main__":
    raise SystemExit(main())
