
//Validamos formulario con jQuery validate

$(function(){
    $("#mis-datos2").validate({ 
        rules:{
            nom:{
                required:true
            },
            ape:{
                required:true
            },
            rut:{
                required:true
            },
            telefono:{
                required:true
            },
            fallo:{
                required:true
            },
        },//Rules
        messages:{
            nom:{
                required:'Ingrese su Nombre..',
                minlength:'Caracteres Insuficientes, mínimo 3..',
            },
            ape:{
                required:'Ingrese su Apellido..',
                minlength:'Caracteres Insuficientes, mínimo 3..'
            },
            rut:{
                required:'Ingrese su Rut con Guion antes del penultimo número..',
                minlength:'Caracteres Insuficientes, mínimo 10..'
            },
            telefono:{
                required:'Ingrese un número de teléfono..',
                minlength:'Caracteres insuficientes, mínimo 8..'
            },
            fallo:{
                required:'Seleccione un tipo de fallo..'
            },
        },//Mesagges
    })
});//Fin Validate