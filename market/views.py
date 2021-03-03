from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, auth
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
#from jwt.utils import force_bytes
from .models import Product, Order, Vendor, Category, OrderItem, Sale
from cart.cart import Cart
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.views.generic import ListView
from django.core.paginator import Paginator
from .forms import orderForm
from django.shortcuts import HttpResponse
from itertools import chain
from .tokens import token_generator


def index(request):
    latest = Product.objects.order_by('-post_date')[:8]
    popular = Product.objects.order_by('-sales')[:8]
    return render(request, 'home.html', {'latest': latest, 'popular': popular})


def register(request):
    if request.user.is_authenticated:
        # print(request.user.id)
        return render(request, 'home.html')
    else:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']
            email = request.POST['email']
            name = request.POST['name']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username Taken')
                    return render(request, 'register.html')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return render(request, 'register.html')
                else:
                    user = User.objects.create_user(
                        username=username, password=password1, email=email, first_name=first_name, last_name=last_name,
                        is_active=False)
                    # user = user.save(commit=False)

                    # Deactivate account till it is confirmed
                    user.save()
                    # current_site = get_current_site(request)
                    # mail_subject = 'Activate your blog account.'
                    # message = render_to_string('acc_active_email.html', {
                    #     'user': user,
                    #     'domain': current_site.domain,
                    #     'uid': urlsafe_base64_encode(force_bytes(str(user.pk))),
                    #     'token': token_generator.make_token(user),
                    # })
                    # to_email = user.email
                    # email = EmailMessage(
                    #     mail_subject, message, 'puznsharma1@gmail.com', to=[to_email]
                    # )
                    # email.send(fail_silently=False)
                    #
                    # messages.info(request, 'Please activate your link')
                    return render(request, 'register.html')

                    bcd = request.POST['location']
                    phone = request.POST['phone']
                    # print(id)
                    if len(name) != 0:
                        if len(bcd) != 0:
                            if len(phone) != 0:
                                if Vendor.objects.filter(name=name).exists():
                                    user.delete()
                                    messages.info(request, 'Name Taken')
                                    return render(request, 'register.html')
                                else:
                                    vendor = Vendor.objects.create(
                                        name=name, user=user, location=bcd, phone=phone)
                                vendor.save()
                                messages.success(
                                    request,
                                    'Please wait for 24 hours to be validate as Vendor but you can enjoy product sa Customer till then')
                                user = auth.authenticate(
                                    username=username, password=password1)
                                auth.login(request, user)
                                # print('user_created')
                                latest = Product.objects.order_by('-post_date')
                                popular = Product.objects.order_by('post_date')
                                return render(request, 'home.html', {'latest': latest, 'popular': popular})

                    user = auth.authenticate(
                        username=username, password=password1)
                    auth.login(request, user)
                    # print('user_created')
                    latest = Product.objects.order_by('-post_date')
                    popular = Product.objects.order_by('post_date')
                    return render(request, 'home.html', {'latest': latest, 'popular': popular})

            else:
                messages.info(request, 'Password are not matching..')
                return render(request, 'register.html')

        else:
            return render(request, 'register.html')


def login(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                if user.is_staff != 0:
                    vendor = Vendor.objects.get(user_id=user.id)
                    print(vendor.id)
                    # products = Product.objects.filter(user_id=)

                messages.success(
                    request, ' You are now logged in Successfully. ')
                latest = Product.objects.order_by('-post_date')
                popular = Product.objects.order_by('post_date')
                return render(request, 'home.html', {'latest': latest, 'popular': popular})

            else:
                messages.info(request, 'Login Credentials not matched.')
                return redirect('login')

        else:
            return render(request, 'login.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            print(id)
            user = User.objects.get(pk=id)

            # if not token_generator.check_token(user,token):
            # 	return redirect('login'+'?message='+'User already activated')

            if user.is_active == 1:
                messages.success(request, 'Account already activated')
                return redirect('login')

            user.is_active = True
            user.save()
            messages.success(request, 'Account activated successfully')
            return redirect('login')
        except Exception as e:
            pass

        return redirect('home')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('/')


def dashboard(request):
    if request.user.is_authenticated:
        return render(request, 'dashboard.html')
    else:
        return redirect('login')


def product(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {'page_obj': page_obj}
    return render(request, 'product.html', content)


def about(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


# @login_required(login_url="/login")


def cart_add(request, id):
    if request.user.is_authenticated:
        cart = Cart(request)
        product = Product.objects.get(id=id)
        cart.add(product=product)
        return JsonResponse({"messages": len(request.session['cart'])})
    else:
        # print('abc')
        return redirect('login')


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    try:
        cart.decrement(product=product)

    finally:
        return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    form = orderForm
    content = {'form': form}
    return render(request, 'cart/cart_detail.html', content)


def vendorproducts(request):
    vproduct = Product.objects.order_by('vendor_id')
    vuser = Vendor.objects.order_by('id')
    # print(vproduct)
    return render(request, 'vendor.html', {'vproducts': vproduct, 'vuser': vuser})


def productcategory(request):
    cproduct = Product.objects.order_by('category_id')
    cats = Category.objects.order_by('id')
    # print(vproduct)
    return render(request, 'category.html', {'cproducts': cproduct, 'cats': cats})


def placeorder(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            order_by = request.user.id
            # print(order_by)
            phone = request.POST['phone']
            location = request.POST['location']
            #delivery_charge = request.POST.['delivery_charge']
            #total = request.POST['grand_total']
            #print(delivery_charge)
            #print(total)
            order = Order.objects.create(order_by_id=order_by, phone=phone, location=location
                                          )
            order.save()
            ses = request.session['cart']
            for key, value in ses.items():
                product_id = (value['product_id'])
                product_qty = (value['quantity'])
                product_price = (value['price'])
                total_amount = float(product_price) * float(product_qty)
                data = OrderItem.objects.create(order_id=order.id, product_id=product_id, quantity=product_qty,
                                                total=total_amount)
                data.save()
                sales = Sale.objects.create(product_id=product_id, quantity=product_qty)
                sales.save()
            del request.session['cart']
    #sending email after order placed
        # email = request.user.email
        # print(email)
        # email_subject = "Order Confirmed"
        # email_body = 'Hi ' + request.user.username + \
        #              '! Your Order has been placed succesfully. Thank you for your business with Farmers Market Nepal. You can track your order status from dashboard section. Thank you!!!'
        # email = EmailMessage(
        #     email_subject,
        #     email_body,
        #     'puznsharma1@gmail.com',
        #     [email],
        # )
        # email.send(fail_silently=False)
    return render(request, 'home.html')


def sales(request):
    sales = Sale.objects.order_by('quantity')
    for sale in sales:
        product = Product.objects.get(id=sale.product_id)
        product.quantity = product.quantity - int(sale.quantity)
        product.sales = product.sales + int(sale.quantity)
        if product.quantity < 0:
            messages.info(request, '%s : Selected product is out of stock.' % product.name)
            return render(request, 'home.html')
        print(product.sales)
        print(product.quantity)
        Product.objects.filter(id=sale.product_id).update(sales=product.sales, quantity=product.quantity)
        Sale.objects.filter(id=sale.id).delete()
    return redirect('home')


def myorder(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(order_by_id=request.user.id)
        for order in orders:
            order_items = OrderItem.objects.filter()
            context = {'order_items': order_items}
            return render(request, 'order.html', context)
    return HttpResponse('you dont have an order')
