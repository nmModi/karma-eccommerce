from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task


@shared_task
def send_spam_email(user_email):
    send_mail(
        'Вы подписались на рассылку',
        'Мы будем присылать вам много спама',
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
    return None


@shared_task
def send_contact_email(subject, msg, email, to):
    send_mail(subject, msg, email, to, fail_silently=False)
    return None
