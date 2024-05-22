from django.db import models
import django
import django.utils
import django.utils.timezone
# Create your models here.
class StatusModel(models.Model) :

    todo = "TODO"
    in_progress = "IN PROGRESS"
    review = "REVIEW"
    done = "DONE"

    STATUS_CHOICE = [
        (todo, "Todo"),
        (in_progress, "In Progress"),
        (review, "Review"),
        (done, "Done")
    ]

    status_name = models.CharField(max_length=50, choices=STATUS_CHOICE, default=todo)

    def __str__(self) :
        return self.status_name