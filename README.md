# Device Systems API EV07

## Descripción

**Device Systems API** es una aplicación backend desarrollada con **FastAPI** para la gestión de usuarios mediante una API REST.

La aplicación permite:

- Listar usuarios.
- Consultar usuarios por ID.
- Filtrar usuarios por rol.
- Filtrar usuarios por estado activo/inactivo.
- Registrar nuevos usuarios.
- Validar datos utilizando Pydantic v2.
- Evitar correos electrónicos duplicados.
- Implementar Response Models.
- Agregar cabeceras HTTP personalizadas.

---

## Tecnologías utilizadas

- Python 3.x
- FastAPI
- Uvicorn
- Pydantic v2
- Swagger UI

---

## Estructura del proyecto

```text
device_systems/
│
├── app/
│   │
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── user_routes.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── user_schema.py
│
├── requirements.txt
│
└── README.md
```

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU-USUARIO/device_systems.git
cd device_systems
```

### 2. Crear entorno virtual

```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows**

```bash
.\venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

## Ejecución del servidor

Ejecutar:

```bash
uvicorn app.main:app --reload
```

Salida esperada:

```text
INFO: Uvicorn running on http://127.0.0.1:8000
```

---

## Documentación automática

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

## Endpoints disponibles

| Método | Endpoint | Descripción |
|---------|----------|-------------|
| GET | / | Mensaje de bienvenida |
| GET | /users | Obtener todos los usuarios |
| GET | /users/{user_id} | Obtener usuario por ID |
| GET | /users?role=admin | Filtrar usuarios por rol |
| GET | /users?is_active=true | Filtrar usuarios activos |
| POST | /users | Crear nuevo usuario |

---

# Modelos de Datos

## UserCreate

Modelo utilizado para crear usuarios.

### Campos

| Campo | Tipo | Validación |
|---------|------|-----------|
| name | string | mínimo 3 caracteres |
| email | EmailStr | correo válido |
| role | string | admin, support o user |
| is_active | boolean | true o false |

---

## UserResponse

Modelo utilizado para responder información de usuarios.

```json
{
  "id": 1,
  "name": "Tatiana",
  "email": "tatiana@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

# Ejemplos de Peticiones

## GET /users

### Petición

```http
GET /users
```

### Respuesta

```json
[
  {
    "id": 1,
    "name": "Tatiana",
    "email": "tatiana@gmail.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "support",
    "is_active": true
  },
  {
    "id": 3,
    "name": "Maria",
    "email": "maria@gmail.com",
    "role": "user",
    "is_active": false
  }
]
```

---

## GET /users/{user_id}

### Petición

```http
GET /users/1
```

### Respuesta

```json
{
  "id": 1,
  "name": "Tatiana",
  "email": "tatiana@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

## GET /users?role=admin

### Petición

```http
GET /users?role=admin
```

### Respuesta

```json
[
  {
    "id": 1,
    "name": "Tatiana",
    "email": "tatiana@gmail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

## GET /users?is_active=true

### Petición

```http
GET /users?is_active=true
```

### Respuesta

```json
[
  {
    "id": 1,
    "name": "Tatiana",
    "email": "tatiana@gmail.com",
    "role": "admin",
    "is_active": true
  },
  {
    "id": 2,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "support",
    "is_active": true
  }
]
```

---

## POST /users

### Petición

```json
{
  "name": "Andres",
  "email": "andres@gmail.com",
  "role": "user",
  "is_active": true
}
```

### Respuesta

```json
{
  "message": "Usuario creado correctamente",
  "user": {
    "id": 4,
    "name": "Andres",
    "email": "andres@gmail.com",
    "role": "user",
    "is_active": true
  }
}
```

---

# Validaciones Implementadas

## Nombre

Debe contener mínimo 3 caracteres.

### Ejemplo inválido

```json
{
  "name": "Jo"
}
```

---

## Correo electrónico

Debe tener formato válido.

### Ejemplo inválido

```json
{
  "email": "correo_invalido"
}
```

---

## Rol

Valores permitidos:

- admin
- support
- user

### Ejemplo inválido

```json
{
  "role": "manager"
}
```

---

## Correo duplicado

Si un correo ya existe en el sistema:

```json
{
  "detail": "El correo ya está registrado"
}
```

---

# Cabeceras HTTP Personalizadas

La API agrega automáticamente las siguientes cabeceras:

```http
X-App-Name: device_systems
X-API-Version: 1.0
```

# Evidencias

## captura 1

![estructura](capturas/estructuraDS.png)

## captura 2

![SwaggerUI](capturas/SwaggerUI.png)

## captura 3

![GET](capturas/GET.png)

## captura 4

![GET](capturas/GET2.png)

## captura 5

![GET](capturas/GET3.png)

## captura 6

![GET](capturas/GET4.png)

## captura 7

![GET](capturas/GET5.png)

## captura 8

![POST](capturas/POST1.png)

## captura 9

![POST](capturas/POST2.png)

## captura 10

![POST](capturas/POST3.png)

# Reflexión FinaL

Durante el desarrollo de esta actividad aprendi el funcionamiento de FastAPI para construir APIs REST de forma rápida y organizada.

Se implementaron endpoints GET y POST, utilizando Path Parameters y Query Parameters para realizar consultas dinámicas. Además, se aplicaron validaciones mediante Pydantic v2, garantizando la integridad de los datos recibidos por la API.

También se comprendió la importancia de los Response Models para estandarizar las respuestas y de las cabeceras HTTP para proporcionar información adicional a los clientes que consumen el servicio.

Swagger UI facilitó la documentación y las pruebas de cada endpoint, permitiendo validar el correcto funcionamiento de la aplicación.

FastAPI demostró ser una herramienta moderna, eficiente y fácil de usar para el desarrollo de APIs REST en Python.




------------------------------------------------------------------------------------------------------------------------------------------





# Device Systems API EV08

## Descripción

**Device Systems API** es una API REST desarrollada con FastAPI para la gestión de usuarios del sistema **device_systems**.

Esta aplicación permite realizar operaciones CRUD completas sobre el recurso **users**, incluyendo:

- Crear usuarios.
- Listar usuarios.
- Consultar usuarios por ID.
- Filtrar usuarios por rol y estado.
- Actualizar usuarios completamente (PUT).
- Actualizar usuarios parcialmente (PATCH).
- Eliminar usuarios.
- Validar datos mediante Pydantic v2.
- Manejar errores mediante HTTPException.
- Documentar automáticamente la API con Swagger UI y ReDoc.
- Reutilizar lógica mediante Dependency Injection (Depends).

---

# Tecnologías utilizadas

- Python 3
- FastAPI
- Uvicorn
- Pydantic v2
- Swagger UI
- ReDoc
- Git
- GitHub
- Postman
- Thunder Client
- Visual Studio Code

---

# Estructura del proyecto

```text
device_systems/
│
├── app/
│   ├── main.py
│   │
│   ├── routes/
│   │   └── user_routes.py
│   │
│   ├── schemas/
│   │   └── user_schema.py
│   │
│   ├── services/
│   │   └── user_service.py
│   │
│   ├── dependencies/
│   │   └── user_dependencies.py
│   │
│   └── data/
│       └── users_db.py
│
├── requirements.txt
│
└── README.md
```

---

# Instalación de dependencias

## Crear entorno virtual

```bash
python -m venv venv
```

## Activar entorno virtual

### Windows PowerShell

```bash
venv\Scripts\Activate.ps1
```

### CMD

```bash
venv\Scripts\activate
```

## Instalar dependencias

```bash
pip install fastapi uvicorn pydantic[email]
```

---

# Ejecutar el servidor

```bash
uvicorn app.main:app --reload
```

Servidor local:

```text
http://127.0.0.1:8000
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Tabla de Endpoints

| Método | Endpoint | Descripción |
|----------|----------|-------------|
| GET | /users | Listar usuarios |
| GET | /users/{user_id} | Obtener usuario por ID |
| GET | /users?role=user | Filtrar por rol |
| GET | /users?is_active=true | Filtrar por estado |
| POST | /users | Crear usuario |
| PUT | /users/{user_id} | Actualizar usuario completo |
| PATCH | /users/{user_id} | Actualizar usuario parcialmente |
| DELETE | /users/{user_id} | Eliminar usuario |
| GET | /users/config/info | Información de configuración |

---

# Ejemplos de peticiones y respuestas

## GET /users

### Respuesta

```json
[
  {
    "id": 1,
    "name": "Carlos",
    "email": "carlos@gmail.com",
    "role": "admin",
    "is_active": true
  }
]
```

---

## POST /users

### Petición

```json
{
  "name": "Tatiana",
  "email": "tatiana@gmail.com",
  "role": "user",
  "is_active": true
}
```

### Respuesta

```json
{
  "message": "Usuario creado correctamente",
  "user": {
    "id": 3,
    "name": "Tatiana",
    "email": "tatiana@gmail.com",
    "role": "user",
    "is_active": true
  }
}
```

---

## PUT /users/{user_id}

### Petición

```json
{
  "name": "Tatiana Actualizada",
  "email": "tatiana_actualizada@gmail.com",
  "role": "support",
  "is_active": true
}
```

### Respuesta

```json
{
  "id": 3,
  "name": "Tatiana Actualizada",
  "email": "tatiana_actualizada@gmail.com",
  "role": "support",
  "is_active": true
}
```

---

## PATCH /users/{user_id}

### Petición

```json
{
  "role": "admin"
}
```

### Respuesta

```json
{
  "id": 3,
  "name": "Tatiana Actualizada",
  "email": "tatiana_actualizada@gmail.com",
  "role": "admin",
  "is_active": true
}
```

---

## DELETE /users/{user_id}

### Respuesta

```json
{
  "message": "Usuario eliminado correctamente"
}
```

---

# Códigos de estado HTTP utilizados

| Código | Significado |
|----------|-------------|
| 200 OK | Operación exitosa |
| 201 Created | Usuario creado correctamente |
| 400 Bad Request | Solicitud incorrecta |
| 404 Not Found | Usuario no encontrado |
| 422 Unprocessable Entity | Error de validación |

---

# Uso de Dependency Injection (Depends)

Para evitar duplicación de código se implementó Dependency Injection mediante **Depends()**.

Las dependencias permiten reutilizar lógica común entre distintos endpoints.

Ejemplos implementados:

- Obtener usuario por ID.
- Validar si un usuario existe.
- Obtener configuración general de la API.

Ejemplo:

```python
from fastapi import Depends

def get_user_or_404(user_id: int):
    ...
```

## Beneficios

- Código más limpio.
- Menos duplicación.
- Mayor mantenibilidad.
- Mejor organización del proyecto.

---

# Manejo de errores implementado

Se utilizó **HTTPException** para controlar errores y responder adecuadamente al cliente.

Errores implementados:

- Usuario no encontrado.
- Correo electrónico duplicado.
- Actualización sin datos.
- Eliminación de usuario inexistente.
- Validaciones Pydantic.

Ejemplo:

```json
{
  "detail": {
    "error": true,
    "message": "Usuario no encontrado",
    "status_code": 404
  }
}
```

---

# Evidencias y Capturas

# Documentación automática Swagger/OpenAPI

## Captura 1 – Swagger UI Principal

![captura](capturas/8.1.png)

## Captura 2 – Endpoint GET /users

![captura](capturas/8.2.png)

![captura](capturas/8.3.png)

## Captura 3 – Endpoint POST /users

![captura](capturas/8.4.png)

## Captura 4 – Endpoint PUT /users/{user_id}

![captura](capturas/8.5.png)

## Captura 5 – Endpoint PATCH /users/{user_id}

![captura](capturas/8.6.png)

## Captura 6 – Endpoint DELETE /users/{user_id}

![captura](capturas/8.7.png)

## Captura 7 – Endpoint GET /users/config/info

![captura](capturas/8.8.png)

## Captura 8 – ReDoc funcional

![captura](capturas/REDOC.png)

---

# Pruebas funcionales

## Captura 9 – GET /users

![captura](capturas/9.1.png)

## Captura 10 – GET /users/{user_id}

![captura](capturas/9.2.png)

## Captura 11 – POST /users

![captura](capturas/9.3.png)

## Captura 12 – PUT /users/{user_id}

![captura](capturas/9.4.png)

## Captura 13 – PATCH /users/{user_id}

![captura](capturas/9.5.png)

## Captura 14 – DELETE /users/{user_id}

![captura](capturas/9.6.png)

---

# Evidencias de errores controlados

## Captura 15 – Usuario inexistente

![captura 1](capturas/9.7.png)

## Captura 16 – Correo duplicado

![captura 1](capturas/9.8.png)

## Captura 17 – Datos inválidos

![captura 1](capturas/9.9.png)

## Captura 18 – Actualizar usuario inexistente

![captura 1](capturas/9.10.png)

## Captura 19 – PATCH vacío

![captura 1](capturas/9.11.png)

## Captura 20 – Eliminar usuario inexistente

![captura 1](capturas/9.12.png)

---

# Reflexión Final

Esta actividad permitió comprender cómo una API REST puede evolucionar desde una implementación básica hasta una solución más profesional y organizada.

Durante el desarrollo se implementó un CRUD completo, manejo de errores mediante HTTPException, validación de datos con Pydantic, documentación automática con Swagger y ReDoc, y reutilización de lógica mediante Dependency Injection.

FastAPI demostró ser una herramienta moderna y eficiente para el desarrollo de APIs REST gracias a su facilidad de uso, velocidad y generación automática de documentación.

--------------------------------------------------------------------------------------------------------------------------

# Device Systems API EV09


## Captura de la estructura del proyecto

Insertar aquí la captura de la estructura completa del proyecto en Visual Studio Code.

Ejemplo:

![Estructura del proyecto](capturas/estructura9.png)

---

## Captura de la base de datos generada

Insertar aquí la captura donde se observe la base de datos SQLite generada (`device_systems.db`) y los registros almacenados.

Ejemplo:

![Base de datos](capturas/sqlite.png)

---

## Capturas de Swagger UI

### Swagger General

![Swagger General](capturas/11.1.png)

### Endpoint Documentado - Schema de Entrada

![Endpoint Documentado, Schema Entrada](capturas/11.2.3.png)

### Schema de Respuesta

![Schema Respuesta](capturas/11.4.png)

### Parámetros de Consulta

![Parámetros de Consulta](capturas/11.5.png)

### Parámetro de Ruta

![Parámetro de Ruta](capturas/11.6.png)

### ReDoc

![ReDoc](capturas/11.7.png)

---

## Evidencia de prueba de cada endpoint

### Crear usuario (POST)

![Crear Usuario](capturas/12.1.png)

### Crear usuario con correo duplicado

![Correo Duplicado](capturas/12.2.png)

### Listar usuarios (GET)

![Listar Usuarios](capturas/12.3.png)

### Obtener usuario por ID (GET)

![Usuario por ID](capturas/12.4.png)

### Usuario inexistente

![Usuario Inexistente](capturas/12.5.png)

### Filtrar usuarios por rol

![Filtro por Rol](capturas/12.6.png)

### Filtrar usuarios activos

![Filtro Activos](capturas/12.7.png)

### Actualizar usuario completo (PUT)

![PUT Usuario](capturas/12.8.png)

### Actualizar usuario parcialmente (PATCH)

![PATCH Usuario](capturas/12.9.png)

### Eliminar usuario (DELETE)

![DELETE Usuario](capturas/12.10.png)

### Verificar eliminación del usuario

![Usuario Eliminado](capturas/12.11.png)

---

## Evidencia de errores controlados

### Usuario inexistente

![Usuario Inexistente](capturas/10.1.png)

### Correo duplicado

![Correo Duplicado](capturas/10.2.png)

### Datos inválidos

![Datos Inválidos](capturas/10.3.png)

### Rol no permitido

![Rol no permitido](capturas/10.4.png)

### PATCH vacío

![PATCH Vacío](capturas/10.5.png)

### Eliminar usuario inexistente

![Eliminar Usuario Inexistente](capturas/10.6.png)

---

## Explicación de la diferencia entre modelo SQLAlchemy y schema Pydantic

Los modelos SQLAlchemy representan las tablas de la base de datos y permiten realizar operaciones CRUD sobre los datos almacenados.

Los schemas Pydantic se utilizan para validar los datos que recibe y devuelve la API. Gracias a ellos se verifica que los datos tengan el formato correcto antes de ser procesados.

En resumen:

- SQLAlchemy se encarga de la persistencia de datos.
- Pydantic se encarga de la validación de datos.
- SQLAlchemy interactúa con la base de datos.
- Pydantic interactúa con las solicitudes y respuestas de la API.

---

## Reflexión final sobre la importancia de usar persistencia en una API

La implementación de persistencia mediante SQLAlchemy y SQLite permitió que la información de los usuarios se almacene de forma permanente, evitando la pérdida de datos al reiniciar el servidor.

Además, el uso de una base de datos facilita la gestión de grandes cantidades de información, mejora la organización de los datos y permite realizar consultas, actualizaciones y eliminaciones de manera eficiente.

Esta actividad permitió comprender la importancia de separar la lógica de negocio, la validación de datos y la persistencia, logrando una API más robusta, escalable y cercana a entornos reales de desarrollo.

---------------------------------------------------------------------------------------------------------------------------------

# Device Systems API EV10

## Captura de ejecución de alembic init

![Alembic](capturas/1.png)

---

## Captura de creación de migración con alembic revision --autogenerate

![Alembic](capturas/2.png)

---

## Manejo de errores

### Usuario inexistente

![Manejo de errores](capturas/11.1A.png)

### Dispositivo inexistente
![Manejo de errores](capturas/11.2A.png)

### Dispositivo no disponible

![Manejo de errores](capturas/11.3A.png)

### Dispositivo no disponible

![Manejo de errores](capturas/11.4A.png)
I
### Préstamo inexistente

![Manejo de errores](capturas/11.5A.png)

### Intento de devolver un préstamo ya devuelto

![Manejo de errores](capturas/11.6A.png)

### Número de serie duplicado

![Manejo de errores](capturas/11.7A.png)


## Documentación Swagger/OpenAPI

### Ejecutar migraciones con Alembic

![Swagger](capturas/13.1.png)

### Crear usuario.

![Swagger](capturas/13.2.png)

### Crear dispositivo.

![Swagger](capturas/13.3.png)

### Crear préstamo.

![Swagger](capturas/13.4.png)

### Intentar prestar un dispositivo no disponible.

![Swagger](capturas/13.5.png)

### Listar préstamos con información de usuario y dispositivo.

![Swagger](capturas/13.6.png)

### Filtrar préstamos por estado.

![Swagger](capturas/13.7.png)

### Filtrar préstamos por tipo de dispositivo.

![Swagger](capturas/13.8.png)

### Consultar préstamos de un usuario.

![Swagger](capturas/13.9.png)

### Devolver un dispositivo.

![Swagger](capturas/13.10.png)

### Validar que el dispositivo vuelva a estar disponible.

![Swagger](capturas/13.11.png)

### Consultar historial de préstamos del dispositivo.

![Swagger](capturas/13.12.png)

## Reflexión sobre la importancia de migraciones, relaciones y consultas avanzadas

Las migraciones permiten gestionar y controlar los cambios realizados en la estructura de la base de datos durante el desarrollo de un proyecto. Gracias a herramientas como Alembic es posible mantener un historial de modificaciones y garantizar que todos los entornos utilicen la misma versión de la base de datos.

Las relaciones entre tablas permiten modelar correctamente los procesos del sistema. En este proyecto se establecieron relaciones entre usuarios, dispositivos y préstamos mediante claves foráneas, garantizando la integridad de la información y evitando inconsistencias en los datos.

Las consultas avanzadas y los filtros facilitan la obtención de información específica de manera eficiente. Funcionalidades como consultar préstamos por usuario, filtrar por estado o por tipo de dispositivo permiten administrar mejor los recursos y obtener información relevante para la toma de decisiones.

En conclusión, las migraciones, las relaciones entre entidades y las consultas avanzadas son elementos fundamentales para desarrollar aplicaciones robustas, organizadas, escalables y fáciles de mantener.

---------------------------------------------------------------------------------------------------------------------------

# Device Systems API EV11

## Captura de la estructura del proyecto

![Estructura del proyecto](capturas/Estructura11.png)

![Estructura del proyecto](capturas/estructura11.1.png)

---

## Captura de migración Alembic aplicada

![Migración Alembic](capturas/alembic.png)

![Migración Alembic](capturas/alembic.1.png)

---

## Capturas aplicar rate limiting

### 5 solicitudes por minuto

![rate limiting](capturas/11.1F.png)

---

### 3 solicitudes por minuto

![rate limiting](capturas/11.2F.png)

---

### 30 solicitudes por minuto

![rate limiting](capturas/11.3F.png)

---

### 10 solicitudes por minuto

![rate limiting](capturas/11.4F.png)

---

## Pruebas funcionales

### 1. Registro de usuario

![Pruebas](capturas/13.1F.png)

---

## 2. Registro con contraseña débil

![Pruebas](capturas/13.2F.png)

---

### 3. Registro con email duplicado

![Pruebas](capturas/13.3F.png)

---

### 4. Login correcto

![Pruebas](capturas/13.4F.png)

---

## 5. Login con contraseña incorrecta

![Pruebas](capturas/13.5F.png)

---

### 6. Consulta de /auth/me

![Pruebas](capturas/13.6F.png)

---

## 7. Acceso a ruta protegida sin token

![Pruebas](capturas/13.7F.png)

---

### 9. Acceso con usuario sin permisos

![Pruebas](capturas/13.9F.png)

---

## 10. Creación de dispositivo con rol permitido

![Pruebas](capturas/13.10F.png)

---

## 11. Eliminación de dispositivo con rol no permitido

![Pruebas](capturas/13.11F.png)

---

### 12. Configuración CORS

![Pruebas](capturas/13.12F.png)

---

## 13. Cabeceras generadas por middleware

![Pruebas](capturas/13.13F.png)

---

### 14. Activación de rate limiting

![Pruebas](capturas/13.14F.png)

![Pruebas](capturas/13.14.2F.png)

---

## 15. Verificación de Swagger/OpenAPI

![Pruebas](capturas/13.15F.png)

![Pruebas](capturas/13.15.2F.png)

![Pruebas](capturas/13.15.3F.png)

![Pruebas](capturas/13.15.4F.png)

![Pruebas](capturas/13.15.5F.png)

![Pruebas](capturas/13.15.6F.png)

![Pruebas](capturas/13.15.7F.png)

---

## Explicación de CORS configurado

La API tiene configurado CORS mediante el middleware `CORSMiddleware` de FastAPI.

Se permiten solicitudes desde los siguientes orígenes:

```python
allow_origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]

# Reflexión final sobre la importancia de la seguridad en APIs REST

La seguridad en las APIs REST es un aspecto fundamental para proteger la información y garantizar que únicamente los usuarios autorizados puedan acceder a los recursos del sistema. Durante el desarrollo de este proyecto se implementaron diferentes mecanismos de seguridad, como autenticación mediante JWT, control de roles y permisos, validación de contraseñas seguras, protección de rutas, limitación de solicitudes (Rate Limiting), configuración de CORS y uso de middleware para el monitoreo de peticiones.

Estas medidas permiten reducir riesgos como accesos no autorizados, robo de información, ataques de fuerza bruta y abuso de los servicios expuestos por la API. Además, la documentación mediante Swagger/OpenAPI facilita la comprensión de los mecanismos de seguridad implementados y mejora la experiencia de los desarrolladores que consumen la API.

Como aprendizaje principal, se concluye que la seguridad no debe considerarse una característica opcional, sino un componente esencial desde las primeras etapas del desarrollo. Una API segura protege los datos, mejora la confiabilidad del sistema y brinda mayor confianza tanto a los usuarios como a las organizaciones que utilizan la aplicación.