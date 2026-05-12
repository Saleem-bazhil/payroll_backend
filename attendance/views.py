from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance, LeaveRequest
from .serializer import AttendanceSerializer, LeaveRequestSerializer

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


class LeaveRequestViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = LeaveRequest.objects.select_related("employee").all().order_by("-applied_on")
        role = "superadmin" if user.is_superuser else user.role
        if role == "employee":
            return queryset.filter(employee__user=user)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        employee = getattr(user, "employee_profile", None)
        if employee:
            serializer.save(employee=employee)
        else:
            serializer.save()

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        user = request.user
        role = "superadmin" if user.is_superuser else user.role
        if role not in ["superadmin", "admin"]:
            return Response({"detail": "Permission denied."}, status=403)
        leave = self.get_object()
        leave.status = "Approved"
        leave.save()
        return Response({"status": "Approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        user = request.user
        role = "superadmin" if user.is_superuser else user.role
        if role not in ["superadmin", "admin"]:
            return Response({"detail": "Permission denied."}, status=403)
        leave = self.get_object()
        leave.status = "Rejected"
        leave.save()
        return Response({"status": "Rejected"})

    
