from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.pop('password')

        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError()

        return User.objects.create_user(**validated_data, password=password)
