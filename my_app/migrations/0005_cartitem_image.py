# Generated by Django 5.0.3 on 2024-08-27 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0004_cartitem_delete_orders_delete_orderupdate_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='image',
            field=models.ImageField(default='', upload_to='shop/images'),
        ),
    ]
