let estadoReserva = {
    salaSeleccionada: null, // ID de la sala seleccionada
    salaData: null, //Objeto de la sala seleccionada
    horaInicio: null,
    horaTermino: null,
    invitados: [],
};

let salas = {}; //Almacena la info de todas las salas 
let salasInstancias = {} //Almacena instancias de flatpickr;

const API_BASE = '/api/v1/';

function cargarSalas() {
    fetch(`${API_BASE}/salas/`)
        .then(response => response.json())
        .then(salaLista => {
            const gridSalas = document.getElementById('salas-grid');
            gridSalas.innerHTML = '';

            salaLista.forEach(sala => {
                salas[sala.id] = sala; //Guardar info de la sala

                //Crear botón de sala
                const salaR = document.createElement('a');
                salaR.href = '#';
                salaR.className = 'btn-1 sala-btn';
                salaR.dataset.salaId = sala.id;
                salaR.innerHTML = `
                <div class="sala-info">
                    <strong>${sala.nombre_sala}</strong><br>
                    <small>Capacidad: ${sala.capacidad}</small>
                </div>
                `;
                
                salaR.addEventListener('click', (e) => {
                    e.preventDefault();
                    seleccionarSala(sala.id);
                });
                
                gridSalas.appendChild(salaR);
            });
    })
    .catch(error => {console.error('Error al cargar salas:', error);});
}

// Usar para flatpickr, faltan variables y que sea dinamico
const config = {
    minMaxTime: {
        enableTime: true,
        minDate: "today",
        minTime: "08:00",
        maxTime: "16:00",
    }
};
flatpickr("[data-id=minMaxTime]", config.minMaxTime);