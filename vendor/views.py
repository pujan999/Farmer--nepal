from django.shortcuts import render

from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
from blog.models import Blog
from dashboard.forms import EditVendorForm, EditProductForm, EditStatusForm
from market.models import Product, Vendor, Category, Order, OrderItem
from django.contrib.auth.models import User, auth

from datetime import datetime, date
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa


def vendorlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff == 1 and user.is_superuser == 0:
                auth.login(request, user)
                messages.success(
                    request, ' You are now logged in Successfully vendor. ')

                latest = Product.objects.order_by('-post_date')
                popular = Product.objects.order_by('post_date')


                return redirect('vendor_page')

            else:
                messages.info(request, ' UnAuthorized account')
                return redirect('vendorlogin')

        else:
            messages.info(request, 'Login Credentials not matched.')
            return redirect('vendorlogin')

    else:
        return render(request, 'vendor/login.html')


def vendor_page(request):
    vendor = Vendor.objects.get(user=request.user)
    print(vendor.name)

    prod = Product.objects.filter(vendor=vendor.id)
    cate = Category.objects.all()
    order_prod = OrderItem.objects.filter(product__vendor__id=vendor.id)

    arg = {'cate': cate, 'vendor': vendor,'prod':prod}
    return render(request, 'vendor/Vpage.html', arg)


def vendor_product(request):
    if request.method == "POST":
        name = request.POST['name']
        c_name = request.POST['category']
        price = request.POST['price']
        description = request.POST['description']
        image = request.FILES.get("image", None)
        originalprice =  request.POST['originalprice']
        quantity = request.POST['quantity']
        sales = request.POST['sales']
        post_date = request.POST['post_date']
        unit = request.POST['unit']
        vendor = Vendor.objects.get(user=request.user)

        print(vendor.name)

        product = Product.objects.create(vendor=vendor, category=Category.objects.filter(name=c_name).first(),
                                         name=name, price=price, description=description, image=image,
                                          originalprice=originalprice,
                                         quantity=quantity, sales=sales, post_date=post_date, unit=unit)

        product.save()
        messages.success(
            request, ' product added successfully ')
        return redirect(reverse('vendor_page'))
    else:
        return redirect(reverse('vendor_page'))



def remove_vproduct(request):
    id = request.POST.get('product_id', None)
    product = Product.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        product.delete()
        messages.success(
            request, ' product removed successfully ')
        return redirect(reverse('vendor_page'))


def update_Vproduct(request, pk):
    prod = Product.objects.get(id=pk)
    if request.method == 'POST':
        new_name = request.POST.get('new_name')
        c_name = request.POST.get('new_category')
        price = request.POST.get('new_price')
        description = request.POST.get('new_description')
        image = request.FILES.get("new_image", None)
        originalprice = request.POST.get('new_originalprice')
        quantity = request.POST.get('new_quantity')
        sales = request.POST.get('new_sales')
        post_date = request.POST.get('new_post_date')
        unit = request.POST.get('new_unit')

        prod.name=new_name
        prod.c_name= c_name
        prod.price=price
        prod.description=description
        prod.image=image
        prod.originalprice=originalprice
        prod.quantity=quantity
        prod.sales=sales
        prod.post_date=post_date
        prod.unit=unit

        prod.save()
        messages.success(
            request, ' Product updated successfully ')
        return redirect('vendor_page')

    else:
        cate = Category.objects.all()

        arg = {'cate': cate, 'prod': prod}
        return render(request, 'vendor/update_Vpage.html', arg)


def vendor_orders(request):
    vendor = Vendor.objects.get(user=request.user)
    prods = Product.objects.filter(vendor=vendor.id)
    prod = OrderItem.objects.filter(product__vendor_id=vendor.id)
    cate = Category.objects.all()
    sum_total = sum([prod.total for prod in prod])

    print(vendor.name)

    arg = {'cate': cate, 'vendor': vendor, 'prod': prod,'sum_total':sum_total}
    return render(request, 'vendor/orders.html', arg)

def export_topdf(request):
    today = date.today()
    month = today.month
    vendor = Vendor.objects.get(user=request.user)
    prod = OrderItem.objects.filter(product__vendor_id=vendor.id)
    sum_total = sum([prod.total for prod in prod])
    print(sum_total)
    template_path = 'vendor/pdf.html'
    context = {'prod': prod, 'today': today, 'sum_total': sum_total,'vendor':vendor}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = ' filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def vendorlogout(request):
    auth.logout(request)
    messages.info(request, 'successfully logout')
    return redirect('vendorlogin')
