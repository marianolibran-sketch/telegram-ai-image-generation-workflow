# Security audit — community template, updated public package

**Scope:** The current public project (workflow JSON, README, license and documentation) and the exported workflow `affiliate-content-bot.json`. This is an offline review, **not** a penetration test of n8n or Cloudflare/Telegram accounts.

## Checks performed

| Check | Result |
|---|---|
| JSON parses successfully | Pass |
| Workflow nodes have no attached credential references | Pass |
| No pinned workflow execution data | Pass |
| No live bot-token/JWT/Bearer-token/email/long-number matches in the public workflow scan | Pass (pattern-based) |
| Cloudflare HTTP endpoints use placeholder account ID | Pass |
| Telegram access filter uses placeholder chat ID | Pass |
| Only expected Cloudflare domains in outbound HTTP Request URLs | Pass |
| No external HTTP destinations hidden in JavaScript code | No matching URLs observed |
| All connection endpoints reference existing nodes | Pass |
| All 25 functional node parameters and all connections preserved from the prior public template | Pass (structured comparison) |
| Documentation additions (README, architecture, release checklist, MIT license) | Reviewed; no real account tokens or personal references intentionally included |
| Revised visual layout imported/executed on clean n8n | **Not performed** |
| Personal Git repository/history | **Not yet reviewed** |
| All earlier private copies, backups, credentials | **Outside this audit** |

## Residual risks / actions

1. This workflow needs **private** credentials and real chat/account identifiers to run. A configured export must NOT be recommitted.
2. Original/private exports (if retained locally) must remain outside the Git repository. Some previous exports may contain private account/chat identifiers. This public template is not a secure backup of your live instance.
3. Review all future README images, screenshots and examples before publishing.
4. If a token was previously posted in any conversation, committed to Git, or shared elsewhere, **revoke and replace** it at the provider. A sanitized JSON cannot revoke it.
5. `YOUR_TELEGRAM_CHAT_ID` deliberately prevents the public template from processing messages until configured. The README should not ask users to publish their numeric IDs.
6. Test actual import/configuration and one complete cycle on a **separate** bot before release.

To repeat the offline scan from the repository root:

```bash
python3 audit_workflow.py
```

**Interpretation:** a PASS is a useful screening result, **not** an absolute guarantee of safety or correct runtime behavior.

## Updated user-supplied export

This update adopts the revised canvas layout and new internal node IDs from the user-supplied n8n export. Its functional node parameters and connection graph were compared with the earlier public template and found identical. The source export contained six Telegram credential bindings, six node webhook identifiers, and instance/workflow metadata; those were removed from the public JSON. Other than the visual layout and newly generated IDs, no workflow behavior changes were intentionally made. This does not constitute a live runtime test.
