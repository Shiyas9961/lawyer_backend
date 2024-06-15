from django.db import models
from tenants.models import TenantModel
# Create your models here.
class UserModel (models.Model) :

    user_id = models.CharField(primary_key=True, max_length=50)
    username = models.CharField(max_length=100, null=True)
    phone_no = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True, unique=True)
    tenant = models.ForeignKey(TenantModel, on_delete=models.CASCADE)

    def __str__(self) :
        return self.username