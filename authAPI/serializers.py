from rest_framework import serializers
from .models import User


# class UserProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserProfile
#         fields = (,)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # profile = UserProfileSerializer(required=True)

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

        instance.email = validated_data.get("email", instance.email)
        instance.save()

        return instance
