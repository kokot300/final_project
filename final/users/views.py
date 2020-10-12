from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView, CreateView

from .forms import CreateUserForm
from .models import UserProfile


# Create your views here.


class RegisterUserView(FormView):
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            form.save()
        return super().form_valid(form)


class CreateUserProfileView(LoginRequiredMixin, CreateView):
    model = UserProfile
    template_name = 'registration/profile.html'
    success_url = '/accounts/profile/'
    fields = [
        'phone',
        'birth_date',
        'user',
    ]

    def form_valid(self, form):
        if form.instance.user != self.request.user:
            raise ValidationError('invalid user')
        return super(CreateUserProfileView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return render(request, 'profile.html', {})
