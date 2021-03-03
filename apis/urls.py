from django.contrib import admin
from django.urls import path
from .import views


urlpatterns =[
	path('productapi/',views.ProductApi,name='ProductApi'),
  path('vendordetails/',views.Vendor_details,name='vendordetails'),
  path('vendorregistiation/',views.vendorregistiation,name='vendorregistiation')
	
]