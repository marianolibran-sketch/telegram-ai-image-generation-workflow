# Telegram Affiliate Content Bot — n8n

**An open-source workflow template for collecting 9 products via Telegram and creating promotional image drafts using Cloudflare Workers AI.**

A Telegram bot collects a product photo, name and code for each of 9 products; n8n stores the list, sends images to Cloudflare Workers AI, composes the covers and returns up to **18 output files** (9 covers + 9 collages). If Cloudflare rejects a generation with error **3030**, the workflow attempts to use the original Telegram photo as a fallback.

> **Status: release candidate — not yet verified on a clean installation.** The original private workflow completed a 9-product run; this sanitized public template has been structurally checked, **successfully imported in an existing n8n installation, but not tested end to end or verified on a clean installation**. Image quality is inconsistent. Treat all images as *drafts* and inspect them before publishing.

**[Guía de configuración en español](GUIA_CONFIGURACION.md)** · **[Architecture](ARCHITECTURE.md)** · **[Security](SECURITY.md)** · **[Release checklist](RELEASE_CHECKLIST.md)**

## What it does

- Collects 9 product submissions in a **private Telegram chat**; each submission includes **one photo with a caption**.
- Stores cycle state in an n8n **Data Table** so a cycle can be resumed.
- Requests an AI **cover** and **2×2 collage** using Cloudflare Workers AI.
- Adds product name/code to the cover with n8n image-processing nodes.
- Sends the resulting files back to Telegram, flagging Cloudflare moderation fallbacks when needed.

### Workflow at a glance

```mermaid
flowchart LR
    A[Telegram: photo + caption] --> B[Validate authorized chat]
    B --> C[(n8n Data Table)]
    C --> D{9 products ready?}
    D -- No --> E[Ask for next product]
    D -- Yes --> F[Process one product at a time]
    F --> G[Download Telegram photo]
    G --> H[Cloudflare cover + collage]
    H --> I{Image available?}
    I -- Yes --> J[Resize and compose images]
    I -- 3030 blocked --> K[Fallback to original photo]
    K --> J
    J --> L[Prepare 18 files]
    L --> M[Send to Telegram]
```

See the [more detailed architecture diagram](ARCHITECTURE.md) and open the sticky note **`Nota - 00 · EMPEZÁ ACÁ - MAPA DE CONFIGURACIÓN`** at the top-left of the imported n8n canvas.

## Requirements

- n8n with **Telegram Trigger**, **Telegram**, **Data Table**, **HTTP Request**, **Edit Image** and **Code** nodes available.
- Your **own Telegram bot** created via [@BotFather](https://core.telegram.org/bots/features#botfather).
- Your **own Cloudflare account**, Workers AI access, API token and available quota.
- A **public HTTPS webhook URL** reachable by Telegram (especially important with local Docker installations).
- A private Telegram chat for the authorized user; this template is not configured as a multi-user bot.

## Install and configure

1. Import **[`affiliate-content-bot.json`](affiliate-content-bot.json)** into n8n as a **new workflow**. Do not overwrite an existing private workflow.
2. Create a Telegram bot with **@BotFather**. Create a **Telegram API credential** in n8n and assign it to all **6 Telegram nodes**.
3. In **`Normalizar entrada`**, replace `YOUR_TELEGRAM_CHAT_ID` with the ID of your own private chat (only in your *local* n8n instance).
4. Create the n8n Data Table **`Ciclos_Afiliados`** with the five columns below, and select your table in **`Leer ciclo guardado`** and **`Guardar estado`**.
5. In n8n, create an **HTTP Header Auth credential** with `Authorization: Bearer YOUR_CLOUDFLARE_TOKEN`; assign it to both **`CF - ...`** nodes. Do **not** store the token in the workflow JSON.
6. In those same two Cloudflare nodes, replace `YOUR_CLOUDFLARE_ACCOUNT_ID` in the **URL** with your own account ID.
7. Verify webhook reachability and credentials. Test the full cycle with **non-sensitive sample photos** before actual use.

| Data Table column | Type |
| --- | --- |
| `chat_id` | Text |
| `estado` | Text |
| `cantidad` | Number |
| `productos_json` | Text (sufficient length for serialized JSON) |
| `ciclo_id` | Text |

All setup locations, node names and links are in the **[Spanish step-by-step guide](GUIA_CONFIGURACION.md)**.

## Using the Telegram bot

Send these exact messages to **your own bot** in your **authorized private chat**:

1. **`iniciar ciclo de generación`** — starts a cycle (or retries generation if 9 products were already saved).
2. Send **one photo per message**, with this **photo caption**:

   ```text
   Nombre: Mouse gamer de ejemplo
   ID: EJEMPLO123
   Precio: $25000
   Precio anterior: $30000
   Descuento: 15%
   ```

   Only `Nombre` and `ID` are required. Price fields are optional; the bot does not validate a price/discount against any marketplace.
3. Repeat until **9 products** are saved. The workflow then attempts to create 9 covers + 9 collages and send the files.
4. **`reiniciar ciclo`** — discards the current cycle and starts again.

> **Sample names, prices and codes are fictional.** This workflow does not automatically fetch Mercado Libre products, validate affiliate IDs or publish advertisements.

## Configuration map

| Change | Exact n8n location |
| --- | --- |
| Telegram token | n8n **Telegram API credential**, assigned to `Telegram Trigger`, `Get a file`, `Telegram - pedir siguiente`, `Telegram - corregir formato`, `Send a document`, `Send a text message` |
| Authorized Telegram chat | `Normalizar entrada` → JavaScript code → `YOUR_TELEGRAM_CHAT_ID` |
| Storage | `Leer ciclo guardado` + `Guardar estado` → select your `Ciclos_Afiliados` Data Table |
| Cloudflare API token | n8n **HTTP Header Auth credential**, assigned to the two `CF - ...` HTTP Request nodes |
| Cloudflare Account ID | Both `CF - ...` nodes → `URL` → `YOUR_CLOUDFLARE_ACCOUNT_ID` |
| Cover prompt | `CF - PORTADA (FLUX.2)` → body parameter `prompt` |
| Collage prompt | `CF - COLLAGE (FLUX.2)` → body parameter `prompt` |
| Cover lettering/layout | `COMPONER PORTADA - TEXTOS EXACTOS` → image-edit operations |

**Keep the existing `chatId`, `fileId` expressions and loop connections.** The workflow is designed for exactly **9 products**; changing this count requires code changes and testing.

## Repository contents

```text
telegram-ai-image-generation-workflow/
├── README.md
├── LICENSE
├── SECURITY.md
├── .gitignore
├── affiliate-content-bot.json       # Sanitized workflow
├── GUIA_CONFIGURACION.md
├── ARCHITECTURE.md
├── RELEASE_CHECKLIST.md
├── SECURITY_AUDIT.md
└── audit_workflow.py                 # Offline privacy checks
```

## Known limitations

- **Product fidelity is not guaranteed**: generated pictures can change the product, repeat viewpoints or produce poor compositions.
- Cloudflare's **3030 moderation rejection** may trigger an original-photo fallback; fallback collages do **not** represent four different views.
- Other API or processing errors can still interrupt execution; this is **not a guaranteed 18-file delivery**.
- The current design expects **9 products**, a single authorized **private** Telegram chat and Cloudflare Workers AI (model used in JSON: `@cf/black-forest-labs/flux-2-klein-4b`).
- AI/model access, quotas, prices and output formats depend on the provider and may change.
- The sanitized export is **not yet live-tested in an isolated n8n instance**.

## Safety, testing and contributing

Read [SECURITY.md](SECURITY.md) before distributing or modifying the export. A configured workflow may include **your real chat ID and Cloudflare account ID**. Never commit those values, working tokens, photos, Data Table contents, n8n execution logs or raw private exports.

Run the offline checker before publishing:

```bash
python3 audit_workflow.py
```

A passing scan is **not a guarantee** that no private information remains. The [release checklist](RELEASE_CHECKLIST.md) includes the import test, end-to-end test and Git history review still required before announcing a stable release. Please don't post working secrets in GitHub issues.

## License

Distributed under the [MIT License](LICENSE). The copyright line can be personalized with the repository owner's preferred name or GitHub handle before public release.

*This is an independent community project, not an official Telegram, Cloudflare, Mercado Libre or n8n product.*
