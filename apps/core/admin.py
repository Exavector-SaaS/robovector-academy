from django.contrib import admin


class TenantAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        org = getattr(request, "organization", None)
        if not org:
            return qs.none()

        return qs.filter(organization=org)

    def save_model(self, request, obj, form, change):
        org = getattr(request, "organization", None)

        if not obj.organization_id:
            obj.organization = org

        obj.save()

    def has_module_permission(self, request):
        if request.user.is_superuser:
            return True

        return hasattr(request, "organization") and request.organization is not None
