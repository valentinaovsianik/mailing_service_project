from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Recipient, Message, Mailing, MailingAttempt
from django.core.mail import send_mail



class AboutView(TemplateView):
    template_name = 'mailing/about.html'


class ContactsView(TemplateView):
    template_name = 'mailing/contacts.html'


# Представления для модели Recipient
class RecipientListView(ListView):
    model = Recipient
    template_name = 'mailing/recipient_list.html'
    context_object_name = 'recipients'

class RecipientDetailView(DetailView):
    model = Recipient
    template_name = 'mailing/recipient_detail.html'
    context_object_name = 'recipient'

class RecipientCreateView(CreateView):
    model = Recipient
    template_name = 'mailing/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:recipient_list')

class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'mailing/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('mailing:recipient_list')

class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailing/recipient_confirm_delete.html'
    success_url = reverse_lazy('mailing:recipient_list')

# Представления для модели Message
class MessageListView(ListView):
    model = Message
    template_name = 'mailing/message_list.html'
    context_object_name = 'messages'

class MessageDetailView(DetailView):
    model = Message
    template_name = 'mailing/message_detail.html'
    context_object_name = 'message'

class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailing/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailing:message_list')

class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailing/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('mailing:message_list')

class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailing/message_confirm_delete.html'
    success_url = reverse_lazy('mailing:message_list')

# Представления для модели Mailing
class MailingListView(ListView):
    model = Mailing
    template_name = 'mailing/mailing_list.html'
    context_object_name = 'mailings'

class MailingDetailView(DetailView):
    model = Mailing
    template_name = 'mailing/mailing_detail.html'
    context_object_name = 'mailing'

class MailingCreateView(CreateView):
    model = Mailing
    fields = ['send_time_start', 'send_time_end', 'status', 'message', 'recipients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

class MailingUpdateView(UpdateView):
    model = Mailing
    fields = ['send_time_start', 'send_time_end', 'status', 'message', 'recipients']
    template_name = 'mailing/mailing_form.html'
    success_url = reverse_lazy('mailing:mailing_list')

class MailingDeleteView(DeleteView):
    model = Mailing
    template_name = 'mailing/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing:mailing_list')


def send_mailing(request, pk):
    """Отправка рассылки вручную"""
    mailing = get_object_or_404(Mailing, pk=pk)
    recipients = mailing.recipients.all()

    for recipient in recipients:
        try:
            send_mail(
                subject=mailing.message.subject,
                message=mailing.message.content,
                from_email='from@example.com',
                recipient_list=[recipient.email],
            )
            MailingAttempt.objects.create(
                mailing=mailing,
                status='success',
                server_response="Сообщение отправлено успешно"
            )
        except Exception as e:
            MailingAttempt.objects.create(
                mailing=mailing,
                status='failed',
                server_response=str(e)
            )

    mailing.update_status()
    return render(request, 'mailing/send_confirmation.html', {'mailing': mailing})



def index(request):
    # Подсчёт количества всех рассылок
    total_mailings = Mailing.objects.count()

    # Подсчёт количества активных рассылок (со статусом 'Запущена')
    active_mailings = Mailing.objects.filter(status='started').count()

    # Подсчёт количества уникальных получателей
    unique_recipients = Recipient.objects.distinct().count()

    context = {
        'total_mailings': total_mailings,
        'active_mailings': active_mailings,
        'unique_recipients': unique_recipients,
    }
    return render(request, 'mailing/index.html', context)