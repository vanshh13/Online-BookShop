from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from .forms import NameForm
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from itertools import product
from .models import *
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import datetime, timedelta
import json
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Order
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
# from .middlewares import auth, guest

def get_name(request):
    if request.method == "POST":  
        query = request.POST.get('query', '')   
        books = Book.objects.filter(
        models.Q(book_name__icontains=query) |
        models.Q(author_name__icontains=query) |
        models.Q(genre__icontains=query)
         )
        return render(request,"customer/index.html",{'books': books})
        
    books = Book.objects.all()
    return render(request,"customer/index.html",{'books': books})
                
# for admin users only 

def managebook(request):
    books = Book.objects.all() 
    context = {'books': books}
    return render(request, "admin/managebook.html",context)


def updatebook(request, book_id):
    book = get_object_or_404(Book, book_id=book_id)

    if request.method == 'POST':
        print("POST request received") 
        Bookname = request.POST.get('Bookname')
        Category = request.POST.get('Catagory')  
        price = request.POST.get('price')
        author = request.POST.get('author')
        description = request.POST.get('description')
        genre = request.POST.get('genre')
        image = request.FILES.get('image')  
        update_action = request.POST.get('UPDATE')
        delete_action = request.POST.get('DELETE')
        print("Update Action:", update_action)  
        print("Delete Action:", delete_action)  
        stock = request.POST.get('stock')
        
        if update_action:
            print("Update action detected")  
    
            book.book_name = Bookname
            book.category = Category
            book.price = price
            book.author_name = author
            book.description = description
            book.genre = genre
            book.stock = stock
           
            if image:
                if book.cover_image:
                    default_storage.delete(book.cover_image.name)
                print("New image found:", image.name)  
                filename = default_storage.save('media/book_covers/' + image.name, ContentFile(image.read()))
                print("New filename:", filename)  
                book.cover_image.name = filename
            book.save()
            messages.success(request, 'Book updated successfully')
        elif delete_action:
            print("Delete action detected")  
            
            book.delete()
            return redirect('/admin/admin_dashboard/managebook/')  # Redirect after deletion

    context = {'book': book}
    return render(request, 'admin/updatebook.html', context)

def addbook(request):
    if request.method == "POST":
        Bookname = request.POST.get('Bookname')
        Category = request.POST.get('Category')
        price = request.POST.get('price')
        author = request.POST.get('author')
        description = request.POST.get('description')
        genre = request.POST.get('genre')
        stock = request.POST.get('stock')
        image = request.FILES.get('file')  
     
        if not Bookname or not Category or not price or not author or not description or not genre or not image:
            messages.error(request, "All fields are required.")
        else:
            book = Book.objects.create(
                book_name=Bookname,
                description=description,
                category=Category,
                price=price,
                author_name=author,
                cover_image=image,
                genre=genre,
                stock= stock
            )
            messages.info(request, "Book created successfully!")
            return redirect("/admin/admin_dashboard/addbook/")

    return render(request, "admin/addbook.html")

def manageorder(request):
    orders = Order.objects.all()
    context = {'orders': orders}
    return render(request, "admin/manageorder.html", context)

def update_order_status(request, order_id):
    order = get_object_or_404(Order, orderid=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        if order.status == 'canceled': 
            order.delete()
    return redirect("/admin/admin_dashboard/manageorder/")
    
def orderdetail(request):
    order_details = OrderDetail.objects.all()
    context = {'order_details': order_details}
    return render(request, "admin/orderdetail.html",context)


def userdetail(request):
    customers = Customer.objects.all()
    context = {'customers': customers}
    return render(request, "admin/userdetail.html",context)

def index(request):
    return get_name(request)

def about(request):
    return render(request,"customer/about.html")
    

def profile(request):
    if request.user.is_authenticated:
        user = request.user

        try:
            profile = Customer.objects.get(username=user)
            order = Order.objects.filter(customer = profile.customer_id)
            context = {
                'user': user,
                'profile': profile,
                'order' : order
            }
            return render(request, "customer/profile.html", context)
        except Customer.DoesNotExist:
            return render(request, "basic/login_customer.html")

    return redirect('/dashboard/login/')

def prof(request):
    context  =  {
                "messages" : ""
            }
    return redirect("/dashboard/login/",context)


def edit(request):    
    if request.user.is_authenticated:
        user = request.user

        try:
            profile = Customer.objects.get(username=user)
            context = {
                'user': user,
                'profile': profile,
            }
            return render(request, "customer/edit.html", context)
        except Customer.DoesNotExist:
            return render(request, "basic/login.html")

    return redirect('/dashboard/login/')

def edit_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        address = request.POST.get('address')
        image = request.FILES.get('image')
        user = request.user
        profile = Customer.objects.get(username=user)

        profile.firstname = first_name
        profile.lastname = last_name
        profile.mobile = mobile
        profile.address = address
        profile.email = email

        if image:
            if profile.image:
                default_storage.delete(profile.image.name)
            print("New image found:", image.name)  
            filename = default_storage.save('media/customer_images/' + image.name, ContentFile(image.read()))
            print("New filename:", filename) 
            profile.image.name = filename
        profile.save()

        return redirect('profile')

    return render(request, 'customer/edit.html', {'profile': profile})


checklogin_customer = False
checklogin_admin = False

def register_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        if User.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect('/register/')

        last = "customer"
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last, email=email)
        user.save()
        customer = Customer.objects.create(
            firstname=first_name,
            username=user,
            lastname=last_name,
            email=email,
            address=address,
            mobile=mobile
        )
        customer.save()

        messages.info(request, "Account created successfully!")
        return redirect('/dashboard/login/')

    return render(request, 'basic/register.html')

def cust_login_view(request):
     if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/dashboard/login/')
         
        user = authenticate(request,username=username, password=password)
         
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/dashboard/login/')
        else:
            if user.last_name == "customer":
                login(request, user)
                global checklogin_customer
                checklogin_customer = True 
                profile = Customer.objects.get(username=user)
                return redirect('/dashboard/',{'profile': profile})
            else :
                return redirect('/dashboard/login/')
            
     return render(request, 'basic/login_customer.html') 

def shopping(request):
    if(checklogin_customer):
       return render(request,'dashboard/shopping/')
    else:  
        context  =  {
                "messages" : ""
            }  
    return render(request,'basic/login_customer.html',context)

def logout_view(request):
    logout(request)
    global checklogin_customer
    checklogin_customer = False
    return redirect('/')

def admin_logout_view(request):
    logout(request)
    global checklogin_admin
    checklogin_admin = False
    return redirect('/admin/')

def about_view(request):
    if request.user.is_authenticated: 
        user = request.user
        profile = Customer.objects.get(username= user)
        return render(request,"customer/about.html",{'profile':profile})
    else:
        return render(request,"customer/about.html")
    

def home(request):
    return render(request, 'customer/index.html')

def dashboard_adminview(request):
    return render(request, 'admin/admin.html')

def orderTrack(request):
    order_id = request.POST.get('orderid')

    orderTrack = get_object_or_404(Order, pk=order_id)

   
    orderTrack.date += timedelta(days=2)  
    order_details = OrderDetail.objects.filter(order=orderTrack)
    order_track_data = {
        'date': orderTrack.date.strftime('%Y-%m-%d'),  
        'status': orderTrack.status,  
    }

    context = {
        'orderTrackData': order_track_data,
        'Orderdetail':order_details
    }
    return render(request, 'customer/orderTrack.html', context)

def admin_login_view(request):
     if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
         
        if not User.objects.filter(username=username).exists():
            messages.error(request, "Invalid Username")
            return redirect('/admin/')
         
        user = authenticate(request,username=username, password=password)
         
        if user is None:
            messages.error(request, "Invalid Password")
            return redirect('/admin/')
        else:
            login(request, user)
            global checklogin_admin
            checklogin_admin = True
            if user.last_name == "admin":
                return redirect('/admin/admin_dashboard/')
            else:
                return redirect('/admin/')
            
     return render(request, 'basic/login_admin.html') 

def delete_order(request):
    if request.method == 'POST':
        cart_detail_id  = request.POST.get('delete')
        cart_detail = ShoppingCartDetail.objects.get(pk=cart_detail_id)
        cart_detail.delete()

    return redirect('/dashboard/shopping/')


def confirm_order(request):
    if request.method == 'POST':
        user = request.user
        customer = Customer.objects.get(username=user)

        shopping_cart = ShoppingCart.objects.get(customer_id=customer.customer_id)
        total = shopping_cart.calculate_total_price()
        
        if total == 0:
            return redirect('/dashboard/')

        new_order = Order.objects.create(
            date=timezone.now(),
            customer=customer,
            status='Pending' 
        )

        cart_details = ShoppingCartDetail.objects.filter(shopping_cart=shopping_cart)

        for cart_detail in cart_details:
            quantity_key = f'quantity_{cart_detail.id}'
            quantity = int(request.POST.get(quantity_key, 0))  
            
            OrderDetail.objects.create(
                order=new_order,
                book=cart_detail.book,
                quantity=quantity,
                unitcost=cart_detail.book.price,
                subtotal=quantity * cart_detail.book.price  
            )

        
        shopping_cart.cart_details.all().delete()

        return redirect('/dashboard/')

    return redirect('/dashboard/') 

def shop(request):
    user = request.user
    
    customer = get_object_or_404(Customer, username=user)

    shopping_cart = ShoppingCart.objects.get(customer_id=customer)

    cart_details = ShoppingCartDetail.objects.filter(shopping_cart=shopping_cart)

    context = {
        'cart_details': cart_details,
        'total_price': shopping_cart.calculate_total_price(),
    }

    return render(request, 'customer/shoppingcart.html', context)

# add to cart
def Addtocart_book(request):
    if request.method == "POST":
        book_id = request.POST.get('book')
        book = Book.objects.get(pk=book_id)
        
        if request.user.is_authenticated:
            customer = Customer.objects.get(username=request.user)

            if ShoppingCartDetail.objects.filter(shopping_cart__customer_id=customer, book=book).exists():
                books = Book.objects.all()
                return redirect('/dashboard/')
            cart, created = ShoppingCart.objects.get_or_create(customer_id=customer)

            shopping_cart_detail = ShoppingCartDetail.objects.create(shopping_cart=cart, book=book, quantity=1)
            
            return redirect('/dashboard/')
        else:
            return render(request,"basic/login_customer.html")
    else:
        return HttpResponse("'message': 'Invalid request method'")


def search_books(request):
    query = request.POST.get('query', '')   
    results = Book.objects.filter(
        models.Q(book_name__icontains=query) |
        models.Q(author_name__icontains=query) |
        models.Q(genre__icontains=query)
    )
    user = request.user
    if user.is_authenticated:
        profile = Customer.objects.get(username= user)
        return render(request, 'customer/index.html', {'books': results, 'query': query,'profile': profile})
   
    return render(request, 'customer/index.html', {'books': results, 'query': query})


def dashboard_view(request):
    user = request.user
    profile = Customer.objects.get(username = user)
    if request.method == "POST":  
        query = request.POST.get('query', '')   
        results = Book.objects.filter(
        models.Q(book_name__icontains=query) |
        models.Q(author_name__icontains=query) |
        models.Q(genre__icontains=query)
        )
        return render(request, 'customer/index.html', {'books': results, 'query': query, 'profile': profile})
    books = Book.objects.all()
    return render(request, 'customer/index.html', {'books': books,'profile': profile})


def cancelOrder(request):
    user = request.user
    customer = Customer.objects.get(username=user)
    if request.method == 'POST':
        order_id = request.POST.get('orderid')
        
        order = Order.objects.get(orderid=order_id)
        if(order.status == 'delivered'):
            return redirect('profile')
        order.status = 'canceled'
        order.save()
        order.delete()
        messages.error(request, "Order cancelled Successfully")
        return redirect('profile')
    return render(request, 'customer.html', {'order': order,'profile': customer})


def contact_us(request):
    if request.method == 'POST':
        user = request.user
        if request.user.is_authenticated:  
            profile = Customer.objects.get(username=request.user)
            firstname = request.POST.get('firstname')
            message_text = request.POST.get('message')
            email = request.POST.get('email')
            timestamp = timezone.now()
            if(firstname==profile.firstname and email==profile.email):
                message = Message.objects.create(customer=profile, messagecontent=message_text, timestamp=timestamp)

                if message:
                    messages.success(request,'Message sent successfully')
                    print("successfully")
                    return redirect('/dashboard/about/')  
                else:
                    messages.error(request,'Failed to create message')
                    print("Failed to create message")
                    return redirect('/dashboard/about/')
            else:
                print(firstname)
                print(email)
                print("Invalid firstname or email")
                return redirect('/dashboard/about/') 
        else:
            return redirect('/dashboard/login/')
    else:
        return render(request, 'customer/about.html')


def message_list(request):
    messages = Message.objects.all()
    return render(request, 'admin/feedback.html', {'messages': messages})



def increase_quantity(request):
    cart_detail_id = request.POST.get('cart_item_id')
    cart_detail = get_object_or_404(ShoppingCartDetail, pk=cart_detail_id)
    
    # Increase quantity by 1
    cart_detail.quantity += 1
    cart_detail.save()
    
    return 

def decrease_quantity(request):
    cart_detail_id = request.POST.get('cart_item_id')
    cart_detail = get_object_or_404(ShoppingCartDetail, pk=cart_detail_id)
    
    # Increase quantity by 1
    cart_detail.quantity -= 1
    cart_detail.save()
    
    return 

def confirm_order(request):
    if request.method == 'POST':
        user = request.user
        customer = Customer.objects.get(username=user)

        shopping_cart = ShoppingCart.objects.get(customer_id=customer.customer_id)
        total = shopping_cart.calculate_total_price()
        
        if total == 0:
            return redirect('/dashboard/')

        payment_type = request.POST.get('payment_type')

        # Create a new order
        new_order = Order.objects.create(
            date=timezone.now(),
            customer=customer,
            status='Pending', 
            payment_type=payment_type, 
            total_payment=total 
        )

        cart_details = ShoppingCartDetail.objects.filter(shopping_cart=shopping_cart)

        for cart_detail in cart_details:
            
            
            OrderDetail.objects.create(
                order=new_order,
                book=cart_detail.book,
                quantity=cart_detail.quantity, 
                unitcost=cart_detail.book.price,
                subtotal=cart_detail.quantity * cart_detail.book.price 
            )

        shopping_cart.cart_details.all().delete()

        return redirect('/dashboard/')

    return redirect('/dashboard/')


def book_detail(request, book_id):
    book = Book.objects.get(pk=book_id)
    context = {'book': book}
    print("user not found")
    return render(request, 'customer/bookcatalog.html', context)

def book_detail_auth(request, book_id):
    user = request.user
    book = Book.objects.get(pk=book_id)
    context = {'book': book}
    if user.is_authenticated:
        print("user in no auth")
        profile = Customer.objects.get(username = user)
        context = {'profile': profile,'book': book}
    return render(request, 'customer/bookcatalog.html', context)