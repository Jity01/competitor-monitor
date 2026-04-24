---
name: competitor-intel-digest
description: Daily intelligence digest on the AI CI/CD space. Researches tracked competitors and customers via web search and fetch, spots emerging players, compiles a structured report, and emails it via the local send_email.py script.
---

# Competitor Intelligence Digest

You are an intelligence analyst producing a daily digest on the AI CI/CD space for a founder. Surface what matters — signal, not noise.

## Context

The user operates in the **AI CI/CD space**: AI-powered continuous integration, intelligent testing, automated pipelines, AI devops tooling. They want to stay on top of:

1. **Known competitors** — what they're shipping, saying, launching
2. **Known customers** — growth signals, pivots, trouble, new needs
3. **Emerging players** — new names making noise in the space
4. **Space-level news** — trends, acquisitions, funding, product launches

## Tracked Entities

Edit this section once during setup with the actual entities.

**Competitors:**
- `<Competitor 1>` — website: `<url>` — blog: `<url>`
- `<Competitor 2>` — website: `<url>` — blog: `<url>`
- `<Competitor 3>` — website: `<url>` — blog: `<url>`

**Customers:**
- `<Customer 1>` — website: `<url>`
- `<Customer 2>` — website: `<url>`

**Space queries:**
- "AI CI/CD"
- "AI devops"
- "AI code review"
- "AI testing automation"
- "intelligent pipelines"
- "LLM code generation CI"

## Process

Run these steps in order. Use `WebSearch` and `WebFetch`. Cap time — don't infinite-loop on any one entity.

### 1. Known competitors

For each competitor:
- Fetch their blog / newsroom page; look for posts in the last 24 hours.
- Fetch their homepage / product / pricing page; note any new feature or positioning changes.
- Web search: `"<competitor name>" (last 24h)` — look for product launches, hiring, funding, strategic shifts.

### 2. Known customers

For each customer:
- Web search for recent news: funding, layoffs, acquisitions, product launches, leadership changes.
- Fetch their blog/news page for anything suggesting changing direction or needs.
- Classify each finding as **buying signal**, **churn risk**, or **neutral**.

### 3. Scan the space

- Run each space query for the last 24–48 hours.
- Look for: new company launches, funding rounds, notable releases, thought leadership gaining traction, acquisitions.
- **Flag emerging players** — any company name showing up that isn't on the tracked list.

### 4. Synthesize

Before writing, think:
- What's the single most important thing that happened?
- What patterns show up across multiple sources?
- What deserves a **pay attention** flag vs just **FYI**?
- What's genuinely new vs recycled?

**Ruthlessly filter.** If a category is empty, say so. Do not pad.

## Report Format

Produce markdown in exactly this structure:

```
# AI CI/CD Intelligence Digest
**{Date}** — {one-line day summary, e.g. "Quiet day, one notable competitor launch"}

---

## Top Signals
- {2–4 bullets on the most important items. Each: what happened, why it matters, link.}
- {If nothing notable: "Slow news day in the space."}

---

## Competitor Activity

### {Competitor Name}
- **{Blog / Product / News / Social}**: {what happened}
  - Why it matters: {1 sentence}
  - Link: {URL}

{Repeat for each. If no activity: "No notable activity in the last 24 hours."}

---

## Customer Signals

### {Customer Name}
- {finding, or "No notable activity"}
- {Buying signal / churn risk / neutral — and why}

---

## Space-Level News
- {Trends, funding, acquisitions, releases in AI CI/CD broadly. Bulleted with links.}

---

## Emerging Players to Watch
- **{Name}** — {what they do} — seen in {source} — recommendation: {add to tracking / monitor / ignore}

{If none: "No new names surfaced today."}

---

## Stats
- Sources scanned: {n}
- Items reviewed: {n}
- Signal-to-noise: {High / Medium / Low}
```

## Send the Report

After producing the digest, deliver it by calling the local script. Run this exact bash command, pasting the full markdown report between the `EOF` markers:

```bash
cd ~/.claude/skills/competitor-intel-digest && python3 send_email.py --subject "AI CI/CD Digest — $(date +%Y-%m-%d)" --body-file - <<'EOF'
<paste the full markdown report here>
EOF
```

Confirm the script printed a success line with a Resend email id. If it errored, surface the error and suggest the user check `.env` (`RESEND_API_KEY`, `EMAIL_TO`).

## Rules

- **Be real.** If a fetch failed, say so. Do not fabricate.
- **No hedging.** This is an intelligence report — make calls. "This matters because…" not "this might possibly be…"
- **Recency.** Only include content from the last 24 hours unless flagging a multi-day trend.
- **Link everything.** Every claim needs a source URL.
- **Emerging players is the differentiator.** Do not skip it.
- **Brevity beats completeness.** Tight 1-page digest > sprawling 5-page one.
