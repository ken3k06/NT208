#!/bin/bash
set -e

cd "$(dirname "$0")" || exit 1

echo "🚀 Starting CVHT Smart Advisor Stack..."
echo ""
echo "📌 Available commands:"
echo "   ./run.sh backend   - Start FastAPI backend (port 8000)"
echo "   ./run.sh frontend  - Start Next.js frontend (port 3000)"
echo "   ./run.sh db        - Start PostgreSQL container"
echo "   ./run.sh all       - Start backend + frontend"
echo ""

CMD="${1:-all}"

case "$CMD" in
  backend)
    echo "▶️  Starting FastAPI backend..."
    cd backend
    source ../.venv/bin/activate
    uvicorn app.main:app --reload --port 8000
    ;;
  frontend)
    echo "▶️  Starting Next.js frontend..."
    cd frontend
    npm run dev
    ;;
  db)
    echo "▶️  Starting PostgreSQL..."
    docker compose up -d postgres
    echo "✅ PostgreSQL running on localhost:5432"
    ;;
  all)
    echo "▶️  Starting all services in background..."
    cd backend
    source ../.venv/bin/activate
    echo "  📡 Backend on http://localhost:8000"
    uvicorn app.main:app --reload --port 8000 &
    BACKEND_PID=$!
    
    sleep 2
    cd ../frontend
    echo "  🎨 Frontend on http://localhost:3000"
    npm run dev &
    FRONTEND_PID=$!
    
    echo ""
    echo "✅ Stack running!"
    echo "   📡 API docs: http://localhost:8000/docs"
    echo "   🎨 UI: http://localhost:3000"
    echo ""
    echo "Press Ctrl+C to stop"
    
    wait
    ;;
  *)
    echo "❌ Unknown command: $CMD"
    exit 1
    ;;
esac
