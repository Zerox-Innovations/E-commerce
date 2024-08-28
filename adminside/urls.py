from django.urls import path
from adminside.views import * 
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
      path('userslist/',AdminAccoundlistView.as_view(),name='userslist'),
      path('userupdate/',AdminAccountRetriveUpdateView.as_view(),name='userupdate'),
      path('category/',AdminCategoryCrud.as_view(),name='category'),
      path('specification/',AdminSpecificationCrud.as_view(),name='specification'),
      path('product/',AdminProductCrud.as_view(),name='product'),
     ]



# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)