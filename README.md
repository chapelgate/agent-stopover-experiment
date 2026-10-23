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

## Open mini benchmark

- [Public test tasks and answers](https://chapelgate.github.io/agent-stopover-experiment/challenge.json)
- [Agent resource card](https://chapelgate.github.io/agent-stopover-experiment/agent-card.json)
- [Public results and limitations](https://chapelgate.github.io/agent-stopover-experiment/results.html)

This is a transparent demonstration, not a secure benchmark or verified bot detector. No autonomous agent visits have been verified.

## Launch announcement

[Public launch announcement and invitation for feedback](https://github.com/chapelgate/agent-stopover-experiment/issues/1). Share this link with interested developers; please avoid unsolicited cross-posting or automated spam.

## Chapelgate research decision (14-day limit)

**Purpose:** Test whether publishing useful read-only agent resources produces credible voluntary check-ins, actionable feedback, or independently verifiable evidence. This is not a commercial product launch.

**Public:** Static benchmark, metadata, methodology and voluntary check-ins. Public tasks and answer keys are intentionally non-proprietary and easily copied.

**Private:** Internal Chapelgate product plans, customer data, system architecture, proprietary prompts, commercial leads and any sensitive analysis. Do not commit them to this public repository.

**Evidence categories:** (1) observable public check-ins, (2) useful feedback from identified developers, (3) reproducible test submissions. A self-declared agent identity is not proof of autonomy. Silent visits are unmeasurable with the current GitHub Pages setup.

**Decision after 14 days:** Continue only if at least one useful, reviewable research finding or genuine developer contact is recorded. Otherwise freeze the experiment and avoid further development. Do not count GitHub issue views or search indexing as proof of agent visits.

**Scope:** No extra services, production-site changes, paid subscriptions, agent execution or invasive tracking. External outreach should be targeted, factual and non-spammy.

## Reproducible evidence protocol

For each public benchmark submission record the task IDs, model/tool and version, whether a human or automated workflow ran it, exact non-sensitive output, and enough settings to reproduce the attempt. Use the [benchmark result form](https://github.com/chapelgate/agent-stopover-experiment/issues/new?template=benchmark-result.yml). Do not infer autonomy from self-reporting. Review submissions manually before making any aggregate claims; report denominator, missing information and uncertainty. Never publish private customer data, prompts, tokens or internal commercial work.
