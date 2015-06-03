from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from jetka.settings import JETKA_EMAIL

import celery


@celery.task()
def send_email(t):
    try:
        if t['type_message'] == u'html':
            msg = EmailMessage(t['subject'], t['content'], t['email_from'], [t['email_to']])
            msg.content_subtype = t['type_message']
            msg.send()
        else:
            send_mail(t['subject'], t['content'], t['email_from'], [t['email_to']])
    except:
        send_mail(t['subject'], t['content'], t['email_from'], [t['email_to']])