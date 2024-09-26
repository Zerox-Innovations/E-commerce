from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('address/', UserAddressView.as_view(), name='address'),
    path('checkout/',UserCheckoutView.as_view(),name='checkout'),
    path('payment/',UserPaymentView.as_view(),name='payment'),
    path('success/', StripeSuccessView.as_view(), name='success'),
    path('order/', OrderListView.as_view(), name='order'),
]

