from rest_framework import serializers
from .models import User, Account, Transaction
from banking_app import services

from django.contrib.auth import get_user_model

from banking_app.constants import TYPE

User = get_user_model()


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone_number = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.UserData(**data)


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user information.
    """

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}
        extra_kwargs = {
            "email": {"required": False},
            "phone_number": {"required": False},
        }

    def update(self, instance, validated_data):
        """
        Update and save the user profile.
        """
        instance.first_name = validated_data.get(
            "first_name", instance.first_name
        )
        instance.last_name = validated_data.get(
            "last_name", instance.last_name
        )
        instance.email = validated_data.get("email", instance.email)
        password = validated_data.get("password")
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = "__all__"
        read_only_fields = ["id", "account_number"]


class TransactionSerializer(serializers.ModelSerializer):
    type = serializers.ChoiceField(choices=TYPE)

    class Meta:
        model = Transaction
        fields = "__all__"
        read_only_fields = ["id", "timestamp", "ip_address", "account"]
