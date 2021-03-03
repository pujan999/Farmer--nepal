from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=250, null=True, unique=True)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=250, null=True, unique=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def slug(self):
        return slugify(self.name)


class Product(models.Model):
    name = models.CharField(max_length=250, null=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    price = models.IntegerField(null=True)
    description = models.CharField(max_length=250, null=True)
    image = models.ImageField(upload_to='products/', null=True)
    originalprice = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField(null=True, default=0)
    sales = models.IntegerField(null=True, default=0)
    post_date = models.DateTimeField(auto_now_add=True, null=True)
    unit = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    order_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    order_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.BooleanField(default=False, null=True, blank=False)
    phone = PhoneField(blank=True, help_text='Contact phone number')
    location = models.CharField(max_length=250, null=True)

    def __str__(self):
        return self.order_by.first_name


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    deliveryCharge = models.IntegerField(null=True, blank=True)
    total = models.IntegerField(null=True)

    def __str__(self):
        return self.product.name

    @property
    def order_by(self):
        name = self.order.order_by
        return name

    @property
    def order_date(self):
        return self.order.order_date


class Advertisment(models.Model):
    title = models.CharField(max_length=500, null=True)
    discription = models.TextField(max_length=1500, null=True)
    tag = models.CharField(max_length=500, null=True)
    image = models.ImageField(upload_to='add/', null=True)
    date_post = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class Footeradvertisment(models.Model):
    title = models.CharField(max_length=500, null=True)
    disc = models.TextField(max_length=1500, null=True)
    image = models.ImageField(upload_to='footeradd/', null=True)
    date_post = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title


class Sale(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=True)

    def __str__(self):
        return self.product.name
