from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash

# Create your views here.
from blog.models import Blog, Comments
from dashboard.forms import EditVendorForm, EditProductForm, EditStatusForm
from market.models import Product, Vendor, Category, Order, OrderItem, Advertisment, Footeradvertisment
from django.contrib.auth.models import User, auth
from django.core.paginator import Paginator
from itertools import chain

from datetime import datetime, date
from django.db.models import Sum
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

from django.template.loader import render_to_string
import tempfile


def adminlogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_superuser == 1:
                auth.login(request, user)
                messages.success(
                    request, ' You are now logged in Successfully Admin. ')
                order = Order.objects.all()
                total_order = Order.objects.all().count()

                today = date.today()
                print(date)
                print(total_order)

                return redirect('dashboard')

            else:
                messages.info(request, ' UnAuthorized account')
                return redirect('adminlogin')

        else:
            messages.info(request, 'Login Credentials not matched.')
            return redirect('adminlogin')

    else:
        return render(request, 'admin/login.html')


def dashboard(request):
    order = Order.objects.all()
    total_order = Order.objects.all().count()
    delivered_orders = Order.objects.filter(status=True)

    today = date.today()
    print(date)
    print(total_order)

    todays_order = Order.objects.filter(order_date__contains=today).count()
    todays_orders = Order.objects.filter(order_date__contains=today)
    arg = {'order': order, 'total_order': total_order, 'todays_orders': todays_orders, 'todays_order': todays_order,
           'delivered_orders': delivered_orders}
    return render(request, 'admin/index.html', arg)


def add_vendor(request):
    vendor_data = Vendor.objects.all()
    args = {'vendor_data': vendor_data}
    return render(request, 'admin/vendors.html', args)


def remove(request):
    id = request.POST.get('vendor_id', None)
    vendor = Vendor.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        vendor.delete()
        Vendor.objects.all().update()
        messages.success(
            request, ' Vendor removed successfully ')

        return redirect(reverse('add_vendor'))


def remove_Vproduct(request):
    id = request.POST.get('product_id', None)
    product = Product.objects.get(id=id)
    vendor = Vendor.objects.get(id=product.vendor_id)
    pk = vendor.id
    print(pk)
    if request.method == 'POST':
        product.delete()
        Product.objects.all().update()
        messages.success(
            request, ' Vendors product removed successfully ')

        return redirect('vendoritem', pk=pk)


def update(request, pk):
    if request.method == 'POST':
        vendor = Vendor.objects.get(id=pk)
        Vendor_form = EditVendorForm(request.POST, instance=vendor)
        if Vendor_form.is_valid():
            vendor = Vendor_form.save()
            # update_session_auth_hash(request, vendor)
            return redirect(reverse('add_vendor'))
        else:
            return redirect(reverse('vendor'))
            messages.info(request, 'invalid credential')

    else:
        vendor = Vendor.objects.get(id=pk)
        print(vendor.name)
        Vendor_form = EditVendorForm(instance=vendor)
        arg = {'form': Vendor_form}
        return render(request, 'admin/edit_vendor.html', arg)


def add_product(request):
    prod = Product.objects.all()
    cate = Category.objects.all()
    vendor = Vendor.objects.all()
    arg = {'cate': cate, 'vendor': vendor, 'prod': prod}
    return render(request, 'admin/Product.html', arg)


def remove_product(request):
    id = request.POST.get('product_id', None)
    product = Product.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        product.delete()
        messages.success(
            request, ' Product removed successfully ')
        return redirect(reverse('add_product'))


def update_product(request, pk):
    if request.method == 'POST':
        product = Product.objects.get(id=pk)
        Product_form = EditProductForm(request.POST, instance=product)
        if Product_form.is_valid():
            product = Product_form.save()
            # update_session_auth_hash(request, product)
            return redirect(reverse('add_product'))

        else:
            return redirect(reverse('Product'))
            messages.info(request, 'invalid credential')

    else:
        product = Product.objects.get(id=pk)

        product_form = EditProductForm(instance=product)
        arg = {'form': product_form}
        return render(request, 'admin/edit_product.html', arg)


def order(request):
    order = Order.objects.all()
    total_order = Order.objects.all().count()

    today = date.today()
    print(date)
    print(total_order)

    todays_order = Order.objects.filter(order_date__contains=today).count()
    todays_orders = Order.objects.filter(order_date__contains=today)
    arg = {'order': order, 'total_order': total_order, 'todays_order': todays_order, 'todays_orders': todays_orders}
    return render(request, 'admin/order.html', arg)


def update_status(request, pk):
    if request.method == 'POST':
        order = Order.objects.get(id=pk)
        Order_form = EditStatusForm(request.POST, instance=order)
        if Order_form.is_valid():
            order = Order_form.save()
            update_session_auth_hash(request, order)
            return redirect(reverse('order'))
        else:
            return redirect(reverse('order'))
            messages.info(request, 'invalid credential')

    order = Order.objects.get(id=pk)

    Order_form = EditStatusForm(instance=order)
    arg = {'form': Order_form}
    return render(request, 'admin/edit_status.html', arg)


def orderitem(request, pk):
    order = Order.objects.get(id=pk)
    orderitem = OrderItem.objects.filter(order_id=order.id)
    sum_total = sum([order.total for order in orderitem])

    print(sum_total)
    arg = {'order': order, 'orderitem': orderitem, 'sum_total': sum_total}
    return render(request, 'admin/or_items.html', arg)


def todaysorders(request):
    today = date.today()
    todays_order = Order.objects.filter(order_date__contains=today).count()
    if todays_order != 0:
        todayorder = Order.objects.filter(order_date__contains=today)
        print(todayorder)
        args = {'todayorder': todayorder}
        return render(request, 'admin/todayorder.html', args)
    else:
        order = Order.objects.all()
        today = date.today()
        total_order = Order.objects.all().count()
        todays_order = Order.objects.filter(order_date__contains=today).count()
        arg = {'order': order, 'total_order': total_order, 'todays_order': todays_order}
        return render(request, 'admin/order.html', arg)


def confirm_vendor(request, pk):
    vendor = Vendor.objects.get(id=pk)
    print(vendor.user.is_staff)
    if request.method == 'POST':

        if vendor.user.is_staff == False:
            print(vendor.name)
            # vendor.user.is_staff = True
            # vendor.save()
            uu = vendor.user
            uu.is_staff = True
            uu.save()

            return redirect('add_vendor')

        else:
            return redirect('add_vendor')
    else:
        return redirect('add_vendor')


def vendoritem(request, pk):
    vendor = Vendor.objects.get(id=pk)
    product = Product.objects.filter(vendor_id=vendor.id)
    result_list = list(
             sorted(
            chain(product),
            key = lambda instance: instance.quantity
        ))
    print(result_list)
    paginator = Paginator(result_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    print(page_obj)
    arg = {'vendor': vendor, 'product': product,'page_obj': page_obj}
    return render(request, 'admin/vitems.html', arg)


def category(request):
    if request.method == 'POST':
        name = request.POST['category']

        category = Category.objects.create(name=name)
        category.save()
        return redirect(reverse('category'))
    else:
        category = Category.objects.all()
        arg = {'category': category}
        return render(request, 'admin/category.html', arg)


def adminlogout(request):
    auth.logout(request)
    messages.info(request, 'successfully logout')
    return redirect('adminlogin')


def edit_profile(request):
    user = request.user
    print(user.username)
    if request.method == 'POST':
        new_username = request.POST.get('new_username')
        old_password = request.POST.get('old_password')
        new_password = request.POST.get('new_password')
        print(new_username)
        if user.check_password(old_password):
            user.username = new_username
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)
            return redirect('adminlogout')
        else:
            messages.info(request, 'invalid credentilas')
            return render(request, 'admin/edit_profile.html', {'user': user})
    else:
        return render(request, 'admin/edit_profile.html', {'user': user})


def delivered(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        print(order.status)

        if order.status == False:
            order.status = True
            order.save()

            return redirect('dashboard')

        else:
            order.status = False
            order.save()
            return redirect('dashboard')
    else:
        return redirect('dashboard')


def customers(request):
    customers = User.objects.filter(is_superuser=False)
    args = {'customers': customers}
    return render(request, 'admin/customer.html', args)


def remove_customer(request):
    id = request.POST.get('user_id', None)
    customer = User.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        customer.delete()
        User.objects.all().update()
        messages.success(
            request, ' Customer removed successfully ')

        return redirect(reverse('customers'))


def products_vendor(request):
    vproduct = Product.objects.order_by('vendor_id')
    vuser = Vendor.objects.order_by('id')
    # print(vproduct)
    return render(request, 'admin/fil_vendor.html', {'vproducts': vproduct, 'vuser': vuser})


def products_category(request):
    cproduct = Product.objects.order_by('category_id')
    cats = Category.objects.order_by('id')
    print(cproduct)
    return render(request, 'admin/fil_category.html', {'cproducts': cproduct, 'cats': cats})


def customers_order(request, pk):
    customer = User.objects.get(id=pk)
    orderproduct = OrderItem.objects.filter(order__order_by_id=customer.id)
    sum_total = sum([order.total for order in orderproduct])
    print(customer.username)
    args = {'customer': customer, 'order': order, 'orderproduct': orderproduct, 'sum_total': sum_total}

    return render(request, 'admin/customeritems.html', args)


def blogs_page(request):
    blogs = Blog.objects.all()
    print(blogs)
    args = {'blogs': blogs}
    return render(request, 'admin/blogs.html', args)


def remove_blog(request):
    id = request.POST.get('blog_id', None)
    blog = Blog.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        blog.delete()
        Blog.objects.all().update()
        messages.success(
            request, ' Blog removed successfully ')

        return redirect(reverse('blogs_page'))


def blog_comments(request, pk):
    comments = Comments.objects.filter(blog_id=pk)
    blog = Blog.objects.get(id=pk)
    args = {'comments': comments, 'blog': blog}
    return render(request, 'admin/blogcomments.html', args)


def advertisement(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('discription')
        tag = request.POST.get('tag')
        image = request.FILES.get("image", None)
        date_post = request.POST.get('date_post')

        Adv = Advertisment.objects.create(title=title, discription=description, tag=tag, image=image,
                                          date_post=date_post)
        Adv.save()
        messages.success(
            request, ' Adv added successfully ')
        return redirect('advertisement')
    else:
        adv = Advertisment.objects.all()
        arg = {'adv': adv}
        return render(request, 'admin/advertisement.html', arg)


def remove_adv(request):
    id = request.POST.get('adv_id', None)
    adv = Advertisment.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        adv.delete()
        Advertisment.objects.all().update()
        messages.success(
            request, ' Advt removed successfully ')
        return redirect(reverse('advertisement'))


def update_adv(request, pk):
    if request.method == 'POST':
        title = request.POST.get('new_title')
        description = request.POST.get('new_discription')
        tag = request.POST.get('new_tag')
        image = request.FILES.get("new_image", None)
        date_post = request.POST.get('new_date_post')

        adv = Advertisment.objects.get(id=pk)

        adv.title = title
        adv.description = description
        adv.tag = tag
        adv.image = image
        adv.date_post = date_post
        adv.save()
        messages.success(
            request, ' Advt updated successfully ')

        return redirect('advertisement')
    else:
        adv = Advertisment.objects.get(id=pk)
        arg = {'adv': adv}
        return render(request, 'admin/update_adv.html', arg)


def second_adv(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('disc')
        image = request.FILES.get("image", None)
        date_post = request.POST.get('date_post')

        Adv = Footeradvertisment.objects.create(title=title, disc=description, image=image, date_post=date_post)
        Adv.save()
        messages.info(request, 'Adds added succesfully')
        return redirect('second_adv')
    else:
        adv = Footeradvertisment.objects.all()
        arg = {'adv': adv}
        return render(request, 'admin/second_adv.html', arg)


def remove_Fadv(request):
    id = request.POST.get('adv_id', None)
    adv = Footeradvertisment.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        adv.delete()
        Footeradvertisment.objects.all().update()
        return redirect(reverse('second_adv'))


def update_Fadv(request, pk):
    adv = Footeradvertisment.objects.get(id=pk)
    if request.method == 'POST':
        title = request.POST.get('new_title')
        image = request.FILES.get("new_image", None)
        date_post = request.POST.get('new_date_post')
        description = request.POST.get('disc')

        adv.title = title
        adv.image = image
        adv.date_post = date_post
        adv.disc = description
        adv.save()
        return redirect('second_adv')
    else:
        arg = {'adv': adv}
        return render(request, 'admin/update_Fadv.html', arg)


def category(request):
    cate = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        cat = Category.objects.create(name=name)
        cat.save()
        return redirect('category')
    else:
        arg = {'cate': cate}
        return render(request, 'admin/add_categories.html', arg)


def remove_category(request):
    id = request.POST.get('cat_id', None)
    catg = Category.objects.get(id=id)
    print(id)
    if request.method == 'POST':
        catg.delete()
        Category.objects.all().update()
        return redirect(reverse('category'))


def export_pdf(request):
    today = date.today()
    month = today.month
    Oproduct = OrderItem.objects.filter(order__order_date__contains=month)
    sum_total = sum([Oproduct.total for Oproduct in Oproduct])
    print(sum_total)
    template_path = 'admin/pdf-output.html'
    context = {'Oproduct': Oproduct, 'today': today, 'sum_total': sum_total}
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

def print_bill(request,pk):
    order = Order.objects.get(id=pk)
    orderitem = OrderItem.objects.filter(order_id=order.id)
    sum_total = sum([order.total for order in orderitem])

    print(sum_total)
    arg = {'order': order, 'orderitem': orderitem, 'sum_total': sum_total}
    today = date.today()
    month = today.month
    print(sum_total)
    template_path = 'admin/bill.html'
    context = { 'order': order, 'orderitem': orderitem,'today': today, 'sum_total': sum_total}
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


def adminlogut(request):
    auth.logout(request)
    messages.info(request, 'successfully logout')
    return redirect('adminlogin')
