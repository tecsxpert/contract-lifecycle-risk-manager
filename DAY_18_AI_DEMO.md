# Day 18 AI Demo — Recommend, Generate Report, and Health Check

## New demo endpoints

1. **AI service health**
   - `GET http://localhost:5000/health`
   - Response:
     ```json
     {
       "status": "ok",
       "service": "ai-service",
       "healthy": true
     }
     ```

2. **Recommend action**
   - `POST http://localhost:8080/api/ai/recommend`
   - Input:
     ```json
     {
       "prompt": "This contract includes payment terms, confidentiality clauses, and a moderate risk score."
     }
     ```
   - Expected response:
     ```json
     {
       "recommendation": "Review the risk score and add remediation terms. Clarify payment terms and add late payment penalties.",
       "sanitized_prompt": "This contract includes payment terms, confidentiality clauses, and a moderate risk score."
     }
     ```

3. **Generate report**
   - `POST http://localhost:8080/api/ai/report`
   - Input:
     ```json
     {
       "prompt": "Analyze contract risk and summarize confidentiality requirements."
     }
     ```
   - Expected response:
     ```json
     {
       "report": "Contract report: This contract appears to carry a moderate risk profile. Key areas to review are payment terms, vendor obligations, and confidentiality controls. Follow up with a detailed clause review and compliance check.",
       "sanitized_prompt": "Analyze contract risk and summarize confidentiality requirements."
     }
     ```

## Demo steps

1. Start the stack using Docker Compose.
2. Verify the AI service health endpoint:
   - `GET http://localhost:5000/health`
3. Call the backend recommend endpoint:
   - `POST http://localhost:8080/api/ai/recommend`
4. Call the backend report endpoint:
   - `POST http://localhost:8080/api/ai/report`
5. Confirm the output contains actionable recommendations or a generated contract report.

## 60-second Flask + Groq explanation

This AI service is built with Flask, a lightweight Python web framework, and it sits inside its own container. Flask receives requests from the backend, sanitizes prompts, and protects against unsafe instructions before any AI logic runs. The service uses Groq as the AI provider; Groq is the external model engine that our microservice would call for advanced language understanding. In this demo, the Flask service returns safe recommendation and report text based on the sanitized prompt, so the audience can see how the AI path is separated, protected, and ready to connect to a real Groq model endpoint in production.
