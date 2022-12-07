from rest_framework import serializers
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "email", "password", "timezone_Shift")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        instance.timezone_Shift = validated_data.get(
            "timezone_Shift", instance.timezone_Shift
        )
        instance.email = validated_data.get("email", instance.email)
        instance.save()

        return instance
