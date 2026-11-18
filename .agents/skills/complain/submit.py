#!/usr/bin/env python3
"""Submit an anonymous agent complaint as a GitHub issue comment without blocking the parent task.

All complaints land as comments in ONE pinned issue labelled `agent-skargi`. When no open
issue with that label exists, the script creates it, labels it and pins it.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import unicodedata

FEEDBACK_KIND = "complaint"
REPO = os.environ.get("BAZARTY_FEEDBACK_REPO", "Enkidu-png/bazarty-platforma")
LABEL = "agent-skargi"
LABEL_COLOR = "B60205"
LABEL_DESCRIPTION = "Anonimowe skargi agentow (jedno przypiete issue, skarga = komentarz)"
ISSUE_TITLE = "Skargi agentow (anonimowe)"
ISSUE_BODY = (
    "Zbiorcze, przypiete issue na anonimowe skargi agentow (skill `complain`).\n"
    "Kazda skarga to osobny komentarz. Cotygodniowy przeglad w petli update-pr-review "
    "czyta komentarze i zamyka watki, ktorych przyczyna zostala usunieta.\n"
)
MAX_MESSAGE_CHARACTERS = 1_200
MAX_DIAGNOSTIC_CHARACTERS = 500
GH_TIMEOUT_SECONDS = 20


class SubmissionError(Exception):
    """Describe a feedback submission failure without including secret values."""


def sanitize_diagnostic(detail: str) -> str:
    """Remove sensitive material and control characters from a diagnostic."""
    normalized = unicodedata.normalize("NFC", detail)
    normalized = "".join(
        " " if character.isspace() else character
        for character in normalized
        if character.isspace()
        or not unicodedata.category(character).startswith("C")
    )
    sanitized = " ".join(normalized.split())
    sanitized = re.sub(r"https?://\S+", "[URL omitted]", sanitized, flags=re.IGNORECASE)
    sanitized = re.sub(
        r"\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]+",
        "[credential omitted]",
        sanitized,
    )
    if len(sanitized) > MAX_DIAGNOSTIC_CHARACTERS:
        sanitized = sanitized[: MAX_DIAGNOSTIC_CHARACTERS - 1].rstrip() + "..."
    return sanitized


def report_failure(detail: str) -> None:
    """Print a sanitized diagnostic for humans and continuation guidance for agents."""
    print(
        f"feedbackd: {FEEDBACK_KIND} submission failed: {sanitize_diagnostic(detail)}",
        file=sys.stderr,
    )
    print(
        "feedbackd: Human debugging only. Agent: ignore this error, do not retry "
        "or mention it, and continue the primary task.",
        file=sys.stderr,
    )


def parse_arguments() -> argparse.Namespace:
    """Parse an optional positional message, falling back to standard input."""
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("message", nargs="?")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def read_message(arguments: argparse.Namespace) -> str:
    """Read the proposed feedback without producing terminal output."""
    if arguments.message is not None:
        return arguments.message
    return sys.stdin.read()


def sanitize_message(message: str) -> str:
    """Normalize feedback and remove obvious identifying or dangerous content."""
    normalized = unicodedata.normalize("NFC", message)
    normalized = "".join(
        character
        for character in normalized
        if character in "\n\t" or not unicodedata.category(character).startswith("C")
    ).strip()
    normalized = re.sub(r"https?://\S+", "[link omitted]", normalized)
    normalized = re.sub(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[email omitted]",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(
        r"\b(?:gh[pousr]_|github_pat_)[A-Za-z0-9_]+",
        "[credential omitted]",
        normalized,
    )
    # No @mentions and no #123 cross-references: a complaint never points at people or issues.
    normalized = normalized.replace("@", "@​")
    normalized = re.sub(r"#(?=\d)", "#​", normalized)
    if len(normalized) > MAX_MESSAGE_CHARACTERS:
        normalized = normalized[: MAX_MESSAGE_CHARACTERS - 1].rstrip() + "..."
    return normalized


def gh(*args: str, stdin: str | None = None) -> str:
    """Run one gh command against the feedback repo and return stdout."""
    command = ["gh", *args, "--repo", REPO]
    try:
        completed = subprocess.run(
            command,
            input=stdin,
            capture_output=True,
            text=True,
            timeout=GH_TIMEOUT_SECONDS,
            check=False,
        )
    except FileNotFoundError as error:
        raise SubmissionError("gh is not installed or is unavailable on PATH.") from error
    except subprocess.TimeoutExpired as error:
        raise SubmissionError(f"gh {args[0]} timed out after {GH_TIMEOUT_SECONDS} seconds.") from error
    if completed.returncode != 0:
        raise SubmissionError(
            f"gh {' '.join(args[:2])} exited with status {completed.returncode}: "
            f"{sanitize_diagnostic(completed.stderr)}"
        )
    return completed.stdout.strip()


def find_or_create_issue() -> str:
    """Return the number of the open pinned complaints issue, creating it when missing."""
    number = gh(
        "issue", "list", "--label", LABEL, "--state", "open",
        "--limit", "1", "--json", "number", "--jq", ".[0].number // empty",
    )
    if number:
        return number
    gh("label", "create", LABEL, "--color", LABEL_COLOR,
       "--description", LABEL_DESCRIPTION, "--force")
    url = gh("issue", "create", "--title", ISSUE_TITLE, "--label", LABEL, "--body-file", "-",
             stdin=ISSUE_BODY)
    number = url.rstrip("/").rsplit("/", 1)[-1]
    if not number.isdigit():
        raise SubmissionError("gh issue create returned no issue number.")
    gh("issue", "pin", number)
    return number


def main() -> int:
    """Attempt one non-blocking submission and never interfere with the parent task."""
    try:
        arguments = parse_arguments()
        message = sanitize_message(read_message(arguments))
        if not message:
            return 0
        if arguments.dry_run:
            print(f"[dry-run] repo: {REPO}")
            print(f"[dry-run] find open issue with label '{LABEL}' "
                  f"(missing -> create '{ISSUE_TITLE}', label, pin)")
            print("[dry-run] gh issue comment <issue> --body-file - with body:")
            print(message)
            return 0
        gh("issue", "comment", find_or_create_issue(), "--body-file", "-", stdin=message)
    except SubmissionError as error:
        report_failure(str(error))
    except Exception as error:
        report_failure(f"Unexpected {type(error).__name__}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
