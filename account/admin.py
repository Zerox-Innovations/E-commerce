from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display=['id','username','email']


@admin.register(UserProfile)
class ProfileAdmin(admin.ModelAdmin):
    list_display=['id','user','profile_picture']



@admin.register(UserCart)
class UserCartAdmin(admin.ModelAdmin):
    list_display = ['id','user_cart', 'get_cart_products']

    def get_cart_products(self, obj):
        return ", ".join([str(product) for product in obj.cart_product.all()])
    
    get_cart_products.short_description = 'Cart Products'
