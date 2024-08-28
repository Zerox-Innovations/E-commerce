from django.contrib import admin
from adminside.models import *
# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','product_name']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name']

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display=['id','processor']