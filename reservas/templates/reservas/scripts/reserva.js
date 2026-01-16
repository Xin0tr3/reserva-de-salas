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

document.addEventListener('DOMContentLoaded', function() {
    cargarSalas();
    configurarEventosNavegacion();
});


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

function seleccionarSala(salaId) {
    const sala = salas[salaId];
    if (!sala) return;

    estadoReserva.salaSeleccionada = salaId;
    estadoReserva.salaData = sala;
    estadoReserva.invitados = []; //Sirve para resetear invitados en caso de cambiar sala

    documentquerySelectorAll('.sala-btn').forEach(btn => {
        btn.classList.remove('seleccionado');
    });
    document.querySelector(`[data-sala-id="${salaId}"]`).classList.add('seleccionado');

    document.getElementById('nombre-sala-seleccionada').textContent = sala.nombre_sala;
    document.getElementById('capacidad-sala-seleccionada').textContent = sala.capacidad_maxima;
    document.getElementById('horario-sala').textContent = `${sala.hora_minima} - ${sala.hora_maxima}`;

    configurarFlatpickr(sala);

    mostrarPaso(2);

}

function configurarFlatpickr(sala){

    const [horaMinHH, horaMinMM] = sala.hora_minima.split(':');
    const [horaMaxHH, horaMaxMM] = sala.hora_maxima.split(':');
    
    const config = {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        minDate: "today",
        time_24hr: true,
        minuteIncrement: 30,
        minTime: sala.hora_minima,
        maxTime: sala.hora_maxima,
        locale: {
            firstDayOfWeek: 1
        }
    }

    if (salasInstancias['inicio']) salasInstancias['inicio'].destroy();
    if (salasInstancias['termino']) salasInstancias['termino'].destroy();

    salasInstancias['inicio'] = flatpickr('#fecha-inicio', {
        ...config,
        onChange: (selectedDates) => {
            if (selectedDates.length > 0) {
                estadoReserva.fechaInicio = selectedDates[0];
                obtenerHorasDisponibles(selectedDates[0]);
            }
        }
    });

    salasInstancias['termino'] = flatpickr('#fecha-termino', {
        ...config
    });
}

async function obtenerHorasDisponibles(fechaSeleccionada){
    const sala = estadoReserva.salaData;
    const salaId = estadoReserva.salaSeleccionada;

    const fechaStr = fechaSeleccionada.toISOString().split('T')[0];

    const [horaMinStr, minMinStr] = sala.hora_minima.split(':');
    const [horaMaxStr, minMaxStr] = sala.hora_maxima.split(':');
    const horaMin = parseInt(horaMinStr);
    const horaMax = parseInt(horaMaxStr);

    let horasDisponibles = [];
    let horasOcupadas = [];

    for (let hora = horaMin; hora < horaMax; hora++) {
        const horaInicio = `${String(hora).padStart(2, '0')}:00`;
        const horaTermino = `${String(hora + 1).padStart(2, '0')}:00`;

        try {
            const response = await fetch(
                `${API_BASE}/salas/?fecha=${fechaStr}&hora_inicio=${horaInicio}&hora_termino=${horaTermino}`
            );
            const salasDisponibles = await response.json();

            // Buscar si nuestra sala está en las disponibles
            const salaEstaDisponible = salasDisponibles.some(s => s.id == salaId);

            if (salaEstaDisponible) {
                horasDisponibles.push({ hora, horaStr: horaInicio });
            } else {
                horasOcupadas.push({ hora, horaStr: horaInicio });
            }
        } catch (error) {
            console.error('Error consultando disponibilidad:', error);
        }
    }
    mostrarHorasDisponibles(horasDisponibles, horasOcupadas, fechaStr);

}

function mostrarHorasDisponibles(horasDisponibles, horasOcupadas, fechaStr){
    const contenedor = document.getElementById('horas-disponibles');

    const fechaObj = new Date(fechaStr);
    const fechaFormato = fechaObj.toLocateDateString('es-Cl', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    let html = `<h4>Horas disponibles para ${fechaFormato}</h4>`;
    html += `<div class="horas-grid">`;

    const sala = estadoReserva.salaData;
    const [horaMinStr] = sala.hora_minima.split(':');
    const [horaMaxStr] = sala.hora_maxima.split(':');
    const horaMin = parseInt(horaMinStr);
    const horaMax = parseInt(horaMaxStr);

    for (let hora = horaMin; hora < horaMax; hora++) {
        const horaStr = `${String(hora).padStart(2, '0')}:00`;
        const disponible = horasDisponibles.some(h => h.horaStr === horaStr);

        if (disponible) {
            html += `
                <button class="hora-disponible" data-hora="${horaStr}" onclick="seleccionarHora('${horaStr}')">
                    ${horaStr}
                </button>
            `;
        } else {
            html += `
                <button class="hora-no-disponible" disabled title="No disponible">
                    ${horaStr}
                </button>
            `;
        }
    }

    html += '</div>';
    contenedor.innerHTML = html;
}

function seleccionarHora(horaInicio) {
    const [hh, mm] = horaInicio.split(':');
    const horaTermino = `${String(parseInt(hh) + 1).padStart(2, '0')}:${mm}`;

    const fecha = document.getElementById('fecha-inicio').value.split(' ')[0];

    const fechaInicioCompleta = `${fecha} ${horaInicio}`;
    const fechaTerminoCompleta = `${fecha} ${horaTermino}`;

    document.getElementById('fecha-inicio').value = fechaInicioCompleta;
    document.getElementById('fecha-termino').value = fechaTerminoCompleta;

    estadoReserva.fechaInicio = new Date(`${fecha}T${horaInicio}`);
    estadoReserva.fechaTermino = new Date(`${fecha}T${horaTermino}`);

    console.log('Hora seleccionada:', fechaInicioCompleta, '-', fechaTerminoCompleta);
}

let contadorInvitados = 0;

document.addEventListener('click', function(e){
    if (e.target && e.target.id === 'agregar-invitado') {
        e.preventDefault();
        agregarInvitado();
    }

    if (e.target && e.target.classList.contains('btn-eliminar-invitado')) {
        e.preventDefault();
        eliminarInvitado(e.target.dataset.invitadoId);
    }
});

function agregarInvitado(){
    const sala = estadoReserva.salaData;
    const capacidadDisponible = sala.capacidad_maxima - estadoReserva.invitados.length;

    if (capacidadDisponible <= 0){
        alert(`No puedes agregar más invitados. Limite: ${sala.capacidad_maxima} personas`);
        return;
    }

    const invitadoId = contadorInvitados++;
    const htmlInvitado = `
        <div class="invitado-card" id="invitado-${invitadoId}" data-invitado-id="${invitadoId}">
            <h4>Invitado ${invitadoId + 1}</h4>
            
            <label>Nombre:</label>
            <input type="text" class="nombre-invitado" placeholder="Nombre" data-invitado-id="${invitadoId}">
            
            <label>Apellidos:</label>
            <input type="text" class="apellidos-invitado" placeholder="Apellidos" data-invitado-id="${invitadoId}">
            
            <label>Rol:</label>
            <select class="rol-invitado" data-invitado-id="${invitadoId}">
                <option value="FUNCIONARIO">Funcionario</option>
                <option value="ACADEMICO">Académico</option>
                <option value="ALUMNO">Alumno</option>
            </select>
            
            <label>Carrera:</label>
            <input type="text" class="carrera-invitado" placeholder="Carrera (opcional)" data-invitado-id="${invitadoId}">
            
            <label>Facultad:</label>
            <input type="text" class="facultad-invitado" placeholder="Facultad (opcional)" data-invitado-id="${invitadoId}">
            
            <label>Sexo:</label>
            <select class="sexo-invitado" data-invitado-id="${invitadoId}">
                <option value="SIN ESPECIFICAR">Sin especificar</option>
                <option value="HOMBRE">Hombre</option>
                <option value="MUJER">Mujer</option>
            </select>
            
            <button type="button" class="btn-eliminar-invitado" data-invitado-id="${invitadoId}">Eliminar</button>
        </div>
    `;

    document.getElementById('contenedor-invitados'). insertAdjacentHTML('beforeend', htmlInvitado);
    actualizarCapacidadRestante();
}

function eliminarInvitado(invitadoId){
    document.getElementById(`invitado-${invitadoId}`).remove();
    estadoReserva.invitados = estadoReserva.invitados.filter(inv => inv.id != invitadoId);
    actualizarCapacidadRestante();
}

function actualizarCapacidadRestante(){
    const sala = estadoReserva.salaData;
    const invitadosActuales = document.querySelectorAll('.invitado-card').length;
    const capacidadRestante = sala.capacidad_maxima - invitadosActuales;
    document.getElementById('capacidad-restante').textContent = capacidadRestante;
}

function recolectarInvitados(){
    const invitadosDOM = document.querySelectorAll('.invitado-card');
    estadoReserva.invitados = [];

    invitadosDOM.forEach((card, index) => {
        const nombre = card.querySelector('.nombre-invitado').value.trim();
        const apellidos = card.querySelector('.apellidos-invitado').value.trim();
        const rol = card.querySelector('.rol-invitado').value.trim();
        const carrera = card.querySelector('.carrera-invitado').value.trim();
        const facultad = card.querySelector('.facultad-invitado').value.trim();
        const sexo =  card.querySelector('.sexo-invitado').value.trim();

        if (nombre && apellidos){
            estadoReserva.invitados.push({
                nombre_invitado: nombre,
                apellidos_invitado: apellidos,
                rol: rol,
                carrera: carrera,
                facultad: facultad,
                sexo: sexo
            });
        }
    });

    return estadoReserva.invitados;
}

function mostrarResumen(){
    const sala = salaReserva.salaData;
    const resumenHTML = `
    <div class="resumen-section">
        <h3>Informacion de la reserva</h3>
        <p><strong>Sala:</strong>${sala.nombre_sala}</p>
        <p><strong>Fecha inicio:</strong>${estadoReserva.fechaInicio.toLocaleString('es-CL')}</p>
        <p><strong>Fecha termino:</strong>${estadoReserva.fechaTermino.toLocaleString('es-CL')}</p>
        <p><strong>Evento:</strong>${document.getElementById('tevento').value}</p>
        <p><strong>Descripcion:</strong>${document.getElementById('devento').value}</p>
    </div>

    <div class="resumen-section">
        <h3>Informacion del reservante</h3>
        <p><strong>Nombre:</strong>${document.getElementById('nusuario').value}</p>
        <p><strong>Departamento:</strong>${document.getElementById('depto').value}</p>
        <p><strong>Correo:</strong>${document.getElementById('correo').value}</p>
        <p><strong>RUT:</strong>${document.getElementById('rut').value}</p>
        <p><strong>Equipamiento extra:</strong>${document.getElementById('equip').value}</p>
    </div>

    <div class="resumen-section">
        <h3>Invitados (${estadoReserva.invitados.length})</h3>
        ${estadoReserva.invitados.length > 0 ? `
            <ul>
            ${estadoReserva.invitados.map(inv => 
                `<li> ${inv.nombre_invitado} ${inv.apellidos_invitado} (${inv.rol})<li>`
            ).join('')}
        </ul>
        ` : '<p>Sin invitados</p>}'}
        
    </div>
    `;
    document.getElementById('resumen-reserva').innerHTML = resumenHTML;
}

// Validaciones

function validarPaso3(){
    const tevento = document.getElementById('tevento').value.trim();
    const devento = document.getElementById('devento').value.trim();
    const nusuario = document.getElementById('nusuario').value.trim();
    const depto = document.getElementById('depto').value.trim();
    const correo = document.getElementById('correo').value.trim();
    const rut = document.getElementById('rut').value.trim();

    if(!tevento){
        alert('Por favor ingrese titulo del evento.');
        return false;
    }
    if(!devento){
        alert('Por favor ingrese descripcion del evento.');
        return false;
    }
    if(!nusuario){
        alert('Por favor ingrese nombre del reservante.');
        return false;
    }
    if(!depto){
        alert('Por favor ingrese departamento.');
        return false;
    }
    if(!correo || !validarEmail(correo)){
        alert('Por favor ingrese correo del reservante.');
        return false;
    }
    if(!rut || !validarRut(rut)){
        alert('Por favor ingrese RUT del reservante.');
        return false;
    }
    return true;
}

function validarEmail(email){
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(email);
}

function validarRut(rut){
    const rutSinFormato = rut.replace(/[\.\-]/g, '');
    return rutSinFormato.length >= 8 && rutSinFormato.length <= 9;
}

// Navegacion

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
    
    //Paso 1 al paso 2
    document.getElementById('siguiente-paso-1').addEventListener('click', function(){
        if (!estadoReserva.salaSeleccionada){
            alert('Por favor seleccione una sala.');
            return;
        }
        mostrarPaso(2);
    });

    //Paso 2 al paso 1
    document.getElementById('volver-paso-1').addEventListener('click', function(){
        mostrarPaso(1);
    });
        
    //Paso 2 al paso 3
    document.getElementById('siguiente-paso-2').addEventListener('click', function(){
        if (!estadoReserva.fechaInicio || !estadoReserva.fechaTermino){
            alert('Por favor seleccione una fecha y hora.');
            return;
        }
        mostrarPaso(3);
        actualizarCapacidadRestante();
    });

    //Paso 3 al paso 2
    document.getElementById('volver-paso-2').addEventListener('click', function(){
        mostrarPaso(2);
    });

    //Paso 3 al paso 4
    document.getElementById('siguiente-paso-3').addEventListener('click', function(){
        if (!validarPaso3()) {
            return;
        }
        recolectarInvitados();
        mostrarResumen();
        mostrarPaso(4);
    });

    //Paso 4 al paso 3
    document.getElementById('volver-paso-3').addEventListener('click', function(){
        mostrarPaso(3);
    });

    //Paso 4 - Confirmar
    document.getElementById('confirmar-reserva').addEventListener('click', function(){
        confirmarReserva();
    });
}

async function confirmarReserva(){
    const boton = document.getElementById('confirmar-reserva');
    boton.disabled = true;
    boton.textContent = 'Confirmando...';

    const payload = {
        hora_inicio: estadoReserva.fechaInicio.toISOString(),
        hora_termino: estadoReserva.fechaTermino.toISOString(),
        nombre_reservante: document.getElementById('nusuario').value,
        departamento: document.getElementById('depto').value,
        email: document.getElementById('correo').value,
        nombre_evento: documento.getElementById('tevento').value,
        descripcion_evento: document.getElementById('devento').value,
        equipamiento_extra: document.getElementById('equip').value,
        rut: document.getElementById('rut').value,
        sala_reservada: estadoReserva.salaSeleccionada,
        invitados: estadoReserva.invitados
    };
    
    try {
        const response = await fetch(`${API_BASE}/reservar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload)
        });

        if (response.ok) {
            const data = await response.json();
            mostrarExito(data);
        } else {
            const errores = await response.json();
            mostrarErrores(errores);
            boton.disabled = false;
            boton.textContent = 'Confirmar Reserva';
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error al enviar la reserva, intente de nuevo');
        boton.disabled = false;
        boton.textContent = 'Confirmar Reserva';
    }
}

function mostrarExito(data){
    document.getElementById('codigo-reserva').textContent = reserva.codigo;
    document.getElementById('correo-confirmacion').textContent = reserva.email;
    mostrarPaso(5);
}   

function mostrarErrores(errores){
    let mensajeError = 'Errores en la reserva: \n';

    if (typeof errores === 'object'){
        for (let [campo,mensajes] of Object.entries(errores)){
            if (Array.isArray(mensajes)){
                mensajeError += `\n${campo}: ${mensajeError.join(', ')}`;
            } else {
                mensajeError += `\n${campo}: ${mensajes}`;
            }
        }
    } else {
        mensajeError += errores;
    }
    alert(mensajeError);
}
