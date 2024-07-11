from django.shortcuts import render, redirect
from .models import *
import os
from django.conf import settings
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
from django.contrib.auth import login, logout
from .forms import RegistrationForm 
from .utils import enviar_solicitud_transbank
from django.urls import reverse
from transbank.error.transbank_error import TransbankError
import uuid
from django.shortcuts import render, get_object_or_404, redirect

def iniciar_pago(request):
    monto = 10000
    orden_compra = str(uuid.uuid4())  # Utiliza un UUID para garantizar unicidad

    data = {
        "buy_order": orden_compra,
        "session_id": request.session.session_key or str(uuid.uuid4()),  # Asegúrate de que session_id no sea None
        "amount": monto,
        "return_url": request.build_absolute_uri(reverse('confirmar_pago'))
    }

    try:
        response = enviar_solicitud_transbank("https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions", data)
        
        # Debug: Imprimir respuesta completa
        print(f"Respuesta de Transbank: {response}")

        if 'token' in response and 'url' in response:
            Transaccion.objects.create(orden_compra=orden_compra, monto=monto, token=response['token'])
            return redirect(response['url'])
        else:
            error_message = response.get("error", "Error desconocido en la respuesta de Transbank.")
            messages.error(request, f'Error en la respuesta de Transbank: {error_message}')
            return redirect('carroCompras')
    except TransbankError as e:
        messages.error(request, f'Error de Transbank: {str(e)}')
        return redirect('carroCompras')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')
        return redirect('carroCompras')

def confirmar_pago(request):
    token = request.POST.get('token_ws')
    if not token:
        messages.error(request, 'Token no proporcionado.')
        return redirect('carroCompras')

    try:
        response = enviar_solicitud_transbank(f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}", {})
        
        if response['status'] == "AUTHORIZED":
            orden_compra = response['buy_order']
            transaccion = Transaccion.objects.get(token=token)
            transaccion.estado = "pagado"
            transaccion.save()
        else:
            messages.error(request, f"Error en el pago: {response.get('response_code')} - {response.get('description')}")
        
        return render(request, 'pago_confirmado.html', {'response': response})
    except TransbankError as e:
        messages.error(request, f'Error de Transbank: {str(e)}')
        return redirect('carroCompras')
    except Exception as e:
        messages.error(request, f'Error inesperado: {str(e)}')
        response = {"error": str(e)}
        return render(request, 'pago_confirmado.html', {'response': response})


def detalle_producto(request, sku):
    producto = get_object_or_404(Producto, sku=sku)
    return render(request, 'detalle_producto.html', {'producto': producto})


def cerrar_sesion(request):
    logout(request)
    return redirect('/')

def registro(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Registro exitoso!.')
            return redirect('/')
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


def inicio(request):
    request.session["usuario"] = request.user.username
    usuario = request.session["usuario"]
    productos = Producto.objects.all()
    categoria_teclados = Producto.objects.filter(id_categoria = 1)
    categoria_switches = Producto.objects.filter(id_categoria = 2)

    # Crea el contexto que será enviado a la página
    context = {
        'usuario': usuario,
        'prod': productos,
        'cate_switches': categoria_switches,
        'cate_teclados': categoria_teclados,
    }
    return render(request, 'inicio.html', context)

# Función para cargar la página de teclados
def teclados(request):
    productos = Producto.objects.all()
    categoria_teclados = Producto.objects.filter(id_categoria = 1)
    return render(request,"teclados.html",{"prod":productos,"cate_teclados":categoria_teclados})

# Función para cargar la página de switches
def switches(request):
    productos = Producto.objects.all()
    categoria_switches = Producto.objects.filter(id_categoria = 2)
    return render(request,"switches.html",{"prod":productos,"cate_switches":categoria_switches})

# Función para cargar el carrito de compras
def carroCompras(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    # Por cada producto en el carrito, se añade al total y se guarda en la lista de productos
    for sku, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(sku=sku)
            if producto.stock > 0:  
                subtotal = producto.precio * cantidad
                total += subtotal
                productos.append({
                    'nombre': producto.nombre,
                    'cantidad': cantidad,
                    'precio': producto.precio,
                    'subtotal': subtotal,
                })
        except Producto.DoesNotExist:
            pass
    context = {
        'productos': productos,
        'total': total,
    }
    return render(request, 'carroCompras.html', {'productos': productos, 'total': total})

def cargarAgregarProducto(request):
    categorias = Categoria.objects.all()
    productos = Producto.objects.all()
    return render(request,"agregarProducto.html",{"cate":categorias, "prod":productos})

# Función para agregar un producto a la base de datos
def agregarProducto(request):
    # Obtiene los valores del formulario de la petición
    v_sku = request.POST['txtSku']
    v_precio = request.POST['nPrecio']
    v_nombre = request.POST['txtNombre']
    v_cantidad = request.POST['nCantidad']
    v_descripcion = request.POST['txtDescripcion']
    v_img = request.FILES['txtImg']
    v_categoria = Categoria.objects.get(id_categoria = request.POST['cmbCategoria'])
    # Crea el nuevo producto en la base de datos
    Producto.objects.create(sku = v_sku,nombre = v_nombre,stock = v_cantidad,precio = v_precio,descripcion = v_descripcion, id_categoria = v_categoria, imagen_url = v_img)        
    return redirect('/agregarProducto')

# Función para cargar la página de editar producto
def cargarEditarProducto(request,sku):
    # Obtiene el producto y todas las categorías de la base de datos
    productos = Producto.objects.get(sku = sku)
    categorias = Categoria.objects.all()
    return render(request,"editarProducto.html",{"prod":productos,"cate":categorias})

# Función para editar un producto en la base de datos
def editarProducto(request):
    # Obtiene los valores del formulario de la petición
    v_sku = request.POST['txtSku']
    productoBD = Producto.objects.get(sku = v_sku)
    v_nombre = request.POST['txtNombre']
    v_stock = request.POST['txtStock']
    v_precio = request.POST['txtPrecio']
    v_descripcion = request.POST['txtDescripcion']
    v_categoria = Categoria.objects.get(id_categoria = request.POST['cmbCategoria'])
    try:
        v_img = request.FILES['txtImg']
        ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(productoBD.imagen_url))
        os.remove(ruta_imagen)
    except:
        v_img = productoBD.imagen_url
    # Actualiza el producto en la base de datos
    productoBD.nombre = v_nombre
    productoBD.stock = v_stock
    productoBD.precio = v_precio
    productoBD.descripcion = v_descripcion
    productoBD.imagen_url = v_img
    productoBD.id_categoria = v_categoria
    productoBD.save()
    return redirect('/agregarProducto')

# Función para eliminar un producto de la base de datos
def eliminarProducto(request,sku):
    # Obtiene el producto de la base de datos
    producto = Producto.objects.get(sku = sku)
    ruta_imagen = os.path.join(settings.MEDIA_ROOT, str(producto.imagen_url))
    os.remove(ruta_imagen)
    # Elimina el producto de la base de datos
    producto.delete()
    # Redirige al usuario a la página de agregar producto
    return redirect('/agregarProducto')

# Función para agregar un producto al carrito
def agregarAlCarrito(request):
    sku = request.POST.get('sku')  # Esto debería capturar el SKU correctamente

    if not sku:
        # Si no hay SKU, puedes decidir qué hacer, quizás redirigir o mostrar un error
        return HttpResponse('SKU requerido.', status=400)

    try:
        producto = Producto.objects.get(sku=sku)
        if producto.stock > 0:
            # Añade el producto al carrito
            carrito = request.session.get('carrito', {})
            carrito[sku] = carrito.get(sku, 0) + 1
            request.session['carrito'] = carrito
            return redirect('carroCompras')
        else:
            return HttpResponse('Producto agotado.', status=400)
    except Producto.DoesNotExist:
        return HttpResponse('Producto no encontrado.', status=404)


# Función para verificar el stock de un producto
def verificar_stock(request):
    sku = request.GET.get('sku')
    cantidad = request.GET.get('cantidad')
    try:
        producto = Producto.objects.get(sku=sku)
        stock_disponible = producto.stock >= int(cantidad)
        # Devuelve si hay stock disponible o no
        return JsonResponse({'stock_disponible': stock_disponible})
    except Producto.DoesNotExist:
        return JsonResponse({'error': 'El producto no existe.'})

# Función para procesar el pago

def procesarPago(request):
    carrito = request.session.get('carrito', {})

    for sku, cantidad in carrito.items():
        try:
            producto = Producto.objects.get(sku=sku)
            if producto.stock >= cantidad:
                producto.stock -= cantidad
                producto.save()
            else:
                return HttpResponse('No hay suficiente stock disponible.', status=400)

        except Producto.DoesNotExist:
            return HttpResponse('El producto no existe.', status=400)

    request.session['carrito'] = {}
    return redirect('carroCompras')


def api_productos(request):
    productos = Producto.objects.all()
    lista_productos = list(productos.values())  # convierte el QuerySet en una lista de diccionarios
    return JsonResponse(lista_productos, safe=False)
