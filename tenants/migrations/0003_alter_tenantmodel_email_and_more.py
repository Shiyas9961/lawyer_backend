# Generated by Django 4.2.13 on 2024-05-24 05:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tenants', '0002_tenantmodel_tenant_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tenantmodel',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='tenantmodel',
            name='tenant_name',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
    ]
