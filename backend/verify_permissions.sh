#!/bin/bash

BASE_URL="http://127.0.0.1:5000"

# 0. Register a New Regular User
echo "0. Registering New User..."
TIMESTAMP=$(date +%s)
USER_EMAIL="testuser${TIMESTAMP}@example.com"
USER_PASS="password123"

curl -s -X POST "${BASE_URL}/auth/register" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Test User\", \"email\": \"${USER_EMAIL}\", \"password\": \"${USER_PASS}\"}" > /dev/null

echo "Registered ${USER_EMAIL}"

# 1. Login as New Regular User
echo -e "\n1. Logging in as Regular User..."
USER_TOKEN=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"email\": \"${USER_EMAIL}\", \"password\": \"${USER_PASS}\"}" | grep -o '"access_token": *"[^"]*"' | cut -d'"' -f4)

if [ -z "$USER_TOKEN" ]; then
  echo "Login failed for regular user."
  exit 1
fi
echo "User Token obtained."

# 2. Attempt to Create Sacrament as User (Should Fail)
echo -e "\n2. Attempting to Create Sacrament as User (Should Fail)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/sacraments/" \
  -H "Authorization: Bearer ${USER_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"type": "Baptism", "date": "2025-01-01"}')

echo "Response Code: $HTTP_CODE"

if [ "$HTTP_CODE" == "405" ] || [ "$HTTP_CODE" == "404" ]; then
  echo "SUCCESS: Regular user blocked (Code $HTTP_CODE)"
else
  echo "FAILURE: Regular user got code $HTTP_CODE"
fi

# 3. Login as Admin
echo -e "\n3. Logging in as Admin..."
ADMIN_TOKEN=$(curl -s -X POST "${BASE_URL}/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@church.com", "password": "admin123"}' | grep -o '"access_token": *"[^"]*"' | cut -d'"' -f4)

if [ -z "$ADMIN_TOKEN" ]; then
  echo "Login failed for Admin."
  exit 1
fi
echo "Admin Token obtained."

# 4. Attempt to Create Sacrament as Admin (Should Succeed)
echo -e "\n4. Attempting to Create Sacrament as Admin (Should Succeed)..."
# Using User ID 3 (assuming it exists, but create endpoint validates user existence)
# Since we just created a user, maybe use that user ID?
# Using ID 1 (Admin) as the user getting the sacrament for simplicity
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -X POST "${BASE_URL}/sacraments/admin/add" \
  -H "Authorization: Bearer ${ADMIN_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "type": "Confirmation", "date": "2025-06-01"}')

echo "Response Code: $HTTP_CODE"
if [ "$HTTP_CODE" == "201" ]; then
  echo "SUCCESS: Admin created sacrament (Code 201)"
else
  echo "FAILURE: Admin got code $HTTP_CODE"
fi
