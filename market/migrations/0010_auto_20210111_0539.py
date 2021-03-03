# Generated by Django 3.1.5 on 2021-01-11 05:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('market', '0009_auto_20210110_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.RemoveField(
            model_name='product',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='product',
            name='image',
        ),
        migrations.RemoveField(
            model_name='product',
            name='price',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='ProductDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.IntegerField(null=True)),
                ('description', models.CharField(max_length=250, null=True)),
                ('image', models.ImageField(upload_to='products/')),
                ('discount', models.IntegerField(blank=True, null=True)),
                ('quantity', models.CharField(max_length=1000, null=True)),
                ('product', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='market.product')),
            ],
        ),
    ]