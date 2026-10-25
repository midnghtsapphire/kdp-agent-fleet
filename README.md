# KDP Agent Fleet

Self-contained, Dockerized multi-agent system for Amazon KDP publishing automation.

Handles preparation, validation, listing copy, review sequences, and sales monitoring with human approval gates. Designed to be sold as a template, Docker image, or GitHub Action.

## What it does

- **Intake Agent** — validates manuscript, cover, and metadata
- **Listing Agent** — generates KDP-ready title, description, keywords, categories, A+ outline
- **Format Checker** — cover/interior rules (size, DPI, bleed)
- **Review Sequencer** — post-publish email, social, and review request plans
- **Sales Monitor** — ingests KDP CSV reports
- **Orchestrator** — routes work, enforces approval, logs everything

## Why this name ranks higher

`kdp-agent-fleet` puts the highest-intent keywords first: **KDP**, **agent**, **fleet**.  
People searching for KDP automation, agent fleets, or publishing agents will surface this higher than generic names like "book-bot" or "publish-tool".

## Quick start

```bash
git clone https://github.com/midnghtsapphire/kdp-agent-fleet.git
cd kdp-agent-fleet
cp .env.example .env
# add your OPENAI_API_KEY or other provider
docker compose up --build
```

## Sell it

- Docker image on Docker Hub or GHCR
- GitHub Action (see `.github/workflows/kdp-fleet.yml`)
- Whop product listing (template + docs)

## Stack

- LangGraph (agent orchestration + checkpoints)
- Optional n8n for file watching and notifications
- Docker + docker-compose
- Human approval via webhook or Slack

## License

MIT — modify and resell freely.
