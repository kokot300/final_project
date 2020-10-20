from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView, CreateView, ListView

from .forms import CreateUserForm
from .models import UserProfile, Address


# Create your views here.


class RegisterUserView(FormView):
    """
    serves the new user registration form
    """
    form_class = CreateUserForm
    template_name = 'registration/register.html'
    success_url = '/accounts/login/'

    def form_valid(self, form):
        """
        overrides default form_valid method
        """
        form = CreateUserForm(self.request.POST)
        if form.is_valid():
            form.save()
        return super().form_valid(form)


class CreateUserProfileView(LoginRequiredMixin, CreateView):
    """
    creates profile for user.
    """
    model = UserProfile
    template_name = 'registration/profile.html'
    success_url = '/accounts/profile/'
    fields = [
        'phone',
        'birth_date',
    ]

    def form_valid(self, form):
        """
        overrides default form_valid method. it prevents profile creation for another user
        """
        user = User.objects.get(id=self.request.user.id)
        form.instance.user = user
        return super(CreateUserProfileView, self).form_valid(form)


class CreateAddressView(LoginRequiredMixin, CreateView):
    """
    creates new address for a user
    """
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
        """
        overrides default form_valid method. it prevents profile creation for another user
        """
        # print(self.request.user.id)
        user = User.objects.get(id=self.request.user.id)
        profile = UserProfile.objects.get(user=user)
        profile_id = profile.pk
        form.instance.profile_id = profile_id
        # if form.instance.profile != self.request.user:
        #     raise ValidationError('invalid user')
        return super(CreateAddressView, self).form_valid(form)


class UserProfileView(LoginRequiredMixin, View):
    """
    shows to user his profile
    """
    login_url = '/accounts/login/'

    def get(self, request):
        """
        manages get requests
        """
        profile = UserProfile.objects.get(pk=request.user.pk)
        ctx = {
            'profile': profile,
        }
        return render(request, 'profile.html', ctx)


class UserAddressesView(LoginRequiredMixin, ListView):
    """
    shows to user his addresses
    """
    model = Address
    template_name = 'addresses_list.html'
    paginate_by = 5

    def get_queryset(self):
        """
        filters out addresses that doesn't belong to logged user
        """
        user = User.objects.get(pk=self.request.user.pk)
        profile = UserProfile.objects.get(user=user)
        return Address.objects.filter(profile=profile)
