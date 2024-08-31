from account.models import *
from adminside.models import *
from rest_framework import serializers



class UserCheckoutSerializer(serializers.ModelSerializer):
    cart_product = serializers.SerializerMethodField()

    class Meta:
        model = UserCart
        fields = ['id', 'cart_product', 'product_quantity', 'total_price']

    def get_cart_product(self, obj):
        return obj.cart_product.values('product_name','product_image','product_color','product_price')

