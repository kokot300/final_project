"""final URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from .views import ShopView, CategoriesView, ProductDetailsView, ProductFilterView, AddToCardView, CardView

urlpatterns = [
    path('', ShopView.as_view(), name='product_list'),
    path('categories/', CategoriesView.as_view(), name='category_list'),
    path('<int:pk>/details/', ProductDetailsView.as_view(), name='product_details'),
    path('search/', ProductFilterView.as_view(), name='product_search'),
    path('add_to_card/', AddToCardView.as_view(), name='add_to_card'),
    path('card/', CardView.as_view(), name='card'),
]
