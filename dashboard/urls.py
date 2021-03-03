from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.adminlogin, name='adminlogin'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_vendor/', views.add_vendor, name='add_vendor'),
    path('remove/', views.remove, name='remove'),
    path('update/<int:pk>', views.update, name='update'),
    path('add_product/', views.add_product, name='add_product'),
    path('remove_product/', views.remove_product, name='remove_product'),
    path('order/', views.order, name='order'),
    path('orderitem/<int:pk>', views.orderitem, name='orderitem'),
    path('todaysorders', views.todaysorders, name='todayorder'),
    path('update_product/<int:pk>', views.update_product, name='update_product'),
    path('update_status/<int:pk>', views.update_status, name='update_status'),
    path('confirm_vendor/<int:pk>', views.confirm_vendor, name='confirm_vendor'),
    path('vendoritem/<int:pk>/', views.vendoritem, name='vendoritem'),
    path('category/', views.category, name='category'),
    path('adminlogout', views.adminlogout, name='adminlogout'),
    path('edit_profile', views.edit_profile, name='edit_profile'),
    path('delivered/<int:pk>/', views.delivered, name='delivered'),
    path('remove_Vproduct/', views.remove_Vproduct, name='remove_Vproduct'),
    path('customers/', views.customers, name='customers'),
    path('remove_customer/', views.remove_customer, name='remove_customer'),
    path('adminlogout/',views.adminlogout,name='adminlogout'),
    path('products_vendor/', views.products_vendor,name='products_vendor'),
    path('products_category/', views.products_category,name='products_category'),
    path('customers_order/<int:pk>/',views.customers_order, name='customers_order'),
    path('blogs_page/',views.blogs_page,name='blogs_page'),
    path('remove_blog/', views.remove_blog,name='remove_blog'),
    path('blog_comments/<int:pk>/', views.blog_comments, name= 'blog_comments'),
    path('advertisement',views.advertisement,name='advertisement'),
    path('remove_adv/', views.remove_adv,name='remove_adv'),
    path('update_adv/<int:pk>', views.update_adv, name='update_adv'),
    path('second_adv',views.second_adv,name='second_adv'),
    path('remove_Fadv/', views.remove_Fadv,name='remove_Fadv'),
    path('update_Fadv/<int:pk>', views.update_Fadv, name='update_Fadv'),
    path('category', views.category,name='category'),
    path('remove_category/', views.remove_category,name='remove_category'),
    path('export_pdf/', views.export_pdf, name='export_pdf'),
    path('print_bill/<int:pk>/', views.print_bill, name='print_bill'),

]