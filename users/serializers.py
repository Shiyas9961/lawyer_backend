from rest_framework import serializers
from .models import UserModel

class UserModelsSerializer(serializers.ModelSerializer) :

    class Meta :
        model = UserModel
        fields = "__all__"

class UserRegisterSerializer(serializers.Serializer) :

    username = serializers.CharField(required = True, max_length = 100)
    password = serializers.CharField(required = True, max_length = 100)
    email = serializers.EmailField(required = True)
    phone_no = serializers.CharField(max_length = 13, required = True)
    role = serializers.CharField(max_length = 50)
    tenand_id = serializers.CharField(required = True)

