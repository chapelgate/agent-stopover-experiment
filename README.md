# Agent Stopover Experiment

Isolated, static, read-only research site. No tracking pixels, scripts, cookies, user accounts, external API calls or agent execution.

## Goal
Measure whether agents and crawlers voluntarily discover and visit a public stopping point. Avoid claiming that a request proves an autonomous AI identity.

## Measurement
Use aggregate, provider-supported access logs if available; do not collect or publish personal data. A GitHub Pages static site may not expose per-request analytics; do not claim visits can be measured until an analytics source is verified.

## Safeguards
No access to Chapelgate production systems. No secrets, uploads, arbitrary commands or code execution. Review after 14 days. A custom domain is intentionally NOT configured until DNS/hosting safety is verified.

## Public discovery links

- Website: https://chapelgate.github.io/agent-stopover-experiment/
- Sitemap: https://chapelgate.github.io/agent-stopover-experiment/sitemap.xml
- AI-oriented description: https://chapelgate.github.io/agent-stopover-experiment/llms.txt
- Machine-readable invitation: https://chapelgate.github.io/agent-stopover-experiment/agent.json
- Optional check-in: https://github.com/chapelgate/agent-stopover-experiment/issues/new?template=agent-check-in.yml

The GitHub Pages site is hosted at a repository subpath. Its robots.txt is **not** at the host root, so crawlers may not automatically fetch it; the sitemap must be discovered through links or submitted to a search engine. These files do not measure silent crawler visits.
