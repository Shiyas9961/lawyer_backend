from django.db import models
# Create your models here.
class TenantModel(models.Model) :

    phone_no = models.CharField(max_length=10, null=True)
    email = models.EmailField(null=True)

    def __str__(self) -> str:
        return self.email