from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views import generic, View
from django.contrib.auth import get_user_model

from users.token import token_generator
from users.mixins import FormMixin
from .forms import EmailForm
from .mixins import SendEmailMixin


class GetEmailView(FormMixin, generic.TemplateView):
    template_name = None
    form_class = EmailForm

    def form_valid(self, form):
        if not get_user_model().objects.filter(email=form.cleaned_data['email']).exists():
            return self.form_invalid(form)
        self.request.session['USER_EMAIL'] = form.cleaned_data['email']
        return redirect(self.get_success_url())


class SendEmailView(SendEmailMixin, View):
    """
    View to send email using django's smtp system
    """
    success_url = None

    def get_success_url(self):
        if self.success_url:
            return self.success_url
        raise ImproperlyConfigured(
            f"{self.__class__.__name__} missing 'success_url' attribute, define 'success_url' attribute or define "
            f"'get_success_url' method")

    def get(self, request, *args, **kwargs):
        self.send_mail()
        return redirect(self.get_success_url())


def generate_uidb64_url(pattern_name, user, absolute=False, request=None, **kwargs):
    uidb64 = urlsafe_base64_encode(force_bytes(user.id))
    token = token_generator.make_token(user)
    url = reverse_lazy(pattern_name, kwargs={"uidb64": uidb64, "token": token, **kwargs})
    if absolute:
        return request.build_absolute_uri(url)
    return url
