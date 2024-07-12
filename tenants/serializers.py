from rest_framework import serializers
from .models import TenantModel

class TenantSerializer (serializers.ModelSerializer) :

    class Meta :
        model = TenantModel
        fields = '__all__'