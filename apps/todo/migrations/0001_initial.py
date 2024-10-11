# Generated by Django 5.1.1 on 2024-10-10 22:48

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import apps.todo.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskOrm",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            (apps.todo.models.StatusEnum["PENDING"], apps.todo.models.StatusEnum["PENDING"]),
                            (apps.todo.models.StatusEnum["IN_PROGRESS"], apps.todo.models.StatusEnum["IN_PROGRESS"]),
                            (apps.todo.models.StatusEnum["COMPLETED"], apps.todo.models.StatusEnum["COMPLETED"]),
                        ],
                        default=apps.todo.models.StatusEnum["PENDING"],
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[
                            (apps.todo.models.PriorityEnum["LOW"], apps.todo.models.PriorityEnum["LOW"]),
                            (apps.todo.models.PriorityEnum["MEDIUM"], apps.todo.models.PriorityEnum["MEDIUM"]),
                            (apps.todo.models.PriorityEnum["HIGH"], apps.todo.models.PriorityEnum["HIGH"]),
                        ],
                        default=apps.todo.models.PriorityEnum["LOW"],
                    ),
                ),
                ("duration_in_days", models.IntegerField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("completed_at", models.DateTimeField(blank=True, null=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "db_table": "tasks",
            },
        ),
    ]
