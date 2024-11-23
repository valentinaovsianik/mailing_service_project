# Generated by Django 5.1.2 on 2024-10-31 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=200, verbose_name="Заголовок")),
                ("content", models.TextField(verbose_name="Содержимое")),
                ("preview_image", models.ImageField(upload_to="blog_previews/", verbose_name="Изображение")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")),
                ("published", models.BooleanField(default=False, verbose_name="Опубликовать")),
                ("views", models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")),
            ],
            options={
                "verbose_name": "Блоговая запись",
                "verbose_name_plural": "Блоговые записи",
            },
        ),
    ]