# Day 17 — Fresh Seeded State Verification

## Goal
Reset the Docker environment to a clean state, ensure Flyway seeds sample contract records, and confirm the core scenarios are visible.

## Command
Run from the project root:
```powershell
docker compose down -v
docker compose up --build
```

## Fresh seeded state behavior
- PostgreSQL is recreated and cleared by `docker compose down -v`.
- Flyway migrations run automatically on backend startup.
- The new migration file `backend/src/main/resources/db/migration/V3__seed_data.sql` inserts sample contract rows.
- After startup, the `/api/contracts` endpoint should return visible records for:
  - Widget Supply Agreement
  - Service Level Agreement
  - NDA for Partnership
  - Lease Contract
  - Consulting Agreement

## Confirmed scenarios
- Fresh startup with seeded records available.
- Paginated `GET /api/contracts?page=0&size=10` returns sample contracts.
- Contract details are visible and accessible from the backend.
- Any frontend or API record listing scenario should show rows from the seeded dataset.

## Notes
This update supports Day 17 by making Docker resets deterministic and ensuring a repeatable seeded state for demos and validations.
