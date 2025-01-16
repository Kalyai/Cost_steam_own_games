from rest_framework import serializers
from .models import SteamUser

class SteamUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SteamUser
        fields = '__all__'
