from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
from adminside.models import *
# Create your models here.

class Myaccountmanager(BaseUserManager):
    
    def create_user(self, first_name, last_name, username, email,phone_number, password=None,):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have an username")
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name,
            phone_number=phone_number
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password):
        user=self.create_user(
            email=self.normalize_email(email),
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            phone_number=None
        )
        user.is_admin   = True
        user.is_active  = True
        user.is_staff   = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

    
class Account(AbstractBaseUser):
    first_name      = models.CharField(max_length=50,null=True,blank=True)
    last_name       = models.CharField(max_length=50,null=True,blank=True)
    username        = models.CharField(max_length=50,unique=True)
    email           = models.EmailField(max_length=100,unique=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
#required
    date_joined = models.DateTimeField(auto_now_add = True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects=Myaccountmanager()
    
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self,label): #add
        return True


class UserProfile(models.Model):
    user = models.OneToOneField(Account, on_delete=models.CASCADE,related_name='profile')
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='profilepicture')
    city = models.CharField(blank=True,max_length=100)
    state = models.CharField(blank=True,max_length=100)
    country = models.CharField(blank=True,max_length=100)
    zip_code = models.IntegerField(blank=True,null=True)
    
    
def __str__(self):
    return self.user.first_name

def full_address(self):
    f'{self.address_line_1}{self.address_line_2}'



class UserCart(models.Model):
    user_cart = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='user_cart') 
    cart_product = models.ManyToManyField(Product,blank=True,related_name='cart_product')
    product_quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(null=True)

def __str__(self):
    return self.cart_product.product_name