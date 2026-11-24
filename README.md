# Sistema de Reserva de Salas

Aplicación web desarrollada en **Django** y **Django REST Framework** para la gestión, solicitud y administración de reservas de salas. El sistema permite a los usuarios consultar disponibilidad y reservar espacios, mientras que los administradores cuentan con un panel de control completo para gestionar salas, usuarios y estados de reserva.

## Características Principales

* **Gestión de Reservas (Usuarios):**
  * Consulta y solicitud de salas disponibles (`reservar_salas.html`).
  * Cancelación de reservas activas (`cancelar_reserva.html`).
  * Notificaciones automáticas por correo electrónico (`emails.py`).
* **Panel de Administración:**
  * Inicio de sesión y control de acceso (`inicio_sesion.html`, `admin_inicio.html`).
  * Administración integral de **Salas**, **Reservas** y **Usuarios** (`gestion_salas.html`, `gestion_reservas.html`, `gestion_usuarios.html`).
* **API RESTful:**
  * Endpoints dedicados (`reservas/api/`) con serializadores y vistas para la comunicación dinámica con el frontend mediante JavaScript.
* **Mantenimiento Automatizado:**
  * Comando personalizado de gestión (`limpiar_pendientes`) para depurar reservas pendientes expiradas o no confirmadas.

## Tecnologías Utilizadas

* **Backend:** Python 3, Django, Django REST Framework.
* **Frontend:** HTML5, CSS3, JavaScript (Vanilla JS para consumo de API y dinamismo en vistas).
* **Base de Datos:** SQLite (por defecto en Django, configurable en `settings.py`).

## Estructura del Proyecto

```text
reserva-de-salas-main/
├── manage.py                     # Utilidad de línea de comandos de Django
├── reservaSalas/                 # Configuración principal del proyecto
│   ├── settings.py               # Configuraciones (BD, apps, correo, estáticos)
│   ├── urls.py                   # Rutas globales
│   ├── asgi.py / wsgi.py         # Puntos de entrada para despliegue
└── reservas/                     # Aplicación principal
    ├── api/                      # Endpoints, vistas y serializadores REST
    ├── management/commands/      # Comandos personalizados (limpiar_pendientes.py)
    ├── migrations/               # Migraciones de base de datos
    ├── static/reservas/          # Archivos estáticos (CSS y scripts JS)
    ├── templates/reservas/       # Plantillas HTML (vistas de usuario y admin)
    ├── admin.py                  # Configuración del panel admin nativo
    ├── emails.py                 # Lógica de envío de correos
    ├── forms.py                  # Formularios de Django
    ├── models.py                 # Modelos de datos (Salas, Reservas, etc.)
    ├── tests.py                  # Pruebas unitarias y de integración
    ├── urls.py                   # Rutas de la aplicación
    └── views.py                  # Controladores de vistas web
```

## Instalación y Configuración

Sigue estos pasos para ejecutar el proyecto en un entorno local:

### 1. Clonar o descomprimir el repositorio
```bash
cd reserva-de-salas-main
```

### 2. Crear y activar un entorno virtual
```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependencias
*(Nota: Si no cuentas con un archivo `requirements.txt`, instala los paquetes base del proyecto)*
```bash
pip install django djangorestframework
```

### 4. Aplicar migraciones
Genera las tablas necesarias en la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un superusuario
Para acceder al panel de administración:
```bash
python manage.py createsuperuser
```

### 6. Ejecutar el servidor de desarrollo
```bash
python manage.py runserver
```
La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Comandos Útiles

* **Limpiar reservas pendientes:**
  Para ejecutar el comando personalizado incluido en el proyecto:
  ```bash
  python manage.py limpiar_pendientes
  ```

* **Ejecutar pruebas:**
  Para verificar el correcto funcionamiento mediante los tests configurados en `reservas/tests.py`:
  ```bash
  python manage.py test reservas
  ```

## Configuración Adicional

* **Correo Electrónico:** Asegúrate de configurar las variables `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER` y `EMAIL_HOST_PASSWORD` en `reservaSalas/settings.py` para que el módulo `emails.py` funcione correctamente en producción.