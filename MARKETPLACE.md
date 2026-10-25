# KDP Agent Fleet — Marketplace

Multi-agent system that prepares Amazon KDP books for publish.

Validates your manuscript and cover, writes listing copy, builds review sequences, and monitors sales. Stops at human approval gates. Sold as a Docker image, GitHub Action, or template.

## What you get

| Agent | What it does |
|-------|--------------|
| Intake | Validates manuscript, cover, and metadata. Rejects incomplete packages. |
| Listing | Generates title, subtitle, description, keywords, categories, A+ outline. |
| Format Checker | Enforces KDP cover and interior rules (bleed, trim, DPI, margins). |
| Review Sequencer | Builds post-publish email, social, and review request plans. |
| Sales Monitor | Ingests KDP CSV reports and flags anomalies. |
| Verification | Independent check (does not grade its own work). |
| Swarm | Parallel agents for faster passes. |
| Orchestrator | Routes work, enforces approval, logs every decision. |

## Pricing

**You buy the software. You bring your own OpenRouter key.**

| Plan | Price | Inference |
|------|-------|-----------|
| Free | $0 | Your OpenRouter key |
| Pro | $29/mo or $290/yr | Your OpenRouter key |
| Team | $79/mo | Your OpenRouter key + support |

- No token markup. You pay OpenRouter directly.
- First login requires a paid model. Free models are allowed after that.
- Optional: use your own OpenAI or Anthropic key via OpenRouter BYOK.

## Quick start

```bash
git clone https://github.com/midnghtsapphire/kdp-agent-fleet.git
cd kdp-agent-fleet
cp .env.example .env
# add your OPENROUTER_API_KEY
docker compose up --build
```

Or use the GitHub Action:

```yaml
- uses: midnghtsapphire/kdp-agent-fleet@main
  with:
    manuscript: manuscript.docx
    cover: cover.jpg
    metadata: metadata.json
  env:
    OPENROUTER_API_KEY: ${{ secrets.OPENROUTER_API_KEY }}
```

## Delivery

- Docker image (GHCR)
- GitHub Action
- Template repo (MIT license)
- Whop instant delivery

## Requirements

- OpenRouter account and API key
- Manuscript (`.docx` or `.epub`)
- Cover image (KDP size/DPI)
- Metadata sheet (title, keywords, categories)

## License

MIT — modify and resell freely.
