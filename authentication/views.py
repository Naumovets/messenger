from braces.views import AnonymousRequiredMixin
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from authentication.forms import RegisterUserForm, LoginUserForm


class RegisterUser(AnonymousRequiredMixin, CreateView):
    template_name = 'authentication/register.html'
    form_class = RegisterUserForm
    model = User

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('messages')

    def get_success_url(self):
        return reverse_lazy('messages')


class LoginUser(LoginView):
    redirect_authenticated_user = True
    template_name = 'authentication/login.html'
    form_class = LoginUserForm

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'

        return context

    def get_success_url(self):
        return reverse_lazy('messages')


def user_logout(request):
    logout(request)
    return redirect('messages')
