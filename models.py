# - * - coding: utf-8 - * -
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe
from django.core.exceptions import ValidationError


import re


def normalize_string(s):
    """
    Удаление лишних символов и приведение к верхнему регистру.
    """
    return re.sub(r'\W+', '', s.replace('-', '_')).lower()


def validate_str(value):
    if re.sub(r'\W+', '', value) == '':
        raise ValidationError(_(u'Может содержать только латинские символы, цифры, символ "-" будет заменен на "_"'))


class Event(models.Model):
    status = models.BooleanField(verbose_name=_(u'Активно'))
    event_name = models.CharField(max_length=100, unique=True, help_text=_(u'Уникальный текстовый идентификатор события.'), verbose_name=_(u'Тип почтового события'))
    name = models.CharField(max_length=256, verbose_name=_(u'Название'))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_(u'Описание'))
    
    def __unicode__(self):
        return u'[ %s ] == %s' % (self.event_name, self.name)
    
    def related_label(self):
        return self.__unicode__
    
    def save(self, *args, **kwargs):
        self.event_name = normalize_string(self.event_name)
        super(Event, self).save(*args, **kwargs)
        return self
    
    class Meta:
        verbose_name = _(u'Тип почтового события')
        verbose_name_plural = _(u'Типы почтовых событий')


class TemplateVarsManager(models.Manager):
    
    def get_query_set(self):
        res = {}
        for item in super(TemplateVarsManager, self).get_query_set().filter(status=True).values('var_name', 'content', ):
            res.update({item['var_name']:item['content']})
        return res


class TemplateVars(models.Model):
    date_of_create = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_(u'Дата создания'))
    date_of_change = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name=_(u'Дата изменения'))
    status = models.BooleanField(verbose_name=_(u'Активно'))
    var_name = models.CharField(max_length=100, unique=True, validators=[validate_str], verbose_name=_(u'Название переменной'), help_text=_(u'Уникальный текстовый идентификатор переменной.'))
    description = models.CharField(max_length=256, verbose_name=_(u'Описание'), help_text=_(u'Краткое описание содержимого переменной.'))
    content = models.TextField(verbose_name=_(u'Контент'))
    objects = models.Manager()
    template_vardict = TemplateVarsManager()
    
    def __unicode__(self):
        return u'{{ %s }} :: %s' % (self.var_name, self.description)
    
    def save(self, *args, **kwargs):
        self.var_name = normalize_string(self.var_name)
        super(TemplateVars, self).save(*args, **kwargs)
        return self
    
    class Meta:
        verbose_name = _(u'Шаблонная переменная')
        verbose_name_plural = _(u'Шаблонные переменные')


class TemplateManager(models.Manager):
    
    def get_query_set(self):
        return super(TemplateManager, self).get_query_set().filter(status=True, email_event__status=True) \
            .values(
                'delay_day',
                'delay_hour',
                'delay_minute',
                'email_to',
                'email_from',
                'subject',
                'type_message',
                'content',
            )


class Template(models.Model):
    date_of_create = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=_(u'Дата создания'))
    date_of_change = models.DateTimeField(auto_now=True, auto_now_add=True, verbose_name=_(u'Дата изменения'))
    status = models.BooleanField(verbose_name=_(u'Активно'))
    delay_day = models.IntegerField(default=0, verbose_name=_(u'Дни'))
    delay_hour = models.IntegerField(default=0, verbose_name=_(u'Часы'))
    delay_minute = models.IntegerField(default=0, verbose_name=_(u'Минуты'))
    email_event = models.ForeignKey(Event, verbose_name=_(u'Тип почтового события'), related_name='templates')
    email_to = models.CharField(max_length=256, verbose_name=_(u'Кому'), help_text=mark_safe(_(u"Имя переменной <strong>email_to</strong>")), blank=True, null=True)
    email_from = models.CharField(max_length=256, verbose_name=_(u'От кого'), help_text=mark_safe(_(u"Имя переменной <strong>email_from</strong>")), blank=True, null=True)
    subject = models.CharField(max_length=256, verbose_name=_(u'Тема'), help_text=mark_safe(_(u"Имя переменной <strong>subject</strong>")), blank=True, null=True)
    type_message = models.CharField(max_length=4, choices=(('html', 'HTML'), ('text', 'TEXT')), default='html', verbose_name=_(u'Тип сообщения'))
    content = models.TextField(verbose_name=_(u'Контент'))
    objects = models.Manager()
    template_fieldsdict = TemplateManager()
    
    
    def __unicode__(self):
        return u'%s' % _(u'Почтовый шаблон')
    
    class Meta:
        verbose_name = _(u'Почтовый шаблон')
        verbose_name_plural = _(u'Почтовые шаблоны')

