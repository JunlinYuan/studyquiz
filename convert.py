#!/usr/bin/env python3
"""Convert a single-file quiz markdown into a JSON quiz file.

Usage:
    python convert.py quiz.md [-o quiz.json] [--validate]

The markdown file uses YAML frontmatter for metadata and inline type tags
({choice} or {freetext}) on question headers.  Answers are embedded in
blockquote sections within the same file.

Requires only the Python standard library.
"""

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _strip_blockquote(text: str) -> str:
    """Remove leading '> ' from every line."""
    lines = text.splitlines()
    out = []
    for line in lines:
        if line.startswith("> "):
            out.append(line[2:])
        elif line.startswith(">"):
            out.append(line[1:])
        else:
            out.append(line)
    return "\n".join(out)


def _strip_html_comments(text: str) -> str:
    """Remove HTML comments <!-- ... -->."""
    return re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)


def _clean_whitespace(text: str) -> str:
    """Collapse 3+ consecutive newlines to 2, strip outer whitespace."""
    text = text.strip()
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


# ---------------------------------------------------------------------------
# YAML frontmatter parser (no external deps)
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str):
    """Parse YAML frontmatter between --- delimiters.

    Returns (metadata_dict, remaining_text).
    Handles simple key: value pairs and quoted strings.
    """
    if not text.startswith("---"):
        return {}, text

    lines = text.split("\n")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break

    if end_idx is None:
        return {}, text

    fm_lines = lines[1:end_idx]
    remaining = "\n".join(lines[end_idx + 1:])

    meta = {}
    for line in fm_lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        m = re.match(r'^(\w+)\s*:\s*(.*)$', line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            # Strip surrounding quotes
            if len(val) >= 2 and val[0] == val[-1] and val[0] in ('"', "'"):
                val = val[1:-1]
            meta[key] = val

    return meta, remaining


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

_PART_RE = re.compile(r'^##\s+Part\s+(\d+)\s*:\s*(.+)', re.IGNORECASE)
_QUESTION_RE = re.compile(
    r'^###\s+Q(\d+)\.\s+(.+?)\s*\{(choice|freetext)\}\s*$'
)
_OPTION_RE = re.compile(r'^-\s+([A-Z])\s*:\s*(.*)')
_ANSWER_CHOICE_RE = re.compile(r'^\*\*Answer:\s*([A-Z])\*\*')
_ANSWER_FREETEXT_RE = re.compile(r'^\*\*Answer:\*\*')
_GIVEN_RE = re.compile(r'^\*\*Given:\*\*\s*(.*)')
_SEPARATOR_RE = re.compile(r'^---\s*$')


def parse_quiz(md: str) -> dict:
    """Parse a single-file quiz markdown into a structured dict."""

    md = _strip_html_comments(md)
    meta, body = _parse_frontmatter(md)

    lines = body.split("\n")
    total_lines = len(lines)

    # Metadata from frontmatter
    title = meta.get("title", "")
    subtitle = meta.get("subtitle", None)
    instructions = meta.get("instructions", "")
    prereq = meta.get("prereq", None)
    prereq_url = meta.get("prereqUrl", None)

    # First pass: locate parts and questions
    parts = []
    questions = []
    current_part = None

    # Indices of structural elements for slicing
    struct_indices = []  # (line_idx, type, data)

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Check for part header
        pm = _PART_RE.match(stripped)
        if pm:
            struct_indices.append((i, "part", {
                "number": int(pm.group(1)),
                "title": pm.group(2).strip(),
            }))
            continue

        # Check for question header
        qm = _QUESTION_RE.match(stripped)
        if qm:
            struct_indices.append((i, "question", {
                "id": int(qm.group(1)),
                "title": qm.group(2).strip(),
                "type": qm.group(3),
            }))
            continue

    # Second pass: extract part descriptions and question content
    current_part_num = 0

    for si, (line_idx, stype, sdata) in enumerate(struct_indices):
        # Determine end of this block
        if si + 1 < len(struct_indices):
            end_idx = struct_indices[si + 1][0]
        else:
            end_idx = total_lines

        if stype == "part":
            current_part_num = sdata["number"]
            # Collect description lines (between part header and next struct)
            desc_lines = []
            for j in range(line_idx + 1, end_idx):
                l = lines[j].strip()
                if l == "" or _SEPARATOR_RE.match(l):
                    continue
                # Stop at the first question header
                if _QUESTION_RE.match(l):
                    break
                desc_lines.append(l)

            parts.append({
                "number": sdata["number"],
                "title": sdata["title"],
                "description": " ".join(desc_lines) if desc_lines else "",
            })

        elif stype == "question":
            q = _parse_question_block(
                lines, line_idx, end_idx, sdata, current_part_num
            )
            questions.append(q)

    return {
        "title": title,
        "subtitle": subtitle,
        "instructions": instructions,
        "prereq": prereq,
        "prereqUrl": prereq_url,
        "parts": parts,
        "questions": questions,
    }


def _parse_question_block(
    lines: list, start: int, end: int, qdata: dict, part_num: int
) -> dict:
    """Parse a single question block from line `start` to `end`."""

    qid = qdata["id"]
    qtitle = qdata["title"]
    qtype = qdata["type"]
    block = lines[start + 1:end]  # skip the header line

    # -- Separate stem, options, blockquote sections --
    stem_lines = []
    options = {}
    current_option = None
    current_option_lines = []
    given_text = None
    answer_text = None
    explanation_lines = []
    in_answer = False
    in_given = False
    in_blockquote = False
    in_code_block = False  # track code blocks inside options

    # Track whether we've entered blockquote territory (answer/given)
    # or option territory
    phase = "stem"  # stem -> options -> blockquotes

    for raw_line in block:
        line = raw_line
        stripped = line.strip()

        # Skip separators
        if _SEPARATOR_RE.match(stripped):
            continue

        # === PHASE: stem ===
        if phase == "stem":
            # Check if this line starts options
            om = _OPTION_RE.match(stripped)
            if om:
                phase = "options"
                current_option = om.group(1)
                current_option_lines = [om.group(2)]
                continue

            # Check if this line starts a blockquote
            if stripped.startswith(">"):
                phase = "blockquote"
                # Fall through to blockquote handling below
            else:
                if stripped:
                    stem_lines.append(stripped)
                continue

        # === PHASE: options ===
        if phase == "options":
            # Track code blocks within options
            if stripped.startswith("```"):
                in_code_block = not in_code_block

            # If we're inside a code block, always append to current option
            if in_code_block:
                current_option_lines.append(raw_line.rstrip())
                continue

            # After closing a code block, check if a backtick line ended it
            # (already handled above with the toggle)

            om = _OPTION_RE.match(stripped)
            if om:
                # Save previous option
                if current_option:
                    options[current_option] = _finalize_option(
                        current_option_lines
                    )
                current_option = om.group(1)
                current_option_lines = [om.group(2)]
                continue

            # Check if we've moved to blockquote territory
            if stripped.startswith(">"):
                # Save current option
                if current_option:
                    options[current_option] = _finalize_option(
                        current_option_lines
                    )
                    current_option = None
                phase = "blockquote"
                # Fall through
            elif stripped == "":
                # Blank line - could be between options or end of options
                continue
            else:
                # Continuation of current option
                current_option_lines.append(stripped)
                continue

        # === PHASE: blockquote ===
        if phase == "blockquote":
            if stripped.startswith(">"):
                bq_content = stripped[1:].strip() if len(stripped) > 1 else ""

                # Check for Given:
                gm = _GIVEN_RE.match(bq_content)
                if gm:
                    in_given = True
                    in_answer = False
                    given_text = gm.group(1).strip() if gm.group(1).strip() else ""
                    continue

                # Check for Answer: X (choice)
                am = _ANSWER_CHOICE_RE.match(bq_content)
                if am:
                    in_answer = True
                    in_given = False
                    answer_text = am.group(1)
                    continue

                # Check for Answer: (freetext)
                afm = _ANSWER_FREETEXT_RE.match(bq_content)
                if afm:
                    in_answer = True
                    in_given = False
                    answer_text = ""
                    continue

                # Continuation of current blockquote section
                if in_given:
                    if given_text:
                        given_text += "\n" + bq_content
                    else:
                        given_text = bq_content
                elif in_answer:
                    explanation_lines.append(bq_content)
                continue
            elif stripped == "":
                # Blank line inside blockquote region - could separate
                # given from answer blocks
                continue
            else:
                # Non-blockquote line after blockquotes - ignore
                continue

    # Finalize any remaining option
    if current_option and phase == "options":
        options[current_option] = _finalize_option(current_option_lines)

    # Build the question dict
    stem = " ".join(stem_lines).strip()

    if qtype == "choice":
        explanation = _clean_whitespace("\n".join(explanation_lines))
        q = {
            "id": qid,
            "part": part_num,
            "title": qtitle,
            "stem": stem,
            "type": "choice",
            "options": options,
            "answer": answer_text or "",
            "explanation": explanation,
        }
    else:
        # freetext
        answer_body = _clean_whitespace("\n".join(explanation_lines))
        q = {
            "id": qid,
            "part": part_num,
            "title": qtitle,
            "stem": stem,
            "type": "freetext",
            "given": given_text if given_text else None,
            "answer": answer_body,
        }

    return q


def _finalize_option(lines: list) -> str:
    """Join option lines, handling code blocks properly."""
    if not lines:
        return ""

    # First line is always from the "- A: ..." match
    first = lines[0].strip()
    rest = lines[1:]

    if not rest:
        return first

    # Check if there's a code block in the option
    has_code = any("```" in l for l in rest)
    if has_code:
        # Preserve code block formatting with newlines
        parts = [first]
        for l in rest:
            parts.append(l)
        return "\n".join(parts)
    else:
        # Simple multi-line text: join with spaces
        parts = [first]
        for l in rest:
            parts.append(l.strip())
        return " ".join(parts)


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(data: dict) -> list:
    """Validate the quiz JSON structure. Returns list of issues."""
    issues = []

    if not data.get("title"):
        issues.append("Missing title")
    if not data.get("instructions"):
        issues.append("Missing instructions")

    part_numbers = {p["number"] for p in data.get("parts", [])}
    if not part_numbers:
        issues.append("No parts found")

    questions = data.get("questions", [])
    if not questions:
        issues.append("No questions found")

    seen_ids = set()
    for q in questions:
        qid = q["id"]
        if qid in seen_ids:
            issues.append(f"Duplicate question ID: Q{qid}")
        seen_ids.add(qid)

        if q["part"] not in part_numbers:
            issues.append(f"Q{qid}: references non-existent Part {q['part']}")

        if not q.get("stem"):
            issues.append(f"Q{qid}: missing stem text")

        if q["type"] == "choice":
            if not q.get("options"):
                issues.append(f"Q{qid}: no options found")
            if not q.get("answer"):
                issues.append(f"Q{qid}: no answer letter")
            elif q["answer"] not in q.get("options", {}):
                issues.append(
                    f"Q{qid}: answer '{q['answer']}' not in options"
                )
        elif q["type"] == "freetext":
            if not q.get("answer"):
                issues.append(f"Q{qid}: no answer text")

    return issues


def print_summary(data: dict, issues: list):
    """Print a validation summary."""
    print(f"Title: {data.get('title', '(none)')}")
    print(f"Subtitle: {data.get('subtitle', '(none)')}")
    print(f"Parts: {len(data.get('parts', []))}")
    print(f"Questions: {len(data.get('questions', []))}")

    # Count by type
    choice_count = sum(
        1 for q in data.get("questions", []) if q["type"] == "choice"
    )
    freetext_count = sum(
        1 for q in data.get("questions", []) if q["type"] == "freetext"
    )
    print(f"  Choice: {choice_count}")
    print(f"  Free-text: {freetext_count}")

    if issues:
        print(f"\nIssues ({len(issues)}):")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\nNo issues found.")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Convert single-file quiz markdown to JSON."
    )
    parser.add_argument("quiz_md", help="Path to quiz markdown file")
    parser.add_argument(
        "-o", "--output",
        default="quiz.json",
        help="Output JSON path (default: quiz.json)",
    )
    parser.add_argument(
        "--validate",
        action="store_true",
        help="Validate the output and print a summary",
    )
    args = parser.parse_args()

    quiz_path = Path(args.quiz_md)
    if not quiz_path.exists():
        print(f"Error: file not found: {quiz_path}", file=sys.stderr)
        sys.exit(1)

    try:
        md = quiz_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {quiz_path}: {e}", file=sys.stderr)
        sys.exit(1)

    result = parse_quiz(md)

    # Validate
    issues = validate(result)
    if args.validate:
        print_summary(result, issues)
        print()

    # Check for fatal issues
    fatal = [i for i in issues if "No questions" in i or "No parts" in i]
    if fatal:
        print("Fatal parsing errors:", file=sys.stderr)
        for f in fatal:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)

    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(result['questions'])} questions to {out_path}")

    if issues and not args.validate:
        print(f"Warnings: {len(issues)} issue(s) found. "
              "Run with --validate for details.", file=sys.stderr)

    sys.exit(0)


if __name__ == "__main__":
    main()
