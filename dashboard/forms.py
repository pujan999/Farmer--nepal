from market.models import Vendor, Product, Order
from django import forms


class EditVendorForm(forms.ModelForm):
    template_name = 'edit_vendor.html'

    class Meta:
        model = Vendor
        fields = (
            'name',
            'location',
            'phone',
            #'user.is_staff'




        )

class EditProductForm(forms.ModelForm):
    template_name = 'edit_product.html'

    class Meta:
        model = Product
        fields = (
        'name' ,
        'vendor',
        'category' ,
        'price' ,
        'description',
        'image' ,
       'originalprice',
        'quantity',
        'sales',
        'unit' ,

        )
class EditStatusForm(forms.ModelForm):
    template_name = 'edit_status.html'

    class Meta:
        model = Order
        fields = (
        'status' ,


        )