from rest_framework import serializers
from market .models import Product, Vendor
# from django.contrib.auth.models import User



class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"


class VendorSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = Vendor
        fields = '__all__'


