from django.forms import ModelForm

from .models import Order


class AddAddressForm(ModelForm):
    """
    form used to update order model by adding address (that means shipping the order)
    """
    class Meta:
        model = Order
        fields = ['address',]
