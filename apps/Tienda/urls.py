from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.inicio),
    path('agregarProducto', views.cargarAgregarProducto),
    path('agregarProductoForm', views.agregarProducto),
    path('editarProducto/<sku>', views.cargarEditarProducto),
    path('editarProductoForm', views.editarProducto),
    path('eliminarProducto/<sku>', views.eliminarProducto),
    path('teclados', views.teclados),
    path('carrocompras', views.carroCompras, name='carroCompras'),
    path('switches', views.switches),
    path('agregar_al_carrito', views.agregarAlCarrito, name='agregar_al_carrito'),
    path('procesar_pago', views.procesarPago, name='procesar_pago'),
    path('api/productos/', views.api_productos, name='api_productos'),
    path('registro/', views.registro, name='registro'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('cerrar_sesion/', views.cerrar_sesion, name='cerrar_sesion'),
    path('producto/<int:sku>/', views.detalle_producto, name='detalle_producto'),
    path('iniciar_pago/', views.iniciar_pago, name='iniciar_pago'),
    path('confirmar_pago/', views.confirmar_pago, name='confirmar_pago'),
]

def registro(request):
    # ... (resto de la vista)
    return redirect('inicio_sesion')  # Redirige a 'inicio_sesion'