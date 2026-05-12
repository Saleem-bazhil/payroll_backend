import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payroll.settings')
django.setup()

from django.contrib.auth import get_user_model
from attendance.serializer import LeaveRequestSerializer
from rest_framework.test import APIRequestFactory

factory = APIRequestFactory()
u = get_user_model().objects.get(username='payroll')
request = factory.post('/api/attendance/leave-requests/')
request.user = u

data = {'leave_type': 'Permission', 'reason': 'Test permission', 'start_date': '2026-05-13', 'start_time': '14:00', 'end_time': '15:00'}
ser = LeaveRequestSerializer(data=data, context={'request': request})
print('Is Valid:', ser.is_valid())
if not ser.is_valid():
    print('Errors:', ser.errors)
else:
    try:
        ser.save()
        print('SAVE SUCCESSFUL!')
    except Exception as e:
        print('SAVE FAILED WITH EXCEPTION:', type(e).__name__, str(e))
