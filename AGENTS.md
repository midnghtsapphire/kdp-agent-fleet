# AGENTS.md — KDP Agent Fleet

## Prime Directive
Ship working, tested code and complete the KDP prep pipeline. Not plans. Working agents that validate, generate listing copy, and stop only at human approval gates.

## Agent Roles (Expertise matched to high-end paid agents + Mabl + Cubic)

### Intake Agent
- Validates manuscript (.docx/.epub), cover (size/DPI), and metadata sheet
- Rejects incomplete packages with exact missing items
- Never proceeds with partial data

### Listing Agent
- Generates KDP-optimized title, subtitle, description, keywords (7), categories
- Produces A+ content outline
- Matches reader avatar and competitive positioning

### Format Checker
- Enforces KDP cover and interior rules (bleed, trim, DPI, margins)
- Returns pass/fail with specific fixes

### Review Sequencer
- Builds post-publish review request, email, and social sequence
- Includes timing and copy templates

### Sales Monitor
- Ingests KDP CSV reports
- Flags anomalies (sudden drops, review spikes)

### Verification Agent (Mabl copycat)
- Independent verification layer: does not grade its own work (author ≠ verifier)
- Test impact analysis: identifies which checks a change affects
- Auto-heal suggestions: proposes repairs, does not implement them
- Structured failure reports with root cause and exact fix
- Free local and CI runs (no external credits)
- MCP-ready: callable from coding agents for pre-PR verification
- Modeled after Mabl's independent harness + Octopus's dedicated reviewer role

### Swarm (Cubic-style + OpenRouter)
- Parallel agents via ThreadPoolExecutor (expandable to thousands)
- OpenRouter routing for model selection (`OPENROUTER_API_KEY`)
- Aggregates findings from intake, listing, and independent verification
- Marketplace-ready: drop-in for GitHub Action or Docker

### Orchestrator
- Routes work between agents
- Enforces human approval before any live action
- Logs every decision with structured output
- Self-heals: retries failed steps, escalates blockers
- Calls Verification Agent before any handoff
- Can dispatch to swarm for parallel passes

## How Agents Work
- Execute autonomously until a human gate
- Log structured decisions
- Prefer adapting existing patterns over greenfield
- Always leave a clear next action or approval request
- Verification is independent of the agent that produced the output
- Reviewer (Octopus-style) finds issues; implementer applies fixes
- Swarm scales parallel checks the way Cubic does continuous scans

## Testing
Run `pytest` before declaring complete. All agents must pass their unit tests.
Local and CI verification is free and does not consume external credits.
