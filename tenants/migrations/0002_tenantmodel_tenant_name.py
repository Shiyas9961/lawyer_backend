# Generated by Django 4.2.13 on 2024-05-22 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tenantmodel',
            name='tenant_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
