# Generated by Django 5.0.6 on 2024-06-08 04:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_remove_producto_categoria_producto_detalle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='producto',
            name='detalle',
            field=models.CharField(blank=True, max_length=40, verbose_name='Detalle'),
        ),
    ]
