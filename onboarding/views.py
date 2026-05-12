from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Onboarding
from .serializers import OnboardingSerializer

class OnboardingViewSet(viewsets.ModelViewSet):
    queryset = Onboarding.objects.all().order_by('-created_at')
    serializer_class = OnboardingSerializer
    permission_classes = [IsAuthenticated]
