from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
    """
    overrides UserCreationForm. there are less fields needed
    """
    class Meta:
        """
        specifies the model and fields.
        """
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']