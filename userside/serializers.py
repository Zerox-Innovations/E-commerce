from account.models import *
from adminside.models import *
from userside.models import *
from rest_framework import serializers


class UserAddressSerializer(serializers.ModelSerializer):

    class Meta :

        model = Address
        fields = ['address_line','land_mark','street','city','state','country','zip_code','default_address']



class UserCheckoutSerializer(serializers.ModelSerializer):
    cart_product = serializers.SerializerMethodField()

    class Meta:
        model = UserCart
        fields = ['id', 'cart_product', 'product_quantity', 'total_price']

    def get_cart_product(self, obj):
        return obj.cart_product.values('product_name','product_image','product_color','product_price')
    

class PaymentProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_price', 'product_image']

class PaymentSerializer(serializers.ModelSerializer):
    cart_products = serializers.SerializerMethodField()  # To include nested product details
    total_price = serializers.SerializerMethodField()  # Add total_price field
    product_quantity = serializers.SerializerMethodField()  # Add product_quantity field

    class Meta:
        model = Payment
        fields = ['cart_products', 'total_price', 'product_quantity','packing_charge', 'delivery_charge', 'payment_method']

    def get_cart_products(self, obj):
        cart = obj.cart_details  # Assuming cart_details is a ForeignKey to the UserCart model
        products = cart.cart_product.all()
        return PaymentProductSerializer(products, many=True).data

    def get_total_price(self, obj):
        return obj.cart_details.total_price  # Fetch total price from the cart

    def get_product_quantity(self, obj):
        return obj.cart_details.product_quantity  # Fetch product quantity from the cart
 # Nest product details



class OrderSerializer(serializers.ModelSerializer):
    # Mark fields as read-only since they're provided programmatically
    user = serializers.ReadOnlyField(source='user.email')  # You can change this to `source='user.username'` if needed
    order_details = serializers.ReadOnlyField(source='order_details.id')
    oreder_id = serializers.ReadOnlyField()
    address = serializers.ReadOnlyField(source='address.__str__') 

    class Meta:
        model = UserOrder
        fields = ['user', 'order_details', 'order_id', 'status', 'created_at','address']





class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image']

class OrderedCartSerializer(serializers.ModelSerializer):
    cart_product = OrderedProductSerializer(many=True)

    class Meta:
        model = UserCart
        fields = ['cart_product']

class OrderGetSerializer(serializers.ModelSerializer):
    order_details = OrderedCartSerializer(source='order_details.cart_details')

    class Meta:
        model = UserOrder
        fields = ['id','order_details', 'created_at']


class OrderUpdateSerializer(serializers.ModelSerializer):

    class Meta :
        model = UserOrder
        fields = []



