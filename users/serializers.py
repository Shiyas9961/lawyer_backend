from rest_framework import serializers
from .models import UserModel

class UserModelsSerializer(serializers.ModelSerializer) :

    class Meta :
        model = UserModel
        fields = "__all__"