# Generated by Django 4.2.3 on 2023-07-10 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tienda', '0002_alter_producto_imagen_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock_minimo',
            field=models.IntegerField(default=0),
        ),
    ]
