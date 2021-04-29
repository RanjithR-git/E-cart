# Generated by Django 3.1.7 on 2021-04-21 07:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0003_coupons'),
        ('user', '0006_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='product',
        ),
        migrations.AddField(
            model_name='cart',
            name='cart_product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='admin1.product'),
        ),
    ]