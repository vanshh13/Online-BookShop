from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.get_name,name='hom'),
    path('dashboard/profile/',views.profile,name='profile'),
    path('profile/',views.prof,name='prof'),
    path('shopping/',views.shopping,name='shopping'),
    path('dashboard/shopping/',views.shop,name='shop'),
    path('dashboard/profile/edit/',views.edit,name='edit'),
    path('register/',views.register_view,name='register'),
    path('dashboard/login/',views.cust_login_view,name='login'),
    path('dashboard/profile/logout_view/',views.logout_view,name='logout'),
    path('dashboard/',views.dashboard_view,name='dashboard_view'),
    path('about/',views.about,name='about'),
    path('dashboard/about/',views.about_view,name='about_view'),
    path('edit_profile/',views.edit_profile,name='edit_profile'),
    path('', views.search_books, name='search_books'),
    path('dashboard/profile/orderTrack/', views.orderTrack, name='orderTrack'),
    path('add/', views.Addtocart_book, name='Addtocart_book'),
    path('dashboard/shopping/confirm_order/', views.confirm_order, name='confirm_order'),
    path('dashboard/shopping/delete_order/', views.delete_order, name='delete_order'),
    
    path('cancelOrder/', views.cancelOrder, name='cancelOrder'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('dashboard/shopping/increase_quantity/', views.increase_quantity, name='increase_quantity'),
    path('dashboard/shopping/decrease_quantity/', views.decrease_quantity, name='decrease_quantity'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('dashboard/book/<int:book_id>/', views.book_detail_auth, name='book_detail_auth'),

    # admin dashboard
    path('admin/admin_dashboard/manageorder/update_order_status?<int:order_id>/', views.update_order_status, name='update_order_status'),
    path('admin/',views.admin_login_view,name='login_admin'),
    path('admin/admin_dashboard/',views.dashboard_adminview,name='admindashboard'),
    path('admin/admin_dashboard/addbook/',views.addbook, name='addbook'),
    path('admin/admin_dashboard/managebook/',views.managebook, name='managebook'),
    path('admin/admin_dashboard/manageorder/',views.manageorder,name='manageorder'),
    path('admin/admin_dashboard/orderdetail/',views.orderdetail,name='orderdetails'),
    path('admin/admin_dashboard/userdetail/',views.userdetail,name='userdetails'),
    path('admin/admin_dashboard/managebook/updatebook?<int:book_id>/', views.updatebook, name='updatebook'),
    path('admin/admin_dashboard/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/userdetail/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/addbook/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/managebook/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/manageorder/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/orderdetail/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/admin_logout_view/',views.admin_logout_view,name= 'adminlogout'),
    path('admin/admin_dashboard/messages/', views.message_list, name='message_list')

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)