from django.db import models

class Recipient(models.Model):
    """Модель для хранения информации о клиентах"""
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = 'Получатель'
        verbose_name_plural = 'Получатели'

    def __str__(self):
        return self.full_name


class Message(models.Model):
    """Модель для хранения сообщений"""
    subject = models.CharField(max_length=255)
    body = models.TextField()

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class Mailing(models.Model):
    """Модель управления рассылками"""
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('started', 'Запущена'),
        ('finished', 'Завершена'),
    ]

    send_time_start = models.DateTimeField(verbose_name="Дата и время начала отправки")
    send_time_end = models.DateTimeField(verbose_name="Дата и время окончания отправки")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='created', verbose_name="Статус")
    message = models.ForeignKey('Message', on_delete=models.CASCADE, verbose_name="Сообщение")
    recipients = models.ManyToManyField('Recipient', verbose_name="Получатели")

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'

    def __str__(self):
        return f"Рассылка: {self.message.subject} ({self.get_status_display()})"

    def update_status(self):
        """Обновляет статус рассылки на основе времени"""
        current_time = now()
        if self.status == 'created' and current_time >= self.send_time_start:
            self.status = 'started'
        if self.status == 'started' and current_time >= self.send_time_end:
            self.status = 'finished'
        self.save()


class MailingAttempt(models.Model):
    """Модель для попыток рассылки"""

    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    mailing = models.ForeignKey(Mailing, on_delete=models.CASCADE, related_name='attempts', verbose_name="Рассылка")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время попытки")
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, verbose_name="Статус")
    server_response = models.TextField(verbose_name="Ответ почтового сервера")

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f"Попытка для рассылки '{self.mailing}' - {self.get_status_display()} в {self.timestamp:%Y-%m-%d %H:%M:%S}"
