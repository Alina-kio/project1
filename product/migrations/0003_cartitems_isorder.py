# Generated by Django 4.2.4 on 2023-08-23 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_cartitems_total_items'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='isOrder',
            field=models.BooleanField(default=False),
        ),
    ]
