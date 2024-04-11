console.log("tamalo");



$(function(){
    $("#formularioRegistro").validate({
        rules:{
            txtUsuario:{
                required: true,
                minlength:5
            },
            txtNombre:{
                required: true,
                minlength:5
            },
            txtApellido:{
                required: true,
                minlength:5
            },
            txtPassword:{
                required: true,
                minlength:5
            },
            txtCorreo:{
                required: true,
                minlength:5,
                email: true
            }
        },
        messages:{
            txtUsuario:{
                required: "Debe ingresar un usuario",
                minlength: "El largo mínimo es 5"
            },
            txtNombre:{
                required: "Debe ingresar un nombre",
                minlength: "El largo mínimo es 5"
            },
            txtApellido:{
                required: "Debe ingresar un apellido",
                minlength: "El largo mínimo es 5"
            },
            txtUsuario:{
                required: "Debe ingresar un usuario",
                minlength: "El largo mínimo es 5"
            },
            txtCorreo:{
                required: "Debe ingresar un correo",
                minlength: "El largo mínimo es 5"
            },
            txtPassword:{
                required: "Debe ingresar un contraseña",
                minlength: "El largo mínimo es 5"
            }
        }
    })
})