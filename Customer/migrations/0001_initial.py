# Generated by Django 3.2.5 on 2021-08-23 17:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('modify_time_stamp', models.DateTimeField(auto_now=True)),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
                ('country', models.CharField(default='Iran', help_text='enter the country name that you lived', max_length=50, verbose_name='Country')),
                ('province', models.CharField(blank=True, help_text='enter the province name that you lived', max_length=50, null=True, verbose_name='Province')),
                ('city', models.CharField(blank=True, help_text='enter the city name that you lived', max_length=50, null=True, verbose_name='City')),
                ('exact_address', models.TextField(blank=True, help_text='enter the exact address of where you lived', max_length=200, null=True, verbose_name='Exact Address')),
                ('house_number', models.PositiveIntegerField(blank=True, help_text='enter house number', null=True, verbose_name='House number')),
                ('zip_code', models.PositiveIntegerField(blank=True, help_text='enter the zip-code', null=True, verbose_name='Zip-Code')),
                ('owner', models.ForeignKey(help_text='select owner', on_delete=django.db.models.deletion.CASCADE, to='Customer.customer', verbose_name='Owner')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
