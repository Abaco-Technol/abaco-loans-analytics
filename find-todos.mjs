import { Codex } from "@openai/codex-sdk";
import { promises as fs } from 'fs';

const codex = new Codex();
const thread = codex.startThread();

const run = async () => {
  // In a real scenario, you would first read project files to find "TODO" comments.
  const todoContent = "TODO: Refactor the user authentication module.";

  const prompt = `Based on the following TODO, create a detailed implementation plan in Markdown format: ${todoContent}`;
  
  const result = await thread.run(prompt);
  const plan = result.finalResponse;

  await fs.mkdir('.plans', { recursive: true });
  await fs.writeFile('.plans/auth-refactor-plan.md', plan);
  
  console.log("Implementation plan created in .plans/auth-refactor-plan.md");
};

run().catch(console.error);
