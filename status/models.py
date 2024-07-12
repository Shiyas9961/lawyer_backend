from django.db import models
import django
import django.utils
import django.utils.timezone
# Create your models here.
class StatusModel(models.Model) :
    
    status_name = models.CharField(max_length=50, null=True)

    def __str__(self) :
        return self.status_name