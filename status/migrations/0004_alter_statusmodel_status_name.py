# Generated by Django 4.2.13 on 2024-05-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('status', '0003_remove_statusmodel_created_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusmodel',
            name='status_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]