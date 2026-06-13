import requests

url = "https://ghrce-timetable.onrender.com/api/auth/login"
payload = {
    "email": "admin@ghrce.edu",
    "password": "admin123"
}
try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
