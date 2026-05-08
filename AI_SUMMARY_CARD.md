# AI Summary Card — Day 15

## Project
**Contract Lifecycle Risk Manager**

## GitHub
https://github.com/manoj2049/contract-lifecycle-risk-manager

## 3 Core AI Endpoints

1. **AI prompt submit**
   - `POST http://localhost:8080/api/ai/prompt`
   - Sends contract prompt text through the backend to the AI service.
   - Returns sanitized prompt output or an error response for unsafe input.

2. **Backend contract list**
   - `GET http://localhost:8080/api/contracts?page=0&size=10`
   - Retrieves paginated contract records for the frontend.
   - Supports empty-state safe responses.

3. **Backend contract create**
   - `POST http://localhost:8080/api/contracts`
   - Creates a new contract entry with authorization enforcement.
   - Returns `201 Created` with the saved contract.

## Tech Stack

- **Frontend**: React 19 + Vite + Tailwind CSS
- **Backend**: Spring Boot 3.2 + Java 17 + JWT security
- **AI Service**: Python 3.11 + Flask + request sanitization
- **Database**: PostgreSQL 15 + Flyway migrations
- **Cache**: Redis 7
- **DevOps**: Docker Compose for full stack orchestration

## Demo Day Notes
- This card is designed for print.
- Print 2 copies for Demo Day.
- Use the `ai_developer_2` branch for all current work.
