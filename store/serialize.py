from rest_framework import serializers
from .models import *

class FormSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True)
    gender = serializers.ChoiceField(choices=Gender)
    age = serializers.IntegerField(min_value=18, max_value=65)
    english_lvl = serializers.ChoiceField(choices=English)

    def create(self, validated_data):
        """
        Create and return a new Snippet instance, given the validated data.
        """
        return ModelSerial.objects.create(**validated_data)
