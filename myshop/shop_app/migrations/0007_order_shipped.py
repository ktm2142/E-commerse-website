# Generated by Django 5.0.4 on 2024-05-09 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0006_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipped',
            field=models.BooleanField(default=False),
        ),
    ]
