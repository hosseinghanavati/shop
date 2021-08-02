# Generated by Django 3.2.5 on 2021-08-01 12:01

import Product.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0003_auto_20210731_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('modify_time_stamp', models.DateTimeField(auto_now=True)),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text='Brand name', max_length=50, unique=True, verbose_name='Name')),
                ('image', models.FileField(blank=True, help_text='upload the category image', null=True, upload_to='Brands/images/', verbose_name='category image')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('modify_time_stamp', models.DateTimeField(auto_now=True)),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('name', models.CharField(help_text='product name', max_length=100, verbose_name='Name')),
                ('image', models.FileField(blank=True, help_text='upload the product image', null=True, upload_to='Product/images/', verbose_name='product image')),
                ('inventory', models.PositiveIntegerField(help_text='how many of this product we have in our inventory', verbose_name='Inventory')),
                ('price', models.PositiveIntegerField(help_text='set price of product', verbose_name='Price')),
                ('brand', models.ForeignKey(help_text='choose brand of product', on_delete=django.db.models.deletion.CASCADE, to='Product.brand', verbose_name='Brand')),
                ('category', models.ForeignKey(help_text='choose category of product', on_delete=django.db.models.deletion.CASCADE, to='Product.category', verbose_name='Category')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('modify_time_stamp', models.DateTimeField(auto_now=True)),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('PT', 'percent'), ('AT', 'amount')], default='PT', help_text='Choose type of discount', max_length=2, verbose_name='Type')),
                ('discount_in_percent', models.FloatField(blank=True, help_text='set discount in percent type', null=True, validators=[Product.validators.discount_percent_validator], verbose_name='Amount in percent')),
                ('discount_in_amount', models.PositiveIntegerField(blank=True, help_text='set discount in amount', null=True, verbose_name='Discount in amount')),
                ('maximum_amount', models.IntegerField(blank=True, help_text='if you choose percent type you can insert maximum amount', null=True, verbose_name='Maximum amount')),
                ('product', models.ForeignKey(help_text='choose the product', on_delete=django.db.models.deletion.CASCADE, to='Product.product', verbose_name='Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
