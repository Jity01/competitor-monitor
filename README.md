# Competitor Intelligence Monitor

A Claude-powered daily digest on the AI CI/CD space. Claude researches your tracked competitors, customers, and the broader space, then emails you a structured report.

## What you get in your inbox

- **Top Signals** — the few things that actually matter today
- **Competitor Activity** — blog posts, product changes, news, social
- **Customer Signals** — buying signals, churn risk, or neutral updates
- **Space-Level News** — funding, acquisitions, launches in AI CI/CD
- **Emerging Players to Watch** — new names showing up in the space

## ⚠️ One important constraint before you start

This tool sends from Resend's built-in sandbox sender, `onboarding@resend.dev`, so you don't have to verify a domain. The tradeoff:

> **`EMAIL_TO` must exactly match the email address you signed up for Resend with.** Resend's sandbox sender refuses to deliver to any other address. If you want to email someone else (a teammate, a distribution list, etc.), you'll need to verify your own domain — see the last section of this README.

## Setup

### 1. Clone

```bash
git clone <repo-url> ~/competitor-monitor
cd ~/competitor-monitor
```

If you clone somewhere else, note the path — you'll plug it into `SKILL.md` in step 5.

### 2. Install Python dependencies

```bash
pip3 install -r requirements.txt
```

### 3. Get a Resend API key

- Sign up at [resend.com](https://resend.com) — **remember which email address you use; that's the only address the digest can go to.**
- Create an API key in the dashboard.
- No domain verification needed — we send from the built-in `onboarding@resend.dev` sandbox.

### 4. Configure `.env`

```bash
cp env.example .env
```

Then edit `.env`:

```
RESEND_API_KEY=re_xxxxxxxxxxxx
EMAIL_TO=the-email-you-used-for-resend@example.com
```

Test it:

```bash
echo "# Test\n\nHello from the monitor." | python3 send_email.py --subject "Test digest" --body-file -
```

You should see `Sent to ...` and get an email. If not, double-check the API key and that `EMAIL_TO` matches your Resend account email.

### 5. Fill in the skill

Open `SKILL.md` and:

- Replace the `<Competitor>` / `<Customer>` placeholders under **Tracked Entities** with the real names and URLs.
- In the **Send the Report** section at the bottom, replace `<REPO_PATH>` with the path you cloned to (e.g. `~/competitor-monitor`).

### 6. Install as a Claude skill

Copy the repo (or symlink it) into Claude's skills directory:

```bash
mkdir -p ~/.claude/skills
ln -s ~/competitor-monitor ~/.claude/skills/competitor-intel-digest
```

The skill name is picked up from the YAML frontmatter in `SKILL.md`.

### 7. Schedule it

In Claude Desktop → scheduled tasks, create a daily task that invokes the `competitor-intel-digest` skill. Something like:

> Run the competitor-intel-digest skill and send the resulting digest.

## How it runs

1. Claude Desktop fires the scheduled task each morning.
2. Claude loads `SKILL.md`, reads the tracked entities, and researches via web search + fetch.
3. Claude writes the digest in the prescribed markdown format.
4. Claude runs `python3 send_email.py --subject "…" --body-file -` and pipes the digest in.
5. `send_email.py` renders markdown to HTML and sends via Resend from `onboarding@resend.dev`.

## Customizing

- **Tracked entities**: edit the **Tracked Entities** section of `SKILL.md`.
- **Space queries**: same section.
- **Report format**: edit the fenced report template inside `SKILL.md`.
- **Email styling**: edit the `<style>` block in `render_html` in `send_email.py`.

## Troubleshooting

**No email arrived**
- Check spam.
- Make sure `EMAIL_TO` exactly matches the email you signed up for Resend with — `onboarding@resend.dev` refuses to deliver anywhere else.
- Run the test command from step 4. A failure there is config, not skill.

**Skill runs but never calls the script**
- The skill uses a literal `bash` block with `<REPO_PATH>`. If you didn't replace that in step 5, Claude has no valid path.
- Try an absolute path (`/Users/you/competitor-monitor`) instead of `~`.

**Want to send to someone other than yourself, or from your own domain**
- Verify a domain in Resend, then change the `EMAIL_FROM` constant at the top of `send_email.py` to an address on that domain. The env-less design assumes the self-alert case; moving past it is one line.
