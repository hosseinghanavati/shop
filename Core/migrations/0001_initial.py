# Generated by Django 3.2.5 on 2021-07-31 04:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time_stamp', models.DateTimeField(auto_now_add=True)),
                ('modify_time_stamp', models.DateTimeField(auto_now=True)),
                ('delete_time_stamp', models.DateTimeField(blank=True, default=None, null=True)),
                ('deleted', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
