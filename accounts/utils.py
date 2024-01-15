from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator


def detect_user(user):
    if user.role == 2:
        redirect_url = 'client-dashboard'
        return redirect_url
    elif user.role == 1:
        redirect_url = 'restaurant-dashboard'
        return redirect_url
    # elif user.role == "UNKNOWN" and user.is_superuser:
    else:
        if user.is_superuser:
            redirect_url = '/admin'
            return redirect_url


def send_verification_email(request, user):
    from_email = settings.DEFAULT_EMAIL
    mail_subject = 'Verify your email address'
    current_site = get_current_site(request)
    message = render_to_string('accounts/emails/accounts_email_verification.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    to_email = user.email
    mail = EmailMessage(mail_subject, message, from_email, to=[to_email])
    mail.send()
