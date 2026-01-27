// Variables globales
let lista = [];
let TIPO_GESTION = '';
let PAGINA_ACTUAL = 1;
let ITEMS_POR_PAGINA = 10;
let ITEM_SELECCIONADO = null;

const API_BASE = '/api/v1/';

const CONFIG = {
    'reservas': {
        'endpoint': '/api/v1/admin/reservas/',
        'contenedor': 'contenedor-reservas',
        'detalles': 'detalles-reservas',
        'campos': ['nombre_evento', 'sala_reservada', 'hora_inicio', 'estado_reserva'],
        'mostrarExcel': true,
        'mostrarCalendario': true
    },
    'salas': {
        'endpoint': '/api/v1/admin/salas/',
        'contenedor': 'contenedor-salas',
        'detalles': 'detalles-salas',
        'campos': ['nombre_sala', 'capacidad_maxima', 'hora_minima'],
        'mostrarExcel': false,
        'mostrarCalendario': false
    },
    'usuarios': {
        'endpoint': '/api/v1/admin/usuarios/',
        'contenedor': 'contenedor-usuario',
        'detalles': 'detalles-usuario',
        'campos': ['username', 'email', 'first_name', 'last_name'],
        'mostrarExcel': false,
        'mostrarCalendario': false
    }
};

document.addEventListener('DOMContentLoaded', function() {
    // Detectar tipo de gestión según los IDs presentes
    if (document.getElementById('contenedor-salas')) {
        TIPO_GESTION = 'salas';
    } else if (document.getElementById('contenedor-usuario')) {
        TIPO_GESTION = 'usuarios';
    } else if (document.getElementById('contenedor-reservas')) {
        TIPO_GESTION = 'reservas';
    }

    if (TIPO_GESTION) {
        cargarItems(TIPO_GESTION);
        configurarEventosNavegacion();
    }
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function cargarItems(gestion) {
    const endpoint = CONFIG[gestion].endpoint;
    
    fetch(endpoint, {credentials: 'include'})
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error, status: ${response.status}`);
            }
            return response.json();
        })
        .then(datos => {
            lista = datos;
            mostrarPagina(1);
            generarPaginacion();
        })
        .catch(error => {
            console.error('Error al cargar items:', error);
            alert('Error al cargar los datos');
        });
}

function mostrarPagina(numeroPagina) {
    PAGINA_ACTUAL = numeroPagina;
    const inicio = (numeroPagina - 1) * ITEMS_POR_PAGINA;
    const fin = inicio + ITEMS_POR_PAGINA;
    const itemsPagina = lista.slice(inicio, fin);

    renderizarItems(itemsPagina);
    window.scrollTo(0, 0);
}

function renderizarItems(items) {
    const config = CONFIG[TIPO_GESTION];
    const contenedor = document.getElementById(config.contenedor);
    
    if (items.length === 0) {
        contenedor.innerHTML = '<p>No hay items para mostrar</p>';
        return;
    }

    let html = '<table class="tabla-gestion"><thead><tr>';
    
    // Encabezados
    const campos = config.campos;
    campos.forEach(campo => {
        html += `<th>${campo.replace(/_/g, ' ').toUpperCase()}</th>`;
    });
    html += '<th>ACCIONES</th></tr></thead><tbody>';

    // Filas
    items.forEach(item => {
        html += '<tr>';
        
        campos.forEach(campo => {
            let valor = item[campo];
            
            if (campo === 'hora_inicio' && valor) {
                valor = new Date(valor).toLocaleString('es-CL');
            } else if (campo === 'sala_reservada' && typeof valor === 'object' && valor !== null) {
                valor = valor.nombre_sala || valor.id;
            } else if (campo === 'hora_minima' && valor) {
                valor = valor;
            }
            
            html += `<td>${valor || '-'}</td>`;
        });
        
        html += '<td class="acciones">';
        html += `<button class="btn-ver" data-id="${item.id}" data-codigo="${item.codigo || ''}">Ver</button>`;
        html += `<button class="btn-editar" data-id="${item.id}" data-codigo="${item.codigo || ''}">Editar</button>`;
        html += `<button class="btn-eliminar" data-id="${item.id}" data-codigo="${item.codigo || ''}">Eliminar</button>`;
        
        // Botones especiales para reservas
        if (TIPO_GESTION === 'reservas') {
            html += `<button class="btn-excel" data-codigo="${item.codigo}">Excel</button>`;
            html += `<button class="btn-calendario" data-codigo="${item.codigo}">Calendario</button>`;
        }
        
        html += '</td></tr>';
    });

    html += '</tbody></table>';
    contenedor.innerHTML = html;

    // Agregar event listeners a los botones
    agregarEventosBotones();
}

function generarPaginacion() {
    const totalPaginas = Math.ceil(lista.length / ITEMS_POR_PAGINA);
    const contenedorPaginacion = document.getElementById('paginacion');
    
    if (totalPaginas <= 1) {
        contenedorPaginacion.innerHTML = '';
        return;
    }

    let html = '<div class="botones-paginacion">';
    
    // Mostrar seleccionado ± 1
    const mostrarAntes = PAGINA_ACTUAL > 1 ? PAGINA_ACTUAL - 1 : null;
    const mostrarDespues = PAGINA_ACTUAL < totalPaginas ? PAGINA_ACTUAL + 1 : null;

    // Botón primera página
    if (PAGINA_ACTUAL > 2) {
        html += `<button class="btn-pagina" data-pagina="1">1</button>`;
        if (PAGINA_ACTUAL > 3) {
            html += '<span class="puntos">...</span>';
        }
    }

    // Página anterior
    if (mostrarAntes) {
        html += `<button class="btn-pagina" data-pagina="${mostrarAntes}">${mostrarAntes}</button>`;
    }

    // Página actual
    html += `<button class="btn-pagina activa" data-pagina="${PAGINA_ACTUAL}">${PAGINA_ACTUAL}</button>`;

    // Página siguiente
    if (mostrarDespues) {
        html += `<button class="btn-pagina" data-pagina="${mostrarDespues}">${mostrarDespues}</button>`;
    }

    // Botón última página
    if (PAGINA_ACTUAL < totalPaginas - 1) {
        if (PAGINA_ACTUAL < totalPaginas - 2) {
            html += '<span class="puntos">...</span>';
        }
        html += `<button class="btn-pagina" data-pagina="${totalPaginas}">${totalPaginas}</button>`;
    }

    html += '</div>';
    contenedorPaginacion.innerHTML = html;

    // Event listeners para paginación
    document.querySelectorAll('.btn-pagina').forEach(btn => {
        btn.addEventListener('click', function() {
            const pagina = parseInt(this.dataset.pagina);
            mostrarPagina(pagina);
            generarPaginacion();
        });
    });
}

function agregarEventosBotones() {
    // Botón Ver
    document.querySelectorAll('.btn-ver').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const item = lista.find(i => i.id === parseInt(id));
            mostrarDetalles(item, 'ver');
        });
    });

    // Botón Editar
    document.querySelectorAll('.btn-editar').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const item = lista.find(i => i.id === parseInt(id));
            mostrarDetalles(item, 'editar');
        });
    });

    // Botón Eliminar
    document.querySelectorAll('.btn-eliminar').forEach(btn => {
        btn.addEventListener('click', function() {
            const id = this.dataset.id;
            const codigo = this.dataset.codigo;
            const item = lista.find(i => i.id === parseInt(id));
            mostrarModalEliminacion(item, codigo);
        });
    });

    // Botón Excel (solo Reservas)
    document.querySelectorAll('.btn-excel').forEach(btn => {
        btn.addEventListener('click', function() {
            const codigo = this.dataset.codigo;
            window.location.href = `/api/v1/admin/reservas/${codigo}/excel/`;
        });
    });

    // Botón Calendario (solo Reservas)
    document.querySelectorAll('.btn-calendario').forEach(btn => {
        btn.addEventListener('click', function() {
            const codigo = this.dataset.codigo;
            window.location.href = `/api/v1/admin/reservas/${codigo}/calendario/`;
        });
    });
}

function mostrarDetalles(item, modo) {
    ITEM_SELECCIONADO = item;
    const config = CONFIG[TIPO_GESTION];
    const contenedorDetalles = document.getElementById(config.detalles);
    
    let html = '<div class="detalles-contenedor">';

    // Mostrar todos los campos del item
    for (const [clave, valor] of Object.entries(item)) {
        let etiqueta = clave.replace(/_/g, ' ').toUpperCase();
        let valorMostrado = valor;

        if (clave === 'hora_inicio' || clave === 'hora_termino') {
            valorMostrado = new Date(valor).toLocaleString('es-CL');
        } else if (clave === 'sala_reservada' && typeof valor === 'object' && valor !== null) {
            valorMostrado = valor.nombre_sala || valor.id;
        }

        if (modo === 'ver') {
            html += `<div class="campo-detalles"><label>${etiqueta}</label><p>${valorMostrado || '-'}</p></div>`;
        } else if (modo === 'editar') {
            html += `<div class="campo-editable"><label>${etiqueta}</label><input type="text" class="input-editar" data-campo="${clave}" value="${valorMostrado || ''}" ${clave === 'id' ? 'disabled' : ''}></div>`;
        }
    }

    html += '</div>';
    contenedorDetalles.innerHTML = html;
    mostrarPaso(2);
}

function mostrarModalEliminacion(item, codigo) {
    const modal = document.getElementById('modal-confirmacion');
    const tituloModal = document.getElementById('titulo-modal');
    const btnConfirmar = document.getElementById('btn-confirmar-eliminar');

    tituloModal.textContent = '¿Confirmas la eliminación?';
    
    btnConfirmar.onclick = function() {
        eliminarItem(item.id, codigo);
        cerrarModal();
    };

    modal.style.display = 'flex';
}

function cerrarModal() {
    document.getElementById('modal-confirmacion').style.display = 'none';
}

function eliminarItem(id, codigo) {
    const config = CONFIG[TIPO_GESTION];
    const endpoint = codigo ? 
        `${config.endpoint}${codigo}/` : 
        `${config.endpoint}${id}/`;

    fetch(endpoint, {
        method: 'DELETE',
        credentials: 'include',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        }
        })
        .then(response => {
            if (response.ok) {
                alert('Item eliminado correctamente');
                cargarItems(TIPO_GESTION);
                mostrarPaso(1);
            } else {
                alert('Error al eliminar el item');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al eliminar');
        });
}

function mostrarPaso(numeroPaso) {
    document.querySelectorAll('.paso').forEach(paso => {
        paso.classList.add('oculto');
        paso.classList.remove('activo');
    });

    const pasoActual = document.getElementById(`paso-${numeroPaso}`);
    if (pasoActual) {
        pasoActual.classList.remove('oculto');
        pasoActual.classList.add('activo');
    }

    window.scrollTo(0, 0);
}

function configurarEventosNavegacion() {
    // Botón Volver
    const btnVolver = document.getElementById('volver-paso-1');
    if (btnVolver) {
        btnVolver.addEventListener('click', function() {
            mostrarPaso(1);
        });
    }

    // Botón Guardar
    const btnGuardar = document.getElementById('guardar-cambios');
    if (btnGuardar) {
        btnGuardar.addEventListener('click', function() {
            guardarCambios();
        });
    }

    // Botón Cerrar Modal
    const btnCerrarModal = document.getElementById('btn-cerrar-modal');
    if (btnCerrarModal) {
        btnCerrarModal.addEventListener('click', cerrarModal);
    }

    // Cerrar modal al hacer clic fuera
    window.onclick = function(event) {
        const modal = document.getElementById('modal-confirmacion');
        if (event.target === modal) {
            cerrarModal();
        }
    };
}

function guardarCambios() {
    if (!ITEM_SELECCIONADO) {
        alert('No hay item seleccionado');
        return;
    }

    const config = CONFIG[TIPO_GESTION];
    const datos = {};

    document.querySelectorAll('.input-editar').forEach(input => {
        const campo = input.dataset.campo;
        datos[campo] = input.value;
    });

    const codigo = ITEM_SELECCIONADO.codigo || ITEM_SELECCIONADO.id;
    const endpoint = `${config.endpoint}${codigo}/`;

    fetch(endpoint, {
        method: 'PATCH',
        credentials: 'include',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(datos)
    })
        .then(response => {
            if (response.ok) {
                alert('Cambios guardados correctamente');
                cargarItems(TIPO_GESTION);
                mostrarPaso(1);
            } else {
                alert('Error al guardar los cambios');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al guardar');
        });
}




