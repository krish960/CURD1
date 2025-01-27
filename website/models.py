from django.db import models
from decimal import Decimal
from django.utils.timezone import now


class Customer(models.Model):
    Customer_name = models.CharField(max_length=100)
    Customer_email = models.EmailField()
    Customer_phone = models.CharField(max_length=15)
    Customer_addres = models.TextField()
    total_spent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  #


class Customer(models.Model):
    Customer_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)  # Allow phone numbers

    def __str__(self):
        return self.Customer_name


class Stack(models.Model):
    brandr_name = models.CharField(max_length=100)
    brandr_Value = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    add_product_value = models.IntegerField(default=0) 

class Bill(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    stack = models.ForeignKey('Stack', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    gov_tax = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    paid_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    username = models.CharField(max_length=100)
    customer_phone = models.CharField(max_length=15, null=True, blank=True)  

class Shop_info(models.Model):
    shop_name=models.CharField(max_length=100)
    shop_number= models.IntegerField() 
    shop_email=models.CharField(max_length=100)
    shop_address=models.CharField(max_length=100)
    shop_owner_name=models.CharField(max_length=100)


class User(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  

    def __str__(self):
        return self.username
# class Bill(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     stack = models.ForeignKey(Stack, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2)
#     gov_tax = models.DecimalField(max_digits=10, decimal_places=2)
#     total = models.DecimalField(max_digits=10, decimal_places=2)
#    




# from django.db import models

class PaymentOrder(models.Model):
    order_id = models.CharField(max_length=255, unique=True)
    amount = models.IntegerField()
    status = models.CharField(max_length=10, default='locked')  # 'locked' or 'unlocked'

    def __str__(self):
        return f"Order ID: {self.order_id}, Status: {self.status}"
