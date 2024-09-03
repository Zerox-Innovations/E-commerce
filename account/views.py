from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import*
from django.contrib.auth import authenticate
from .models import Account
from account.auth.tokens import get_tokens_for_user
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.permissions import IsAuthenticated
from account.customtoken import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.db.models import Sum
# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Zerox E-commerce")



class UserRegisterView(APIView):
    @swagger_auto_schema(
        tags=["User Authentication"],
        operation_description="User Registration",
        responses={
            200: openapi.Response(
                description='User created successfully',
                schema=AccountSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AccountSerializer,
    )

    def post(self,request):

        serializer = AccountSerializer(data=request.data)

        if serializer.is_valid():               
            user = Account.objects.create_user(     
                first_name = serializer.validated_data.get('first_name'),
                last_name = serializer.validated_data.get('last_name'),
                phone_number = serializer.validated_data.get('phone_number'),
                password = serializer.validated_data.get('password'),
                email = serializer.validated_data.get('email'),
                username = serializer.validated_data.get('username'),       
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    

    @swagger_auto_schema(
        tags=["User Authentication"],
        operation_description="User Login",
        responses={
            200: openapi.Response(
                description='User login successfully',
                schema=LoginSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=LoginSerializer,
    
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')

            user = authenticate(request, email=email, password=password)

            if user is not None:
                user.is_active = True
                user.save()
                
                token=get_tokens_for_user(user)

                return Response({'Msg': 'Login Success','token': token}, status=status.HTTP_200_OK)
            return Response({'Msg': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        print(serializer.errors, 'serializer errors')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    




class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="Retrieve User Profile",
        responses={
            200: openapi.Response(
                description='User Profile Retrieved',
                schema=UserprofileSerializer  # Use the explicit schema defined earlier
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
    )
    def get(self, request):
        try:
            usr = request.user
            user = Account.objects.get(email=usr.email)
            serializer = UserprofileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'Msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="User Profile Updation",
        responses={
            200: openapi.Response(
                description='User Profile Updation successful',
                schema=UserprofileSerializer  # Use the schema directly here
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        manual_parameters=[
            openapi.Parameter('first_name', openapi.IN_FORM, description="First Name", type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_FORM, description="Last Name", type=openapi.TYPE_STRING),
            openapi.Parameter('phone_number', openapi.IN_FORM, description="Phone Number", type=openapi.TYPE_STRING),
            openapi.Parameter('profile', openapi.IN_FORM, description="Profile", type=openapi.TYPE_STRING),
            openapi.Parameter(
            'profile.address_line_1',
            openapi.IN_FORM,
            description="Address Line 1",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'profile.address_line_2',
            openapi.IN_FORM,
            description="Address Line 2",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'profile.profile_picture',
            openapi.IN_FORM,
            description="profile_picture",
            type=openapi.TYPE_FILE
        ),
        openapi.Parameter(
            'profile.city',
            openapi.IN_FORM,
            description="City",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'profile.state',
            openapi.IN_FORM,
            description="State",
            type=openapi.TYPE_STRING
        ),
        openapi.Parameter(
            'profile.country',
            openapi.IN_FORM,
            description="Country",
            type=openapi.TYPE_STRING
        ),
     
        ]
    )
    def put(self, request):
        try:
            usr = request.user
            user = Account.objects.get(email=usr.email)
            serializer = UserprofileSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({'Msg': 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        tags=["User Profile"],
        operation_description="Delete User Profile",
        responses={
            200: openapi.Response(
                description='User Profile Deleted Successfully',
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
    )
    def delete(self, request):
        try:
            usr = request.user
            user = Account.objects.get(email=usr.email)
            user.delete()
            return Response({"Msg": 'Your Account Was Deleted'}, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"Msg": 'User Not Found'}, status=status.HTTP_400_BAD_REQUEST)
        
        
class CahngePasswordView(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(
        tags=["User Password"],
        operation_description="User Change Password",
       responses={
            200: openapi.Response(
                description='User change password successfull',
                schema=ChangePasswordSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=ChangePasswordSerializer,
    )

    def patch(self, request):
        serializer=ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user=request.user
            old_password=serializer.validated_data.get('old_password')
            new_password=serializer.validated_data.get('new_password')
            confirm_password=serializer.validated_data.get('confirm_password')
            
            if user.check_password(old_password):

                if new_password==confirm_password:
                    user.set_password(new_password)
                    user.save()

                    return Response({'Msg':'Password was changed'},status=status.HTTP_200_OK)
                return Response({'Msg':'New password and Confirm Password are not match'})
            return Response({'Msg':'Invalid Old password'},status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class ResetPasswordRequestView(APIView):
    @swagger_auto_schema(
        tags=["User Password"],
        operation_description="User Request for Reset Password ",
         responses={
            200: openapi.Response(
                description='User Resest password request was send',
                schema=ResetPasswordRequestSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=ResetPasswordRequestSerializer,
    )
    def post(self, request):
        serializer = ResetPasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = Account.objects.get(email=email)
                
                token = generate_password_reset_token(user)
                print(token)
                send_password_reset_email(user, token)
                return Response({'msg': 'Password reset email sent'}, status=status.HTTP_200_OK)
            except Account.DoesNotExist:
                return Response({'msg': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordConfirmView(APIView):
    @swagger_auto_schema(
        tags=["User Password"],
        operation_description="User Confirm Reset Password",
        responses={
            200: openapi.Response(
                description='User Reset Password Successful',
                schema=ResetPasswordConfirmSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=ResetPasswordConfirmSerializer,
    )
    def post(self,request,token):

        try:
            user_id = decode_password_reset_token(token)
            user = Account.objects.get(id = user_id)
            serializer = ResetPasswordConfirmSerializer(data=request.data)
            if serializer.is_valid():
                new_password = serializer.validated_data.get('new_password')
                # confirm_password = serializer.validated_data.get('confirm_password')
                user.set_password(new_password)
                user.save()
                return Response({'Msg':'Your password reset successfully'},status=status.HTTP_200_OK)
            return Response (serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except ValidationError as e:
            return Response({'Msg':str(e)},status=status.HTTP_404_NOT_FOUND)




class UserProductsRetrive(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["All Product Get"],
        operation_description="Retrieve All product for user",
        responses={
            200: openapi.Response(
                description='All product Retrived',
                schema=UserAllProductSerializer  # Use the explicit schema defined earlier
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
    )
    def get(self,request):
        try:
            
            products = Product.objects.all()
            serializer = UserAllProductSerializer(products,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"Msg":'Products No found'},status=status.HTTP_404_NOT_FOUND)





class UserProductDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Product Get"],
        operation_description="Retrieve Needed product Details for user",
        responses={
            200: openapi.Response(
                description='Product Retrived',
                schema=UserProductGetSerializer  # Use the explicit schema defined earlier
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="product_id to Retrive the Needed Product",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
    )
    def get(self,request):
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({'Msg':"Enter the product Id"},status= status.HTTP_404_NOT_FOUND)
        
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({'Msg': "product_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            product = Product.objects.get(id = product_id)
            serializer = UserProductGetSerializer(product)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"Msg":'Product not found'},status=status.HTTP_404_NOT_FOUND)





class UserAddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=["Add To Cart"],
        operation_description="Add a product to the user's cart or increase its quantity if it already exists.",
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="ID of the product to add to the cart",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description='Product quantity increased',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'Msg': openapi.Schema(type=openapi.TYPE_STRING, description="Message"),
                    }
                )
            ),
            201: openapi.Response(
                description='New cart item created',
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'cart_product': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_OBJECT),  # Adjust this to match your ProductSerializer fields
                        ),
                        'product_quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product"),
                        'total_price': openapi.Schema(type=openapi.TYPE_INTEGER, description="Total price in the cart"),
                    }
                )
            ),
            400: openapi.Response(description='Bad Request'),
            404: openapi.Response(description='Not Found'),
            500: openapi.Response(description='Server Error')
        }
    )

    def post(self, request):
   
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({'Msg': "Enter the product Id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({'Msg': "product_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'Msg': "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart_item = UserCart.objects.filter(user_cart=request.user,cart_product=product)
        if cart_item.exists():
            for cart_item in cart_item:
                cart_item.product_quantity +=1
                price = cart_item.cart_product.aggregate(total=Sum('product_price'))['total']
                cart_item.total_price = price * cart_item.product_quantity
                cart_item.save()
            return Response({"Msg":'Product quantity increased'},status=status.HTTP_200_OK)

        new_cart = UserCart.objects.create(
            user_cart = request.user,
            total_price= product.product_price,

        )
        new_cart.cart_product.add(product)

        response_data = {
        'cart_product': ProductSerializer(new_cart.cart_product.all(), many=True).data,
        'product_quantity': new_cart.product_quantity ,
        'total_price': new_cart.total_price
            }
        return Response(response_data,status=status.HTTP_201_CREATED)
        
        
            

    @swagger_auto_schema(
        tags=["Add To Cart"],
        operation_description="Retrieve The User's Cart Products",
        responses={
            200: openapi.Response(
                description='User cart Retrived',
                schema=UserProductGetSerializer  # Use the explicit schema defined earlier
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
    )
    def get(self,request):
        
        user=request.user
        try:
            user_cart = UserCart.objects.filter(user_cart=user)
            serializer = UserCartGetSerializer(user_cart,many=True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except UserCart.DoesNotExist:
            return Response({"Msg":'User cart not created'},status=status.HTTP_404_NOT_FOUND)
        




    @swagger_auto_schema(
    tags=["Add To Cart"],
    operation_description="Update the quantity of a product in the user's cart.",
    manual_parameters=[
        openapi.Parameter(
            'cart_id',
            openapi.IN_QUERY,
            description="ID of the cart item to update",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'product_quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Updated quantity of the product"),
        },
        required=['product_quantity']
    ),
    responses={
        200: openapi.Response(
            description='Cart item updated',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'cart_product': openapi.Schema(
                        type=openapi.TYPE_ARRAY,
                        items=openapi.Schema(type=openapi.TYPE_OBJECT),  # Adjust to match ProductSerializer fields
                    ),
                    'product_quantity': openapi.Schema(type=openapi.TYPE_INTEGER, description="Quantity of the product"),
                    'total_price': openapi.Schema(type=openapi.TYPE_INTEGER, description="Total price in the cart"),
                }
            )
        ),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Not Found'),
        500: openapi.Response(description='Server Error')
    }
)

    def put(self, request):
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'Msg': "Enter the cart_id"}, status=status.HTTP_404_NOT_FOUND)
        
        try:
            cart_id = int(cart_id)
        except (ValueError, TypeError):
            return Response({'Msg': "cart_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = request.user
            cart_item = UserCart.objects.filter(user_cart=user, id=cart_id).first()
            

            if not cart_item:
                return Response({"Msg": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UserCartSerializer(cart_item, data=request.data, partial=True)
            
            if serializer.is_valid():
                quantity = serializer.validated_data.get('product_quantity', cart_item.product_quantity)
                cart_item.product_quantity = quantity

               
                price = cart_item.cart_product.aggregate(total=Sum('product_price'))['total']
                cart_item.total_price = price*quantity
                cart_item.save()

                response_data = {
                    'cart_product': ProductSerializer(cart_item.cart_product.all(), many=True).data,
                    'product_quantity': cart_item.product_quantity,
                    'total_price': cart_item.total_price
                }

                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserCart.DoesNotExist:
            return Response({"Msg": "User cart not found"}, status=status.HTTP_404_NOT_FOUND)

        



    @swagger_auto_schema(
    tags=["Delete From Cart"],
    operation_description="Delete a product from the user's cart.",
    manual_parameters=[
        openapi.Parameter(
            'cart_id',
            openapi.IN_QUERY,
            description="ID of the cart item to delete",
            type=openapi.TYPE_INTEGER,
            required=True
        )
    ],
    responses={
        200: openapi.Response(
            description='Product removed from cart',
            schema=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'Msg': openapi.Schema(type=openapi.TYPE_STRING, description="Success message with product names"),
                }
            )
        ),
        400: openapi.Response(description='Bad Request'),
        404: openapi.Response(description='Cart item not found'),
        500: openapi.Response(description='Server Error')
    }
)
    def delete(self, request):
        cart_id = request.GET.get('cart_id')
        if not cart_id:
            return Response({'Msg': "Enter the cart_id"}, status=status.HTTP_404_NOT_FOUND)

        try:
            cart_id = int(cart_id)
        except (ValueError, TypeError):
            return Response({'Msg': "cart_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        try:
            cart_item = UserCart.objects.filter(user_cart=user, id=cart_id).first()

            if not cart_item:
                return Response({"Msg": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

            product_names = list(cart_item.cart_product.values_list('product_name', flat=True))
            product_names_str = ', '.join(product_names)

            cart_item.delete()

            return Response({"Msg": f'Product {product_names_str} has been removed from your cart'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"Msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)









