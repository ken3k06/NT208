# Progress Log - March 1, 2026

## ✅ Hoàn thành hôm nay

### 1. **Project Structure Setup**
- Tạo monorepo skeleton: `backend/`, `frontend/`, `playwright/`
- Config files: `.gitignore`, `docker-compose.yml`, `README.md`
- Run script: `run.sh` để start services nhanh

### 2. **Backend (FastAPI)**
#### Database
- ✅ Models: `User`, `Student`, `Score` với SQLAlchemy ORM
- ✅ Schema support: SQLite (demo mode, không cần Docker)
- ✅ CSV import script: `app/scripts/import_csv.py`
- ✅ Seed data: 12 sinh viên, 36 điểm qua 2 học kỳ

#### Authentication
- ✅ JWT authentication với `python-jose`
- ✅ Password hashing: PBKDF2-SHA256
- ✅ RBAC: `ADMIN` (Dean) và `ADVISOR` (CVHT)
- ✅ Endpoints:
  - `POST /api/v1/auth/login` - Đăng nhập
  - `GET /api/v1/auth/me` - Lấy user hiện tại
  - `POST /api/v1/auth/seed-users` - Seed demo users

#### API Endpoints
- ✅ `GET /api/v1/students/?class_code=ATTT2023.1` - Lấy danh sách sinh viên (có filter)
- ✅ `GET /api/v1/dashboard/macro` - KPI Dean (mock data)
- ✅ `GET /api/v1/dashboard/micro` - Red flags Advisor (mock data)
- ✅ `POST /api/v1/chat/query` - AI chat query (skeleton)

#### Services
- ✅ `services/security.py`: JWT + password hashing
- ✅ `services/risk.py`: Risk scoring algorithm (heuristic)
- ✅ `services/ai_sql.py`: LangChain chat (basic)

### 3. **Frontend (Next.js)**
- ✅ App Router structure
- ✅ Global CSS: Dark theme professional
- ✅ Components:
  - `StatCard` - KPI cards
  - `api.ts` - API client helper
- ✅ Pages:
  - `/` - Landing page
  - `/dashboard` - Dean dashboard với 3 KPIs

### 4. **Dependencies Installed**
**Backend Python:**
- fastapi, uvicorn, sqlalchemy, psycopg2-binary
- pydantic-settings, python-dotenv
- langchain, langchain-openai, langchain-community
- python-jose[cryptography], passlib[bcrypt]
- apscheduler, httpx

**Frontend Node:**
- next, react, react-dom
- recharts, lucide-react
- typescript, eslint

**Testing:**
- playwright (installed browsers)

### 5. **Demo Users Created**
```
admin@uit.edu.vn / admin123 (ADMIN role)
advisor1@uit.edu.vn / advisor123 (ADVISOR role)
```

### 6. **Running Services**
- Backend: `http://localhost:8000` ✅
- Frontend: `http://localhost:3000` ✅
- API Docs: `http://localhost:8000/docs`

---

## 📝 Files Created Today

### Backend (26 files)
```
backend/
├── .env (SQLite demo mode)
├── .env.example
├── requirements.txt
├── data/
│   ├── students.csv (12 records)
│   └── scores.csv (36 records)
└── app/
    ├── main.py
    ├── core/
    │   └── config.py (JWT settings added)
    ├── db/
    │   ├── base.py
    │   └── session.py
    ├── models/
    │   ├── user.py (NEW)
    │   ├── student.py
    │   └── score.py
    ├── schemas/
    │   ├── auth.py (NEW)
    │   ├── student.py
    │   └── chat.py
    ├── api/v1/
    │   ├── deps.py (NEW - auth dependency)
    │   ├── router.py (added auth router)
    │   └── endpoints/
    │       ├── auth.py (NEW)
    │       ├── students.py (updated: DB query)
    │       ├── dashboard.py
    │       ├── chat.py
    │       └── health.py
    ├── services/
    │   ├── security.py (NEW - JWT/password)
    │   ├── risk.py
    │   └── ai_sql.py
    └── scripts/
        └── import_csv.py (NEW)
```

### Frontend (9 files)
```
frontend/
├── .env.example
├── package.json
├── tsconfig.json
├── next.config.ts
├── eslint.config.mjs
├── app/
│   ├── globals.css
│   ├── layout.tsx
│   ├── page.tsx
│   └── dashboard/
│       └── page.tsx
├── components/
│   └── stat-card.tsx
└── lib/
    └── api.ts
```

### Root (4 files)
```
.gitignore
README.md
docker-compose.yml
run.sh (executable)
```

---

## 🎯 Next Steps (Seminar 1 Prep)

### Ưu tiên cao (tuần tới)
1. **Dashboard UI nối API thật**
   - Thay mock data bằng API calls
   - Hiển thị student list từ DB
   - Chart phân phối điểm (Recharts)

2. **Login Screen**
   - Form đăng nhập
   - JWT storage (localStorage)
   - Protected routes

3. **Red Flags Logic**
   - Query DB tính GPA giảm
   - Highlight sinh viên rủi ro cao

4. **Use Case Documentation**
   - Admin personas
   - Advisor personas
   - System Architecture diagram

### Trung bình (trước demo)
5. **Advising Logs CRUD**
6. **Risk Matrix visualization**
7. **Text-to-SQL basic (guardrail mode)**

### Thấp (sau Seminar 1)
8. **DAA Crawler prototype**
9. **Cronjob scheduler**
10. **Advanced AI features**

---

## 📊 Database Status

**Tables created:**
- `users` (2 records)
- `students` (12 records)  
- `scores` (36 records)

**Sample data:**
- 3 classes: ATTT2023.1, ATTT2023.2, MMTT2023.1
- 2 semesters: 2023-1, 2023-2
- Courses: NT101, MA101, NT208

---

## 🔧 Tech Stack Confirmed

| Layer | Technology |
|-------|-----------|
| Frontend | Next.js 15 (App Router) + TypeScript |
| Backend | FastAPI + Python 3.14 |
| Database | SQLite (demo) → PostgreSQL (production) |
| Auth | JWT + PBAC |
| AI | LangChain + OpenAI |
| Testing | Playwright |
| Deployment | (TBD) |

---

## 💡 Notes

- **SQLite demo mode**: Không cần Docker permissions, chạy local ngay
- **JWT secret**: Hardcoded trong config (development only)
- **Pydantic warning**: Python 3.14 compatibility issue với LangChain, không ảnh hưởng runtime
- **Port conflicts**: Đã xử lý auto-kill process cũ

---

**Thời gian hoàn thành**: ~3 giờ  
**Trạng thái**: ✅ MVP skeleton ready, có data mẫu, auth working, API functional
