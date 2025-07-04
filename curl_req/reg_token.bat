@echo off
curl -X POST http://localhost:8000/users/request-otp/ ^
  -H "Content-Type: application/json" ^
  -d "{\"username\": \"admin@example.com\"}"
pause
