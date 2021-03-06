# Generated by Django 3.1.5 on 2021-01-22 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0017_auto_20210122_1305'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='name',
            field=models.CharField(max_length=250, null=True, unique=True),
        ),
    ]
