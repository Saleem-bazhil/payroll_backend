from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Attendance
from .serializer import AttendanceSerializer

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Attendance.objects.select_related("employee").all().order_by("-id")
        role = "superadmin" if user.is_superuser else user.role
        if role == "employee":
            return queryset.filter(employee__user=user)
        return queryset

    
