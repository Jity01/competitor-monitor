# Competitor Intelligence Monitor

A Claude skill that checks in on your AI CI/CD competitors, customers, and the broader space each day, then emails you a tidy digest via Resend.

## Setup (about 30 seconds)

```bash
git clone https://github.com/Jity01/competitor-monitor ~/.claude/skills/competitor-intel-digest
cd ~/.claude/skills/competitor-intel-digest
pip3 install resend markdown
cp env.example .env
```

Now open `.env` and fill in two lines:

```
RESEND_API_KEY=re_xxxxx       # grab one at resend.com/api-keys
EMAIL_TO=you@example.com      # use the same email you signed up for Resend with
```

That second line is the one gotcha worth knowing about: we send from Resend's built-in `onboarding@resend.dev` address so you don't have to bother verifying a domain. The tradeoff is that Resend's sandbox sender will only deliver to the email on your Resend account — so `EMAIL_TO` needs to be that same address. If you'd rather email someone else down the road, verify a domain at resend.com/domains and swap the `EMAIL_FROM` constant at the top of `send_email.py`.

Give it a quick test:

```bash
echo "# hi" | python3 send_email.py --subject "test" --body-file -
```

You should see `Sent to …` in your terminal and a test email in your inbox.

Last thing: open `SKILL.md`, swap the `<Competitor>` / `<Customer>` placeholders for your real list, and register `competitor-intel-digest` as a scheduled skill in Claude Desktop.

## If something doesn't work

- **`You can only send testing emails to your own email address`** — `EMAIL_TO` doesn't match the email you used to sign up for Resend. Line them up and you're good.
- **`command not found: python`** — use `python3` instead.
- **The skill can't find `send_email.py`** — make sure you cloned into `~/.claude/skills/competitor-intel-digest` exactly; that's the path the skill uses.
