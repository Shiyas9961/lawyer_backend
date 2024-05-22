# Generated by Django 4.2.13 on 2024-05-22 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='StatusModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(choices=[('TODO', 'Todo'), ('IN PROGRESS', 'In Progress'), ('REVIEW', 'Review'), ('DONE', 'Done')], default='TODO', max_length=50)),
            ],
        ),
    ]