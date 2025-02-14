from rest_framework import serializers
from .models import User, Student
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer  # Importando o modelo de usuário customizado

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    horasComplementares = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'password', 'horasComplementares']
        extra_kwargs = {
            'password': {'write_only': True},
            'horasComplementares': {'required': False}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')

        if "role" not in validated_data:
            validated_data["role"] = "student"

        user = User(**validated_data)
        user.set_password(password)  # Garante que a senha seja criptografada
        user.save()
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            instance.set_password(validated_data.pop('password'))

        if instance.role in ["teacher", "coordinator"]:
            validated_data.pop("horasComplementares", None)

        return super().update(instance, validated_data)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.role != "student":
            representation.pop("horasComplementares", None)
        return representation

class TeacherSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data["role"] = "teacher"  
        user = User(**validated_data)
        user.set_password(validated_data["password"])  
        user.save()
        return user


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ["id", "username", "email", "role", "hours_completed"]

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username_or_email = attrs.get("email")  # O campo enviado pode ser username ou email
        password = attrs.get("password")

        if not username_or_email or not password:
            raise serializers.ValidationError("Email/Username e senha são obrigatórios.")

        # Verifica primeiro se foi enviado um email
        if "@" in username_or_email:
            user = authenticate(username=username_or_email, password=password)
        else:
            # Tenta autenticar pelo username se não for um email
            user = authenticate(username=username_or_email, password=password)

        if not user:
            raise serializers.ValidationError("Credenciais inválidas ou conta inativa.")

        return super().validate(attrs)
    
class DashboardSerializer(serializers.Serializer):
    message = serializers.CharField()




