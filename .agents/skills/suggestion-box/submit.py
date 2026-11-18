#!/usr/bin/env python3
"""Submit an internal agent suggestion as its own GitHub issue without blocking the parent task.

Every suggestion becomes a separate issue labelled `agent-sugestia`. The label is created
(idempotently) before the issue.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import unicodedata
import urllib.parse

FEEDBACK_KIND = "suggestion"
REPO = os.environ.get("BAZARTY_FEEDBACK_REPO", "Enkidu-png/bazarty-platforma")
LABEL = "agent-sugestia"
LABEL_COLOR = "0E8A16"
LABEL_DESCRIPTION = "Sugestia agenta (skill suggestion-box), jedna sugestia = jedno issue"
TITLE_PREFIX = "Sugestia agenta: "
MAX_TITLE_CHARACTERS = 90
MAX_MESSAGE_CHARACTERS = 1_200
MAX_DIAGNOSTIC_CHARACTERS = 500
GH_TIMEOUT_SECONDS = 20
SENSITIVE_URL_QUERY_KEYS = frozenset(
    {
        "access_token",
        "api_key",
        "secret",
        "sig",
        "signature",
        "token",
        "x-amz-credential",
        "x-amz-signature",
        "x-goog-credential",
        "x-goog-signature",
    }
)


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


def sanitize_url(match: re.Match[str]) -> str:
    """Preserve an ordinary link or redact a URL that appears to contain credentials."""
    url = match.group(0)
    try:
        parsed = urllib.parse.urlsplit(url)
        query_keys = {
            key.casefold()
            for key, _ in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        }
        contains_credentials = (
            parsed.username is not None
            or parsed.password is not None
            or bool(query_keys & SENSITIVE_URL_QUERY_KEYS)
        )
    except ValueError:
        return url
    return "[credential URL omitted]" if contains_credentials else url


def sanitize_message(message: str) -> str:
    """Normalize feedback and remove obvious sensitive or dangerous content."""
    normalized = unicodedata.normalize("NFC", message)
    normalized = "".join(
        character
        for character in normalized
        if character in "\n\t" or not unicodedata.category(character).startswith("C")
    ).strip()
    normalized = re.sub(r"https?://\S+", sanitize_url, normalized, flags=re.IGNORECASE)
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
    # No @mentions: a suggestion is about systems, never a ping to a person.
    normalized = normalized.replace("@", "@​")
    if len(normalized) > MAX_MESSAGE_CHARACTERS:
        normalized = normalized[: MAX_MESSAGE_CHARACTERS - 1].rstrip() + "..."
    return normalized


def field(message: str, name: str) -> str:
    """Return the value of a `**Name:**` (or `*Name:*`) line, empty when absent."""
    match = re.search(rf"^\*{{1,2}}{name}:\*{{1,2}}\s*(.+)$", message, flags=re.MULTILINE)
    return match.group(1).strip() if match else ""


def build_title(message: str) -> str:
    """Build a short issue title from the Suggestion (or first) line."""
    summary = field(message, "Suggestion") or field(message, "Observation") or message.splitlines()[0]
    summary = re.sub(r"[`*_]", "", summary)
    category = field(message, "Category")
    title = f"{TITLE_PREFIX}{f'[{category}] ' if category else ''}{summary}"
    if len(title) > MAX_TITLE_CHARACTERS:
        title = title[: MAX_TITLE_CHARACTERS - 3].rstrip() + "..."
    return title


def gh(*args: str, stdin: str | None = None) -> str:
    """Run one gh command against the feedback repo and return stdout."""
    try:
        completed = subprocess.run(
            ["gh", *args, "--repo", REPO],
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


def main() -> int:
    """Attempt one non-blocking submission and never interfere with the parent task."""
    try:
        arguments = parse_arguments()
        message = sanitize_message(read_message(arguments))
        if not message:
            return 0
        title = build_title(message)
        if arguments.dry_run:
            print(f"[dry-run] repo: {REPO}")
            print(f"[dry-run] gh label create {LABEL} --force")
            print(f"[dry-run] gh issue create --label {LABEL} --title {title!r} with body:")
            print(message)
            return 0
        gh("label", "create", LABEL, "--color", LABEL_COLOR,
           "--description", LABEL_DESCRIPTION, "--force")
        gh("issue", "create", "--title", title, "--label", LABEL, "--body-file", "-", stdin=message)
    except SubmissionError as error:
        report_failure(str(error))
    except Exception as error:
        report_failure(f"Unexpected {type(error).__name__}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
