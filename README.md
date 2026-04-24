# Starsling Intel Monitor

A Claude skill that checks in each day on Starsling's direct CI-runner competitors (Depot, Blacksmith, WarpBuild, Namespace, BuildJet, Ubicloud, RunsOn, Actuated), adjacent AI dev-tool players, GitHub Actions itself, and current + prospective customers — then emails you a digest via Resend. Runs as a scheduled task in Claude Cowork.

## Setup

1. **Sign up for Resend** at [resend.com](https://resend.com) — remember which email you use; that's the only address the digest can go to. Create an API key at [resend.com/api-keys](https://resend.com/api-keys).

2. **Upload the skill to Cowork.** In Cowork's skills area, upload `SKILL.md` from this repo. The skill will now appear in your skills list as `competitor-intel-digest`.

3. **Allowlist `api.resend.com` on the Cowork sandbox.** Cowork's sandbox has an outbound-proxy allowlist — the digest step will research and write `digest.md` fine, but the Resend send will fail with `X-Proxy-Error: blocked-by-allowlist` unless the host is on the list. Go to **Settings → Capabilities** and add `api.resend.com` to the network allowlist. On Team/Enterprise workspaces, only a workspace admin can change this — ask them if needed.

4. **Create a scheduled task.** In Cowork, click **+ New task** (top left) or type `/schedule`. Fill in:

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

    **Schedule:** daily at whatever time you like (e.g. 8am). Click **Schedule**.

5. **Trigger a manual run** from the Scheduled tasks page to verify. You should get an email within ~30 seconds of the final step.

## The one gotcha

`EMAIL_TO` must exactly match the email you signed up for Resend with. The skill sends from Resend's built-in `onboarding@resend.dev` sandbox sender so you don't have to verify a domain — the tradeoff is that sandbox sender only delivers to the account owner. If you'd rather email someone else, verify a domain at resend.com/domains and change the `"from"` field inside SKILL.md's send snippet.

## Why the API key is in the prompt

Cowork's cloud sandbox can't reach local files on your Mac, so the skill has to carry its own credentials.

## Tuning the skill

`SKILL.md` ships pre-filled with a tiered competitor list (Tier 1 = direct CI runners, Tier 2 = adjacent AI dev-tool space), a current-customer list, and a YC dev-infra ICP watchlist. Edit whenever the picture changes and re-upload in Cowork (it replaces the old version). The scheduled task re-reads the skill on every run.

## If something doesn't work

- **`X-Proxy-Error: blocked-by-allowlist`** — Cowork's sandbox refused the outbound call to Resend because `api.resend.com` isn't on the network allowlist. Go to **Settings → Capabilities** and add it (see setup step 3). On Team/Enterprise workspaces, a workspace admin has to do this.
- **`You can only send testing emails to your own email address`** — `EMAIL_TO` doesn't match the email you used to sign up for Resend. Line them up.
- **`HTTP 403 ... error code: 1010`** — Cloudflare bot-challenged the send. The skill sets a `User-Agent` header to avoid this; if it's still happening, something stripped the header.
- **Digest was produced but no email arrived** — Claude may have skipped the final Python snippet. Check that `RESEND_API_KEY` and `EMAIL_TO` were exported before the snippet ran, and that the snippet printed a response with an `"id"` field. If the snippet printed a proxy error, see the first entry above.
