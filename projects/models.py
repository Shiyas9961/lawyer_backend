from django.db import models
from tenants.models import TenantModel
# Create your models here.
class ProjectModel (models.Model) :

    project_name = models.CharField(null=True, max_length=200)
    tenand = models.ForeignKey(TenantModel, on_delete=models.SET_NULL, null=True)

    def __str__(self) :
        return self.project_name