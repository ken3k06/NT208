# CVHT Smart Advisor - Skeleton

Monorepo skeleton theo stack:
- Frontend: Next.js (App Router)
- Backend: FastAPI
- Database: PostgreSQL
- AI: LangChain
- E2E: Playwright

## Cấu trúc

- backend: API, business logic, AI endpoints, risk scoring
- frontend: dashboard UI/UX cơ bản
- playwright: test khói (smoke test)

## Quick start

1) PostgreSQL (Docker)
- `docker compose up -d postgres`

2) Backend
- `cd backend`
- `python -m venv .venv && source .venv/bin/activate`
- `pip install -r requirements.txt`
- `cp .env.example .env`
- `uvicorn app.main:app --reload --port 8000`

3) Frontend
- `cd frontend`
- `npm install`
- `cp .env.example .env.local`
- `npm run dev`

4) Playwright
- `cd playwright`
- `npm install`
- `npx playwright install`
- `npm run test`

## API docs
- Swagger: http://localhost:8000/docs

## Giai đoạn tiếp theo
- Thêm crawler DAA + scheduler định kỳ
- Hoàn thiện schema điểm/tín chỉ/học lại
- Kết nối Text-to-SQL có guardrail
- Dashboard macro/micro + cảnh báo red flags
