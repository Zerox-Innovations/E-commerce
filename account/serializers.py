from account.models import *
from adminside.models import *
from rest_framework import serializers


class AccountSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)

    class Meta:
        model= Account
        fields=['username','email','password','password2']
        



    def validate(self,valid):
        password=valid.get('password')
        password2=valid.get('password2')

        if password != password2:
            raise serializers.ValidationError('Password didn\'t match')
        return valid
    
class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=250)

    class Meta:
        model = Account
        fields = ['email', 'password']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model =UserProfile
        fields = ['name','phone_number','profile_picture']


class UserprofileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required = False)

    class Meta:
        model = Account
        fields = ['username','profile']
        ref_name = 'UserSideUserProfileSerializer'

    def update(self, instance, validated_data):

        instance.username = validated_data.get("username", instance.username)
        
        
        instance.save()
        
        profile_data = validated_data.pop('profile', {})
        if profile_data:
            # Get or create the profile instance
            profile_instance, created = UserProfile.objects.get_or_create(user=instance)
            
            # Update the profile fields
            for attr, value in profile_data.items():
                setattr(profile_instance, attr, value)
            
            profile_instance.save()

        return instance
    


class ChangePasswordSerializer(serializers.Serializer):

    old_password=serializers.CharField()
    new_password=serializers.CharField(max_length=100,required=True)
    confirm_password=serializers.CharField(max_length=100,required=True)



class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordConfirmSerializer(serializers.Serializer):

    new_password = serializers.CharField(max_length=250)
    confirm_password = serializers.CharField(max_length=250)

    def validate(self, data):
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if new_password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        # You do not need to implement creation here, so we can pass
        pass

    def update(self, instance, validated_data):
        # You do not need to implement update here, so we can pass
        pass

class UserAllProductSerializer(serializers.ModelSerializer):

    class Meta :
        model = Product
        fields = ['product_name','product_image','product_price']



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category  
        fields = ['category_name', 'category_image','description'] 

class SpecificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specification  
        fields = ['ram', 'memory','main_camera','front_camera','processor']  
class UserProductGetSerializer(serializers.ModelSerializer):
    product_category = CategorySerializer(read_only=True)
    product_spec = SpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'product_name', 
            'product_image', 
            'product_price', 
            'product_color', 
            'product_category', 
            'product_spec', 
            'product_discription'
        ]

        
class CartProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'product_price', 'product_color']

class UserCartGetSerializer(serializers.ModelSerializer):
    cart_product = CartProductSerializer(many=True, read_only=True)  # Nest ProductSerializer here

    class Meta:
        model = UserCart
        fields = ['id', 'cart_product', 'product_quantity', 'total_price']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image','product_price', 'product_color']




class UserCartSerializer(serializers.ModelSerializer):
    cart_product = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Product.objects.all()
    )

    class Meta:
        model = UserCart
        fields = ['id','cart_product', 'product_quantity', 'total_price']


# class UserCartUpdateSerailizer(serializers.ModelSerializer):
#     class Meta:
#         model = UserCart
#         fields = ['product_quantity']