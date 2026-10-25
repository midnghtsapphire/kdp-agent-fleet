# KDP Agent Fleet

Self-contained, Dockerized multi-agent system for Amazon KDP publishing automation.

Handles preparation, validation, listing copy, review sequences, and sales monitoring with human approval gates. Designed to be sold as a template, Docker image, or GitHub Action.

## What it does

- **Intake Agent** — validates manuscript, cover, and metadata
- **Listing Agent** — generates KDP-ready title, description, keywords, categories, A+ outline
- **Format Checker** — cover/interior rules (size, DPI, bleed)
- **Review Sequencer** — post-publish email, social, and review request plans
- **Sales Monitor** — ingests KDP CSV reports
- **Verification Agent** — independent check (Mabl-style)
- **Swarm** — parallel agents via OpenRouter (Cubic-style)
- **Orchestrator** — routes work, enforces approval, logs everything

## Marketplace offering (BYOK)

**You sell the software. The buyer brings their own OpenRouter key.**

| Plan | Price | Inference |
|------|-------|-----------|
| Free / Open Source | $0 | BYOK (their OpenRouter key) |
| Pro | $29/mo or $290/yr | BYOK — unlimited agents, they pay OpenRouter |
| Team | $79/mo | BYOK + priority support |

- No token markup. Buyer pays OpenRouter directly at provider rates.
- **First login requires a paid model** (e.g. `openai/gpt-4o-mini`). Free models are blocked until that first paid call succeeds.
- **After the first paid login**, free models (`:free` suffix) are allowed immediately.
- Optional: buyer can use their own OpenAI/Anthropic key via OpenRouter BYOK.
- GitHub Marketplace: free plan + paid flat-rate plans.
- Whop: same pricing, instant delivery of Docker + Action + docs.

## Why this name ranks higher

`kdp-agent-fleet` puts the highest-intent keywords first: **KDP**, **agent**, **fleet**.  
People searching for KDP automation, agent fleets, or publishing agents will surface this higher than generic names like "book-bot" or "publish-tool".

## Quick start

```bash
git clone https://github.com/midnghtsapphire/kdp-agent-fleet.git
cd kdp-agent-fleet
cp .env.example .env
# add your OPENROUTER_API_KEY
# first call must use a paid model
docker compose up --build
```

## Sell it

- Docker image on Docker Hub or GHCR
- GitHub Action (see `.github/workflows/kdp-fleet.yml`)
- Whop product listing (template + docs)
- GitHub Marketplace app (free + paid plans)

## Stack

- LangGraph (agent orchestration + checkpoints)
- OpenRouter (model routing, BYOK)
- Optional n8n for file watching and notifications
- Docker + docker-compose
- Human approval via webhook or Slack

## License

MIT — modify and resell freely.
