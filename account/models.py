from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from adminside.models import *
# Create your models here.

class Myaccountmanager(BaseUserManager):
    
    def create_user(self, username, email, password=None,):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password,
            phone_number=None
        )
        user.is_admin   = True
        user.is_active  = True
        user.is_staff   = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class Account(AbstractBaseUser):
    username        = models.CharField(max_length=50,unique=True)
    email           = models.EmailField(max_length=100,unique=True)
#required
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects=Myaccountmanager()

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,label): #add
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE,related_name='userprofile')
    name = models.CharField(max_length=250,blank=True,null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    profile_picture = models.ImageField(blank=True, upload_to='profilepicture')
    
    
    def __str__(self):
        return self.user.username





class UserCart(models.Model):
    user_cart = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user_cart') 
    cart_product = models.ManyToManyField(Product,blank=True,related_name='cart_product')
    product_quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True)
    # created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        # Join product names into a single string
        product_names = ', '.join([product.product_name for product in self.cart_product.all()])
        return f"UserCart: {product_names}"