import datetime
from django.db import models
from distutils.command.upload import upload
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.

class Categoria(models.Model):
    idCategoria = models.IntegerField(primary_key=True, verbose_name='Id de Categoria')
    nombreCategoria = models.CharField(max_length=50, blank=True, verbose_name='Nombre de Categoria')
    
    def __str__(self):
        return self.nombreCategoria


class Producto(models.Model):
    idProducto = models.CharField(primary_key=True, max_length=10, verbose_name='Id Producto')
    marca = models.CharField(max_length=40, blank=True, verbose_name='Marca')
    modelo = models.CharField(max_length=40, blank=True, verbose_name='Modelo')
    imagen = models.ImageField(upload_to="imagenes", null=True, verbose_name='Imagen')
    detalle = models.CharField(max_length=40, blank=True, verbose_name='Detalle')
    precio=models.IntegerField(blank=True, null=True, verbose_name="Precio")
    stock = models.IntegerField(default=0, verbose_name="Stock")

    def __str__(self):
        return self.idProducto
    

class Boleta(models.Model):
    id_boleta=models.AutoField(primary_key=True)
    total=models.BigIntegerField()
    fechaCompra=models.DateTimeField(blank=False, null=False, default = datetime.datetime.now)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    estado = models.CharField(max_length=50, default="Procesando Pedido")

    def __str__(self):
        return f'{self.id_boleta}  | {self.estado}'
    

class detalle_boleta(models.Model):
    id_boleta = models.ForeignKey('Boleta', blank=True, on_delete=models.CASCADE)
    id_detalle_boleta = models.AutoField(primary_key=True)
    id_producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    subtotal = models.BigIntegerField()

    def __str__(self):
        return str(self.id_detalle_boleta)
    
