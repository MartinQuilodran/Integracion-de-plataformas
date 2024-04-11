function validarFormulario() {
    let txtUsuario = document.getElementById("id_username").value;

    if (txtUsuario.length == 0) {
        document.getElementById("valUsuario").style.display = "inline";
        document.getElementById("id_username").classList.add("is-invalid");
    } else {
        document.getElementById("id_username").classList.remove("is-invalid");
        document.getElementById("id_username").classList.add("is-valid");
        document.getElementById("valUsuario").style.display = "none";
    }
}

function password() {
    let input = document.getElementById("id_password");

    if (input.type == "password") {
        input.type = "text";
        document.getElementById("mostrar").style.display = "inline";
        document.getElementById("ocultar").style.display = "none";
    } else {
        input.type = "password";
        document.getElementById("mostrar").style.display = "none";
        document.getElementById("ocultar").style.display = "inline";
    }
}

document.addEventListener('DOMContentLoaded', (event) => {
    document.getElementById("valUsuario").style.display = "none";

    document.getElementById("id_username").addEventListener('blur', validarFormulario);
    document.getElementById("button-addon2").addEventListener('click', password);
});
