# Generated by Django 5.1.2 on 2024-10-29 19:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Message",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("subject", models.CharField(max_length=255)),
                ("body", models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name="Recipient",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("full_name", models.CharField(max_length=100)),
                ("comment", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Mailing",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("send_time_start", models.DateTimeField()),
                ("send_time_end", models.DateTimeField()),
                (
                    "status",
                    models.CharField(
                        choices=[("created", "Создана"), ("started", "Запущена"), ("finished", "Завершена")],
                        default="created",
                        max_length=10,
                    ),
                ),
                ("message", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="mailing.message")),
                ("recipients", models.ManyToManyField(to="mailing.recipient")),
            ],
        ),
    ]