@echo off
curl -X POST http://localhost:8000/users/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"testuser@example.com\", \"password\": \"strongpass123\"}"
pause
