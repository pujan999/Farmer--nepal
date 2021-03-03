from django.urls import path
from .import views


urlpatterns = [
    path('vendor/', views.vendorlogin, name='vendorlogin'),
    path('vendor_page/', views.vendor_page, name='vendor_page'),
    path('vendor_product/', views.vendor_product, name='vendor_product'),
    path('update_Vproduct/<int:pk>/', views.update_Vproduct, name='update_Vproduct'),
    path('remove_vproduct/', views.remove_vproduct, name='remove_vproduct'),
    path('vendor_orders/', views.vendor_orders, name='vendor_orders'),
    path('vendorlogout', views.vendorlogout, name='vendorlogout'),
    path('export_topdf/', views.export_topdf, name='export_topdf'),
    ]