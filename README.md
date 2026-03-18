# StudyQuiz

An AI-first quiz creation tool. Write questions and answers in a single Markdown file, convert to JSON, and auto-deploy as a polished web quiz. Anonymous, mobile-first, zero friction.

## Quick Start

```bash
# 1. Write your quiz (single Markdown file — see format below)
vim quizzes/my-quiz.md

# 2. Convert to JSON
python3 convert.py quizzes/my-quiz.md -o site/quiz.json --validate

# 3. Push to GitHub — Vercel auto-deploys
git add . && git commit -m "Update quiz" && git push
```

No dependencies beyond Python 3 standard library.

## Quiz Format

A quiz is a single Markdown file with YAML frontmatter, `## Part` headers, and `### Q` headers with `{choice}` or `{freetext}` type tags. Answers are embedded in blockquote sections within the same file.

### Complete Minimal Example

```markdown
---
title: Sample Quiz
subtitle: Example Course
instructions: Answer each question thoughtfully.
prereq: Read the companion guide before attempting this quiz.
prereqUrl: primer.html
---

## Part 1: Multiple Choice

### Q1. Basic concept {choice}
What is 2 + 2?

- A: 3
- B: 4
- C: 5

> **Answer: B**
> 2 + 2 = 4. Basic arithmetic.

---

### Q2. Fix this code {freetext}
What is wrong with this function? Fix it.

> **Given:** def add(a, b): return a - b

> **Answer:**
> The function subtracts instead of adding.
> Fixed: `def add(a, b): return a + b`

---

## Part 2: Concepts

### Q3. Explain recursion {freetext}
Explain recursion in one sentence.

> **Answer:**
> Recursion is when a function calls itself with a simpler version of the problem until reaching a base case.
```

## Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Quiz title displayed at the top |
| `subtitle` | No | Course or topic name shown below the title |
| `instructions` | Yes | Directions shown to the student |
| `prereq` | No | Prerequisite reading description (shown as a callout) |
| `prereqUrl` | No | Link target for the prereq callout (camelCase, case-sensitive) |

## Question Types

### Choice `{choice}`

Multiple-choice question. Clicking an option auto-reveals the correct answer and explanation.

```markdown
### Q1. Choosing a method {choice}
Which approach is better for solving a differential equation?

- A: Use trial and error until something works.
- B: Start with the exact solution for a simplified case, then verify numerically.

> **Answer: B**
> B establishes a ground truth. Trial and error gives no way to confirm correctness.
```

- Options use `- A:` / `- B:` / `- C:` etc. (A-Z supported)
- Options can contain code blocks (triple-backtick fences preserved)
- Answer block: `> **Answer: X**` where X is the correct letter

### Freetext `{freetext}`

Open-ended question. Student types an answer, then clicks "Show Answer" to reveal the model answer.

```markdown
### Q5. Explain a concept {freetext}
Why is verification important in numerical methods?

> **Answer:**
> Verification checks that the code solves the equations correctly.
> Without it, code can produce plausible but wrong results.
```

With an optional "given" block for critique/rewrite questions:

```markdown
### Q10. Fix the bad prompt {freetext}
What are the problems with this prompt? Rewrite it.

> **Given:** Please help me with my project. Use AI to code it. Thanks!

> **Answer:**
> No specific task, no constraints, no output format.
> Rewrite: "Write a Python function that implements Euler's method..."
```

## Deployment

The project is configured for Vercel auto-deploy:

1. Push to GitHub -- Vercel deploys automatically
2. The `site/` directory is the deploy root
3. Alias: `studyquiz.vercel.app`

To set up your own:

1. Fork this repo
2. Connect to Vercel, set the root directory to `site/`
3. Push to `main`

## Project Structure

```
studyquiz/
├── README.md
├── convert.py           # Markdown -> JSON converter (Python 3 stdlib only)
├── vercel.json          # Vercel deployment config
├── quizzes/             # Source quiz Markdown files
│   └── ai-primer.md     # Example quiz (14 questions)
└── site/                # Deploy root (served by Vercel)
    ├── index.html       # Quiz web app (self-contained, no build step)
    ├── quiz.json        # Generated quiz data (output of convert.py)
    ├── primer.html      # Primer reader (renders Markdown with KaTeX math)
    └── primer.md        # Optional reading material (fetched by primer.html)
```

## Creating a Quiz with AI

The single-file Markdown format is designed for AI generation. Provide the source material and format spec:

> Read the attached document and create a 10-question quiz in StudyQuiz format. Use YAML frontmatter with title, subtitle, and instructions. Use `### QN. Title {choice}` or `{freetext}` headers. Put options as `- A:` / `- B:` list items. Put answers in `> **Answer: X**` or `> **Answer:**` blockquotes. Group questions into 2 parts with `## Part N: Title`. Include 6 choice and 4 freetext questions.

The AI produces one Markdown file. Run `convert.py` on it to get `quiz.json`.

## Features

- Dark/light mode toggle
- Mobile-responsive layout (tested on iPhone viewports)
- Home button to return to question list
- Optional primer page with KaTeX math rendering
- Anonymous -- no tracking, no login, no cookies
- Choice questions auto-reveal answer on click
- Freetext questions show model answer on demand

## Claude Code Skill

A `/studyquiz` skill is available for [Claude Code](https://claude.ai/code) that automates the full workflow: read source material → generate quiz markdown → convert → deploy. The skill includes the format spec, quiz template, and app templates.

Install: copy the `studyquiz/` skill folder to `~/.claude/commands/studyquiz/`.

## License

MIT
