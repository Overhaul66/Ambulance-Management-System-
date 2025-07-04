@echo off
curl -X POST http://localhost:8000/users/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"testuser@example.com\", \"password\": \"strongpass123\", \"first_name\": \"Test\", \"last_name\": \"User\", \"age\": 25, \"role\": \"Individual\"}"
pause
