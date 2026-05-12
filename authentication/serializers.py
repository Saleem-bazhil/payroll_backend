from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RoleTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["role"] = "superadmin" if user.is_superuser else user.role
        employee_profile = getattr(user, "employee_profile", None)
        token["employee_id"] = employee_profile.id if employee_profile else None
        return token
