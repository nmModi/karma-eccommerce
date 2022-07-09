from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, TemplateView, CreateView

from .models import Customer, Subscriber
from .forms import UserRegistrationForm, EmailForm
from .utils import token_generator
from .tasks import send_spam_email, send_contact_email


class ResetPasswordView(PasswordResetView):
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        current_site = get_current_site(self.request)
        message = render_to_string('registration/password_reset_email.html', {
            'user': self.request.user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(self.request.user.pk)),
            'token': token_generator.make_token(self.request.user),
        })
        mail_subject = 'Activate your blog account.'

        msg = EmailMessage(mail_subject, message, settings.EMAIL_HOST_USER, to=[email])
        msg.send()

        return super(PasswordResetView, self).form_valid(form)


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('register_done')

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        customer, created = Customer.objects.get_or_create(user=new_user, name=form.cleaned_data['first_name'],
                                                           email=form.cleaned_data['email'])
        return super(RegisterView, self).form_valid(form)


class ContactView(TemplateView):
    template_name = 'account/contact.html'

    def post(self, request):
        subject = request.POST.get('subject')
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        msg = f'''new message: {message}, from {name}, {email}'''

        send_contact_email.delay(subject, msg, email, [settings.EMAIL_HOST_USER])

        return HttpResponseRedirect('/')


class EmailFormView(CreateView):
    model = Subscriber
    form_class = EmailForm
    success_url = reverse_lazy('shop:product_list')

    def form_valid(self, form):
        form.save()
        send_spam_email.delay(form.instance.email)
        return super().form_valid(form)
