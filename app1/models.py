from django.db import models
from django.contrib.auth.models import User
import datetime
import os


def get_filenme(req,file):
    now_time=datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    files="%s%s"%(now_time,file)
    return os.path.join('uploads/',files)

class Category(models.Model):
    name=models.CharField(max_length=150,null=False,blank=False)
    image=models.ImageField(upload_to=get_filenme,null=True,blank=True)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=150,null=False,blank=False)
    vendor=models.CharField(max_length=150,null=False,blank=False)
    product_image=models.ImageField(upload_to=get_filenme,null=True,blank=True)
    quantity=models.IntegerField(null=False,blank=False)
    selling_price=models.IntegerField(null=False,blank=False)
    description=models.TextField(max_length=500,null=False,blank=False)
    status=models.BooleanField(default=False,help_text="0-Show,1-Hidden")
    trending=models.BooleanField(default=False,help_text="0-Default,1-Trending")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    products_qty=models.IntegerField(null=False,blank=False)
    created_at=models.DateTimeField(auto_now_add=True)

    @property   
    def total_price(self):
        return self.products_qty * self.product.selling_price

class Address(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    mobile=models.CharField(max_length=10)
    house_no=models.CharField(max_length=10)
    street=models.CharField(max_length=10)
    area=models.CharField(max_length=10)
    city=models.CharField(max_length=10)
    pincode=models.CharField(max_length=10)

    def __str__(self):
        return self.user.first_name
    
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    address=models.ForeignKey(Address,on_delete=models.CASCADE)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE)
    payment=models.BooleanField(default=False)

    def __str__(self):
        return self.user.first_name
    
class Payment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    name=models.CharField(max_length=20)
    amount=models.CharField(max_length=100)
    payment_id=models.CharField(max_length=100)
    paid=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Delivery(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=False,blank=False)
    cat_name=models.CharField(max_length=100)
    products=models.CharField(max_length=1000)
    pro_qty=models.CharField(max_length=100)
    total_amt=models.CharField(max_length=100)
    total_price=models.CharField(max_length=100)
    mobile=models.CharField(max_length=100)
    hno=models.CharField(max_length=100)
    street=models.CharField(max_length=100)
    area=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    pincode=models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name
    
class Support(models.Model):
    name=models.CharField(max_length=20)
    mail=models.EmailField()
    mobile=models.CharField(max_length=20)
    time=models.CharField(max_length=20)

    def __str__(self):
        return self.name