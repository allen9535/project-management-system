from rest_framework import serializers

from django.contrib.auth.password_validation import validate_password

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

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        # 계정명이 5자 미만 20자 초과이거나
        # 이미 존재하는 계정명일 경우
        if (len(username) < 5) or (len(username) > 20) or (User.objects.filter(username=username).exists()):
            # ValidationError 발생
            raise serializers.ValidationError()

        # 비밀번호가 5자 미만 20자 초과인 경우
        if (len(password) < 5) or (len(password) > 20):
            # ValidationError 발생
            raise serializers.ValidationError()

        # validate_password의 경우, 유효한 비밀번호이면 None을 반환하고
        # 아니면 ValidationError를 발생시킴
        validate_password(password)

        return attrs
