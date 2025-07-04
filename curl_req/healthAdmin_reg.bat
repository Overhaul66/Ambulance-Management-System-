@echo off
curl -X POST http://localhost:8000/users/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"healthadmin@example.com\", \"password\": \"strongpass123\", \"first_name\": \"Health\", \"last_name\": \"Admin\", \"age\": 40, \"role\": \"HealthAdmin\", \"organization\": {\"org_name\": \"HealthServe New\", \"address\": \"Accra\"}}"
pause