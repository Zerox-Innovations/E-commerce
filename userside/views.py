from django.shortcuts import render,redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from .serializers import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import stripe
from django.db.models import Sum 
from django.conf import settings
import os
from dotenv import load_dotenv
from django.contrib.auth.decorators import login_required
from .id_generating import generate_order_id
from django.http import HttpResponse


# Create your views here.

class UserAddressView(APIView):
    permission_classes =[IsAuthenticated]

    def post(Self,request):

        serializer = UserAddressSerializer(data = request.data)
        if serializer.is_valid():
            user = request.user
            default_address = serializer.validated_data.get('default_address', False)

            if default_address:
                Address.objects.filter(user=user, default_address=True).update(default_address=False)

            if not Address.objects.filter(user=user).exists():
                default_address = True

            
            Address.objects.create(
                user = request.user,
                address_line = serializer.validated_data.get('address_line'),
                land_mark = serializer.validated_data.get('land_mark'),
                street = serializer.validated_data.get('street'),
                city = serializer.validated_data.get('city'),
                state = serializer.validated_data.get ('state'),
                country = serializer.validated_data.get('country'),
                zip_code = serializer.validated_data.get('zip_code'),
                default_address=default_address
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class UserCheckoutView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=["User Checkout"],
        operation_description="Retrieve The User's Cart Products",
        manual_parameters=[
            openapi.Parameter(
                'cart_id',
                openapi.IN_QUERY,
                description="ID of the cart to retrieve checkout details for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='User cart Retrived',
                schema=UserCheckoutSerializer  
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
    )
    def get(self,request):

        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'Msg': "Enter the cart id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_id = int(cart_id)
        except (ValueError, TypeError):
            return Response({'Msg': "product_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            checkout = UserCart.objects.filter(user_cart=request.user,id=cart_id).first()
            serializer = UserCheckoutSerializer(checkout)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except UserCart.DoesNotExist:
            return Response({"Msg":'This cart Product not foubnd'},status=status.HTTP_404_NOT_FOUND)

load_dotenv()

class UserPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        stripe.api_key = os.getenv('STRIPE_SECRET_KEY')
        
        cart_id = request.GET.get('cart_id')
        request.session['cart_id'] = cart_id
        if not cart_id:
            return Response({'Msg': "Enter the cart id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_id = int(cart_id)
        except (ValueError, TypeError):
            return Response({'Msg': "cart_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        

        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            payment_method = serializer.validated_data.get('payment_method')
            request.session['payment_method'] = payment_method
            try:
                cart = UserCart.objects.get(id=cart_id)
            except UserCart.DoesNotExist:
                return Response({"Msg": 'UserCart Not found'}, status=status.HTTP_404_NOT_FOUND)

            
            if payment_method == 'COD':  
                payment = Payment.objects.create(
                    paid_user=request.user,
                    cart_details=cart,
                    payment_method=payment_method
                )

                default_address = Address.objects.filter(user=request.user, default=True).first()

                if not default_address:
                    return Response({"error": "No default address set. Please set one."}, status=status.HTTP_400_BAD_REQUEST)
                
                order = UserOrder.objects.create(
                    user=request.user,
                    order_details=payment,
                    order_id=generate_order_id(),
                    address = default_address,
                )

                response_serializer = PaymentSerializer(payment)
                return Response({
                    'payment': response_serializer.data,
                    'order': OrderSerializer(order).data  # Include order data in the response
                }, status=status.HTTP_201_CREATED)
                

            elif payment_method == 'UPI':
                product_details = []
                for product in cart.cart_product.all():
                    
                    stripe_product = stripe.Product.create(
                        name=product.product_name
                    )

                    
                    stripe_price = stripe.Price.create(
                        unit_amount=int(product.product_price * 100),
                        currency='inr',
                        product=stripe_product.id
                    )

                    product_details.append({
                        'product_name': product.product_name,
                        'stripe_product_id': stripe_product.id,
                        'stripe_price_id': stripe_price.id
                    })

                customer = stripe.Customer.create(
                    email=request.user.email,
                    phone=request.user.phone_number
                )

                checkout_session = stripe.checkout.Session.create(
                    line_items=[
                        {
                            'price': product_details[0]['stripe_price_id'],
                            'quantity': cart.product_quantity,
                        },
                    ],
                    mode='payment',
                    customer=customer.id,
                    success_url='http://127.0.0.1:8000/userside/success/',
                    cancel_url='http://127.0.0.1:8000/cancel.html',
                    metadata={'user_email': request.user.email}
                )
                request.session['user_email'] = request.user.email

                return Response({'url': checkout_session.url}, status=status.HTTP_303_SEE_OTHER)

        return Response(serializer.errors)

    

class StripeSuccessView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):

        cart_id = request.session.get('cart_id')
        if not cart_id :
            return Response({'Msg': "cart_id not found from session"}, status=status.HTTP_404_NOT_FOUND)
        try:
            cart = UserCart.objects.filter(id = cart_id,user_cart= request.user).first()
        except UserCart.DoesNotExist:
            return Response({"Msg":'cart not found'})
        
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            stripe_payment = Payment.objects.create(
                paid_user = request.user,
                cart_details = cart,
                payment_method = request.session.get('payment_method')
            )
            default_address = Address.objects.filter(user=request.user, default=True).first()

            if not default_address:
                return Response({"error": "No default address set. Please set one."}, status=status.HTTP_400_BAD_REQUEST)

            order = UserOrder.objects.create(
                user=request.user,
                order_details=stripe_payment,
                order_id=generate_order_id(),
                address = default_address,
            )

            response_serializer = PaymentSerializer(stripe_payment)
            return Response({
                'payment': response_serializer.data,
                'order': OrderSerializer(order).data  # Include order data in the response
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors)

            

        
class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request):
        try:
            order = UserOrder.objects.filter(user = request.user)
            serializer = OrderGetSerializer(order,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except UserOrder.DoesNotExist:
            return Response({"Msg":'Didn/t oreder any products'},status=status.HTTP_404_NOT_FOUND)
        

    def put(self,request):

        order_id = request.GET.get('order_id')
        request.session['order_id'] = order_id
        if not order_id:
            return Response({'Msg': "Enter the order id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            order_id = int(order_id)
        except (ValueError, TypeError):
            return Response({'Msg': "order_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        






