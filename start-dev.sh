#!/bin/bash

echo "🚀 Starting MemVault Development Servers..."
echo ""

# Start backend in background
echo "📦 Starting Backend on http://localhost:8000..."
cd packages/backend
python3 -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload > /tmp/memvault-backend.log 2>&1 &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Wait a bit for backend to start
sleep 2

# Start frontend in background
echo "🎨 Starting Frontend on http://localhost:3000..."
cd ../frontend
npm run dev > /tmp/memvault-frontend.log 2>&1 &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "✅ Both servers starting..."
echo ""
echo "📍 Access your app:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000/api/v1/docs"
echo ""
echo "📝 View logs:"
echo "   Backend:  tail -f /tmp/memvault-backend.log"
echo "   Frontend: tail -f /tmp/memvault-frontend.log"
echo ""
echo "🛑 To stop: pkill -f 'uvicorn' && pkill -f 'next dev'"
echo ""

# Save PIDs for easy stopping
echo "$BACKEND_PID" > /tmp/memvault-backend.pid
echo "$FRONTEND_PID" > /tmp/memvault-frontend.pid
