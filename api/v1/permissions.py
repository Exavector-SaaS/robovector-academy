from rest_framework.permissions import BasePermission


class IsOrganizationMember(BasePermission):
    def has_permission(self, request, view):
        org = getattr(request, "organization", None)

        if not request.user.is_authenticated or not org:
            return False

        return request.user.memberships.filter(
            organization=org, is_active=True
        ).exists()


class HasRole(BasePermission):
    allowed_roles = []

    def has_permission(self, request, view):
        org = getattr(request, "organization", None)

        if not request.user.is_authenticated or not org:
            return False

        membership = request.user.memberships.filter(
            organization=org, is_active=True
        ).first()

        if not membership:
            return False

        return membership.role in self.allowed_roles
