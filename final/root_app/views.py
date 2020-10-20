from django.shortcuts import render
from django.views import View


# Create your views here.


class IndexView(View):
    """
    manages the root view
    """

    def get(self, request):
        """
        manages get request
        """
        return render(request, 'index.html', {})


class AboutView(View):
    """
    manages the about view
    """

    def get(self, request):
        """
        manages get request
        """
        return render(request, 'about.html', {})


class ContactView(View):
    """
    manages the contact view
    """

    def get(self, request):
        """
        manages get request
        """
        return render(request, 'contact.html', {})
