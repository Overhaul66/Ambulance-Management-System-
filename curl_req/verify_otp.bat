@echo off
curl -X POST http://localhost:8000/users/verify-email/ ^
  -H "Content-Type: application/json" ^
  -d "{\"token\": \"369021\"}"
pause
