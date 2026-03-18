# StudyQuiz

An AI-first quiz creation tool. Write quiz content in Markdown, convert to JSON, and deploy as a polished, anonymous web app. Designed for educators and researchers who want to create self-study quizzes with zero friction.

## Features

- **Single-file input** -- One Markdown file with YAML frontmatter contains all questions, answers, and metadata
- **AI-friendly format** -- The Markdown format is designed so AI tools (Claude, ChatGPT, etc.) can reliably generate quizzes from any source material
- **Auto-deploy** -- Push to GitHub and Vercel deploys automatically
- **Anonymous** -- No tracking, no login, no cookies. Students see questions, pick answers, and compare with model answers
- **Two question types** -- Multiple choice (auto-reveals answer on click) and free-text (manual reveal with model answer)
- **Primer page** -- Optional reading material rendered from Markdown with math support (KaTeX)
- **Mobile-first** -- Clean, responsive design tested on iPhone viewports

## Quick Start

```bash
# 1. Write your quiz in Markdown (see format below)

# 2. Convert to JSON
python3 convert.py quizzes/my-quiz.md quizzes/my-quiz-answers.md -o site/quiz.json

# 3. (Optional) Add a reading primer
cp my-primer.md site/primer.md

# 4. Push to GitHub -- auto-deploys to Vercel
git add . && git commit -m "Update quiz" && git push
```

## Quiz Markdown Format

A quiz consists of two Markdown files: the **quiz file** (questions) and the **answer key** (answers and explanations).

### Quiz File

```markdown
# My Quiz Title

**Course Name — Subject Area**

> Read "The Companion Guide" before attempting this quiz.

**Instructions:** For each question, pick the best option and explain your reasoning.

## Part 1: Multiple Choice

**Q1. Choosing a method** — You need to solve a differential equation. Which approach is better?

> **A:** Use trial and error until something works.
>
> **B:** Start with the exact solution for a simplified case, then verify your numerical method against it.

**Q2. Setting constraints** — Which instruction gives clearer guidance?

> **A:** Write clean code.
>
> **B:** Write a function with docstring, type hints, and one unit test. Maximum 50 lines.

## Part 2: Free Response

**Q3. Fix the bad prompt** — What are the problems with this prompt? Rewrite it.

> Please help me with my project. Use AI to code it. Thanks!

**Q4. Explain a concept** — Why is verification important in numerical methods?

## Part 3: Concepts

**Q5.** Explain the difference between validation and verification using an analogy.
```

### Answer Key File

```markdown
# My Quiz Title — Answer Key

### Q1. Choosing a method — Answer: **B**

B is better because it establishes a ground truth. Trial and error (A) gives no way to confirm correctness.

### Q2. Setting constraints — Answer: **B**

"Clean code" is subjective. B gives measurable criteria: docstring, type hints, unit test, line limit.

### Q3. Fix the bad prompt

Three problems:
1. No specific task
2. No constraints or parameters
3. No output format

Sample rewrite: "Write a Python function `solve.py` that implements Euler's method for dy/dx = -2y, y(0) = 1. Step size h = 0.1, integrate to x = 5. Output: a CSV with columns x, y_numerical, y_exact, error."

### Q4. Explain a concept

Sample answer: Verification checks that the code solves the equations correctly (math is right). Validation checks that the equations describe reality (physics is right). You need both.

### Q5. Validation vs. verification

Sample answer: Verification is checking that you built the bridge according to the blueprint. Validation is checking that the blueprint describes a bridge that will actually hold traffic.
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| Title | Yes | The `# heading` becomes the quiz title |
| Subtitle | No | A `**bold line**` with course/subject info |
| Instructions | No | Line starting with `**Instructions:**` |
| Prereq | No | Line containing "before attempting this quiz" -- shown as a callout |
| Parts | No | `## Part N: Title` headings group questions |

### Question Types

| Type | Format | Behavior |
|------|--------|----------|
| **choice** | Options in `> **A:**` / `> **B:**` blockquote | Clicking an option auto-reveals the correct answer |
| **freetext** | No options; optional `> quoted` given text | Student types answer, clicks "Show Answer" to see model answer |

## JSON Schema

The converter outputs a single JSON file with this structure:

```json
{
  "title": "Quiz Title",
  "subtitle": "Course — Subject",
  "instructions": "Instructions text",
  "prereq": "Prerequisite reading description",
  "prereqUrl": "primer.html",
  "parts": [
    { "number": 1, "title": "Part Title", "description": "Optional description" }
  ],
  "questions": [
    {
      "id": 1,
      "part": 1,
      "title": "Short title",
      "stem": "The question text",
      "type": "choice",
      "options": { "A": "Option A text", "B": "Option B text" },
      "answer": "B",
      "explanation": "Why B is correct"
    },
    {
      "id": 2,
      "part": 2,
      "title": "Short title",
      "stem": "The question text",
      "type": "freetext",
      "given": "Optional prompt to improve or context",
      "answer": "Model answer text"
    }
  ]
}
```

## Deployment

- Hosted on [Vercel](https://vercel.com/) (free tier)
- Connected to GitHub for auto-deploy on push
- The `site/` directory is the deploy root

To set up your own deployment:

1. Fork this repo
2. Connect to Vercel, set the root directory to `site/`
3. Push to `main` -- Vercel deploys automatically

## Project Structure

```
studyquiz/
├── .gitignore
├── README.md
├── convert.py           # Markdown → JSON converter (Python 3, stdlib only)
├── quizzes/             # Source quiz Markdown files
│   └── ai-primer.md     # Example quiz
├── site/                # Deploy root (served by Vercel)
│   ├── index.html       # Quiz app (self-contained, no build step)
│   ├── primer.html      # Primer reader (renders Markdown with KaTeX math)
│   ├── quiz.json        # Generated quiz data (output of convert.py)
│   └── primer.md        # Optional reading material (fetched by primer.html)
```

## Creating a Quiz with AI

The Markdown format is designed to be generated by AI. Provide:

1. **Source material** -- a document, lecture notes, textbook chapter, or any reference
2. **The format template** -- point the AI to the Quiz Markdown Format section above
3. **Desired question mix** -- number and types of questions

Example prompt:

> Read this document and create a 10-question quiz in StudyQuiz Markdown format (see README). Use 6 multiple-choice and 4 free-text questions. Group them into two parts: "Core Concepts" (choice) and "Apply Your Knowledge" (freetext). Also generate the answer key file with explanations.

The AI will produce two Markdown files. Run `convert.py` on them to get `quiz.json`.

## License

MIT
