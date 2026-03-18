---
title: AI Primer Quiz
subtitle: ME433 — Introduction to Computational Fluid Dynamics
instructions: For each question, pick the better option and explain why in one sentence. Some questions ask you to improve a prompt or answer a concept question.
prereq: Read "The Four Components of AI Coding Agents" guide before attempting this quiz.
prereqUrl: primer.html
---

## Part 1: Which Is Better?
Each pair addresses a real trade-off. Both options look reasonable. Pick the one that works better and explain why.

### Q1. Vague vs. specific {choice}
You ask an AI to plan a road trip from Detroit to Chicago. Which instruction produces a more useful result?

- A: Plan a great road trip from Detroit to Chicago. Be thorough and double-check everything.
- B: Plan a 3-day road trip from Detroit to Chicago. Leave Friday 8 AM, arrive Sunday 6 PM. Budget: $500. Two overnight stops. Each day: max 4 hours driving. Include one state park and one 4+ star restaurant. Output: table with columns Day, Departure, Destination, Drive time, Activity, Cost.

> **Answer: B**
> "Be thorough" and "double-check" are vague meta-instructions that do not change the model's computation path. B specifies constraints (budget, driving time, dates), quality criteria (4+ star), and output format (table with columns). Measurable targets beat adjectives.

---

### Q2. One example vs. multiple {choice}
You want the agent to format error output in a specific way. Which is more reliable?

- A: Report grid convergence results in this format:
```
Nx=10:  L2=8.21e-03  Linf=1.34e-02  order=--
```
Follow this pattern for all grid sizes.
- B: Report grid convergence results in this format:
```
Nx=10:  L2=8.21e-03  Linf=1.34e-02  order=--
Nx=20:  L2=2.06e-03  Linf=3.41e-03  order=1.99
Nx=40:  L2=5.16e-04  Linf=8.56e-04  order=2.00
```
Follow this pattern for all grid sizes.

> **Answer: B**
> One example can be misread as a special case. The model might think `order=--` is the format for all rows. Three diverse examples (including different order values) establish the pattern.

---

### Q3. Adjectives vs. measurable constraints {choice}
You want a concise verification report. Which instruction works better?

- A: Write a concise verification report. Keep it short and to the point.
- B: Write a verification report. Max 200 words. Bullet points. One bullet per test case: test name, expected value, computed value, PASS/FAIL.

> **Answer: B**
> "Concise" and "short" are subjective. B gives a measurable word limit (200), structure (bullets, one per test case), and required fields.

---

### Q4. Grand persona vs. narrow role {choice}
You are writing the system prompt for a code-reviewer agent. Which opening is more effective?

- A: You are a senior software engineer and CFD expert. You care deeply about code quality and always provide thoughtful, thorough reviews.
- B: You are the ME433 code-reviewer. Check MATLAB code for: incorrect BCs, wrong stencils, CFL violations, and undocumented deviations from the plan. Report issues only. Do not edit files.

> **Answer: B**
> A is a generic expert persona with vague traits. B defines a narrow role, lists exact checks, and sets constraints (report only, no editing). Narrow scope limits drift.

---

### Q5. Background vs. examples {choice}
Your verifier needs to produce a convergence table. The context window is almost full. You can add one more thing: the full project README, or two example tables showing the correct format. Which do you add?

- A: The README. It gives the model background on the project.
- B: The two example tables. They show the model exactly what the output should look like.

> **Answer: B**
> The verifier's immediate job is to produce a formatted table. The README does not help with that. The examples directly shape the output. When context is tight, cut irrelevant background before cutting examples or constraints.

---

### Q6. More information vs. focused context {choice}
The implementer is producing code that ignores plan details. Which fix is better?

- A: Give the implementer the full problem PDF, the plan, all previous agent outputs, and the conversation history.
- B: Give the implementer only the plan. Make the plan more detailed so it contains everything the implementer needs.

> **Answer: B**
> A floods the implementer with irrelevant material (raw PDF, conversation history), diluting the signal. B keeps context focused: the plan is the single source of truth, made self-contained.

---

### Q7. Prompt instruction vs. tool removal {choice}
Your planner agent sometimes runs the MATLAB solver to "test" its plan. Which fix is better?

- A: Add a prompt instruction: "Focus on planning. Do not run code."
- B: Remove the planner's access to the shell tool so it cannot run MATLAB.

> **Answer: B**
> Models sometimes ignore instructions when a tool is available. Removing the tool makes it structurally impossible to run code.

---

### Q8. Visual check vs. quantitative check {choice}
Your agent produces a lid-driven cavity solver. The flow field looks reasonable at Re=100. Which gives more confidence?

- A: Run at Re=100 and Re=400. If both look physically reasonable, consider it validated.
- B: Run at Re=100 on a 129x129 grid. Compare u(y) at x=0.5 against Ghia et al. (1982), Table I. Check that u at y=0.5 is approximately -0.2109. Report max pointwise difference.

> **Answer: B**
> Visual inspection ("looks reasonable") misses subtle numerical errors. B compares against published reference data at specific points with a quantitative metric.

---

### Q9. One big prompt vs. sequential prompts {choice}
You need a 2D channel flow solver with grid convergence analysis. Which approach is more likely to succeed?

- A: One prompt: "Write a MATLAB solver for 2D channel flow (staggered grid, Nx=50, Ny=30, Re=100, no-slip walls, pressure-driven). Then run grid convergence with Nx=[25,50,100,200], compute L2 errors against Poiseuille exact solution, observed order, save table and log-log plot."
- B: Two prompts. First: "Write a MATLAB solver for 2D channel flow (staggered grid, Nx=50, Ny=30, Re=100, no-slip walls, pressure-driven). Validate against the Poiseuille parabolic profile." After it works: "Using validated channel_flow.m, run grid convergence with Nx=[25,50,100,200]. Compute L2 errors, observed order, save table and log-log plot."

> **Answer: B**
> If the solver has a bug, A runs the convergence study on broken code. B validates first, then uses working code for convergence.

---

### Q10. Temperature vs. format instructions {choice}
Your agent keeps writing results as paragraphs instead of a table. Which fix is more effective?

- A: Set temperature to 0 so the output is deterministic.
- B: Add explicit format instructions: "Output a table with columns Nx, dx, L2_error, observed_order" with one row of example data.

> **Answer: B**
> Temperature controls randomness in word choice. Setting it to 0 makes output deterministic but does not control structure -- the model can deterministically write a paragraph. Explicit format instructions directly constrain the output shape.

---

### Q11. Model selection {choice}
Your report-writer agent copies results from plan.md into a LaTeX template. No complex reasoning needed. Which model choice is better?

- A: Use the strongest available model (Claude Opus / GPT-5.4) for maximum accuracy.
- B: Use a fast model (Gemini Flash / Claude Haiku) since the task is straightforward.

> **Answer: B**
> A simple copy-and-format task does not need the strongest model. A fast model handles it reliably at lower cost and higher speed.

---

## Part 2: Improve the Prompt
Read each bad prompt or agent definition, identify the problems, and rewrite it.

### Q12. Fix the bad prompt {freetext}
What are the problems with this prompt? Rewrite it using the five elements from the guide (task, context, constraints, output format, verification criteria). Choose your own parameters.

> **Given:** Please help me with my CFD project. I need to simulate fluid flow in a cavity. Use AI to code it. Thanks!

> **Answer:**
> Three problems: (1) No specific task -- "simulate fluid flow" is vague. (2) No constraints -- no language, Re, grid, BCs. (3) No output format or verification criteria.
>
> Sample rewrite: "Write a MATLAB function `cavity.m` for a lid-driven cavity using finite differences on a staggered grid. Nx=Ny=65, Re=100, lid velocity U=1. No-slip walls, moving lid at top. Time-march to steady state (residual < 1e-6). Save to `cavity_results.mat`. Validate: compare u(y) at x=0.5 against Ghia et al. (1982). u at y=0.5 should be approximately -0.2109."

---

### Q13. Fix the bad agent definition {freetext}
What are the problems with this agent definition? Rewrite it for a figure-generator agent using the 8-part checklist from the guide.

> **Given:** You are an amazing AI that can do anything. Help the user with whatever they need. Be creative and thorough.

> **Answer:**
> Three problems: (1) No specific role -- "can do anything" has no scope. (2) No task or success condition. (3) No constraints, output format, or tool permissions.
>
> Sample rewrite (figure-generator):
> 1. Identity: "ME433 figure generator"
> 2. Task: "Create PNG figures from simulation data"
> 3. Inputs: "Read solution/*.mat and plan.md Section 7"
> 4. Constraints: "PNG only, no GUI, MATLAB only"
> 5. Output format: "Save to solution/figures/ as fig_<name>.png"
> 6. Examples: "See project spec Figure 2 for style"
> 7. Tool permissions: "File read, file write (figures only), MATLAB"
> 8. Stop condition: "Stop after all planned figures are generated"

---

## Part 3: Concepts
Answer each question in a few sentences.

### Q14. Context window overflow {freetext}
Your MATLAB solver is 4,000 tokens. Your plan is 3,000 tokens. The model's context window is 4,096 tokens. What happens? What should you do?

> **Answer:**
> The total is 7,000 tokens but the window is 4,096. The model silently drops content -- it does not warn you. The solver or plan will be truncated, causing missing functions or incomplete logic. Fix: reduce what you send (split the solver into smaller files, send only the relevant function, or use a model with a larger context window).

---

### Q15. Runs without errors {freetext}
A student says: "The AI wrote code that runs without errors, so it must be correct." What is wrong with this reasoning?

> **Answer:**
> LLMs predict statistically likely token sequences. They do not understand physics. The code can compile, run, produce output, and still have wrong boundary conditions, incorrect discretization, or stability violations. "No errors" means no syntax/runtime errors, not correct physics.

---

### Q16. Context vs. prompt {freetext}
Explain the difference between context and prompt using an analogy. Give one example where improving the context (not the prompt) would most improve the output.

> **Answer:**
> Context is the project folder on an employee's desk. The prompt is the task you hand them. A precise task fails if the desk is empty. Example: asking an agent to "verify convergence rate" (good prompt) without providing the exact solution formula. The agent cannot compute errors. Adding the formula to the context fixes it without changing the prompt.

---

### Q17. Why read-only for code-reviewer {freetext}
The code-reviewer agent is read-only. Why does this produce better results than letting the reviewer fix bugs directly?

> **Answer:**
> If the reviewer could edit files, it might silently fix bugs instead of reporting them. This hides issues from the supervisor and skips the review-fix loop. Read-only forces the reviewer to describe problems, creating a traceable record for the implementer.

---

### Q18. Pipeline iteration after review {freetext}
The implementer writes code that violates two constraints from the plan. The code-reviewer catches both. What happens next in the pipeline?

> **Answer:**
> The implementer runs again with (1) the plan, (2) its own code, and (3) the review report. It fixes both violations and produces updated code. The code-reviewer runs again to verify. This cycle repeats up to a max number of iterations.
