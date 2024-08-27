from django.contrib.auth import views as auth_views, get_user_model
from django.urls import reverse_lazy
from django.views import generic

from . import forms, base_views


class LoginView(auth_views.LoginView):
    """
    Users Login View

    redirect user to url specified in settings.LOGIN_REDIRECT_URL
    set settings.LOGIN_REDIRECT_URL to 'users:redirect-logged-user'
    to redirect user based on the group or role
    """
    template_name = "general/user-login.html"
    form_class = forms.UserLoginForm
    redirect_authenticated_user = True
    pattern_name = "users:redirect-user"

    def get_redirect_url(self):
        return reverse_lazy(self.pattern_name)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)


class RedirectUserView(base_views.RedirectUserView):
    """
    Users Redirect View, redirect logged-in user
    """

    def get_pattern_name(self):
        return reverse_lazy("index")


class LogoutView(auth_views.LogoutView):
    """
    Users Logout View

    redirect user to login page
    """
    next_page = "users:login"
    http_method_names = ["get", "post", "put"]
    success_url = reverse_lazy("users:login")

    def get_success_url(self):
        return self.success_url

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(generic.CreateView):
    """
    User creation/registration view

    regular user is created and redirected to add the user in to a group
    """
    model = get_user_model()
    template_name = "general/user-register.html"
    form_class = forms.UserRegistrationForm
    success_url = reverse_lazy("users:login")

    def get_success_url(self, *args, **kwargs):
        return self.success_url
