from rest_framework import serializers
from .models import User  # Importando o modelo de usuário customizado

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}  # Oculta a senha na resposta

    def create(self, validated_data):
        """Garante que a senha seja criptografada antes de salvar o usuário."""
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


