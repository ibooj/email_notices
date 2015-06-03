# - * - coding: utf-8 - * -
from django.template import Context, loader
from django.utils.timezone import timedelta, now

from email_notices.models import Template, TemplateVars 
from email_notices.tasks import send_email
from django.core.mail import send_mail
from jetka.settings import JETKA_EMAIL
import re


def event(event_name=None, vardict={}):
    '''
        vardict={'email_to': '', 'email_from': '', 'subject': '', }
    '''
    template_vardict = TemplateVars.template_vardict.all()
    template_vardict.update(vardict)
    for t in Template.template_fieldsdict.filter(email_event__event_name=event_name):
        t.update({'content': loader.get_template_from_string(t['content']).render(Context(template_vardict))})
        for vd in vardict:
            repl = True
            if vd == 'email_from':
                try:
                    if t[vd].find('@') > 0:
                        repl = False
                except:
                    pass
            if repl:
                t.update({vd: vardict[vd], })
        send_email.apply_async(
            args=[t],
            eta=now() + timedelta(days=t['delay_day'], hours=t['delay_hour'], minutes=t['delay_minute'])
        )
