from django.forms import ModelForm
from .models import *

class orderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['order_by','phone','location']
        