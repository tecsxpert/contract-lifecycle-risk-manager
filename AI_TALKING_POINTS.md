# AI Talking Points — Day 16

## AI Overview for Demo Day

### What the AI does
- The application routes contract prompts through a dedicated AI microservice.
- The AI service sanitizes incoming text and blocks unsafe prompt content.
- This keeps the AI integration secure while still enabling contract-related AI workflows.

## Groq explained in plain English
- **Groq** is the AI engine provider used by the microservice.
- It is the backend that powers model calls, similar to how a search service answers questions.
- We send sanitized user prompts to Groq and receive clean AI responses.
- In this project, Groq is used as the trusted AI model endpoint behind the Flask service.

## Prompts explained in plain English
- A **prompt** is the exact text we send to the AI service asking it to do something.
- For example: "Summarize the agreement: The vendor must deliver 100 widgets by June 30 with payment due net 30."
- The system first checks the prompt for unsafe or hidden instructions.
- If the prompt is safe, it is forwarded to the AI service, which returns the requested output.
- If the prompt contains malicious text, we reject it and return an error instead.

## Security talking points
- The AI path is isolated in a separate container, limiting the attack surface.
- Prompt sanitization is performed before the AI service processes any user input.
- We block prompt injection attempts such as "ignore previous instructions" or embedded HTML.
- The backend enforces role-based access and only exposes safe endpoints to the frontend.
- Secrets are kept out of the repository using `.env` and are not stored in source control.
- Docker Compose connects services securely using internal network names, not localhost assumptions.

## Day 16 note
- This is a concise card for Demo Day discussion.
- Use it to explain how the AI component works, why Groq is part of the stack, and how security is enforced.
