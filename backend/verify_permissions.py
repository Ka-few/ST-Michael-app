import requests
import json

BASE_URL = "http://127.0.0.1:5000"

# 1. Login as Regular User (Stephen)
print("Logging in as regular user...")
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "stephen@example.com", 
    "password": "password123"
})
if resp.status_code != 200:
    print(f"Login failed: {resp.text}")
    exit(1)

user_token = resp.json()["access_token"]
user_headers = {"Authorization": f"Bearer {user_token}"}
print("Regular user logged in.")

# 2. Try to Create Sacrament as Regular User (Should Fail)
print("\nAttempting to create sacrament as regular user (should fail)...")
try:
    resp = requests.post(f"{BASE_URL}/sacraments/", json={
        "type": "Baptism",
        "date": "2025-01-01"
    }, headers=user_headers)
    
    print(f"Response Code: {resp.status_code}") # Expect 405
    if resp.status_code == 405:
        print("SUCCESS: Regular user prevented from using POST /sacraments/")
    elif resp.status_code == 404:
        print("SUCCESS: Route not found (also acceptable)")
    else:
        print(f"FAILURE: Regular user got {resp.status_code}")
except Exception as e:
    print(f"Request failed: {e}")

# 3. Login as Admin
print("\nLogging in as Admin...")
resp = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "admin@chicagostmichael.org", 
    "password": "adminpassword"
})
if resp.status_code != 200:
    print(f"Admin login failed: {resp.text}")
    # Note: If admin login fails, check if admin user exists with these creds. 
    # Adjust credentials if necessary based on seed data.
    exit(1)

admin_token = resp.json()["access_token"]
admin_headers = {"Authorization": f"Bearer {admin_token}"}
print("Admin logged in.")

# 4. Try to Create Sacrament as Admin (Should Succeed)
print("\nAttempting to create sacrament as Admin...")
# Must allow strict slashes? No, we set strict_slashes=False.
resp = requests.post(f"{BASE_URL}/sacraments/admin/add", json={
    "user_id": 3, # Link to Stephen
    "type": "Confirmation",
    "date": "2025-06-01"
}, headers=admin_headers)

print(f"Response Code: {resp.status_code}")
if resp.status_code == 201:
    print("SUCCESS: Admin created sacrament.")
    sacrament_id = resp.json()["sacrament"]["id"]
    
    # Clean up
    print(f"Cleaning up sacrament {sacrament_id}...")
    requests.delete(f"{BASE_URL}/sacraments/admin/{sacrament_id}", headers=admin_headers)
else:
    print(f"FAILURE: Admin failed to create sacrament. Response: {resp.text}")
