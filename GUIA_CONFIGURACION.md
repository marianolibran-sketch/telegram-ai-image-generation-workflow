# Guía de configuración — Telegram Affiliate Content Bot (n8n)

> **Primero:** importá `affiliate-content-bot.json` en n8n como workflow **nuevo**. No reemplaces ni exportes a GitHub una instancia privada ya configurada.
>
> La primera nota visible del canvas, **`Nota - 00 · EMPEZÁ ACÁ - MAPA DE CONFIGURACIÓN`**, resume exactamente dónde configurar cada dato.

## Checklist de puesta en marcha

- [ ] **Telegram:** en [@BotFather](https://core.telegram.org/bots/features#botfather) ejecutá `/newbot` y conservá el token **en privado**. Creá una credencial *Telegram API* en n8n y seleccionála en estos **seis** nodos:
  - `Telegram Trigger`
  - `Get a file`
  - `Telegram - pedir siguiente`
  - `Telegram - corregir formato`
  - `Send a document`
  - `Send a text message`
- [ ] **Permitir el chat:** abrí `Normalizar entrada` → `jsCode`. Reemplazá exclusivamente el texto `YOUR_TELEGRAM_CHAT_ID` por el ID de tu **chat privado**, sin quitar las comillas. Ejemplo ficticio: `const CHAT_PERMITIDO = '12345678';`. Este filtro permite un solo chat privado por defecto y bloquea a cualquier otro.
- [ ] **Almacenamiento:** creá una Data Table llamada `Ciclos_Afiliados` con cinco columnas exactas: `chat_id` (texto), `estado` (texto), `cantidad` (número), `productos_json` (texto suficientemente largo), `ciclo_id` (texto). Seleccionala en `Leer ciclo guardado` (operación **get**) y `Guardar estado` (operación **upsert**); conservá filtros por `chat_id` y mapeos existentes. Es posible que el selector de tabla no se resuelva automáticamente tras importar.
- [ ] **Cloudflare token:** creá una credencial *Header Auth* en n8n con nombre de encabezado `Authorization` y valor `Bearer TU_TOKEN_PRIVADO`. Asignala a ambos nodos `CF - PORTADA (FLUX.2)` y `CF - COLLAGE (FLUX.2)`.
- [ ] **Cloudflare Account ID:** en el campo **URL** de ambos nodos `CF - ...` reemplazá `YOUR_CLOUDFLARE_ACCOUNT_ID` por tu ID. El token se guarda solo en las credenciales y **nunca** en el campo URL ni en el JSON exportado.
- [ ] **Webhook:** asegurá una URL HTTPS pública accesible desde Telegram. Un n8n local en Docker no recibe webhooks externos sin una configuración de red/túnel adecuada.
- [ ] **Prueba:** importá, asigná credenciales, creá tabla y configurá chat ID en entorno propio. Recién entonces activá o probá el workflow con **datos ficticios**. Verificá el procesamiento completo de 9 productos y los archivos devueltos antes de publicar resultados.

## Cómo encontrar tu chat ID sin publicarlo

1. Una vez que tengas tu bot de prueba, abrí **`Telegram Trigger`** en n8n y utilizá su modo de prueba/escucha de eventos.
2. En Telegram, abrí una **conversación privada** con ese bot y enviá un mensaje cualquiera.
3. Buscá el campo **`message.chat.id`** en los datos que recibe el trigger. Es el identificador del chat que querés autorizar.
4. Copiá el número **solamente en tu instancia privada** en `Normalizar entrada`, reemplazando `YOUR_TELEGRAM_CHAT_ID` **entre las comillas existentes**.

No confundas el **token del bot** (secreto) con el **chat ID** (identificador). Ninguno debe quedar pegado en el JSON público después de configurar tu instalación personal.

## Cómo probar el ciclo

1. Enviá el texto exacto **`iniciar ciclo de generación`** a tu bot en el chat autorizado.
2. Enviá una foto con este pie de foto (ejemplo completamente ficticio):

   ```text
   Nombre: Mouse gamer de ejemplo
   ID: EJEMPLO123
   Precio: $25000
   Precio anterior: $30000
   Descuento: 15%
   ```

   Los únicos campos obligatorios son `Nombre` e `ID`; los otros tres son opcionales.
3. Esperá la confirmación del bot, y repetí **una foto por mensaje** hasta completar los 9 productos.
4. Verificá que los 18 archivos resultantes **se abran y conserven los códigos correspondientes**, y que el mensaje final indique las imágenes de respaldo cuando corresponda.
5. Si querés empezar desde cero, enviá **`reiniciar ciclo`**. El comando inicial también puede volver a intentar la generación cuando ya hay nueve productos almacenados.

**No publiques imágenes sin revisarlas:** el modelo puede alterar detalles del producto y un collage de respaldo no representa cuatro perspectivas reales.

## Personalización sin romper el flujo

| Quiero cambiar | Nodo exacto | Campo o sección |
| --- | --- | --- |
| Token del bot | Los seis nodos de Telegram | `Credential for Telegram API` (credencial de n8n) |
| Chat autorizado | `Normalizar entrada` | `jsCode` → `YOUR_TELEGRAM_CHAT_ID` |
| Tabla | `Leer ciclo guardado` y `Guardar estado` | `Data Table` → seleccionar tu tabla |
| Token de Cloudflare | Ambos nodos `CF - ...` | `Credential for Header Auth` |
| Cuenta Cloudflare | Ambos nodos `CF - ...` | `URL` → `YOUR_CLOUDFLARE_ACCOUNT_ID` |
| Prompt portada | `CF - PORTADA (FLUX.2)` | `Body Parameters` → `prompt` |
| Prompt collage | `CF - COLLAGE (FLUX.2)` | `Body Parameters` → `prompt` |
| Nombre/código dibujados | `COMPONER PORTADA - TEXTOS EXACTOS` | Configuración de imagen, sin eliminar expresiones existentes |

## Dónde NO hace falta tocar nada

- **No borres** los nodos Telegram ni sus expresiones de `chatId` o `fileId`.
- **No cambies** las conexiones del bucle `UNO por UNO - Bucle IA (pendiente)` para modificar el aspecto visual.
- **No cambies** la cantidad 9 sin revisar y probar el código: esta versión **no** es configurable para otra cantidad sin modificaciones funcionales.
- **No subas** una exportación con credenciales/IDs reales o fotos y mensajes de ejecución.

## Enlaces oficiales

- [Crear un bot con BotFather](https://core.telegram.org/bots/features#botfather)
- [Credenciales Telegram en n8n](https://docs.n8n.io/integrations/builtin/credentials/telegram/)
- [Data Tables en n8n](https://docs.n8n.io/data/data-tables/)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)

## Limitaciones conocidas

- La calidad de imágenes generadas puede variar; el modelo puede alterar el producto.
- Algunos pedidos pueden ser bloqueados por Cloudflare (código 3030); hay una ruta de respaldo en el workflow.
- La versión pública se ha revisado estructuralmente, **pero aún no fue probada de punta a punta en una instalación limpia de n8n**.
- Las credenciales se guardan en tu instancia de n8n, no en este repositorio.

## Más documentación

- [Diagrama del funcionamiento](ARCHITECTURE.md)
- [Checklist antes de publicar](RELEASE_CHECKLIST.md)
- [Seguridad y privacidad](SECURITY.md)
