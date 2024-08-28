from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework import status
from account.models import *
from adminside.serializers import *
from adminside.custompermission import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

# Create your views here.

class AdminAccoundlistView(APIView):
    
    permission_classes = [IsAuthenticated,OnlyAdminPermission]
    @swagger_auto_schema(
        tags=["Admin Accound List"],
        operation_description="Admin list all account",
        responses={
            200: openapi.Response(
                description='User created successfully',
                schema=AdminAccountListSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
    )
    def get(self,request):
        try:
            users = Account.objects.filter(is_admin = False)
            serializer = AdminAccountListSerializer(users, many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({'Have not Users'},status=status.HTTP_404_NOT_FOUND)
        



class AdminAccountRetriveUpdateView(APIView):
    permission_classes = [IsAuthenticated,OnlyAdminPermission]
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        tags=["Admin User account Managing"],
        operation_description="Admin User account retrive by ID",
        responses={
            200: openapi.Response(
                description='Admin user account retrive successful',
                schema=AdminUpdateUserprofileSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                'user_id',
                openapi.IN_QUERY,
                description="User ID to retrieve the profile",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        
    )



    def get(self,request):
        user_id = request.GET.get('user_id')
        request.session['user_id']=user_id
        if not user_id:
            return Response({"Msg":'Please Enter the User ID'},status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Account.objects.get(id = user_id)
            serializer = AdminUpdateUserprofileSerializer(user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"Msg":"user not found"},status=status.HTTP_404_NOT_FOUND)
        


    @swagger_auto_schema(
    tags=["Admin User account Managing"],
    operation_description="Admin user Profile Updation",
    responses={
        200: openapi.Response(
            description='Admin User Profile Updation successful',
            schema=AdminUpdateUserprofileSerializer  # Use the schema directly here
        ),
        400: openapi.Response(description='Bad Request'),
        500: openapi.Response(description='Server Error')
    },
    manual_parameters=[
        openapi.Parameter(
            'is_active',
            openapi.IN_FORM,
            description="Is Active Status",
            type=openapi.TYPE_BOOLEAN,  # Correct the type to BOOLEAN for is_active
        ),
    ]
)
    def patch(self,request):
        user_id=request.session.get('user_id')
        try:
            user = Account.objects.get(id=user_id)
            serializer = AdminUpdateUserprofileSerializer(user,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Account.DoesNotExist:
            return Response({"Msg":'User not found'},status=status.HTTP_404_NOT_FOUND)
        
    


class AdminCategoryCrud(APIView):
    permission_classes = [IsAuthenticated,OnlyAdminPermission]
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        tags=["Admin Category Managing"],
        operation_description="Admin Category Creation",
        responses={
            200: openapi.Response(
                description='Category successfully created',
                schema=AdminCategorySerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminCategorySerializer,
    )
    def post(self,request):
        serializer = AdminCategorySerializer(data=request.data)
        if serializer.is_valid():
            category = Category.objects.create(
                category_name = serializer.validated_data.get('category_name'),
                category_image =serializer.validated_data.get ('category_image'),
                description = serializer.validated_data.get('description')
            )
            image_url = None
            if category.category_image:
                image_url = request.build_absolute_uri(category.category_image.url)

            # Prepare the response data including the image URL
            response_data = {
                'category_name': category.category_name,
                'category_image': image_url,
                'description': category.description
            }
            
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    @swagger_auto_schema(
        tags=["Admin Category Managing"],
        operation_description="Admin All Category Retrive",
        responses={
            200: openapi.Response(
                description='Admin All Category successfully Retrive ',
                schema=AdminCategorySerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
    )
    def get(self,request):
        
        try:

            categories = Category.objects.all()
            serializer = AdminCategorySerializer(categories,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'Msg':"Doesn't datas"},status=status.HTTP_404_NOT_FOUND)



    @swagger_auto_schema(
        tags=["Admin Category Managing"],
        operation_description="Admin Category Updation",
        responses={
            200: openapi.Response(
                description='Admin Category Updated',
                schema=AdminCategorySerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminCategorySerializer,
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Category ID to update the category",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
    )
    def put(self,request):
        category_id = request.GET.get('category_id')
        request.session['category_id']=category_id
        if not category_id:
            return Response({"Msg":'Please Enter the Category ID'},status=status.HTTP_400_BAD_REQUEST)
        try:

            editcategory=Category.objects.get(id = category_id)
            serializer = AdminCategorySerializer(editcategory,data=request.data,partial=True)
            if serializer.is_valid():

                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'Msg':"Category not found"},status=status.HTTP_404_NOT_FOUND)
    


    @swagger_auto_schema(
        tags=["Admin Category Managing"],
        operation_description="Admin Category Deletion",
        responses={
            200: openapi.Response(
                description='Admin category deleted successfully',
                schema=AdminCategorySerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        manual_parameters=[
            openapi.Parameter(
                'category_id',
                openapi.IN_QUERY,
                description="Category ID to Delete the category",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],
        
    )
    def delete(self,request):
        category_id = request.GET.get('category_id')
        try:
            delete_category = Category.objects.get(id=category_id)
            delete_category.delete()
            return Response({'Msg':"Category was Delete"},status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'Msg':"Category Not Found"},status= status.HTTP_404_NOT_FOUND)
        

class AdminSpecificationCrud(APIView):
    permission_classes = [IsAuthenticated,OnlyAdminPermission]
    @swagger_auto_schema(
        tags=["Admin Specification Managing"],
        operation_description="Admin Spec Creation",
        responses={
            200: openapi.Response(
                description='Admin Spec successfully created',
                schema=AdminSpecificationSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminSpecificationSerializer,
    )
    def post(self,request):

        serializer = AdminSpecificationSerializer(data=request.data)
        if serializer.is_valid():
            Specification.objects.create(
                ram = serializer.validated_data.get('ram'),
                memory = serializer.validated_data.get ('memory'),
                main_camera = serializer.validated_data.get ('main_camera'),
                front_camera = serializer.validated_data.get ('front_camera'),
                processor = serializer.validated_data.get ('processor'),
            )
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    @swagger_auto_schema(
        tags=["Admin Specification Managing"],
        operation_description="Admin Specification Retrive",
        responses={
            200: openapi.Response(
                description='Admin Specification successfully Retrive',
                schema=AdminSpecificationSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
    )
    def get(self,request):
        try:

            spec = Specification.objects.all()
            serializer = AdminSpecificationSerializer(spec,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Specification.DoesNotExist:
            return Response({"Msg":'No more Specification datas '})
    


    @swagger_auto_schema(
        tags=["Admin Specification Managing"],
        operation_description="Admin Spec Updation",
        responses={
            200: openapi.Response(
                description='User created successfully',
                schema=AdminSpecificationSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminSpecificationSerializer,
        manual_parameters=[
            openapi.Parameter(
                'spec_id',
                openapi.IN_QUERY,
                description="Spe_ID to Update the Specification",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],

    )
    def put(self,request):

        spec_id = request.GET.get('spec_id')
        if not spec_id:
            return Response({'Msg':"Enter the spec Id"},status= status.HTTP_404_NOT_FOUND)
        
        try:
            spec_id = int(spec_id)
        except (ValueError, TypeError):
            return Response({'Msg': "Spec_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        
        try:
        
            spec = Specification.objects.get(id=spec_id)
            serializer = AdminSpecificationSerializer(spec,data= request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Specification.DoesNotExist:
            return Response({'Msg':"Enter the involved id"},status=status.HTTP_400_BAD_REQUEST)
        


    @swagger_auto_schema(
        tags=["Admin Specification Managing"],
        operation_description="Admin Spec Deletion",
        responses={
            200: openapi.Response(
                description='Admin Spec successfully deleted',
                schema=AdminSpecificationSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminSpecificationSerializer,
        manual_parameters=[
            openapi.Parameter(
                'spec_id',
                openapi.IN_QUERY,
                description="Spe_ID to Delete the Specification",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],

    )
    def delete(self,request):

        spec_id = request.GET.get('spec_id')
        if not spec_id:
            return Response({'Msg':"Enter the spec Id"},status= status.HTTP_404_NOT_FOUND)
        
        try:
            spec_id = int(spec_id)
        except (ValueError, TypeError):
            return Response({'Msg': "Spec_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            spec = Specification.objects.get(id=spec_id)
            spec.delete()
            return Response({'Msg':"Spec deleted"},status=status.HTTP_200_OK)
        except Specification.DoesNotExist:
            return Response({'Msg':"Spec Id not found"},status=status.HTTP_404_NOT_FOUND)
        


class AdminProductCrud(APIView):
    permission_classes = [IsAuthenticated,OnlyAdminPermission]
    parser_classes = (MultiPartParser, FormParser)
    @swagger_auto_schema(
        tags=["Admin Product Managing"],
        operation_description="Admin Product Creation",
        responses={
            200: openapi.Response(
                description='Admin Product successfully created',
                schema=AdminProductSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminProductSerializer,
        

    )
    def post(self,request):

        serializer = AdminProductSerializer(data=request.data)
        if serializer.is_valid():
            new_product=Product.objects.create(
                product_name = serializer.validated_data.get('product_name'),
                product_image = serializer.validated_data.get('product_image'),
                product_price = serializer.validated_data.get('product_price'),
                product_color = serializer.validated_data.get('product_color'),
                product_category = serializer.validated_data.get('product_category'),
                product_discription = serializer.validated_data.get('product_discription'),
                stock = serializer.validated_data.get('stock'),
            )
            

            if 'product_spec' in serializer.validated_data:
                product_spec = serializer.validated_data['product_spec']
                new_product.product_spec.set(product_spec)

            image_url = None
            if new_product.product_image:
                image_url = request.build_absolute_uri(new_product.product_image.url)
            response_data = serializer.data
            response_data['product_image'] = image_url
            return Response(response_data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


    @swagger_auto_schema(
        tags=["Admin Product Managing"],
        operation_description="Admin Product Retrive",
        responses={
            200: openapi.Response(
                description='Admin successfully Retrive Product',
                schema=AdminProductSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        
        

    )
    def get(self,request):
        try:
            products = Product.objects.all()
            serializer = AdminProductSerializer(products,many = True)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'Msg':"No more Products"},status= status.HTTP_400_BAD_REQUEST)
        



    @swagger_auto_schema(
        tags=["Admin Product Managing"],
        operation_description="Admin Product Updation",
        responses={
            200: openapi.Response(
                description='Admin Product successfully Updated',
                schema=AdminProductSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Product_ID to Update the Product",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],

    )
    def put(self,request):
        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({"Msg":'Enter the product Id'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({'Msg': "product_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id=product_id)
            serializer = AdminProductSerializer(product,data=request.data,partial = True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({"Msg":'Product Not Found'},status=status.HTTP_404_NOT_FOUND)
        


    @swagger_auto_schema(
        tags=["Admin Product Managing"],
        operation_description="Admin Product Deletion ",
        responses={
            200: openapi.Response(
                description='Admin Product successfully Deleted',
                schema=AdminProductSerializer
            ),
            400: openapi.Response(description='Bad Request'),
            500: openapi.Response(description='Server Error')
        },
        request_body=AdminProductSerializer,
        manual_parameters=[
            openapi.Parameter(
                'product_id',
                openapi.IN_QUERY,
                description="Product_ID to Delete the Product",
                type=openapi.TYPE_STRING,
                required=True
            ),
        ],

    )
    def delete(self,request):

        product_id = request.GET.get('product_id')
        if not product_id:
            return Response({"Msg":'Enter the product Id'},status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product_id = int(product_id)
        except (ValueError, TypeError):
            return Response({'Msg': "product_id must be a valid integer"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            product = Product.objects.get(id = product_id)
            product.delete()
            return Response({"Msg":'Product Was delete'},status= status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({"Msg":'Product Not found'},status= status.HTTP_404_NOT_FOUND)
        
    








    


    
        
    

        
            



        
    
        

