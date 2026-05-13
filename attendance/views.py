import math
from django.utils import timezone
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Attendance, LeaveRequest
from .serializer import AttendanceSerializer, LeaveRequestSerializer

def haversine_distance(lat1, lon1, lat2, lon2):
    # approximate radius of earth in km
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c * 1000  # returns distance in meters

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

    @action(detail=False, methods=["post"])
    def check_in(self, request):
        user = request.user
        try:
            employee = user.employee_profile
        except AttributeError:
            return Response({"detail": "Employee profile not found for this user."}, status=400)

        # Fetch dynamically configured work location per user
        allowed_lat = employee.work_lat
        allowed_lon = employee.work_lon

        if allowed_lat is None or allowed_lon is None:
             return Response({"detail": "Allowed location not set for this employee. Please contact HR."}, status=400)

        user_lat = request.data.get("latitude")
        user_lon = request.data.get("longitude")

        if user_lat is None or user_lon is None:
            return Response({"detail": "Latitude and Longitude are required."}, status=400)

        try:
            distance = haversine_distance(float(user_lat), float(user_lon), float(allowed_lat), float(allowed_lon))
        except ValueError:
            return Response({"detail": "Invalid coordinates provided."}, status=400)

        if distance > 50:
            return Response({
                "detail": f"You are too far from the office ({round(distance)}m). Must be within 50m."
            }, status=403)

        # Check if already checked in today
        today = timezone.now().date()
        existing = Attendance.objects.filter(employee=employee, intime__date=today).first()
        
        if existing:
             return Response({"detail": "Already checked in for today."}, status=400)

        # Create record
        attendance = Attendance.objects.create(
            employee=employee,
            employee_name=employee.employee_name,
            role=employee.role,
            department=employee.department,
            salary=employee.salary,
            intime=timezone.now(),
            status="Present"
        )
        serializer = self.get_serializer(attendance)
        return Response(serializer.data, status=201)

    @action(detail=False, methods=["post"])
    def check_out(self, request):
        user = request.user
        try:
            employee = user.employee_profile
        except AttributeError:
            return Response({"detail": "Employee profile not found for this user."}, status=400)

        allowed_lat = employee.work_lat
        allowed_lon = employee.work_lon

        if allowed_lat is None or allowed_lon is None:
             return Response({"detail": "Allowed location not set for this employee. Please contact HR."}, status=400)

        user_lat = request.data.get("latitude")
        user_lon = request.data.get("longitude")

        if user_lat is None or user_lon is None:
            return Response({"detail": "Latitude and Longitude are required."}, status=400)

        try:
            distance = haversine_distance(float(user_lat), float(user_lon), float(allowed_lat), float(allowed_lon))
        except ValueError:
            return Response({"detail": "Invalid coordinates provided."}, status=400)

        if distance > 50:
            return Response({
                "detail": f"You are too far from the office ({round(distance)}m). Must be within 50m to clock out."
            }, status=403)

        today = timezone.now().date()
        existing = Attendance.objects.filter(employee=employee, intime__date=today).first()
        
        if not existing:
             return Response({"detail": "No clock-in found for today. Cannot clock out."}, status=400)

        if existing.outtime:
             return Response({"detail": "Already clocked out for today."}, status=400)

        existing.outtime = timezone.now()
        existing.save()
        serializer = self.get_serializer(existing)
        return Response(serializer.data, status=200)


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

    
