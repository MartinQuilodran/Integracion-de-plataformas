const formulario = document.getElementById("agregarProductoForm");

formulario.addEventListener('submit', function(evento){
    evento.preventDefault();

    if (document.getElementById("txtSku").value.length == 0) {
        alert("Debe ingresar el codigo del producto.");
        return;
    }else{
        this.submit();
    }


})
