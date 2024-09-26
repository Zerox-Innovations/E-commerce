from django.db import models
from account.models import *
# Create your models here.



class Payment(models.Model):

    PAYMENT_METHOD_CHOICES =[

        ('UPI','UPI'),
        ('COD','Cash on delivary'),
    ]
    paid_user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='paid_user')
    cart_details = models.ForeignKey(UserCart,on_delete=models.CASCADE,related_name='cart_details')
    packing_charge = models.IntegerField(default=50)
    delivery_charge = models.IntegerField(default=40)
    payment_method = models.CharField(max_length=50,choices=PAYMENT_METHOD_CHOICES,null=True)
    # created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payment by {self.paid_user.username}"
    



class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='user_addresses')
    address_line = models.CharField(max_length=100,null=True)
    land_mark = models.CharField(max_length=250,null=True)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    default_address = models.BooleanField(default=False)  

    def __str__(self):
        return f"{self.street}, {self.city}, {self.state}, {self.country} ({self.zip_code})"




class UserOrder(models.Model):
    STATUS = (
        ('Order Confirmed', 'Order Confirmed'),
        ('Shipped',"Shipped"),
        ('Out for delivery',"Out for delivery"),
        ('Delivered', 'Delivered'),
        ('Cancelled','Cancelled'),
        ('Replaced','Replaced'),
    )
    REASON =(
       ( 'Unhope Product','Unhope Produc'),
       ('Unlike','Unlike'),
       ('Too Heavey','Too Heavey'),
    )
    user = models.ForeignKey(Account,on_delete=models.CASCADE,related_name='ordered_user')
    order_details = models.OneToOneField(Payment,on_delete=models.CASCADE,related_name='oreder_details')
    order_id = models.CharField()
    status = models.CharField(max_length=50,choices=STATUS,default='Order Confirmed')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    refund = models.BooleanField(default=False)
    replace_reason = models.CharField(max_length=50,choices=REASON,null=True,blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='order_address')

    

