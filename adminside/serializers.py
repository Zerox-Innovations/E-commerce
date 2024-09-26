from account.models import *
from adminside.models import *
from rest_framework import serializers


class AdminAccountListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Account
        fields =['id','username','email','is_active']





class AdminUserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['name', 'phone_number', 'profile_picture']

class AdminUpdateUserprofileSerializer(serializers.ModelSerializer):
    # Link the profile serializer properly
    profile = AdminUserProfileSerializer(source='userprofile', read_only=True)

    class Meta:
        model = Account
        fields = ['email', 'is_active', 'profile']
        ref_name = 'AdminsideUserProfileSerializer'

    def update(self, instance, validated_data):
        # Handle only Account fields here, since the profile is read-only
        instance.is_active = validated_data.get("is_active", instance.is_active)
        instance.save()
        return instance

    

class AdminCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ['id','category_name','category_image','description']
        
    def update(self, instance, validated_data):
        instance.category_name = validated_data.get("category_name",instance.category_name)
        instance.category_image = validated_data.get("category_image",instance.category_image)
        instance.description = validated_data.get("description",instance.description)

        instance.save()

        return instance
    


class AdminSpecificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Specification
        fields = ['ram','memory','main_camera','front_camera','processor']
    
    def update(self, instance, validated_data):
        instance.ram = validated_data.get("ram",instance.ram)
        instance.memory = validated_data.get("memory",instance.memory)
        instance.main_camera = validated_data.get("main_camera",instance.main_camera)
        instance.front_camera = validated_data.get("front_camera",instance.front_camera)
        instance.ramprocessor = validated_data.get("processor",instance.processor)

        instance.save()
        return instance
    


class AdminProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields =['id','product_name','product_image','product_price','product_color',
                 'product_category','product_spec','product_discription','stock',
                 
                 ]
        
    def update(self, instance, validated_data):

        instance.product_image = validated_data.get("product_image",instance.product_image)
        instance.product_price = validated_data.get("product_price",instance.product_price)
        instance.product_color = validated_data.get("product_color",instance.product_color)
        instance.product_discription = validated_data.get("product_discription",instance.product_discription)
        instance.stock = validated_data.get("stock",instance.stock)

        if 'product_spec' in validated_data:
            product_spec_data = validated_data.pop('product_spec')
            instance.product_spec.set(product_spec_data)

        
        instance.save()

        return instance
    


