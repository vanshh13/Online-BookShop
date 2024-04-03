from django.contrib import admin
from .models import  Customer, Manager, Administrator, Order, Book, OrderDetail, ShoppingCart, Transaction ,ShoppingCartDetail,Message

# admin.site.register(Customer)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('customer_id', 'username', 'firstname', 'lastname', 'email', 'address','mobile')

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('manager_id', 'username', 'firstname', 'lastname', 'email', 'address')

@admin.register(Administrator)
class AdministratorAdmin(admin.ModelAdmin):
    list_display = ('administrator_id', 'username', 'firstname', 'lastname', 'email', 'address')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('orderid', 'date', 'customer_id', 'status')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('book_id', 'book_name', 'author_name', 'price', 'genre','category','description','stock')

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('order', 'book', 'quantity', 'unitcost', 'subtotal')

# @admin.register(ShoppingCart)
# class ShoppingCartAdmin(admin.ModelAdmin):
#     list_display = ('cart_id', 'book_id', 'quantity', 'date_order', 'customer_id')

@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ['cart_id', 'customer_id', 'date_order']

@admin.register(ShoppingCartDetail)
class ShoppingCartDetailAdmin(admin.ModelAdmin):
    list_display = ['shopping_cart', 'book', 'quantity']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_id', 'customer_id', 'transaction_date')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'customer', 'messagecontent','timestamp')
