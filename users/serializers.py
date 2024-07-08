from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}  # поле password доступно только для записи

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)     # Извлечение пароля из валидированных данных, если он есть
        instance = super().update(instance, validated_data)     # Обновление остальных полей через метод update родительского класса
        if password:
            instance.set_password(password)     # Установка хешированного пароля
            instance.save()
            return instance


class UserSoftDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)
        extra_kwargs = {'is_active': {'read_only': True}}

