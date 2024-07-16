#clase que se utiliza para enlazar un modelo con un form y vincularlo a un template
from django import forms
from django.forms import ModelForm
from django.forms import widgets # enlaza elementos de tipo html con los atributos
from django.forms.models import ModelChoiceField 
from django.forms.widgets import Widget 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Categoria, Producto


class ProductoForm(forms.ModelForm):
    class Meta: # configuramos nuestro form
        model= Producto
        fields= ['idProducto', 'marca', 'modelo', 'imagen', 'detalle', 'stock' , 'precio']
        labels={
            'idProducto': 'Id Producto',
            'marca': 'Marca',
            'modelo': 'Modelo',
            'imagen': 'Imagen',
            'detalle': 'Detalle',
            'stock': 'stock',
            'precio': 'precio'
            
        }
        widgets ={
            'idProducto': forms.TextInput(
            attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese Id Producto',
                    'id': 'idProducto'
                }    
            ),
            'marca': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese marca',
                    'id': 'marca'
                }
            ),
            'modelo': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese modelo',
                    'id': 'modelo'
                }
            ),
            'imagen': forms.FileInput(
                attrs={
                    'class': 'form-control',
                    'id': 'imagen'
                }
            ),
            'detalle': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese detalle',
                    'id': 'detalle'
                }
            ),
            'stock': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese stock',
                    'id': 'stock'
                }
            ),
            'precio': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Ingrese precio',
                    'id': 'precio'
                }
            ),
        }


class RegistroUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True, max_length=30)
    last_name = forms.CharField(required=True, max_length=30)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

