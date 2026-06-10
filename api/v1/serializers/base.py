from rest_framework import serializers


class TenantModelSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get("request")
        organization = getattr(request, "organization", None)

        if organization:
            validated_data["organization"] = organization

        return super().create(validated_data)
