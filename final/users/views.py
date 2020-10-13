from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, ListView

from .forms import CreateUserForm
from .models import UserProfile, Address


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
    ]

    def form_valid(self, form):
        user = User.objects.get(id=self.request.user.id)
        form.instance.user = user
        return super(CreateUserProfileView, self).form_valid(form)


class CreateAddressView(LoginRequiredMixin, CreateView):
    model = Address
    template_name = 'create_address.html'
    success_url = reverse_lazy('addresses')
    fields = [
        'address_line_1',
        'address_line_2',
        'city',
        'zip_code',
        'country',
    ]

    def form_valid(self, form):
        # print(self.request.user.id)
        user = User.objects.get(id=self.request.user.id)
        profile = UserProfile.objects.get(user=user)
        profile_id = profile.pk
        form.instance.profile_id = profile_id
        # if form.instance.profile != self.request.user:
        #     raise ValidationError('invalid user')
        return super(CreateAddressView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request):
        return render(request, 'profile.html', {})


class UserAddressesView(LoginRequiredMixin, ListView):
    model = Address
    template_name = 'addresses_list.html'
    paginate_by = 5
