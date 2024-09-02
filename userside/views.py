from django.shortcuts import render
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
# Create your views here.


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
                schema=UserCheckoutSerializer  # Use the explicit schema defined earlier
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




