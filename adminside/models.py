from django.db import models

# Create your models here.



class Category(models.Model):
    category_name = models.CharField(max_length=250)
    category_image = models.ImageField(upload_to='categoryimage',blank=True)
    description = models.CharField(max_length=250)
    


class Specification(models.Model):
    ram = models.CharField()
    memory = models.CharField()
    main_camera = models.CharField()
    front_camera = models.CharField()
    processor = models.CharField(max_length=250)



class Product(models.Model):
    product_name = models.CharField(max_length=250)
    product_image = models.ImageField(upload_to='photos/product',blank=True)
    product_price = models.IntegerField()
    product_color = models.CharField(max_length=250)
    product_category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    product_spec = models.ManyToManyField(Specification,blank=True,related_name='product_spec')
    product_discription = models.CharField(max_length=500)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    

    def __str__(self):
        return self.product_name
