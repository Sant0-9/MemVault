#!/bin/bash

echo "🛑 Stopping MemVault Development Servers..."
echo ""

# Stop backend
if [ -f /tmp/memvault-backend.pid ]; then
    BACKEND_PID=$(cat /tmp/memvault-backend.pid)
    echo "   Stopping Backend (PID: $BACKEND_PID)..."
    kill $BACKEND_PID 2>/dev/null
    rm /tmp/memvault-backend.pid
fi

# Stop frontend
if [ -f /tmp/memvault-frontend.pid ]; then
    FRONTEND_PID=$(cat /tmp/memvault-frontend.pid)
    echo "   Stopping Frontend (PID: $FRONTEND_PID)..."
    kill $FRONTEND_PID 2>/dev/null
    rm /tmp/memvault-frontend.pid
fi

# Fallback: kill by process name
pkill -f "uvicorn app.main:app" 2>/dev/null
pkill -f "next dev" 2>/dev/null

echo ""
echo "✅ Servers stopped!"
