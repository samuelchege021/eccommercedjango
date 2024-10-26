from django.db import models

from django .contrib.auth.models import User

# Create your models here.



class Product(models.Model):
    product_id=models.AutoField
    product_name=models.CharField(max_length=50)
    category=models.CharField(max_length=50)
    subcategory=models.CharField(max_length=50,default="" )
    price=models.IntegerField(default=0)
    desc=models.CharField(max_length=300)
    pub_date=models.DateField()
    image=models.ImageField(upload_to='shop/images',default="")
    
    
    def __str__(self) :
        return self.product_name
    
    
    
    
    
    
    
 
    
class CartItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='shop/images',default="")
    
    date_added=models.DateTimeField(auto_now_add=True)
       
    
    
    
    def __str__(self) :
        
        return f'{self.quantity}*{self.product.name}'

    
#     # models.py

# from django.db import models

# class Payment(models.Model):
#     phone_number = models.CharField(max_length=20)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_id = models.CharField(max_length=255, blank=True, null=True)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self) -> str:
#         return self.phone_number




# class Orders(models.Model):
#     order_id=models.AutoField(primary_key=True)
#     items_json=models.CharField(max_length=500)
#     amount=models.IntegerField(default=0)
#     name=models.CharField(max_length=90)
#     email=models.CharField(max_length=90)
#     address1=models.CharField(max_length=200)
#     address2=models.CharField(max_length=200)
#     city=models.CharField(max_length=100)
#     state=models.CharField(max_length=100)
#     zip_code=models.CharField(max_length=100)
#     oid=models.CharField(max_length=50,blank=True)
#     amountspaid=models.CharField(max_length=500,blank=True,null=True)
#     paymentstatus=models.CharField(max_length=20,blank=True)
#     phone=models.CharField(max_length=100,default="")
    
#     def __str__(self):
#       return self.name

    
# class orderUpdate(models.Model) :
#     update_id=models.AutoField(primary_key=True)
#     order_id=models.IntegerField(default="")
#     update_desc=models.CharField(max_length=5000)
#     timestamp=models.DateField(auto_now_add=True)
#     def __str__(self):
#         return self.update_desc[0:7] + "..."
