from django import template

from ..forms import EmailForm

register = template.Library()


@register.inclusion_tag('account/components/email_form.html')
def email_form():
    return {'email_form': EmailForm()}
