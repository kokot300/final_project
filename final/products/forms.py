from django.forms import ModelForm

from .models import Order


class AddAddressForm(ModelForm):
    """
    form used to update order model by adding address (that means shipping the order)
    """

    class Meta:
        """
        specifies model and field to be used.
        """
        model = Order
        fields = ['address', ]
