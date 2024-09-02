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
    delivery_charge = models.IntegerField()
    payment_method = models.CharField(max_length=3,choices=PAYMENT_METHOD_CHOICES)

    def __str__(self) :
        return self.paid_user

