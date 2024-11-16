#!/bin/bash

echo "Stopping any processes using ports 3001 and 8000..."

# Kill processes using port 3001 (frontend)
lsof -ti:3001 | xargs kill -9 2>/dev/null || echo "No process on port 3001"

# Kill processes using port 8000 (backend)
lsof -ti:8000 | xargs kill -9 2>/dev/null || echo "No process on port 8000"

# echo "Starting backend server..."
# cd backend
# python app.py &

# echo "Starting frontend server..."
# cd ../frontend
# npm start
