from django.contrib.auth import logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from users.django_mail import views as mail_views
from users.token import TokenValidationMixin
from . import forms


class RedirectUserView(LoginRequiredMixin, generic.RedirectView):
    """
    redirect to send email to the user righter a password change link
    or a verification OTP
    otp = True will send an otp instead of link
    """
    otp = False

    def get_redirect_url(self, *args, **kwargs):
        if self.otp:
            return reverse_lazy("users:change-create-otp")
        return reverse_lazy("users:change-send-link-mail")


class ChangeSendMail(LoginRequiredMixin, mail_views.SendEmailView):
    """
    send password change email to user's email
    """
    template_name = "password-change/user-password-change-mail.html"
    email_subject = "Password Change Mail"
    send_html_email = True

    def get_to_email(self):
        return self.request.user.email


class ChangeSendLinkMail(ChangeSendMail):
    """
    send password change link to the user's email
    """
    email_template_name = "password-change/change-link-mail.html"
    success_url = reverse_lazy("users:change-mail-send-done")

    def get_email_context_data(self):
        url = mail_views.generate_uidb64_url(
            pattern_name="users:change-password",
            user=self.request.user,
            absolute=True,
            request=self.request
        )
        context = {"url": url}
        self.request.session["USER_EMAIL_ID"] = self.get_to_email()
        return context


class PasswordChangeView(LoginRequiredMixin, TokenValidationMixin, auth_views.PasswordChangeView):
    """
    change password
    """
    form_class = forms.ChangePasswordForm
    template_name = "password-change/user-password-change.html"

    def get_success_url(self):
        logout(self.request)
        return reverse_lazy("users:login")


class MailSendDoneView(generic.TemplateView):
    """
    render a template after successfully sending email with success message
    """
    template_name = "common/mail-send-done.html"

    def get_context_data(self, *args, **kwargs):
        email = self.request.session.pop("USER_EMAIL_ID")
        context = super().get_context_data()
        context.update({"email": email})
        return context
