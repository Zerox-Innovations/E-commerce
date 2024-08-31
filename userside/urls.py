from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('checkout/',UserCheckoutView.as_view(),name='checkout'),
]

