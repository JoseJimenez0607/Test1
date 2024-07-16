from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id= serializers.ReadOnlyField()
    first_name= serializers.CharField()
    last_name= serializers.CharField()
    username= serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()

    def create(self, data):
        user = User()
        user.first_name = data.get('first_name')
        user.last_name = data.get('last_name')
        user.username = data.get('username')
        user.email = data.get('email')
        user.set_password(data.get('password'))
        user.save()
        return user
    

    def validate_username(self, data):
        users = User.objects.filter(username = data)
        if len(users)!=0:
            raise serializers.ValidationError("El usuario ya existe, ingrese otro usuario")
        else:
            return data
