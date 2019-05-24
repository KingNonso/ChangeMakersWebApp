from django.conf import settings
from django.core.mail import EmailMessage
from django.template import Context
from django.template.loader import render_to_string

from accounts.models import Member

def send_new_user_welcome_email(email, user, host):
    user = Member.objects.filter(id=user)[0]
    c = {'email': email, 'user': user, 'host':host}

    email_subject = render_to_string(
        'accounts/email/subject.txt', c).replace('\n', '')
    email_body = render_to_string('accounts/email/body.html', c)

    email = EmailMessage(
        email_subject, email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email], [],
        headers={'Reply-To': settings.DEFAULT_FROM_EMAIL}
    )
    email.content_subtype = "html"
    return email.send(fail_silently=False)
