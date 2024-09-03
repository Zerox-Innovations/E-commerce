from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('register/',UserRegisterView.as_view(),name='register'),
     path('login/',UserLoginView.as_view(),name='login'),
     path('profile/',ProfileView.as_view(),name='profile'),
     path('changepassword/',CahngePasswordView.as_view(),name='changepassword'),
     path('resetpassword/',ResetPasswordRequestView.as_view(),name='resetpassword'),
     path('confirmpassword/<str:token>/',ResetPasswordConfirmView.as_view(),name='confirmpassword'),



     path('productsget/',UserProductsRetrive.as_view(),name='productsget'),
     path('productdetails/',UserProductDetailsView.as_view(),name='productdetails'),
     path('addtocart/',UserAddToCartView.as_view(),name='addtocart'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)