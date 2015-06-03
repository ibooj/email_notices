# - * - coding: utf-8 - * -
from django.utils.translation import ugettext_lazy as _
from django.contrib import admin
from django.utils.safestring import mark_safe
from django import forms


from email_notices.models import Event, Template, TemplateVars


class EventAdmin(admin.ModelAdmin):
    list_display = ('event_name', 'status', 'name', 'template_count', )
    search_fields = ('event_name', 'name',)
    
    def template_count(self, obj):
        return obj.templates.count()
    template_count.short_description = _(u'Количество шаблонов')
    
    
class TemplateAdminForm(forms.ModelForm):
    
    def set_message_help_text(self):
        output = [u'<div class="message_help_text">']
        output.append(u'<label class="required">%s</label>' % _(u'Доступные переменные drag&drop:'))
        output.append(u'<ul>')
        for item in TemplateVars.objects.filter(status=True):
            output.append(u'<li><strong>{{ %s|safe }}</strong> :: <a href="/admin/email_notices/templatevars/%s/">%s</a></li>' % (item.var_name, item.id, item.description))
        output.append(u'</ul><br />')
        output.append(u'</div>')
        return mark_safe(u'\n'.join(output))
    
    def __init__(self, data=None, *args, **kwargs):
        super(TemplateAdminForm, self).__init__(data, *args, **kwargs)
        self.fields['content'].help_text = self.set_message_help_text()
        
    class Meta:
        model = Template


class TemplateAdmin(admin.ModelAdmin):
    form = TemplateAdminForm
    list_display = ('date_of_change', 'email_to', 'email_from', 'subject', 'type_message', 'delay_day', 'delay_hour', 'delay_minute', 'status', 'email_event')
    list_filter = ('email_event',)
    ordering = ('-delay_day', '-delay_hour', '-delay_minute', )
    fieldsets = (
        (_(u'Отложить оправку - (если все поля содержат 0 то отправка произойдет сразу)'), {
                'classes': ('grp-collapse grp-closed',),
                'fields': ('delay_day', 'delay_hour', 'delay_minute', )
            }
        ),
        (_(u'Заголовки шаблона'), {
                'classes': ('grp-collapse grp-closed',),
                'fields': ('email_to', 'email_from', 'subject', )
            }
        ),
        ('', {
                'fields': ('status', 'email_event', 'type_message', 'content', )
            }
        ),
    )
    
    class Media:
        js = ('email_notices/js/admin.js', )

class TemplateVarsAdmin(admin.ModelAdmin):
    list_display = ('date_of_change', 'status', 'var_name', 'description', )
    

admin.site.register(Event, EventAdmin)
admin.site.register(Template, TemplateAdmin)
admin.site.register(TemplateVars, TemplateVarsAdmin)
