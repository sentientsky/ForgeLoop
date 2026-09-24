from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

from .banner import render_intro
from .compat import compatibility_report, format_compatibility_report
from .context import build_context_pack, render_context_pack
from .core import (
    build_memory_index,
    create_note,
    format_findings,
    repo_status,
    simulate_hook_event,
    validate_repo,
)
from .doctor import doctor_report, format_doctor_report
from .governance import (
    audit_governed_memory,
    format_governance_audit,
    format_governance_log_status,
    record_audit_event,
    verify_audit_log,
)
from .opencli import (
    DEFAULT_INSTALL_TIMEOUT,
    format_opencli_install_result,
    format_opencli_plan,
    format_opencli_status,
    opencli_plan,
    opencli_status,
    run_opencli_install,
)
from .secrets import check_secrets, external_secrets_path, init_external_secrets
from .setup import format_setup_result, run_setup, setup_menu_text, supported_tool_ids
from .tokens import build_token_report, format_token_report, supported_token_tools


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="forgeloop",
        description="Validate and maintain a ForgeLoop repository.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="check repository structure")
    validate_parser.add_argument("root", nargs="?", default=".", help="repository root")
    validate_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    intro_parser = subparsers.add_parser("intro", help="show the ForgeLoop ASCII intro")
    intro_parser.add_argument(
        "--plain",
        "--no-colour",
        "--no-color",
        action="store_true",
        help="print without ANSI colour codes",
    )
    intro_parser.add_argument("--no-tagline", action="store_true", help="hide the tagline")

    index_parser = subparsers.add_parser("index", help="build the local memory index")
    index_parser.add_argument("root", nargs="?", default=".", help="repository root")
    index_parser.add_argument(
        "--check",
        action="store_true",
        help="fail if committed memory index files are out of date",
    )

    status_parser = subparsers.add_parser("status", help="show repository memory status")
    status_parser.add_argument("root", nargs="?", default=".", help="repository root")
    status_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    pack_parser = subparsers.add_parser("pack", help="build a compact pointer-only memory packet")
    pack_parser.add_argument("query", help="task or memory query")
    pack_parser.add_argument("root", nargs="?", default=".", help="repository root")
    pack_parser.add_argument("--limit", type=int, default=8, help="maximum records to return")
    pack_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    compat_parser = subparsers.add_parser("compat", help="check AI coding tool compatibility files")
    compat_parser.add_argument("root", nargs="?", default=".", help="repository root")
    compat_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    doctor_parser = subparsers.add_parser("doctor", help="check local ForgeLoop repository health and release readiness")
    doctor_parser.add_argument("root", nargs="?", default=".", help="repository root")
    doctor_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    tokens_parser = subparsers.add_parser("tokens", help="measure context packet token savings by tool")
    tokens_parser.add_argument("query", help="task or memory query")
    tokens_parser.add_argument("root", nargs="?", default=".", help="repository root")
    tokens_parser.add_argument("--limit", type=int, default=8, help="maximum records to return")
    tokens_parser.add_argument(
        "--tool",
        choices=supported_token_tools() + ["all-supported"],
        default="all-supported",
        help="tool profile to measure",
    )
    tokens_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    setup_parser = subparsers.add_parser("setup", help="select an AI coding tool profile")
    setup_parser.add_argument("root", nargs="?", default=".", help="repository root")
    setup_parser.add_argument("--tool", choices=supported_tool_ids(), help="tool profile to select")
    setup_parser.add_argument("--list", action="store_true", help="show the setup menu and exit")
    setup_parser.add_argument("--dry-run", action="store_true", help="show result without writing local setup")
    setup_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    new_parser = subparsers.add_parser("new", help="create a safe ForgeLoop note from a template")
    new_parser.add_argument("kind", help="note kind, such as discover, frame, check, capture, solution")
    new_parser.add_argument("title", help="note title, quoted if it contains spaces")
    new_parser.add_argument("root", nargs="?", default=".", help="repository root")
    new_parser.add_argument("--date", help="note date in YYYY-MM-DD format, defaults to today")
    new_parser.add_argument("--force", action="store_true", help="overwrite an existing note")
    new_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    hook_parser = subparsers.add_parser("hook-simulate", help="dry-run a future capture hook")
    hook_parser.add_argument("event", choices=["Stop", "PreCompact", "SessionEnd"], help="hook event")
    hook_parser.add_argument("root", nargs="?", default=".", help="repository root")
    hook_parser.add_argument("--input", help="JSON object file. Use '-' to read stdin.")
    hook_parser.add_argument("--interval", type=int, default=15, help="Stop reminder interval")
    hook_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    opencli_parser = subparsers.add_parser("opencli", help="inspect or install the OpenCLI integration")
    opencli_subparsers = opencli_parser.add_subparsers(dest="opencli_command", required=True)
    opencli_status_parser = opencli_subparsers.add_parser("status", help="show OpenCLI integration status")
    opencli_status_parser.add_argument("root", nargs="?", default=".", help="repository root")
    opencli_status_parser.add_argument("--fetch-npm", action="store_true", help="fetch current npm package metadata")
    opencli_status_parser.add_argument("--json", action="store_true", help="print machine-readable output")
    opencli_plan_parser = opencli_subparsers.add_parser("plan", help="show the OpenCLI install plan")
    opencli_plan_parser.add_argument("root", nargs="?", default=".", help="repository root")
    opencli_plan_parser.add_argument("--with-skills", action="store_true", help="include OpenCLI AI skill install step")
    opencli_plan_parser.add_argument("--run-doctor", action="store_true", help="include OpenCLI doctor verification step")
    opencli_plan_parser.add_argument("--fetch-npm", action="store_true", help="include current npm package metadata")
    opencli_plan_parser.add_argument("--json", action="store_true", help="print machine-readable output")
    opencli_install_parser = opencli_subparsers.add_parser("install", help="install or update OpenCLI explicitly")
    opencli_install_parser.add_argument("root", nargs="?", default=".", help="repository root")
    opencli_install_parser.add_argument("--execute", action="store_true", help="actually run install commands")
    opencli_install_parser.add_argument("--with-skills", action="store_true", help="install OpenCLI AI skills too")
    opencli_install_parser.add_argument("--run-doctor", action="store_true", help="run opencli doctor after install")
    opencli_install_parser.add_argument("--timeout", type=int, default=DEFAULT_INSTALL_TIMEOUT, help="command timeout in seconds")
    opencli_install_parser.add_argument("--json", action="store_true", help="print machine-readable output")

    secrets_parser = subparsers.add_parser("secrets", help="manage external secrets metadata")
    secrets_subparsers = secrets_parser.add_subparsers(dest="secrets_command", required=True)
    secrets_path = secrets_subparsers.add_parser("path", help="print the external secrets file path")
    secrets_path.add_argument("root", nargs="?", default=".", help="repository root")
    secrets_path.add_argument("--json", action="store_true", help="print machine-readable output")
    secrets_init = secrets_subparsers.add_parser("init", help="create the external secrets file")
    secrets_init.add_argument("root", nargs="?", default=".", help="repository root")
    secrets_init.add_argument("--force", action="store_true", help="overwrite the external secrets file")
    secrets_init.add_argument("--json", action="store_true", help="print machine-readable output")
    secrets_check = secrets_subparsers.add_parser("check", help="check repo and external secrets state")
    secrets_check.add_argument("root", nargs="?", default=".", help="repository root")
    secrets_check.add_argument("--json", action="store_true", help="print machine-readable output")

    governance_parser = subparsers.add_parser(
        "governance",
        help="audit governed memory metadata and local audit events",
    )
    governance_subparsers = governance_parser.add_subparsers(dest="governance_command", required=True)
    governance_audit = governance_subparsers.add_parser(
        "audit",
        help="check governed memory metadata without reading external data stores",
    )
    governance_audit.add_argument("root", nargs="?", default=".", help="repository root")
    governance_audit.add_argument("--json", action="store_true", help="print machine-readable output")
    governance_log = governance_subparsers.add_parser(
        "log",
        help="record a metadata-only governance event in the external audit log",
    )
    governance_log.add_argument(
        "action",
        choices=["collect", "access", "update", "export", "share", "erase", "retention-review"],
        help="governance action to record",
    )
    governance_log.add_argument("root", nargs="?", default=".", help="repository root")
    governance_log.add_argument("--actor-ref", required=True, help="opaque operator reference, not a name or email")
    governance_log.add_argument("--record-ref", required=True, help="opaque record reference, not a file path")
    governance_log.add_argument("--subject-ref", help="optional opaque subject reference, not personal data")
    governance_log.add_argument("--json", action="store_true", help="print machine-readable output")
    governance_verify = governance_subparsers.add_parser(
        "verify",
        help="verify the external governance audit hash chain",
    )
    governance_verify.add_argument("root", nargs="?", default=".", help="repository root")
    governance_verify.add_argument("--json", action="store_true", help="print machine-readable output")

    args = parser.parse_args(argv)

    if args.command == "intro":
        print(render_intro(colour=not args.plain, tagline=not args.no_tagline))
        return 0

    root = Path(args.root).resolve()

    if args.command == "validate":
        findings = validate_repo(root)
        if args.json:
            print(json.dumps([finding.as_dict(root) for finding in findings], indent=2))
        else:
            print(format_findings(findings, root))
        return 1 if any(finding.level == "error" for finding in findings) else 0

    if args.command == "index":
        result = build_memory_index(root, check=args.check)
        if args.check and result.changed:
            print("Memory index is out of date. Run: python -m forgeloop index .")
            return 1
        action = "checked" if args.check else "written"
        print(
            f"Memory index {action}: {result.record_count} records, "
            f"{result.json_path.relative_to(root)}, {result.markdown_path.relative_to(root)}"
        )
        return 0

    if args.command == "status":
        status = repo_status(root)
        if args.json:
            print(json.dumps(status, indent=2))
        else:
            print(f"ForgeLoop status for {root}")
            print(f"Markdown files: {status['markdown_files']}")
            print(f"Skills: {status['skills']}")
            print(f"Agents: {status['agents']}")
            print(f"Memory records: {status['memory_records']}")
            print(f"Index exists: {status['index_exists']}")
        return 0

    if args.command == "pack":
        try:
            payload = build_context_pack(root, args.query, limit=args.limit)
        except ValueError as exc:
            print(f"Could not build context pack: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(render_context_pack(payload), end="")
        return 0

    if args.command == "compat":
        report = compatibility_report(root)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_compatibility_report(report))
        return 0 if all(target["profile_files_present"] for target in report["targets"]) else 1

    if args.command == "doctor":
        report = doctor_report(root)
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_doctor_report(report))
        return 0 if report["ok"] else 1

    if args.command == "tokens":
        try:
            report = build_token_report(root, args.query, limit=args.limit, tool_id=args.tool)
        except ValueError as exc:
            print(f"Could not build token report: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(report, indent=2))
        else:
            print(format_token_report(report))
        return 0

    if args.command == "setup":
        if args.list:
            print(setup_menu_text())
            return 0
        try:
            result = run_setup(root, tool_id=args.tool, dry_run=args.dry_run)
        except ValueError as exc:
            print(f"Could not run setup: {exc}", file=sys.stderr)
            return 1
        if args.json:
            print(json.dumps(result.as_dict(root), indent=2))
        else:
            print(format_setup_result(result, root))
        return 1 if result.missing_files else 0

    if args.command == "new":
        try:
            note_date = date.fromisoformat(args.date) if args.date else None
            result = create_note(root, args.kind, args.title, note_date=note_date, force=args.force)
        except (FileExistsError, FileNotFoundError, ValueError) as exc:
            print(f"Could not create note: {exc}", file=sys.stderr)
            return 1
        payload = {
            "path": str(result.path.relative_to(root)),
            "created": result.created,
        }
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"Created {result.path.relative_to(root)}")
        return 0

    if args.command == "hook-simulate":
        try:
            payload = _load_json_payload(args.input)
            result = simulate_hook_event(root, args.event, payload, interval=args.interval)
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            print(f"Could not simulate hook: {exc}", file=sys.stderr)
            return 1
        output = {
            "event": result.event,
            "action": result.action,
            "reason": result.reason,
            "details": result.details,
        }
        if args.json:
            print(json.dumps(output, indent=2))
        else:
            print(f"{result.event}: {result.action}")
            print(result.reason)
            print(f"Dry run: {result.details['dry_run']}")
            print(f"Executes commands: {result.details['executes_commands']}")
        return 0

    if args.command == "opencli":
        if args.opencli_command == "status":
            status = opencli_status(root, fetch_npm=args.fetch_npm)
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                print(format_opencli_status(status))
            return 0

        if args.opencli_command == "plan":
            plan = opencli_plan(
                root,
                include_skills=args.with_skills,
                run_doctor=args.run_doctor,
                fetch_npm=args.fetch_npm,
            )
            if args.json:
                print(json.dumps(plan, indent=2))
            else:
                print(format_opencli_plan(plan))
            return 0

        if args.opencli_command == "install":
            timeout = max(30, min(args.timeout, 1800))
            result = run_opencli_install(
                root,
                include_skills=args.with_skills,
                run_doctor=args.run_doctor,
                execute=args.execute,
                timeout=timeout,
            )
            if args.json:
                print(json.dumps(result, indent=2))
            else:
                print(format_opencli_install_result(result))
            return 0 if result["status"] in {"ok", "dry-run"} else 1

    if args.command == "secrets":
        if args.secrets_command == "path":
            path = external_secrets_path(root)
            if args.json:
                print(json.dumps({"path": str(path)}, indent=2))
            else:
                print(path)
            return 0

        if args.secrets_command == "init":
            try:
                path = init_external_secrets(root, force=args.force)
            except (FileExistsError, FileNotFoundError, ValueError, OSError) as exc:
                print(f"Could not initialise secrets: {exc}", file=sys.stderr)
                return 1
            if args.json:
                print(json.dumps({"external": True, "created_or_exists": True}, indent=2))
            else:
                print("External secrets file is ready outside the repository.")
            return 0

        if args.secrets_command == "check":
            status = check_secrets(root)
            if args.json:
                print(json.dumps(status.as_dict(root), indent=2))
            else:
                print("External secrets location: outside the repository")
                print(f"Exists: {status.exists}")
                print(f"Keys: {len(status.keys)}")
                if status.repo_env_files:
                    print("Repo .env files:")
                    for path in status.repo_env_files:
                        print(f"- {path.relative_to(root)}")
                if status.warnings:
                    print("Warnings:")
                    for warning in status.warnings:
                        print(f"- {warning}")
            return 1 if status.repo_env_files else 0

    if args.command == "governance":
        if args.governance_command == "audit":
            report = audit_governed_memory(root)
            if args.json:
                print(json.dumps(report, indent=2))
            else:
                print(format_governance_audit(report))
            return 1 if report["errors"] else 0

        if args.governance_command == "log":
            try:
                event = record_audit_event(
                    root,
                    action=args.action,
                    actor_ref=args.actor_ref,
                    record_ref=args.record_ref,
                    subject_ref=args.subject_ref,
                )
            except (OSError, ValueError) as exc:
                print(f"Could not record governance event: {exc}", file=sys.stderr)
                return 1
            if args.json:
                print(json.dumps(event, indent=2))
            else:
                print(f"Governance event recorded: {event['event_fingerprint']}")
            return 0

        if args.governance_command == "verify":
            status = verify_audit_log(root)
            if args.json:
                print(json.dumps(status, indent=2))
            else:
                print(format_governance_log_status(status))
            return 0 if status["valid"] else 1

    parser.print_help(sys.stderr)
    return 2


def _load_json_payload(input_path: str | None) -> dict:
    if not input_path:
        return {}
    if input_path == "-":
        text = sys.stdin.read()
    else:
        path = Path(input_path)
        if path.is_symlink():
            raise ValueError("Refusing to read JSON input from a symlink")
        if path.stat().st_size > 100_000:
            raise ValueError("JSON input is too large")
        text = path.read_text(encoding="utf-8")
    payload = json.loads(text)
    if not isinstance(payload, dict):
        raise TypeError("JSON input must be an object")
    return payload
