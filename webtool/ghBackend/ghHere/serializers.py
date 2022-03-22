from rest_framework import serializers

from .models import GHRequest

class GHRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = GHRequest
        read_only_fields = ("code", "stl_result", "txt_input", "updated_at", )
        fields = '__all__'

