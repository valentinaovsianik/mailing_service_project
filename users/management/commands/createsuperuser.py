from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = 'Создать суперпользователя без username'

    def handle(self, *args, **kwargs):
        email = input("Введите email: ")
        password = input("Введите пароль: ")
        if User.objects.filter(email=email).exists():
            self.stdout.write("Суперпользователь с таким email уже существует.")
        else:
            User.objects.create_superuser(email=email, password=password)
            self.stdout.write(f"Суперпользователь {email} создан.")
