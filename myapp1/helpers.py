from django.core.mail import send_mail
from django.conf import settings


def send_forget_password_mail(email, token, current_url):
    subject = 'Your forget password link'
    message = f'Hi , click on the link to reset your password {current_url}/change_password/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True
