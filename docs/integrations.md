# Integraciones de diseño y productividad

Esta guía documenta los SDK compatibles para Figma, Notion y Slack, con ejemplos en Node.js/TypeScript y Python. Asegúrate de que el archivo `.env` no se suba al repositorio y contenga los tokens necesarios.

## Variables de entorno

```bash
FIGMA_TOKEN=...   # Personal access token de Figma
NOTION_TOKEN=...  # Secreto de integración de Notion
SLACK_TOKEN=...   # Token de bot de Slack
```

## Node.js / TypeScript

Instala los SDK oficiales o de la comunidad con npm:

```bash
# Cliente REST de Figma (SDK de la comunidad)
npm install figma-js                # O bien: npm install @figma-js/sdk
# Cliente de la API de Notion (oficial)
npm install @notionhq/client

# Cliente de la Web API de Slack (oficial)
npm install @slack/web-api

# Si quieres generar tipos o interactuar con design tokens de Figma
npm install --save-dev figma-export
```

Ejemplos de uso:

```ts
// figma.ts
import { Client as FigmaClient } from 'figma-js';

export const figma = FigmaClient({ personalAccessToken: process.env.FIGMA_TOKEN });

// Alternativa con el paquete @figma-js/sdk
// import { Figma } from '@figma-js/sdk';
// export const figma = new Figma({ personalAccessToken: process.env.FIGMA_TOKEN });

// notion.ts
import { Client as NotionClient } from '@notionhq/client';

export const notion = new NotionClient({ auth: process.env.NOTION_TOKEN });

// slack.ts
import { WebClient } from '@slack/web-api';

export const slack = new WebClient(process.env.SLACK_TOKEN);
```

Para exportar tokens de Figma vía CLI:

```bash
# Install globally
npm install -g figma-export

# Or run via npx
npx figma-export tokens --file-id <your-file-id> --token <your-figma-token>
```

## Python

Instala los paquetes correspondientes con pip:

```bash
# Figma API (librería de la comunidad)
pip install figma-python

# Notion SDK (oficial)
pip install notion-client

# Slack SDK (oficial)
pip install slack-sdk

# Si necesitas credenciales de Google para Sheets u otros servicios:
pip install google-auth-httplib2 google-auth-oauthlib
```

Ejemplo de uso:

```python
import os
from figma import Figma
from notion_client import Client as NotionClient
from slack_sdk import WebClient

figma_client = Figma(access_token=os.getenv("FIGMA_TOKEN"))
notion_client = NotionClient(auth=os.getenv("NOTION_TOKEN"))
slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))

# Ejemplo: obtener un archivo de Figma
# file = figma_client.file("FIGMA_FILE_KEY")
```

Exporta las variables de entorno para sesiones locales:

```bash
export FIGMA_TOKEN=<your-figma-token>
export NOTION_TOKEN=<your-notion-integration-secret>
export SLACK_TOKEN=<your-slack-bot-token>
```
