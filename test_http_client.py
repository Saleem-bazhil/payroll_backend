import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
django.setup()

from rest_framework_simplejwt.tokens import RefreshToken
import requests

from django.contrib.auth import get_user_model

u = get_user_model().objects.get(username='payroll')
refresh = RefreshToken.for_user(u)
token = str(refresh.access_token)

print(f"Generated Access Token for user: {u.username}")

url = "http://127.0.0.1:8000/api/leave-requests/"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
payload = {
    "leave_type": "Leave",
    "reason": "Testing from fully external HTTP client",
    "start_date": "2026-05-20",
    "end_date": "2026-05-22"
}

print("Sending Request to:", url)
try:
    response = requests.post(url, json=payload, headers=headers)
    print("STATUS CODE:", response.status_code)
    print("RESPONSE BODY:", response.text)
except Exception as e:
    print("HTTP REQUEST FAILED:", e)
