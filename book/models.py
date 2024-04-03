from typing import Any
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='customer_username')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True) 
    address = models.TextField()
    mobile  = models.TextField(max_length=10, default='')
    image = models.ImageField(upload_to='customer_images/', null=True, blank=True) 
    def __str__(self):
        return f'{self.firstname} {self.lastname}'


class Manager(models.Model):
    manager_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='manager_username')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f'{self.firstname} {self.lastname}'

class Administrator(models.Model):
    administrator_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name='administrator_username')
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    address = models.TextField()

    def __str__(self):
        return f'{self.firstname} {self.lastname}'



class Book(models.Model):
    book_name = models.CharField(max_length=255)
    author_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    cover_image = models.ImageField(upload_to='book_covers/', null=True, blank=True)
    book_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255,default='')
    stock = models.CharField(max_length=255 , default='available')

    def __str__(self):
        return f'{self.book_name} by {self.author_name}'


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Processing', 'Processing'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_CHOICES = [
        ('cash_on_delivery', 'Cash on Delivery'),
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
    ]

    orderid = models.AutoField(primary_key=True)
    date = models.DateField(default=timezone.now)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, default=1)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_CHOICES,default='cash_on_delivery' )
    total_payment = models.DecimalField(max_digits=10, decimal_places=2 ,default= 0)  # Adjust max_digits and decimal_places as needed

    def calculate_total_price(self):
        cart_details = self.cart_details.all()
        total_price = sum(detail.calculate_subtotal() for detail in cart_details)

        return total_price
    
    def __str__(self):
        return f'ShoppingCart #{self.cart_id} - Customer: {self.customer_id.username}'

    def __str__(self):
        return f'Order #{self.orderid} - Status: {self.status} - Customer: {self.customer.customer_id}'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unitcost = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_subtotal(self):
        return self.quantity * self.book.price

    def __str__(self):
        return f'OrderDetail for Order #{self.order_id} - Book: {self.book.book_name}'

class ShoppingCart(models.Model):
    cart_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_order = models.DateTimeField(auto_now_add=True)

    def calculate_total_price(self):
        cart_details = self.cart_details.all()

        # Calculate total price
        total_price = sum(detail.calculate_subtotal() for detail in cart_details)

        return total_price
    
    def __str__(self):
        return f'ShoppingCart #{self.cart_id} - Customer: {self.customer_id.username}'


class ShoppingCartDetail(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='cart_details')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    def calculate_subtotal(self):
        return self.quantity * self.book.price
    
    def __str__(self):
        return f'Detail for ShoppingCart #{self.shopping_cart.cart_id} - Book: {self.book.book_name}, Quantity: {self.quantity}'   
    

class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Transaction #{self.transaction_id} - Customer: {self.customer_id.username}'



class Message(models.Model):
    message_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    messagecontent = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'Message from {self.customer.firstname} {self.customer.lastname}'