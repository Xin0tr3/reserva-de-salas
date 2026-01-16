let estadoReserva = {
    salaSeleccionada: null, // ID de la sala seleccionada
    salaData: null, //Objeto de la sala seleccionada
};

let salas = {}; //Almacena la info de todas las salas 
let salasInstancias = {} //Almacena instancias de flatpickr;

const API_BASE = '/api/v1/';

document.addEventListener('DOMContentLoaded', function() {
    configurarEventosNavegacion();
});

function mostrarPaso(numeroPaso){
    document.querySelectorAll('.paso').forEach(paso => {
        paso.classList.add('oculto');
        paso.classList.remove('activo');
    });

    const pasoActual = document.getElementById(`paso-${numeroPaso}`);
    pasoActual.classList.remove('oculto');
    pasoActual.classList.add('activo');

    window.scrollTo(0, 0);
}

function configurarEventosNavegacion(){
    document.getElementById('siguiente-paso-1').addEventListener('click', function(){
        if (!validarPaso1() || !buscarReserva()){
            return;
        }
        mostrarPaso(2);
    });

    document.getElementById('volver-paso-1').addEventListener('click', function(){
        mostrarPaso(1);
    });

    document.getElementById('confirmar-cancelacion').addEventListener('click', function(){
        cancelarReserva();
    })
}

function validarPaso1(){
    const codigoReserva = document.getElementById('codigo-cancelacion').value.trim();
    if (!codigoReserva){
        alert('Ingrese un codigo de reserva');
        return false;
    }
    return true;
}

function buscarReserva(){
    const codigoReserva = document.getElementById('codigo-cancelacion').value.trim();

    return fetch(`${API_BASE}reservas/${codigoReserva}/`, {
        method: 'GET'
    })
    .then(response => {
        if (response.status === 404){
            alert('Reserva no encontrada. Verifique el codigo ingresado.');
            return null;
        }
        if (!response.ok){
            alert('Error al buscar la reserva.');
            return null;
        }
        return response.json();
    })
    .then(reserva =>{
        if (reserva){
            mostrarResumen(reserva);
            return true;
        }
        return false;
    })
    .catch(error => {
        alert('Error al buscar la reserva.');
        return false;
    });
}

async function cancelarReserva(){
    const codigoReserva = document.getElementById('codigo-cancelacion').value.trim();

    const response = await fetch(`${API_BASE}reservas/${codigoReserva}/`, {
        method: 'DELETE'
    });

    if (response.ok || response.status === 204){
        alert('Reserva cancelada con exito');
        window.location.href = '/';
    } else {
        const error = await response.json();
        alert(`Error al cancelar la reserva: ${error.message}`);
    }
}

function mostrarResumen(reserva){
    const resumenHTML = `
    <p><strong>Sala:</strong>${reserva.sala_reservada.nombre_sala}</p>
    <p><strong>Evento:</strong>${reserva.nombre_evento}</p>
    <p><strong>Fecha inicio:</strong>${new Date(reserva.hora_inicio).toLocaleString('es-CL')}</p>
    <p><strong>Fecha término:</strong>${new Date(reserva.hora_termino).toLocaleString('es-CL')}</p>
    <p><strong>Reservante:</strong>${reserva.nombre_reservante}</p>
    <p><strong>Invitados:</strong> ${reserva.invitados.length}</p>
`;
    document.getElementById('resumen-reserva-cancelar').innerHTML = resumenHTML;
}