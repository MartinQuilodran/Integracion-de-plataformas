
function actualizarCarroCompras() {
    window.location.reload();
}

function agregarAlCarrito() {
    // Obtener el SKU y la cantidad del formulario
    var sku = document.getElementById('sku').value;
    var cantidad = document.getElementById('cantidad').value;

    // Realizar una solicitud AJAX para verificar el stock disponible
    $.ajax({
        url: '/verificar_stock/',
        type: 'GET',
        data: {
            'sku': sku,
            'cantidad': cantidad
        },
    });
}

$(".Cantidad").change(function() {
    var $row = $(this).closest('tr');
    var precioText = $row.find('.precio').text();
    var precio = parseFloat(precioText.replace('$', ''));
    var cantidad = parseInt($(this).val());

    console.log("Precio: " + precio);
    console.log("Cantidad: " + cantidad);

    if (isNaN(cantidad) || cantidad < 0) {
        cantidad = 0;
        $(this).val(cantidad);
    }

    var nuevoSubtotal = parseFloat(precio * cantidad).toFixed(0);
    console.log("Nuevo Subtotal: " + nuevoSubtotal);
    $row.find('.subtotal').text('$' + nuevoSubtotal);

    var nuevoTotal = 0;
    $(".subtotal").each(function() {
        var subtotal = parseFloat($(this).text().replace('$', ''));
        console.log("Subtotal: " + subtotal);
        nuevoTotal += subtotal;
    });

    nuevoTotal = parseFloat(nuevoTotal).toFixed(0);
    console.log("Nuevo Total: " + nuevoTotal);

    if (nuevoTotal < 0) {
        nuevoTotal = 0;
    }

    $(".total").text('$' + nuevoTotal);
});


