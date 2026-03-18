# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

StudyQuiz: single-file Markdown quizzes → JSON → static web app. No build step, no npm, no external dependencies. Deployed on Vercel at `studyquiz.vercel.app`.

## Commands

```bash
# Convert quiz markdown to JSON (stdlib only, no pip install needed)
python3 convert.py quizzes/my-quiz.md -o site/quiz.json --validate

# Test locally — just open in browser (no dev server needed)
open site/index.html
open site/me433/index.html

# Deploy — push to main, Vercel auto-deploys from site/
git push
```

There are no tests, no linter, and no build step.

## Architecture

**Three components:**

1. **`quizzes/*.md`** — Source format. Single markdown file per quiz with YAML frontmatter, `## Part` headers, `### Q{N}. Title {choice|freetext}` question headers, and blockquote answer sections.

2. **`convert.py`** — Pure Python stdlib converter. Parses markdown → JSON with two-pass architecture (locate structure, then extract content). Has `--validate` flag for checking completeness and correctness.

3. **`site/`** — Static files served by Vercel. Each quiz lives in its own subdirectory (e.g., `site/me433/`) containing a self-contained `index.html` (single-file app with embedded CSS/JS), `quiz.json`, and optional `primer.html`/`primer.md`.

**Frontend is vanilla JS** — no framework, no build. Three screens: Start → Question → End. State managed via a plain object. Dark/light theme via CSS custom properties and `localStorage`. Mobile-first responsive design.

## Adding a New Quiz

1. Create `quizzes/my-quiz.md` following the format spec
2. Create `site/my-quiz/` directory
3. Copy `index.html` from an existing quiz subdirectory (e.g., `site/me433/index.html`)
4. Run: `python3 convert.py quizzes/my-quiz.md -o site/my-quiz/quiz.json --validate`
5. Accessible at `studyquiz.vercel.app/my-quiz/`

## Quiz Markdown Format

```markdown
---
title: Quiz Title
subtitle: Optional subtitle
instructions: Student-facing instructions
prereq: Optional prereq description
prereqUrl: primer.html
---

## Part 1: Section Title

### Q1. Question text {choice}
Stem text.

- A: Option A
- B: Option B

> **Answer: B**
> Explanation here.

---

### Q2. Open question {freetext}
What would you do?

> **Given:** Optional context block
>
> **Answer:**
> Model answer here.
```

Key rules: question headers must have `{choice}` or `{freetext}` tag; options use `- A:` format; answers in blockquotes with `> **Answer: X**` or `> **Answer:**`; `---` separators between questions.

## Vercel Config

`vercel.json` sets `outputDirectory: "site"` with no build command. The `site/` directory is served as-is.

## Code Conventions

- Frontend: vanilla JS, no dependencies, single-file HTML with embedded CSS/JS
- Backend: Python stdlib only (no pip packages)
- Design: Apple-style system fonts, 700px max-width, 12px border-radius cards
- CSS variables for theming (`--bg`, `--text`, `--accent`, etc.)
