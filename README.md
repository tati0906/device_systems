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
