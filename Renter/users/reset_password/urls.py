from django.urls import path
from . import views

urlpatterns = [
    # forgot password
    # two methods
    # using an url to reset password
    # path -
    # using otp to verify and redirect to reset password

    path('', views.GetEmailView.as_view(), name='password-forgot'),
    # redirect user to give their registered email and redirect to chosen path (otp/link)
    path('redirect/', views.RedirectUserView.as_view(), name='reset-password-redirect'),

    # forgot password link method
    # send an email with password reset link
    path('send-mail/link/', views.ResetSendLinkMail.as_view(), name='reset-send-link-mail'),
    # redirect user to a message page
    path('send-mail/done/', views.MailSendDoneView.as_view(), name='reset-mail-send-done'),

    # common for both method
    # reset the password
    path('<uidb64>/<token>/', views.PasswordResetView.as_view(), name='reset-password'),
    # redirect the user
    path('done/', views.PasswordResetDoneView.as_view(), name='reset-password-done'),
]
