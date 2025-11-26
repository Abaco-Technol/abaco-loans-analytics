# Design and productivity integrations

This guide lists the supported SDKs for Figma, Notion, and Slack with examples in Node.js/TypeScript and Python. Keep your `.env` file out of version control and populate it with the required tokens.

## Environment variables

```bash
FIGMA_TOKEN=...   # Figma personal access token
NOTION_TOKEN=...  # Notion integration secret
SLACK_TOKEN=...   # Slack bot token
```

## Node.js / TypeScript

Install the official or community SDKs with npm:

```bash
# Figma REST client (community)
npm install figma-js                # Alternative: npm install @figma-js/sdk
# Notion API client (official)
npm install @notionhq/client

# Slack Web API client (official)
npm install @slack/web-api

# For type generation or design tokens from Figma
npm install --save-dev figma-export
```

Usage examples:

```ts
// figma.ts
import { Client as FigmaClient } from 'figma-js';

export const figma = FigmaClient({ personalAccessToken: process.env.FIGMA_TOKEN });

// Alternative using @figma-js/sdk
// import { Figma } from '@figma-js/sdk';
// export const figma = new Figma({ personalAccessToken: process.env.FIGMA_TOKEN });

// notion.ts
import { Client as NotionClient } from '@notionhq/client';

export const notion = new NotionClient({ auth: process.env.NOTION_TOKEN });

// slack.ts
import { WebClient } from '@slack/web-api';

export const slack = new WebClient(process.env.SLACK_TOKEN);
```

Export Figma design tokens via CLI:

```bash
# Install globally
npm install -g figma-export

# Or run via npx
npx figma-export tokens --file-id <your-file-id> --token <your-figma-token>
```

## Python

Install the relevant packages with pip:

```bash
# Figma API (community)
pip install figma-python

# Notion SDK (official)
pip install notion-client

# Slack SDK (official)
pip install slack-sdk

# If Google credentials are needed for Sheets or other services
pip install google-auth-httplib2 google-auth-oauthlib
```

Usage example:

```python
import os
from figma import Figma
from notion_client import Client as NotionClient
from slack_sdk import WebClient

figma_client = Figma(access_token=os.getenv("FIGMA_TOKEN"))
notion_client = NotionClient(auth=os.getenv("NOTION_TOKEN"))
slack_client = WebClient(token=os.getenv("SLACK_TOKEN"))

# Example: fetch a Figma file
# file = figma_client.file("FIGMA_FILE_KEY")
```

Export environment variables for local sessions:

```bash
export FIGMA_TOKEN=<your-figma-token>
export NOTION_TOKEN=<your-notion-integration-secret>
export SLACK_TOKEN=<your-slack-bot-token>
```
