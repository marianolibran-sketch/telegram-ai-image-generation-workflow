# Release checklist (before making this repository public)

The project is a **release candidate**. Checkboxes are intentionally **unchecked** until someone verifies them in the target environment. A clean JSON parse is not a substitute for a working import or live execution.

## 1. Identity, ownership and license

- [ ] Confirm the repository name, author name / GitHub handle, public description and copyright attribution in `LICENSE`.
- [ ] Confirm that you want to distribute the project under the MIT License and that you can license the material you authored.
- [ ] Keep the repository independent from official Telegram, Cloudflare, n8n or marketplace branding.

## 2. Security and privacy

- [ ] Review **every file** for private IDs, tokens, URLs, customer data, test photographs and hidden execution records.
- [ ] Run `python3 audit_workflow.py` and inspect the results and `SECURITY_AUDIT.md`.
- [ ] Revoke/rotate any tokens previously exposed in a chat, upload or private commit (a clean JSON does not invalidate old tokens).
- [ ] Run `git status`, `git diff --cached`, `git log --all --stat` and review the commit history for accidental secrets.
- [ ] Ensure **no private workflow export** or configured screenshot has been copied into this repository.

## 3. Import and runtime verification (NOT YET DONE)

- [ ] Use a fresh/test n8n installation and import the **public** JSON as a *new* workflow.
- [ ] Confirm all nodes load without compatibility warnings; record the n8n version used.
- [ ] Create a new test Telegram bot; connect the same Telegram credential to **all six** Telegram nodes.
- [ ] Set the test private `chat_id` in `Normalizar entrada` and configure the public HTTPS webhook.
- [ ] Create an empty Data Table with the five documented columns and select it in both Data Table nodes.
- [ ] Connect test Cloudflare credentials and account ID in **both** HTTP nodes, with sufficient available quota.
- [ ] Run a complete cycle of 9 **fictional/non-sensitive** products with real test photos.
- [ ] Verify the 18 delivered files open correctly and captions/IDs match their input; check image MIME types and extensions.
- [ ] Verify a Cloudflare 3030 fallback if it occurs (do not intentionally trigger moderation).
- [ ] Test `reiniciar ciclo` and recovery from an interrupted cycle.

## 4. Presentation and documentation

- [ ] Read the README and Spanish guide as if you were a first-time installer; verify all node labels still match the JSON.
- [ ] Verify any future screenshots/preview images are **redacted** and do not feature tokens, account/chat IDs or real customer data.
- [ ] Optional: add a **redacted** screenshot of the complete canvas and anonymized before/after product outputs. Do not use private product photos without permission.
- [ ] Confirm the limitations and test status are stated accurately: no claim of guaranteed image quality or 18 successful generations.
- [ ] Re-run the security scan **after all final edits** and before the first public commit.

## 5. GitHub publication

- [ ] Create a new public repository using **only this reviewed directory**.
- [ ] Check `git diff --cached` before `git commit` / `git push`.
- [ ] Add a concise project description and appropriate topics (e.g., `n8n`, `telegram-bot`, `automation`, `cloudflare-workers-ai`).
- [ ] Verify the public GitHub view of the README, Mermaid diagram, license and workflow download.

**Release decision:** do not label the project **production-ready** until the clean import and full test cycle pass.
