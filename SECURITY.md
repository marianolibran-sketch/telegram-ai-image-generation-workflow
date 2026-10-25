# Security and responsible publication

## Status

This repository contains a **public template**, not a copy of the author's live n8n instance. The exported workflow uses placeholders and does **not** include node credential bindings or pinned execution output. Automated checks do not guarantee that all private data has been found.

## Before making this repository public

1. Publish **only** files inside this sanitized project directory. Never commit previous raw exports, Docker volumes, database backups, `~/.n8n` contents, bot photos, logs, or execution exports.
2. Run `python3 audit_workflow.py`. Review the JSON, markdown, screenshots, and all changes **manually** as well. Read `SECURITY_AUDIT.md`.
3. Confirm there are no `credentials` bindings, fixed bot/chat identifiers, account identifiers, live keys or tokens, private webhook/tunnel domains, personal information, pinned test output, or customer/product data.
4. **Check Git history and the staged diff**, not just working files: `git diff --cached` and `git log --all --stat`. A later deletion does not erase earlier commits. If a secret was committed, rotate/revoke it; removing it from Git history is an additional step, not a substitute.
5. If a real Telegram or Cloudflare token was ever shared, consider it exposed. Revoke/rotate it in the provider dashboard and update credentials in the **private** n8n instance. Never post replacement tokens in issues or screenshots.
6. Import the public workflow into an isolated n8n installation, configure **new** test credentials, create a **new empty** Data Table and run an end-to-end test before claiming compatibility.
7. Do not upload a configured export to GitHub later. A user's locally edited workflow can contain their private chat ID or account ID, even though this template does not.

## Credential setup

- Telegram bot token: only n8n's **Telegram API credentials**. Set it on all Telegram nodes.
- Cloudflare API token: only n8n's **HTTP Header Auth credential** on both Cloudflare nodes.
- Cloudflare account ID: replace `YOUR_CLOUDFLARE_ACCOUNT_ID` privately in both HTTP Request URLs.
- Telegram chat ID: replace `YOUR_TELEGRAM_CHAT_ID` privately in `Normalizar entrada`. Do not commit the configured file.
- Do not paste tokens in JS code, prompts, notes, README, environment examples, or issues.

## Security/operational caveats

- The chat ID comparison in `Normalizar entrada` is a **simple access filter**, not a general-purpose authentication framework. Keep the n8n instance and Telegram credentials secure.
- n8n execution logs and Data Tables can contain user-supplied product names, IDs, captions and photos. Configure retention and access accordingly. They are **never** part of this repository.
- A public HTTPS webhook is required for Telegram in many self-hosted environments. Use your own domain/tunnel privately; don't commit its full URL unless intentionally public.
- Use API tokens with the **minimum permissions** required and monitor provider quotas.
- Do not commit screenshots of credentials or account settings.

## Reporting a vulnerability

Do not post working tokens or personal data in a public GitHub issue. Contact the repository maintainer privately using their chosen disclosure channel once provided.
