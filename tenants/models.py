from django.db import models
# Create your models here.
class TenantModel(models.Model) :

    tenant_name = models.CharField(max_length=100, null=True, unique=True)
    phone_no = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True, unique=True)

    def __str__(self) -> str:
        return self.email