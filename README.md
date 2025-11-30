# Abaco Loans Analytics

This project contains a Next.js application with an API for generating images using OpenAI's DALL-E 3 model.

## Getting Started

First, install the project dependencies:

```bash
npm install
```

Next, create a `.env.local` file in the root of the project and add the required environment variables:

```env
OPENAI_API_KEY="your-openai-api-key"
API_SECRET_KEY="your-own-secret-key-for-the-api"
DOMINIO="your-domain"
```

Then, run the development server:

```bash
npm run dev
```

The application will be available at http://localhost:3000. The image generation API is at `POST /api/generate-image`.

## Code Analysis

This project uses ESLint for code analysis. You can run the linter manually with:

```bash
npm run lint
```

Additionally, a pre-commit hook is set up with `husky` and `lint-staged` to automatically lint and fix files before they are committed.