# Generated by Django 3.1.7 on 2021-04-22 14:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin1', '0007_offer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupons',
            old_name='valid_from',
            new_name='end',
        ),
        migrations.RenameField(
            model_name='coupons',
            old_name='valid_to',
            new_name='start',
        ),
    ]
