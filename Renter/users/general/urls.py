from django.urls import path
from . import views

urlpatterns = [
    # redirect user based on authentication and authorisation
    path('', views.RedirectUserView.as_view(), name="redirect-user"),

    # user login
    path('login/', views.LoginView.as_view(), name='login'),
    # user logout
    path('logout/', views.LogoutView.as_view(), name='logout'),

    # user registration
    path('register/<str:key>/', views.RegisterView.as_view(), name='signup'),
    path('register/', views.RedirectUserView.as_view(), name='signup'),

    # user deletion
    # send confirmation mail
    path('delete/send-mail/', views.DeleteUserSendMail.as_view(), name='delete-send-mail'),
    # success message
    path('delete/send-mail/done/', views.MailSendDoneView.as_view(), name='delete-mail-done'),
    # delete confirmation page
    path('delete/confirm/', views.DeleteUserConfirmation.as_view(), name='delete-user-confirm'),
    # delete declined
    path('delete/decline/<token>', views.DeleteUseDecline.as_view(), name='delete-user-decline'),
    # delete confirmed
    path('delete/confirm/<token>/', views.DeleteUser.as_view(), name='delete-user'),

    # user update
    # change username
    path('username/<username>', views.ChangeUsername.as_view(), name='change-username'),
    # change fullname
    path('fullname/<username>', views.ChangeFullname.as_view(), name='change-fullname'),
    # change email
    path('email/<username>', views.ChangeEmail.as_view(), name='change-email'),

]
