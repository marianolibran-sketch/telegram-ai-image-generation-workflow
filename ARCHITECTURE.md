# Workflow architecture

This diagram describes the **existing public template**, not a redesign. The nodes and connections in the JSON were intentionally kept unchanged during the documentation stage.

```mermaid
flowchart TB
    subgraph Receiving[1. Telegram and input validation]
        T[Telegram Trigger] --> N[Normalizar entrada]
        N --> DB1[Leer ciclo guardado]
        DB1 --> STATE[Gestionar ciclo y productos]
        STATE --> SWITCH[Guardar o responder]
        SWITCH --> SAVE[Guardar estado]
        SAVE --> NEXT[Telegram - pedir siguiente]
    end
    subgraph Loop[2. Nine-product processing]
        NEXT --> PREP[Preparar 9 solicitudes individuales IA]
        PREP --> BATCH[UNO por UNO - Bucle IA]
        BATCH --> GET[Get a file]
        GET --> RESIZE[Reducir foto para Cloudflare]
        RESIZE --> DATA[Vincular datos y foto]
    end
    subgraph Images[3. AI generation and image composition]
        DATA --> COVER[CF - PORTADA FLUX.2]
        DATA --> COLLAGE[CF - COLLAGE FLUX.2]
        COVER --> KEEP_C[Guardar Portada: AI or 3030 fallback]
        COLLAGE --> KEEP_G[Guardar Collage: AI or 3030 fallback]
        KEEP_C --> COMPOSE[Formato + textos exactos]
        KEEP_G --> SCALE[Formato final collage]
        COMPOSE --> MERGE[Merge]
        SCALE --> MERGE
        MERGE --> RESULT[Resultado del Producto]
        RESULT --> BATCH
    end
    subgraph Delivery[4. Final Telegram delivery]
        BATCH --> FINISH[Preparar 18 Imagenes]
        FINISH --> SEND[Send a document]
        SEND --> TEXT[Send a text message]
    end
```

**Note:** This is a conceptual illustration; the branches and loop are simplified. The authoritative execution graph is the n8n workflow JSON itself. In particular, the final delivery branch fires after the loop completes, not on every iteration.

## Input contract

- Start: exact Telegram message `iniciar ciclo de generación`.
- Reset: exact Telegram message `reiniciar ciclo`.
- Product: one **photo** with caption containing `Nombre:` and `ID:` on separate lines; optional `Precio:`, `Precio anterior:`, `Descuento:`.
- Access: a **single private chat ID** is allowed by `Normalizar entrada` after its placeholder is configured.
- State: an n8n Data Table keyed/filtering by `chat_id` stores the products as serialized JSON.

## Outputs and fallbacks

- Normal result: 9 cover images plus 9 collage images; captions describe product numbers.
- Error 3030: the affected cover/collage uses the original uploaded image instead of an AI-generated result, then proceeds to downstream image steps. This protects the process from that *specific* rejection, not all failure types.
- Final Telegram message includes a fallback count and the product positions affected.
- A fallback collage is **not** a set of four genuine photographs. Always review outputs before redistribution.

## Node configuration quick reference

See the sticky notes inside n8n, the [README configuration map](README.md#configuration-map) and the [Spanish setup guide](GUIA_CONFIGURACION.md). Do not modify paths, `chatId`/`fileId` expressions, or loop edges without tests.
