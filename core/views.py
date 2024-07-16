from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required , user_passes_test
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib import messages
from .models import Categoria, Producto, Boleta, detalle_boleta
from .forms import ProductoForm, RegistroUserForm
from core.compras import Carrito
import mercadopago
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.

def YouTelefone(request):
    datos = Producto.objects.all()
    productos = {
        "datos":datos
    }
    return render(request, 'YouTelefone.html',productos)


def salir(request):
    logout(request)
    return redirect('/')



def siguiente(request):
    datos = Producto.objects.all()  #similar a select * from Producto
    productos = {
        "datos":datos
    }
    return render(request, 'siguiente.html',productos)

def quienesomos(request):
    return render(request, 'quienesomos.html')

def Formularioatencion(request):
    return render(request, 'Formularioatencion.html')

def adminmod(request):
    return render(request, 'adminmod.html')

def contactoForm(request):
    return render(request, 'contactoForm.html')

@login_required
def perfil(request):
    usuario = request.user
    form = RegistroUserForm(instance=usuario)
    return render(request, 'perfil.html', {'form': form})

def crearProducto(request):
    if request.method=='POST':
        productoform = ProductoForm(request.POST, request.FILES)
        if productoform.is_valid():
            productoform.save()     #similar al método insert
            return redirect ('siguiente')
    else:
        productoform=ProductoForm()
    return render (request, 'crearProducto.html', {'productoform': productoform})

def detalle(request, id):
    producto = get_object_or_404(Producto, idProducto=id) #buscamos un objeto por medio del id
    return render (request, 'detalle.html', {'producto' : producto}) #el objeto que se envia es el de las comillas simples


def modificar(request, id):
    producto = Producto.objects.get(idProducto=id) #tambien busca un objeto al igual que con el (get_object_or_404) 
    datos={
        'formodificar': ProductoForm(instance=producto) #crea un objeto de tipo form con la inf. del objeto vehiculo
    }
    if (request.method=='POST'):
        formulario = ProductoForm(request.POST, request.FILES, instance=producto)
        if formulario.is_valid():
            formulario.save()   #modifica el objeto encontrado
            return redirect('siguiente')
    return render (request, 'modificar.html', datos)


def eliminar(request, id):
    producto = get_object_or_404(Producto, idProducto=id) 
    if request.method=='POST':
        if 'eliminar' in request.POST:      #si el usuario selecciona el boton eliminar del html
            producto.delete()
            return redirect('siguiente')
    return render(request, 'eliminar.html', {'producto': producto})


def registrar(request):
    data={
        'form': RegistroUserForm()
    }
    if request.method=='POST':
        formulario = RegistroUserForm(data=request.POST)
        if formulario.is_valid():
            formulario.save()
            #autenticamos y direccionamos al primer path de la app
            user=authenticate(username=formulario.cleaned_data["username"],
                password=formulario.cleaned_data["password1"])
            login(request,user) #activamos el path de inicio
            return redirect('YouTelefone')
        data["form"]=formulario
    return render(request, 'registration/registrar.html', data)


@login_required
def guardar_email(request):
    if request.method == 'POST':
        nuevo_email = request.POST.get('nuevo_email')
        if nuevo_email:
            try:
                request.user.email = nuevo_email
                request.user.save()
                messages.success(request, '¡Tu dirección de correo electrónico ha sido actualizada correctamente!')
            except Exception as e:
                messages.error(request, f'Error al actualizar el correo electrónico: {str(e)}')
        else:
            messages.error(request, 'No se proporcionó un nuevo correo electrónico válido.')
    
    return redirect('perfil')  # Ajusta 'perfil' por la URL correcta hacia donde quieres redirigir

def tienda(request):
    query = request.GET.get('q')
    if query:
        productos_list = Producto.objects.filter(
            Q(marca__icontains=query) | Q(modelo__icontains=query) | Q(idProducto__icontains=query)
        )
    else:
        productos_list = Producto.objects.all()
        
    carrito_compra = Carrito(request)
    carrito_items = carrito_compra.carrito

    # Inicializa el SDK de MercadoPago con tu Access Token
    sdk = mercadopago.SDK("TEST-4043995131249752-052917-dd38399745af8b6e3c7b4e4ec1401282-1562586661")

    # Verifica si el carrito está vacío
    if not carrito_items:
        paginator = Paginator(productos_list, 4)  # Mostrar 4 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'tienda.html', {
            'page_obj': page_obj,
            'carrito_vacio': True,
            'carrito_items': carrito_items,
            'query': query
        })

    # Crea la preferencia de pago
    preference_data = {
        "items": [
            {
                "id": str(item["idProducto"]),
                "title": item["modelo"],
                "quantity": int(item["cantidad"]),
                "currency_id": "CLP",
                "unit_price": float(item["precio"])  # Asegúrate de que el precio sea un número flotante
            }
            for item in carrito_items.values()
        ]
    }

    try:
        preference_response = sdk.preference().create(preference_data)
        preference = preference_response.get("response", {})
        print(preference_response)  # Agregar print para revisar la respuesta completa

        if 'id' not in preference:
            paginator = Paginator(productos_list, 4)  # Mostrar 4 productos por página
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'tienda.html', {
                'page_obj': page_obj,
                'error': 'No se pudo crear la preferencia de pago.',
                'response': preference_response,
                'carrito_items': carrito_items,
                'query': query
            })

        preference_id = preference['id']
        link = preference['sandbox_init_point']

        paginator = Paginator(productos_list, 4)  # Mostrar 4 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'tienda.html', {
            'page_obj': page_obj,
            'id': preference_id,
            'preference': preference,
            'link': link,
            'carrito_items': carrito_items,
            'query': query
        })
    except Exception as e:
        print(f"Error: {e}")  # Agregar print para revisar el error
        paginator = Paginator(productos_list, 4)  # Mostrar 4 productos por página
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'tienda.html', {
            'page_obj': page_obj,
            'error': f'Error al crear la preferencia de pago: {str(e)}',
            'carrito_items': carrito_items,
            'query': query
        })
    
    
def agregar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.agregar(producto=producto)
    return redirect('tienda')


def eliminar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.eliminar(producto=producto)
    return redirect('tienda')


def restar_producto(request, id):
    carrito_compra= Carrito(request)
    producto = Producto.objects.get(idProducto=id)
    carrito_compra.restar(producto=producto)
    return redirect('tienda')


def limpiar_carrito(request):
    carrito_compra= Carrito(request)
    carrito_compra.limpiar()
    return redirect('tienda')


@login_required
def generarBoleta(request):
    precio_total = 0
    carrito = request.session.get('carrito', {})
    productos = []
    mensaje_error = None

    # Verificar si el carrito está vacío
    if not carrito:
        mensaje_error = 'El carrito está vacío. No se puede generar una boleta.'
        return render(request, 'error.html', {'mensaje_error': mensaje_error})

    # Verificar stock antes de crear la boleta
    for key, value in carrito.items():
        producto = get_object_or_404(Producto, idProducto=value['idProducto'])
        cantidad = int(value['cantidad'])
        if producto.stock < cantidad:
            mensaje_error = f'No hay suficiente stock para el producto: {producto.modelo}'
            return render(request, 'error.html', {'mensaje_error': mensaje_error})

    # Calcular precio total
    for key, value in carrito.items():
        precio_total += int(value['precio']) * int(value['cantidad'])

    # Crear la boleta después de verificar el stock
    boleta = Boleta(total=precio_total, usuario=request.user)
    boleta.save()

    for key, value in carrito.items():
        producto = get_object_or_404(Producto, idProducto=value['idProducto'])
        cantidad = int(value['cantidad'])

        # Actualizar el stock del producto
        producto.stock -= cantidad
        producto.save()

        # Crear el detalle de la boleta
        subtotal = cantidad * int(value['precio'])
        detalle = detalle_boleta(
            id_boleta=boleta, 
            id_producto=producto, 
            cantidad=cantidad, 
            subtotal=subtotal
        )
        detalle.save()
        productos.append(detalle)

    datos = {
        'productos': productos,
        'fecha': boleta.fechaCompra,
        'total': boleta.total,
    }

    request.session['boleta'] = boleta.id_boleta

    carrito = Carrito(request)
    carrito.limpiar()

    return render(request, 'detallecarrito.html', datos)

@login_required
def mis_pedidos(request):
    boletas = Boleta.objects.filter(usuario=request.user).order_by('-fechaCompra')
    detalles = []

    for boleta in boletas:
        detalle = detalle_boleta.objects.filter(id_boleta=boleta)
        detalles.append((boleta, detalle))

    return render(request, 'mis_pedidos.html', {'detalles': detalles})



@user_passes_test(lambda u: u.is_staff)
def ver_todos_los_pedidos(request):
    boletas = Boleta.objects.all().order_by('-fechaCompra')
    detalles = []

    for boleta in boletas:
        detalle = detalle_boleta.objects.filter(id_boleta=boleta)
        detalles.append((boleta, detalle))

    return render(request, 'ver_todos_los_pedidos.html', {'detalles': detalles})



def password_reset_complete(request):
    return render(request, 'registration/password_reset_complete.html')

def password_reset_confirm(request):
    return render(request, 'registration/password_reset_confirm.html')


def password_reset_done(request):
    return render(request, 'registration/password_reset_done.html')


def password_reset_email(request):
    return render(request, 'registration/password_reset_email.html')

def password_reset_form(request):
    return render(request, 'registration/password_reset_form.html')