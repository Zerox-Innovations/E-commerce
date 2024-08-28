from django.urls import path
from .views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('register/',UserRegisterView.as_view(),name='register'),
     path('login/',UserLoginView.as_view(),name='login'),
     path('active/',ProfileView.as_view(),name='active'),
     path('changepassword/',CahngePasswordView.as_view(),name='changepassword'),
     path('resetpassword/',ResetPasswordRequestView.as_view(),name='resetpassword'),
     path('confirmpassword/<str:token>/',ResetPasswordConfirmView.as_view(),name='confirmpassword'),



     path('productsget/',UserProductsRetrive.as_view(),name='productsget'),
     path('productdetails/',UserProductDetailsView.as_view(),name='productdetails'),
     path('usercart/',UserAddToCartView.as_view(),name='usercart'),
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)