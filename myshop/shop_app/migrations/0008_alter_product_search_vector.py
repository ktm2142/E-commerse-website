# Generated by Django 5.0.4 on 2024-05-13 11:18

import django.contrib.postgres.search
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0007_order_shipped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='search_vector',
            field=django.contrib.postgres.search.SearchVectorField(null=True),
        ),
    ]
