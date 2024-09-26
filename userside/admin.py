from django.contrib import admin
from userside.models import *
# Register your models here.

@admin.register(Address)
class UserAddressAdmin(admin.ModelAdmin):
    list_display=['id','user']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','paid_user']

@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display=['id','user']
