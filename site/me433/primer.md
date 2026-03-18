# The Four Components of AI Coding Agents

**ME433 — Introduction to Computational Fluid Dynamics**\
Spring 2026 | Prof. Junlin Yuan

---

> You are about to use AI agents to write, test, and verify CFD solvers. This guide covers what you need to know. Read it once. Keep it as a reference. Then take the companion quiz.

In this course, you will use AI coding agents. These programs read your instructions, plan, write code, run it, check it, and fix mistakes on their own. Your job is to supervise. You do not write the code, you write the agent team.

Every AI agent has four components:

| # | Component | What it is | Analogy |
|---|-----------|-----------|---------|
| 1 | **Model** | The "brain" — a large language model that predicts text | The employee's education and experience |
| 2 | **Context** | Everything the model can "see" right now | The project folder on the employee's desk |
| 3 | **Prompt** | Your instructions to the model | The task assignment you write |
| 4 | **Tools** | Actions the model can take beyond generating text | The software and equipment the employee can use |

Get any one wrong and the agent fails. Get all four right and the agent can build a working CFD solver in minutes.

---

## Component 1: Model

### What is a model?

A large language model (LLM) is a neural network trained on text. Given everything that came before, it predicts the next token (roughly, the next word or code fragment). It does not understand your code. It recognizes patterns from training data and generates statistically likely continuations.

Key terms:

| Term | What it means | Why you care |
|------|--------------|-------------|
| **Parameters** | Internal weights learned during training (billions) | More parameters = more capacity, but not always better for your task |
| **Tokens** | The unit the model reads and writes (~0.75 words per token) | You are billed per token. Your prompt, the response, and all context consume tokens |
| **Context window** | Total tokens the model can "see" at once (input + output) | If your code + prompt exceeds this, the model forgets the beginning |
| **Temperature** | Controls randomness (0 = deterministic, 1 = creative) | For code, use low temperature (0–0.2). For brainstorming, higher. But temperature is a blunt tool. It reduces randomness in word choice; it does not control output *structure*. If you need a specific format, explicit format instructions are more reliable than lowering temperature. |


### Common misconceptions

- **"Bigger is always better."** False. A smaller model fine-tuned for code can outperform a larger general model.
- **"The model understands my code."** False. It predicts likely token sequences. It can produce code that compiles, runs, and gives wrong physics.
- **"All models are the same."** False. Models have distinct strengths. Gemini is fast with large context. Claude is thorough and cautious. GPT is versatile.

### Choosing a model

Use the smallest model that reliably handles your task.

- **Simple tasks** (formatting, boilerplate, file operations): Use a fast model (Gemini 3 Flash, GPT-5.4 mini, Claude Haiku 4.5)
- **Complex tasks** (solver architecture, debugging numerics, multi-step reasoning, large code base): Use a stronger model (Claude Sonnet/Opus, GPT-5.4, Gemini Pro)

---

## Component 2: Context

### What is context?

Context is everything the model can see when it generates a response: your prompt, conversation history, files it has read, tool results, and system instructions. All of it must fit inside the context window.

Think of it as the project folder on an employee's desk. Empty folder means guessing. Right specs, equations, and reference code means real work.

### Why context is the highest-leverage component

Giving the model the right information matters more than clever phrasing. A mediocre prompt with good context beats a brilliant prompt with no context.

For CFD agents, useful context includes:

| Context type | Example |
|-------------|---------|
| Governing equations | 1D heat equation: $\partial T/\partial t = K \, \partial^2 T / \partial x^2$ |
| Discretization scheme | Explicit Euler + 2nd-order central difference |
| Stability criteria | CFL condition: $\Delta t = \text{CFL} \cdot \Delta x^2 / (2K)$ |
| Boundary and initial conditions | $T(0,t) = T(1,t) = 0$, $T(x,0) = \sin(\pi x)$ |
| Exact solutions for verification | $T(x,t) = e^{-\pi^2 t} \sin(\pi x)$ |
| Language and environment | MATLAB, 1-based indexing, headless mode |
| Output structure | Files in `solution/`, figures as PNG |

### How context works in your agent team

In your OpenCode setup, context is managed through two mechanisms:

1. **AGENTS.md** — A shared project file that all agents read. It contains language rules, output directory structure, error norm formulas, and code quality standards. This is the "company handbook" that every employee reads on day one.

2. **plan.md** — Created by the planner agent, read by all downstream agents. It contains the numerical scheme, grid parameters, test cases, and verification strategy. This is the "project specification" that the team follows.

### Key principle: context isolation

Each agent in your team has a small, focused context window — only the information it needs for its specific job. The planner sees the problem spec. The implementer sees the plan. The code-reviewer sees the code + plan. This prevents agents from getting confused by irrelevant information.

This is why a team of five specialists (each with 10 pages of focused context) outperforms one generalist agent given 50 pages of everything.

Even when everything fits in the context window, too much irrelevant information dilutes the signal. The model pays less attention to what matters when surrounded by noise. When context is tight, cut irrelevant background before cutting examples or constraints — those directly shape the output.

---

## Component 3: Prompt

### What is a prompt?

A prompt is your instruction to the model. For coding agents, a good prompt reads like a design specification, not a conversation.

### The five elements that matter

Anthropic, Google, and OpenAI all converge on the same core ingredients. Forget the acronyms. Remember these five:

| Element | What to include | Example |
|---------|----------------|---------|
| **Task** | What exactly the agent must produce | "Write a MATLAB function that solves the 1D heat equation using explicit Euler" |
| **Context** | The background information needed | "Grid: uniform, Nx points. Time integration: forward Euler. CFL = 0.5" |
| **Constraints** | What NOT to do, boundaries | "Do not use implicit methods. MATLAB only. No external toolboxes" |
| **Output format** | Exact shape of the deliverable | "Save as `heat_solver.m`. Include header comment with equation and scheme" |
| **Examples / Verification** | Input/output pairs or acceptance criteria | "For Nx=10 and CFL=0.5, the L2 error at t=0.1 should be approximately 0.008" |

### What works (evidence-based)

These five techniques have the strongest support from research and practice:

1. **Be specific about the task and output format.** The single most reliable lever. "Write a function" is vague. "Write a MATLAB function `heat1d.m` that takes `Nx` and `CFL` as inputs and returns the temperature array `T`" is specific.

2. **Give examples when format matters.** Few-shot prompting (showing input/output pairs) is one of the most validated techniques across all vendors. One example helps, but it can be misread as a special case. Two or three diverse examples establish a pattern the model will follow reliably.

3. **Provide real context.** Equations, code, specs, and test values. The model cannot infer physics from nothing.

4. **Break complex work into steps.** Not "solve this CFD problem." Instead: plan the numerics, write the solver, test, verify against exact solution. This changes *how* the model reasons, not just *what* it reasons about. Compare with vague meta-instructions like "be very careful" or "double-check your work," which sound helpful but do not change the model's computation path. Explicit steps do.

5. **Include verification criteria.** Tell the agent how to check its own work. "The observed order of accuracy should approach 2.0 for the 2nd-order scheme."

### What does NOT matter much

- **Generic expert personas** ("You are a world-class CFD expert"): Changes style and tone, not correctness. A narrow role ("You are the ME433 code-reviewer") works better because it scopes the job and limits drift. Personas can be useful for setting a *pervasive tone* (formal, cautious, concise), but they do not make the model smarter or more accurate on technical tasks.
- **Politeness words** ("please," "thank you"): No measurable effect on output quality.
- **Vague quality words** ("write clean code," "be concise," "be careful"): These sound reasonable but give the model no measurable target. "Be concise" is ambiguous. "Under 100 words, bullet points, no filler" is specific and reliably followed. Always prefer measurable constraints over adjectives.
<!-- - **Branded acronym frameworks** (CO-STAR, RISEN, etc.): Memory aids, not magic. They all encode the same five elements above. -->

### Prompt = specification

The best mental model:

> Write your prompt the way you would write a software specification. Be precise about inputs, outputs, constraints, and acceptance criteria. The model is a contractor following your spec.

Vague spec means the contractor guesses. Precise spec means the contractor delivers.

---

## Component 4: Tools

### What are tools?

An LLM without tools is a brain in a jar. It can generate text, but cannot read files, run code, or check results. Tools give it hands.

A tool is a software function the model can call. The model decides *when* to call it and *what arguments* to pass. The host application executes the function, feeds the result back, and the model reasons about what to do next.

### The agentic loop

Every AI coding agent runs this cycle:

```
Think → Act (use a tool) → Observe (read the result) → Repeat
```

For example, the verifier agent in your team:

1. **Think:** "I need to run the MATLAB solver to check if it works."
2. **Act:** Calls the shell tool: `matlab -batch "run('solution/heat_solver.m')"`
3. **Observe:** Reads MATLAB output — sees an error at line 42.
4. **Think:** "There is an index-out-of-bounds error. I need to report this."
5. **Act:** Writes a verification report noting the failure.

Without tools, the verifier could only *guess* whether the code works. With tools, it *knows*.

### Common tools in coding agents

| Tool | What it does | Which agents use it |
|------|-------------|-------------------|
| **File read** | Read source code, specs, plans | All agents |
| **File write** | Create or edit code files | Implementer, report-writer |
| **Shell / terminal** | Run MATLAB, compile, execute scripts | Verifier, implementer |
| **Search** | Find patterns in code, search documentation | Code-reviewer |
| **Web fetch** | Retrieve reference data or documentation | (restricted in this course) |

### Tool permissions: the principle of least privilege

Each agent should only have the tools it needs. This is a safety and quality principle:

| Agent | Can read files | Can write files | Can run code | Why |
|-------|:---:|:---:|:---:|-----|
| Planner | Yes | Yes (plan only) | No | Planners should think, not execute |
| Implementer | Yes | Yes | No | Writes code but does not test it (separation of concerns) |
| Code-reviewer | Yes | No | No | Reviewers must be read-only to stay objective |
| Verifier | Yes | Yes (report) | Yes | Must run code to verify |
| Report-writer | Yes | Yes (report) | Yes (LaTeX compile) | Must compile the report |

If the code-reviewer could edit files, it might "fix" bugs silently instead of reporting them. If the planner could run code, it might skip thinking and jump to trial-and-error. Restricting tools enforces discipline.

### MCP: the universal connector

Model Context Protocol (MCP) is an open standard (Anthropic, 2024) for connecting AI models to tools. Think of it as **USB-C for AI tools**: a universal plug that any model can use with any tool.

Before MCP, every AI application needed custom code for every tool. With MCP, a tool is built once as an MCP server and works with any AI application that supports the protocol.

Example: In Projects 1 & 2, you can make an MCP tool that runs your code, called on demand by ChatGPT/Claude Desktop/OpenCode, ...

---

## Resources

### Official prompt engineering guides

| Source | What it covers |
|--------|---------------|
| [Anthropic: Prompt Engineering](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) | Clarity, context, examples, XML structure, tool use |
| [Anthropic: Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | When to use workflows vs. agents, orchestration patterns |
| [Google: Gemini Prompting Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) | Templates, few-shot, long-context, agentic workflows |
| [OpenAI: Prompt Engineering Guide](https://developers.openai.com/api/docs/guides/prompt-engineering/) | Structured prompts, few-shot, formatting |
| [OpenAI: A Practical Guide to Building Agents](https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf) | Single vs. multi-agent design, tool design, guardrails |

### Practitioner references

| Author | What | Why read it |
|--------|------|------------|
| Simon Willison | [How I use LLMs to help me write code](https://simonwillison.net/2025/Mar/11/using-llms-for-code/) | Best practitioner piece on treating prompts as specs and always testing |
| Ethan Mollick | [A Guide to Prompting AI (for what it is worth)](https://www.oneusefulthing.org/p/a-guide-to-prompting-ai-for-what) | Emphasizes interaction over magic one-shot prompts |
| Lilian Weng | [Prompt Engineering](https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/) (blog) | Broad conceptual overview, research-grounded |

---

## Quick Reference Card

### Writing a good prompt (5 rules)

1. **Specify the task precisely.** What file, what function, what inputs, what outputs.
2. **Give real context.** Equations, boundary conditions, grid parameters, test values.
3. **Set constraints.** Language, libraries, what NOT to do.
4. **Lock the output format.** File names, section headers, figure format.
5. **Include verification criteria.** Expected values, error tolerances, convergence rates.

### Designing a good agent (8-part checklist)

1. **Identity** — Narrow job title, not a grand persona
2. **Task + success condition** — What to produce, how success is judged
3. **Inputs and context** — What files/docs to read as source of truth
4. **Constraints** — Boundaries and prohibitions
5. **Output format** — Exact sections or file structure
6. **Examples** — One or two when format or style matters
7. **Tool permissions** — What tools the agent may and may not use
8. **Stop condition** — When to stop, hand off, or ask for help

