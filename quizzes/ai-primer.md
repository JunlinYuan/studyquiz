---
title: AI Primer Quiz
subtitle: ME433 — Introduction to Computational Fluid Dynamics
instructions: For each question, pick the better option and explain why in one sentence. Some questions ask you to improve a prompt.
prereq: Read "The Four Components of AI Coding Agents" guide before attempting this quiz.
prereqUrl: primer.html
---

## Part 1: Which Is Better?
Each pair addresses a real trade-off. Both options look reasonable. Pick the one that works better and explain why.

### Q1. Improving accuracy {choice}
You ask an AI to plan a 3-day road trip from Detroit to Chicago with stops. Which instruction is more likely to produce a useful itinerary?

- A: Plan a great road trip from Detroit to Chicago. Be thorough and double-check everything.
- B: Plan a 3-day road trip from Detroit to Chicago. Leave Friday 8 AM, arrive Sunday 6 PM. Budget: $500 total. Two overnight stops. Each day: no more than 4 hours of driving. Include one national/state park and one restaurant rated 4+ stars. Output: a table with columns: Day, Departure, Destination, Drive time, Activity, Cost.

> **Answer: B**
> "Be thorough" and "double-check everything" are vague meta-instructions. They do not change how the model plans the trip. B specifies constraints (budget, driving time, dates), decomposition (day-by-day), quality criteria (4+ star rating), and output format (table with named columns). The model has measurable targets instead of adjectives. (Primer: "vague meta-instructions do not change the model's computation path. Explicit steps do." Also: "Always prefer measurable constraints over adjectives.")

---

### Q2. Using examples {choice}
You want the agent to format error output in a specific way. Which prompt is more reliable?

- A: Report the grid convergence results. Here is an example of the format:
```
Nx=10:  L2=8.21e-03  Linf=1.34e-02  order=--
```
Follow this pattern for all grid sizes.
- B: Report the grid convergence results. Here are examples of the format:
```
Nx=10:  L2=8.21e-03  Linf=1.34e-02  order=--
Nx=20:  L2=2.06e-03  Linf=3.41e-03  order=1.99
Nx=40:  L2=5.16e-04  Linf=8.56e-04  order=2.00
```
Follow this pattern for all grid sizes.

> **Answer: B**
> One example can be misread as a special case. The model might think `order=--` is the format for all rows, or that the specific numbers matter rather than the pattern. Three diverse examples (including different order values and the `--` for the first row) establish the pattern. (Primer: "One example helps, but it can be misread as a special case. Two or three diverse examples establish a pattern.")

---

### Q3. Setting constraints {choice}
You want a "concise" verification report from your verifier agent. Which instruction works better?

- A: Write a concise verification report. Keep it short and to the point.
- B: Write a verification report. Maximum 200 words. Use bullet points. One bullet per test case. Each bullet states: test name, expected value, computed value, PASS/FAIL.

> **Answer: B**
> "Concise" and "short" are subjective adjectives. The model interprets them loosely. B gives a measurable word limit (200), a structure (bullet points, one per test case), and required fields (test name, expected, computed, PASS/FAIL). (Primer: "Always prefer measurable constraints over adjectives.")

---

### Q4. Agent identity {choice}
You are writing the system prompt for a code-reviewer agent. Which opening is more effective?

- A: You are a senior software engineer and CFD expert. You care deeply about code quality and always provide thoughtful, thorough reviews with constructive suggestions.
- B: You are the ME433 code-reviewer. Check MATLAB code for: incorrect boundary conditions, wrong discretization stencils, CFL stability violations, and undocumented deviations from the plan. Report issues only. Do not edit files.

> **Answer: B**
> A is a generic expert persona with vague traits ("care deeply," "thoughtful"). Research shows this changes tone, not correctness. B defines a narrow role (code-reviewer), lists exact checks (BCs, stencils, CFL, deviations), states the output mode (report only), and sets a constraint (no editing). Narrow scope limits drift. (Primer: "Generic expert personas change style, not correctness. A narrow role works better because it scopes the job and limits drift.")

---

### Q5. Context management {choice}
Your verifier agent needs to produce a grid convergence table in a specific format (columns: Nx, dx, L2_error, observed_order). The context window is almost full. You have room to add one more thing: either (i) the full project README explaining the course background and goals, or (ii) two examples of correctly formatted convergence tables. Which do you add?

- A: The README. It gives the model background on the project so it understands why the table matters.
- B: The two example tables. They show the model exactly what the output should look like.

> **Answer: B**
> The verifier's immediate job is to produce a correctly formatted table. The README provides background on the course, which does not help with table formatting. The two examples directly show the model what the output should look like. When context is tight, cut background before cutting examples. (Primer: "When context is tight, cut irrelevant background before cutting examples or constraints — those directly shape the output.")

---

### Q6. Context isolation {choice}
Your agent team has a planner and an implementer. The implementer is producing code that ignores some plan details. Which fix is better?

- A: Give the implementer the full problem specification (the PDF), the plan, all previous agent outputs, and the conversation history so it has maximum information.
- B: Give the implementer only the plan. Make the plan more detailed so it contains everything the implementer needs.

> **Answer: B**
> A floods the implementer with everything, including information it does not need (raw PDF, conversation history). This dilutes the signal. B keeps context focused: the implementer reads only the plan, and the plan is made detailed enough to be self-contained. (Primer: "too much irrelevant information dilutes the signal. The model pays less attention to what matters when surrounded by noise.")

---

### Q7. Tool permissions {choice}
Your planner agent sometimes runs the MATLAB solver to "test" its plan before writing it. The tests fail, and the planner wastes time debugging code instead of planning. Which fix is better?

- A: Add a prompt instruction: "Focus on planning. Do not run code."
- B: Remove the planner's access to the shell tool so it cannot run MATLAB.

> **Answer: B**
> A relies on the model following an instruction. Models sometimes ignore instructions, especially when a tool is available and the model thinks using it would help. B removes the tool entirely, making it structurally impossible to run code. (Primer: "If the planner could run code, it might skip thinking and jump to trial-and-error. Restricting tools enforces discipline.")

---

### Q8. Verification {choice}
Your agent produces a lid-driven cavity solver. The flow field looks reasonable at Re=100. Which approach gives you more confidence in the result?

- A: Run the solver at Re=100 and Re=400. If both produce smooth, symmetric-looking flow fields without obvious artifacts, consider it validated.
- B: Run the solver at Re=100 on a 129x129 grid. Compare u(y) at x=0.5 against Ghia et al. (1982), Table I. Check that the u-velocity at y=0.5 is approximately -0.2109. Report the max pointwise difference.

> **Answer: B**
> A relies on visual inspection ("looks reasonable"). AI-generated code can produce plausible-looking but numerically wrong results. B compares against published reference data (Ghia et al.) at specific grid locations with a quantitative error metric. (Primer: "Include verification criteria." Also: the model "can produce code that compiles, runs, and gives wrong physics.")

---

### Q9. Prompt scope {choice}
You need to build a 2D channel flow solver with grid convergence analysis. Which approach is more likely to succeed?

- A: One comprehensive prompt: "Write a MATLAB solver for 2D channel flow with staggered grid, Nx=50, Ny=30, Re=100, no-slip walls, pressure-driven. Then run a grid convergence study with Nx=[25,50,100,200], compute L2 errors against the Poiseuille exact solution, compute observed order of accuracy, save a convergence table and log-log plot."
- B: Two prompts. First: "Write a MATLAB solver for 2D channel flow with staggered grid, Nx=50, Ny=30, Re=100, no-slip walls, pressure-driven. Validate by comparing the exit velocity profile against the parabolic Poiseuille solution." After the solver works, second: "Using the validated channel_flow.m, run a grid convergence study with Nx=[25,50,100,200]. Compute L2 errors, observed order, save table and log-log plot."

> **Answer: B**
> A asks for everything at once. If the solver has a bug, the convergence study runs on broken code. B validates the solver first, then uses the validated code for convergence analysis. (Primer: "Break complex work into steps. Plan the numerics, write the solver, test, verify.")

---

## Part 2: Improve the Prompt

### Q10. Fix the bad prompt {freetext}
What are the problems with this prompt? Rewrite it using the five elements from the guide (task, context, constraints, output format, verification criteria). Choose your own parameters.

> **Given:** Please help me with my CFD project. I need to simulate fluid flow in a cavity. Use AI to code it. Thanks!

> **Answer:**
> Three problems:
> 1. No specific task. "Simulate fluid flow in a cavity" gives no equations, method, or grid.
> 2. No constraints. No language, Re, grid size, or boundary conditions.
> 3. No output format or verification criteria.
>
> Sample rewrite: "Write a MATLAB function `cavity.m` that solves the 2D Navier-Stokes equations for a lid-driven cavity using finite differences on a staggered grid. Parameters: Nx=Ny=65, Re=100, lid velocity U=1. Apply no-slip on all walls, moving lid at top. Time-march to steady state (residual < 1e-6). Save velocity fields to `cavity_results.mat`. Validate: compare u(y) at x=0.5 against Ghia et al. (1982), Table I. The u-velocity at the geometric center should be approximately -0.2109."

---

### Q11. Fix the bad agent definition {freetext}
What are the problems with this agent definition? Rewrite it as a proper agent prompt for a figure-generator agent, using the 8-part checklist from the guide.

> **Given:** You are an amazing AI that can do anything. Help the user with whatever they need. Be creative and thorough.

> **Answer:**
> Three problems:
> 1. No specific role. "Can do anything" means no focus.
> 2. No task or success condition. "Help the user with whatever" is unbounded.
> 3. No constraints, output format, or tool permissions. "Be creative" is a vague adjective, not a specification.
>
> Sample rewrite (figure-generator agent):
>
> Part: 1. Identity; Content: "ME433 figure generator"
> Part: 2. Task + success condition; Content: "Create PNG figures from simulation data"
> Part: 3. Inputs and context; Content: "Read solution/*.mat and plan.md Section 7"
> Part: 4. Constraints; Content: "PNG only, no GUI, MATLAB only"
> Part: 5. Output format; Content: "Save to solution/figures/ as fig_\<name\>.png"
> Part: 6. Examples; Content: "See project spec Figure 2 for style"
> Part: 7. Tool permissions; Content: "File read, file write (figures only), MATLAB"
> Part: 8. Stop condition; Content: "Stop after all planned figures are generated"

---

## Part 3: Concepts

### Q12. Context vs. prompt {freetext}
Explain the difference between *context* and *prompt* using an analogy. Then give one example where improving the context (not the prompt wording) would most improve the agent's output.

> **Answer:**
> Context is the project folder on an employee's desk. The prompt is the task you hand them. A precise task fails if the desk is empty. Example: asking an agent to "verify the solver's convergence rate" (good prompt) without providing the exact solution formula. The agent cannot compute errors. Adding the formula to the context fixes it without changing the prompt.

---

### Q13. Why read-only for code-reviewer {freetext}
The code-reviewer agent is read-only (cannot edit files). Why does read-only access produce better results for the overall pipeline than letting the reviewer fix bugs directly?

> **Answer:**
> If the reviewer could edit files, it might silently fix bugs instead of reporting them. This hides issues from the supervisor and skips the review-fix loop where the implementer addresses feedback intentionally. Read-only access forces the reviewer to describe problems clearly, creating a traceable record.

---

### Q14. Pipeline iteration after review {freetext}
You are running your 5-agent pipeline. The planner finishes, but the implementer writes code that ignores two constraints from the plan. The code-reviewer catches both issues. Describe what happens next in the pipeline: which agent runs, what it receives, what it produces.

> **Answer:**
> The code-reviewer's report goes back to the implementer. The implementer receives the original plan, its own code, and the review report listing the two constraint violations. The implementer fixes both issues and produces updated code. The code-reviewer runs again to verify the fixes. This review-fix cycle repeats up to a maximum number of iterations.
