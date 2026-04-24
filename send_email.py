#!/usr/bin/env python3
"""Send a markdown digest to the configured inbox via Resend.

Called by the competitor-intel skill after it finishes researching.

Usage:
    python3 send_email.py --subject "Subject" --body-file report.md
    python3 send_email.py --subject "Subject" --body-file -   # read body from stdin
"""

import argparse
import os
import sys
from pathlib import Path

import resend

EMAIL_FROM = "onboarding@resend.dev"


def load_env(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def load_config() -> tuple[str, str]:
    load_env(Path(__file__).parent / ".env")
    api_key = os.getenv("RESEND_API_KEY")
    email_to = os.getenv("EMAIL_TO")
    missing = [k for k, v in [("RESEND_API_KEY", api_key), ("EMAIL_TO", email_to)] if not v]
    if missing:
        sys.exit(f"ERROR: missing env vars: {', '.join(missing)}. Check your .env file.")
    return api_key, email_to


def read_body(path_arg: str) -> str:
    if path_arg == "-":
        return sys.stdin.read()
    path = Path(path_arg)
    if not path.exists():
        sys.exit(f"ERROR: file not found: {path}")
    return path.read_text(encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Send digest email via Resend")
    parser.add_argument("--subject", required=True)
    parser.add_argument("--body-file", required=True, help="Markdown file path, or '-' for stdin")
    args = parser.parse_args()

    api_key, email_to = load_config()
    body = read_body(args.body_file)
    if not body.strip():
        sys.exit("ERROR: empty body, refusing to send.")

    resend.api_key = api_key
    result = resend.Emails.send({
        "from": EMAIL_FROM,
        "to": [email_to],
        "subject": args.subject,
        "text": body,
    })
    print(f"Sent to {email_to} (id: {result.get('id', 'unknown')})")


if __name__ == "__main__":
    main()
