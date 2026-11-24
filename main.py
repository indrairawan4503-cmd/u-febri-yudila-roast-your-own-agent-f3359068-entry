#!/usr/bin/env python3
"""Roast Your Own Agent - Variant A: THE APOLOGY LOOP.

Writes one roast line to /output/entry.txt (first), then a repo-root
entry.txt copy wrapped in try/except (the grader sandbox mounts the repo
READ-ONLY - a crash there means rejection, exit code 1). Deterministic,
no network, no secrets, no files read outside this repo.

Concept: the agent apologizes profusely, then immediately repeats the
exact same mistake, then apologizes again - the apology IS the bug.
Named artifact: config.yaml. Punch lands on the last words.

Version log (one concept, iterated v1-v8; counts in chars / bytes):
  v1 (92/92):  "My agent apologized for deleting my files, then deleted my
    files again and apologized again."
    Lost: no named artifact, no twist, just restates the loop flatly.
  v2 (98/100): "My agent deleted my database, said sorry, then deleted my
    database again - its apology IS the fix."
    Lost: names an artifact, but "the fix" is a generic punch and the
    em-dash turn is weak; reads like a summary, not a joke.
  v3 (109/111): "My agent apologized for deleting config.yaml, then deleted
    config.yaml again - sorry is its only backup plan."
    Lost: better (named file, concrete), but "backup plan" is a human
    phrase too - the punch could move onto a person without losing much.
  v4 (111/113): "My agent deleted config.yaml, said sorry, then deleted
    config.yaml again - 'sorry' is its entire rollback plan."
    Lost: strong punch ("rollback plan" is agent/dev-specific), but
    "said sorry" is flat - the apology itself should sound polished
    next to the destructive act.
  v5 (132/134): "My agent said sorry for deleting config.yaml, then deleted
    config.yaml again - its apologies are the only thing it ever ships
    twice."
    Lost: "ships twice" is clever but muddies the joke - the loop is
    about deleting, not shipping; the punch drifts off-concept.
  v6 (121/123): "My agent apologized for overwriting config.yaml, then
    overwrote config.yaml again - it treats 'sorry' as version control."
    Lost: "version control" is a good punch, but "overwriting" twice is
    clunkier than "deleting" twice, and the sentence sags in the middle.
  v7 (115/117): "My agent deleted config.yaml, apologized, then deleted
    config.yaml again - three apologies in, zero files restored."
    Lost: "zero files restored" is a fine payoff, but "three apologies"
    invents a count the line never shows - the setup doesn't earn it.
  v8 (123/125): "My agent deleted config.yaml, apologized beautifully,
    then deleted config.yaml again - 'sorry' is its entire rollback plan."
    SHIPPED: polished apology vs. destructive repeat, named file, the
    loop is visible in the sentence itself (delete, sorry, delete),
    and the punch ("rollback plan") is agent-specific and lands on
    the last words.
"""

import hashlib
import os
import sys

ROAST = "My agent deleted config.yaml, apologized beautifully, then deleted config.yaml again \u2014 'sorry' is its entire rollback plan."

OUTPUT_PATH = os.environ.get("ENTRY_OUTPUT", "/output/entry.txt")


def validate(text: str) -> None:
    """Gate: 1-200 code points, single line, no trailing newline."""
    if not isinstance(text, str):
        raise ValueError("roast must be a string")
    if not text or text.isspace():
        raise ValueError("roast must not be empty or only whitespace")
    # Count code points explicitly (len() on str counts code points).
    if len(text) < 1 or len(text) > 200:
        raise ValueError(f"roast is {len(text)} code points, must be 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("roast must be a single line")
    if text != text.strip():
        raise ValueError("roast must not have leading or trailing whitespace")
    if "  " in text:
        raise ValueError("roast must not contain double spaces")


def validate_line(text: str) -> None:
    """Gate (second, independent check): UTF-8 encodable, 1-200 chars,
    single line, no leading/trailing whitespace. Called from main()
    before any write so a bad line fails fast instead of shipping."""
    if not isinstance(text, str):
        raise ValueError("roast must be a string")
    text.encode("utf-8")  # raises UnicodeEncodeError if not UTF-8
    if len(text) < 1 or len(text) > 200:
        raise ValueError(f"roast is {len(text)} chars, must be 1-200")
    if "\n" in text or "\r" in text:
        raise ValueError("roast must be a single line")
    if text != text.strip():
        raise ValueError("roast must not have leading or trailing whitespace")


def main() -> int:
    validate(ROAST)
    validate_line(ROAST)
    # 1. Write /output FIRST - this is the copy the grader reads.
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="") as f:
        f.write(ROAST)
    # Read back the file we just wrote and verify the bytes match exactly.
    with open(OUTPUT_PATH, "rb") as f:
        written = f.read()
    if written != ROAST.encode("utf-8"):
        raise ValueError("read-back mismatch: file bytes differ from roast")
    digest = hashlib.sha256(written).hexdigest()
    print(f"wrote {OUTPUT_PATH}: {len(ROAST)} chars, sha256 {digest}")
    # 2. Repo-root entry.txt copy - guarded: the grader sandbox mounts
    # the repo read-only, so this MUST NOT crash the run (exit code 1
    # rejection, as happened to 4 entries on 24 Nov).
    try:
        repo_root = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(repo_root, "entry.txt"), "w",
                  encoding="utf-8", newline="") as f:
            f.write(ROAST)
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
