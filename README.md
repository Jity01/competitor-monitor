# Competitor Intelligence Monitor

A Claude skill that researches AI CI/CD competitors, customers, and emerging players daily, and emails you a digest via Resend.

## Setup (30 seconds)

```bash
git clone https://github.com/Jity01/competitor-monitor ~/.claude/skills/competitor-intel-digest
cd ~/.claude/skills/competitor-intel-digest
pip3 install -r requirements.txt
cp env.example .env
```

Open `.env` and fill in two lines:

```
RESEND_API_KEY=re_xxxxx       # from resend.com/api-keys
EMAIL_TO=you@example.com      # MUST be the email you signed up for Resend with
```

> **Why `EMAIL_TO` must match your Resend signup email:** we send from Resend's built-in `onboarding@resend.dev` sandbox sender so you don't have to verify a domain. That sender only delivers to the account owner. If you want to email someone else, verify a domain at resend.com/domains and change `EMAIL_FROM` in `send_email.py`.

Test it:

```bash
echo "# hi" | python3 send_email.py --subject "test" --body-file -
```

You should see `Sent to ...` and an email in your inbox. Then edit `SKILL.md` to swap the `<Competitor>` / `<Customer>` placeholders for the real ones, and schedule the `competitor-intel-digest` skill daily in Claude Desktop.

## Troubleshooting

- **`You can only send testing emails to your own email address`** — `EMAIL_TO` doesn't match your Resend signup email. Fix one or the other.
- **`command not found: python`** — use `python3`.
- **Skill can't find the script** — make sure you cloned to `~/.claude/skills/competitor-intel-digest` exactly. That's the path the skill uses.
