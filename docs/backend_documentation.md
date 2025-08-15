# Visión General del Proyecto

Este proyecto es un **backend ligero de CRM** construido con Flask y SQLAlchemy. Su objetivo principal es gestionar clientes (`Cliente`) a través de una API RESTful, mientras sirve la interfaz web estática desde el directorio `frontend`. La arquitectura se centra en la simplicidad y la extensibilidad, permitiendo que nuevos módulos o mejoras se integren sin reescribir componentes esenciales.

## Objetivos Clave
- **Persistencia**: Almacenar datos de clientes en una base SQLite (`clientes.db`), con un modelo sencillo pero completo.
- **API RESTful**: Exponer operaciones CRUD a través de endpoints bajo `/api/clientes`.
- **Entrega Frontend**: Servir la página principal desde `static_folder='../frontend'`, lo que facilita el despliegue de una SPA o páginas estáticas sin configuración adicional.

## Estructura del Código
```
├── __init__.py          # Configuración y creación de la app Flask
├── models.py            # Definición del modelo Cliente con SQLAlchemy
└── routes.py            # Endpoints CRUD para clientes
```

El flujo de trabajo típico consiste en:
1. **Cliente** (frontend) envía una petición HTTP a `/api/clientes/...`.
2. Flask recibe la solicitud, valida los datos y ejecuta la lógica correspondiente.
3. SQLAlchemy interactúa con SQLite para persistir o recuperar información.
4. La respuesta se serializa a JSON y se devuelve al cliente.

---

# Arquitectura del Sistema

## Componentes Principales
| Componente | Descripción |
|------------|-------------|
| **Flask**  | Servidor WSGI que maneja las rutas, la configuración y el ciclo de vida de la aplicación. |
| **SQLAlchemy** | ORM que abstrae la capa de base de datos (SQLite) y proporciona mapeo objeto-relacional. |
| **Blueprint `clientes_bp`** | Agrupa todas las rutas relacionadas con clientes, manteniendo la modularidad. |
| **Static Files** | La carpeta `frontend/` contiene los archivos estáticos (HTML/CSS/JS). Flask sirve estos recursos directamente. |

## Diagrama de Arquitectura
```mermaid
flowchart TD
    A[Cliente (Browser)] -->|HTTP| B[Flask App]
    B --> C{Endpoint}
    C -->|GET| D[SQLAlchemy Query]
    C -->|POST/PUT/DELETE| E[SQLAlchemy Operation]
    D --> F[SQLite DB]
    E --> F
    B --> G[Static Files (index.html)]
```

---

# Endpoints de la API

## Tabla de Rutas y Operaciones

| Método | Ruta | Descripción | Parámetros | Respuesta |
|--------|------|-------------|------------|-----------|
| `GET`  | `/api/clientes/` | Lista todos los clientes. | Ninguno | `200 OK` con array JSON de clientes. |
| `POST` | `/api/clientes/` | Crea un nuevo cliente. | `nombre_completo`, `email`, `status`; opcional: `empresa`, `telefono`. | `201 Created` con objeto JSON del cliente creado. |
| `PUT`  | `/api/clientes/<int:cliente_id>` | Actualiza campos de un cliente existente. | Cualquier campo del modelo; requiere al menos uno. | `200 OK` con objeto JSON actualizado. |
| `DELETE` | `/api/clientes/<int:cliente_id>` | Elimina un cliente. | Ninguno | `200 OK` con mensaje de confirmación. |

## Esquema de Datos (`Cliente`)
```json
{
  "id": 1,
  "nombre_completo": "Juan Pérez",
  "empresa": "Acme Corp",
  "email": "juan.perez@example.com",
  "telefono": "+34 600 123 456",
  "fecha_registro": "2025-08-16T12:34:56.789Z",
  "status": "Activo"
}
```

### Validaciones Clave
- `nombre_completo`, `email` y `status` son obligatorios al crear.
- `email` debe ser único.
- `status` solo acepta `"Activo"`, `"Inactivo"` o `"Potencial"`.
- En actualización, se permite modificar cualquier campo existente.

---

# Instrucciones de Instalación y Ejecución

1. **Clonar el repositorio**  
   ```bash
   git clone https://github.com/tu_usuario/crm-backend.git
   cd crm-backend
   ```

2. **Crear un entorno virtual (opcional pero recomendado)**  
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate   # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**  
   ```bash
   pip install -r requirements.txt
   ```
   *Si `requirements.txt` no existe, instala manualmente:*  
   ```bash
   pip install Flask SQLAlchemy
   ```

4. **Configurar la base de datos (SQLite)**  
   La aplicación crea automáticamente `clientes.db` en el directorio raíz al iniciar.

5. **Ejecutar la aplicación**  
   ```bash
   export FLASK_APP=run.py      # En Windows: set FLASK_APP=run.py
   flask run --host=0.0.0.0 --port=5000
   ```
   La API estará disponible en `http://localhost:5000/api/clientes/`.

6. **Acceder al frontend**  
   Navega a `http://localhost:5000/` para cargar la página estática.

---

# Flujo de Datos Clave

1. **Solicitud POST /api/clientes/**  
   - El cliente envía JSON con datos del nuevo cliente.  
   - Flask valida y crea una instancia `Cliente`.  
   - SQLAlchemy añade la entidad a la sesión y la persiste en SQLite.  
   - Se devuelve el objeto serializado.

2. **Solicitud GET /api/clientes/**  
   - Flask ejecuta `Cliente.query.all()`.  
   - Cada registro se convierte a dict mediante `to_dict()`.  
   - Respuesta JSON con lista completa.

3. **Solicitud PUT /api/clientes/<id>**  
   - Se recupera el cliente por ID (`get_or_404`).  
   - Los campos enviados se asignan dinámicamente.  
   - Se confirma la transacción y devuelve el registro actualizado.

4. **Solicitud DELETE /api/clientes/<id>**  
   - Cliente buscado y eliminado de la sesión.  
   - Commit finaliza la eliminación en SQLite.  
   - Mensaje de éxito devuelto al cliente.

---

# Extensiones Futuras (Opcional)

| Área | Posible Mejora |
|------|----------------|
| **Autenticación & Autorización** | Añadir JWT o OAuth para proteger endpoints sensibles. |
| **Validaciones Avanzadas** | Usar Marshmallow o Pydantic para schemas y validaciones más robustas. |
| **Migraciones de Base de Datos** | Integrar Flask-Migrate (Alembic) para gestionar cambios en el esquema. |
| **Testing Automatizado** | Implementar pruebas unitarias/funcionales con pytest y coverage. |
| **Despliegue en Docker** | Crear un `Dockerfile` y `docker-compose.yml` para entornos reproducibles. |
| **Logging Centralizado** | Configurar logging a nivel de aplicación con handlers externos (ELK, Sentry). |

---