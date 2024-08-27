from django.contrib.auth import get_user_model
from django.contrib.auth import views as auth_views
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views import generic

from users.django_mail import views as mail_views
from users.token import TokenValidationMixin
from . import forms


class GetEmailView(mail_views.GetEmailView):
    template_name = 'password-forgot/user-password-reset-mail.html'
    success_url = reverse_lazy("users:reset-password-redirect")


class RedirectUserView(generic.RedirectView):
    """
    redirect the user to provide their registered email to
    send a reset link or an OTP
    otp = True will send otp instead of link
    """
    otp = False

    def get_redirect_url(self, *args, **kwargs):
        if self.otp:
            return reverse_lazy("users:reset-create-otp")
        return reverse_lazy("users:reset-send-link-mail")


class ResetSendMail(mail_views.SendEmailView):
    """
    send reset mail to the provided email if it is registered
    """
    template_name = "password-forgot/user-password-reset-mail.html"
    success_url = reverse_lazy("users:reset-mail-send-done")
    email_subject = "Password Reset Mail"
    send_html_email = True

    def get_to_email(self):
        return self.request.session.get("USER_EMAIL")


class ResetSendLinkMail(ResetSendMail):
    """
    send password reset link to the email
    """
    email_template_name = "password-forgot/reset-link-mail.html"

    def get_email_context_data(self):
        user = get_object_or_404(get_user_model(), email=self.get_to_email())
        url = mail_views.generate_uidb64_url(
            pattern_name="users:reset-password",
            user=user,
            absolute=True,
            request=self.request
        )
        context = {"url": url}
        return context


class MailSendDoneView(generic.TemplateView):
    """
    render a template after successfully sending email with success message
    """
    template_name = "common/mail-send-done.html"

    def get_context_data(self, *args, **kwargs):
        email = self.request.session.pop("USER_EMAIL")
        context = super().get_context_data()
        context.update({"email": email})
        return context


class PasswordResetView(TokenValidationMixin, auth_views.PasswordResetConfirmView):
    """
    password reset
    """
    form_class = forms.PasswordResetForm
    success_url = reverse_lazy("users:reset-password-done")
    template_name = "password-forgot/user-password-reset.html"

    def get_user(self):
        user_id = urlsafe_base64_decode(self.kwargs['uidb64'])
        return get_object_or_404(get_user_model(), id=user_id)


class PasswordResetDoneView(generic.TemplateView):
    """
    render a template after successfully password reset
    """
    template_name = "password-forgot/user-password-reset-done.html"
