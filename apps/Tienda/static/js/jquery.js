//FILTRAR POR SKU
$(function(){
    $("#btnBuscar").on('click', function(){
        let valor = $("#buscar").val().toLowerCase();
        $("table tbody tr").filter(function(){
            $(this).toggle($(this).find('td:eq(1)').text().toLowerCase().indexOf(valor) > -1);
            //.find('td:eq(1)') FILTRAR POR NUMERO DE COLUMNA (SKU)
        })
    })
})

var botonesEliminar = document.querySelectorAll("table #eliminar");

botonesEliminar.forEach(function(boton) {
  boton.addEventListener("click", function() {
    var fila = boton.parentNode.parentNode;
    fila.parentNode.removeChild(fila);
  });
});


$("#eliminar").on("click",function(){
    $(".descuento").slideUp();
})

$(document).ready(function() {
  var confirmDeleteButton = document.getElementById('confirmDelete');
  var deleteButtons = document.querySelectorAll('.delete-btn');
  
  deleteButtons.forEach(function(button) {
    button.addEventListener('click', function(e) {
      e.preventDefault();
      var sku = this.dataset.sku;
      confirmDeleteButton.href = "/eliminarProducto/" + sku;
      var modal = new bootstrap.Modal(document.getElementById('confirmModal'));
      modal.show();
    });
  });
});

window.onload = function() {
  var precioElementos = document.getElementsByClassName('precio-destacado');

  for(var i = 0; i < precioElementos.length; i++){
      var precio = precioElementos[i].innerHTML.replace("$", "");
      precio = parseFloat(precio);
      precio = precio.toLocaleString();
      precioElementos[i].innerHTML = "$" + precio;
  }
}
