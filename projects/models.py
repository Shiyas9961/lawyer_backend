from django.db import models

# Create your models here.
class ProjectModel (models.Model) :

    project_name = models.CharField(null=True, max_length=200)

    def __str__(self) :
        return self.project_name