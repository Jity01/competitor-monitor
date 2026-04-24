# Starsling Intel Monitor

A Claude skill that checks in each day on Starsling's direct CI-runner competitors (Depot, Blacksmith, WarpBuild, Namespace, BuildJet, Ubicloud, RunsOn, Actuated), adjacent AI dev-tool players, GitHub Actions itself, and current + prospective customers — then emails you a digest via Resend. Runs as a scheduled task in Claude Cowork.

## Setup

1. **Sign up for Resend** at [resend.com](https://resend.com) — remember which email you use; that's the only address the digest can go to. Create an API key at resend.com/api-keys.

2. **In Claude Cowork**, create a new scheduled task using `SKILL.md` from this repo as the skill definition. Paste the following into the task fields:

    **Name:**
    ```
    Starsling Intel Digest
    ```

    **Prompt:** (swap in your real key + email)
    ```
    Before doing anything else, set these two environment variables for this session (use `export` in a bash step):

      RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxx
      EMAIL_TO=you@example.com

    Then run the competitor-intel-digest skill. Produce today's Starsling intelligence digest following the format defined in the skill — deep-research Tier 1 CI-runner competitors (Depot, Blacksmith, Namespace, WarpBuild, BuildJet, Ubicloud, RunsOn, Actuated, GitHub Actions), lightly scan Tier 2 adjacent AI dev-tool players, check current customers + ICP watchlist for signals, and actively surface emerging players. Save the final digest to a file named digest.md in the current working directory. Finally, run the Python email-send snippet at the bottom of the skill to deliver it via Resend.
    ```

3. **Pick a schedule** (daily at 8am is a good default) and save.

4. **Trigger a manual run** to verify — you should get an email within ~30 seconds of the final step.

## The one gotcha

`EMAIL_TO` must exactly match the email you signed up for Resend with. The skill sends from Resend's built-in `onboarding@resend.dev` sandbox sender so you don't have to verify a domain — the tradeoff is that sandbox sender only delivers to the account owner. If you'd rather email someone else, verify a domain at resend.com/domains and change the `"from"` field inside SKILL.md's send snippet.

## Why the API key is in the prompt

Cowork's cloud sandbox can't reach local files on your Mac, so the skill has to carry its own credentials.

## Tuning the skill

`SKILL.md` ships pre-filled with a tiered competitor list (Tier 1 = direct CI runners, Tier 2 = adjacent AI dev-tool space), a current-customer list, and a YC dev-infra ICP watchlist. Edit those sections whenever the picture changes — the scheduled task re-reads the skill on every run.

## If something doesn't work

- **`You can only send testing emails to your own email address`** — `EMAIL_TO` doesn't match the email you used to sign up for Resend. Line them up.
- **`HTTP 403 ... error code: 1010`** — Cloudflare bot-challenged the send. The skill sets a `User-Agent` header to avoid this; if it's still happening, something stripped the header.
- **Digest was produced but no email arrived** — Claude may have skipped the final Python snippet. Check that `RESEND_API_KEY` and `EMAIL_TO` were exported before the snippet ran, and that the snippet printed a response with an `"id"` field.
