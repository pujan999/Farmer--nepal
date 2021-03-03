from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import VerificationView
from .import views


urlpatterns = [
    path('', views.index, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('product/', views.product, name='product'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),

    path('logout/', views.logout, name='logout'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
    path('vendorproducts/', views.vendorproducts, name='vendorproducts'),
    path('productcategory/', views.productcategory, name='productcategory'),
    path('placeorder/', views.placeorder, name='placeorder'),
    path('sales/', views.sales, name='sales'),
    path('myorder/', views.myorder, name='myorder'),
path('activate/<uidb64>/<token>',VerificationView.as_view(),name='activate')



]
