# Generated by Django 5.0.7 on 2024-07-26 16:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product_des',
        ),
        migrations.RemoveField(
            model_name='cart',
            name='product_price',
        ),
    ]
