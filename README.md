# ProyectoIngSoft2

Descripción General del Sistema

Este proyecto corresponde a un Sistema de Reservas de Servicios, desarrollado en Python con Flask, que permite:

Registro e inicio de sesión de usuarios.

Gestión de servicios (creación y consulta).

Creación de reservas.

Procesamiento de pagos.

Consulta del historial de reservas según rol (Cliente, Proveedor o Administrador).

El sistema sigue una arquitectura en capas, separando claramente:

Presentación: server.py (API REST con Flask)

Lógica de Negocio: logica.py

Acceso a Datos: configuracion_db.py

Calidad y Pruebas: test_logica.py, pruebas de integración y rendimiento

Arquitectura del Sistema
Backend/
│
├── server.py              # Endpoints Flask (API)
├── logica.py              # Lógica de negocio
├── configuracion_db.py    # Conexión y ejecución de consultas PostgreSQL
├── test_logica.py         # Pruebas unitarias (Caja Blanca)
├── load_test.js           # Pruebas de rendimiento con k6
├── templates/
│   └── index.html         # Frontend básico
└── README.md

Configuración del Entorno
1️ Crear y activar entorno virtual
python -m venv venv
source venv/Scripts/activate   # Git Bash en Windows

2️ Instalar dependencias
pip install flask flask-cors psycopg2 pytest pytest-mock coverage flask-testing python-dateutil

Configuración de Base de Datos

El archivo configuracion_db.py contiene:

Variables de conexión:

DB_HOST

DB_NAME

DB_USER

DB_PASSWORD

DB_PORT

Funciones clave:

conectar_db() → abre la conexión

execute_query() → ejecuta consultas SQL y maneja commits/rollback

Esta función es inyectada en la lógica de negocio, aplicando el Principio de Inversión de Dependencias (DIP).

Ejecución de la Aplicación
Iniciar el servidor Flask
python server.py


El backend quedará disponible en:

http://localhost:5000

Endpoints Principales
Endpoint	Método	Descripción
/api/register	POST	Registro de usuario
/api/login	POST	Inicio de sesión
/api/services	GET	Listado de servicios
/api/service	POST	Crear servicio
/api/reservation	POST	Crear reserva
/api/process_payment	POST	Procesar pago
/api/history/{id}/{rol}	GET	Historial de reservas
Pruebas Unitarias (Caja Blanca)

Las pruebas unitarias se encuentran en el archivo:

test_logica.py

¿Qué se prueba?

Registro de usuarios

Validaciones de correo y contraseña

Autenticación (Login)

Creación de servicios

Reservas

Pagos
La base de datos se simula usando mocks, garantizando pruebas aisladas.

Ejecutar pruebas unitarias
pytest

Resultado esperado:

12 passed

Cobertura de Código
Ejecutar pruebas con cobertura
pytest --cov=logica --cov-report html


Esto genera la carpeta:

htmlcov/

Ver reporte de cobertura

Abrir en el navegador:

htmlcov/index.html

Cobertura alcanzada: 85.4%

Pruebas de Integración (Caja Negra)

Estas pruebas validan la interacción real entre:

Flask

PostgreSQL

Endpoints REST

Levantar PostgreSQL con Docker
docker run --name agenda-postgres -e POSTGRES_PASSWORD=12345 -d -p 5432:5432 postgres

Ejecutar pruebas de integración
pytest -m integration

Resultado esperado:

19 pruebas aprobadas

1 prueba fallida (defecto D-101 – compensación)

Pruebas de Rendimiento (k6)

Archivo utilizado:

load_test.js

Ejecutar prueba de carga
k6 run load_test.js


Métricas obtenidas:

50 usuarios concurrentes

Latencia P95: 480 ms

Tasa de error: 0.1%


Seguridad

Implementación de Rate Limit (HTTP 429).

Validación de métodos de pago.

Control de acceso por rol (RBAC).

Pendiente:

Configuración de la cabecera HSTS (defecto D-102).
