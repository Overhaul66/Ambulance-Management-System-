@echo off
curl -X POST http://localhost:8000/users/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\": \"driveradmin@example.com\", \"password\": \"strongpass123\", \"first_name\": \"Driver\", \"last_name\": \"Admin\", \"age\": 35, \"role\": \"DriverAdmin\", \"organization\": {\"org_name\": \"DriverHub New\", \"address\": \"Kumasi\"}}"

pause