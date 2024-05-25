from django.db import models
from status.models import StatusModel
from projects.models import ProjectModel
from tenants.models import TenantModel
from users.models import UserModel

# Create your models here.
class TicketModel(models.Model) :

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.ForeignKey(StatusModel, on_delete=models.CASCADE, related_name='status_table')
    project = models.ForeignKey(ProjectModel, on_delete=models.SET_NULL, related_name='project_table', null=True)
    tenant = models.ForeignKey(TenantModel, on_delete=models.CASCADE, related_name='tenant_table')
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='user_table')