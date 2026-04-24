Series Tracker API
API REST para gestionar una lista de series. Construida con FastAPI y PostgreSQL (Neon), con imágenes almacenadas en Cloudinary.
🔗 Backend en producción: https://series-api-pbls.onrender.com
📄 Swagger UI: https://series-api-pbls.onrender.com/docs
🖥️ Repositorio del cliente: https://github.com/dallycita/series-client 

Screenshot


Stack

Lenguaje: Python 3.12
Framework: FastAPI
Base de datos: PostgreSQL via Neon
ORM / queries: psycopg2 (SQL directo)
Validación: Pydantic v2
Imágenes: Cloudinary
Deploy: Render


Correr localmente
1. Clonar el repositorio
bashgit clone https://github.com/dallycita/series-api
cd series-api

2. Crear entorno virtual e instalar dependencias
bashpython -m venv venv
source venv/bin/activate     
pip install -r requirements.txt

3. Configurar variables de entorno
Crear un archivo .env en la raíz con:
envDATABASE_URL=postgresql://user:password@host/dbname
CLOUDINARY_CLOUD_NAME=tu_cloud_name
CLOUDINARY_API_KEY=tu_api_key
CLOUDINARY_API_SECRET=tu_api_secret

4. Crear las tablas en la base de datos
Ejecutar el siguiente SQL en tu instancia de PostgreSQL:
sqlCREATE TABLE series (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    status VARCHAR(50) DEFAULT 'pendiente',
    synopsis TEXT,
    year INTEGER,
    image_path TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE user_ratings (
    id SERIAL PRIMARY KEY,
    series_id INTEGER REFERENCES series(id) ON DELETE CASCADE,
    score NUMERIC(4,1) NOT NULL,
    review TEXT,
    rated_at TIMESTAMP DEFAULT NOW()
);

5. Levantar el servidor
bashuvicorn app.main:app --reload
El servidor queda disponible en http://localhost:8000.
La documentación interactiva en http://localhost:8000/docs.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| `GET` | `/series` | Listar series (paginado, búsqueda, ordenamiento) |
| `GET` | `/series/:id` | Obtener serie por ID |
| `POST` | `/series` | Crear serie nueva |
| `PUT` | `/series/:id` | Editar serie existente |
| `DELETE` | `/series/:id` | Eliminar serie |
| `POST` | `/series/:id/rating` | Agregar rating a una serie |
| `GET` | `/series/:id/rating` | Ver ratings de una serie |
| `POST` | `/upload` | Subir imagen (máx 1 MB, JPG/PNG/WebP) |

### Parámetros de `GET /series`

| Parámetro | Tipo | Default | Descripción |
|-----------|------|---------|-------------|
| `page` | int | 1 | Número de página |
| `limit` | int | 10 | Resultados por página (máx 100) |
| `q` | string | `""` | Búsqueda por título |
| `sort` | string | `created_at` | Campo de ordenamiento |
| `order` | string | `desc` | `asc` o `desc` |

CORS
CORS permite que un cliente web en un origen diferente (distinto dominio o puerto) pueda hacer peticiones a este servidor. Está configurado con allow_origins: ["*"] para aceptar peticiones de cualquier origen durante desarrollo y producción.

Estructura del proyecto
series-api/
├── app/
│   ├── main.py          # Entrada principal, middlewares
│   ├── database.py      # Conexión a PostgreSQL
│   ├── schemas.py       # Modelos Pydantic (validación)
│   ├── crud.py          # Queries SQL
│   └── routers/
│       ├── series.py    # Endpoints de series
│       ├── ratings.py   # Endpoints de ratings
│       └── upload.py    # Endpoint de subida de imágenes
├── openapi.yaml         # Spec OpenAPI 3.1
├── requirements.txt
└── .env                 # (no incluido en el repo)

Challenges implementados

✅ Spec OpenAPI/Swagger — archivo openapi.yaml con todos los endpoints documentados
✅ Swagger UI — servido automáticamente por FastAPI en /docs
✅ Códigos HTTP correctos — 201 al crear, 204 al eliminar, 404 si no existe, 400 en input inválido
✅ Validación server-side — Pydantic v2 con mensajes de error en JSON
✅ Paginación — page y limit en GET /series
✅ Búsqueda por nombre — parámetro q con LIKE case-insensitive
✅ Ordenamiento — sort y order=asc|desc, con whitelist de campos válidos
✅ Sistema de rating — tabla user_ratings propia con endpoints REST dedicados
✅ Subida de imágenes — validación de tipo, tamaño (máx 1 MB) y verificación con Pillow; almacenamiento en Cloudinary


Reflexión
Elegí usar FastAPI porque ya me sentía cómodo con Python y quería probar algo más moderno que Flask. La verdad, la experiencia me gustó bastante: cosas como la validación automática con Pydantic y que Swagger se genere prácticamente solo hacen que todo el proceso sea mucho más rápido y ordenado. Definitivamente lo volvería a usar, sobre todo para APIs donde desde el inicio se necesita buena documentación y validación sólida.

El reto más interesante fue manejar la subida de imágenes a Cloudinary, asegurándome primero de validarlas en el servidor (tipo MIME y usando Pillow). También me ayudó mucho entender CORS en la práctica, esos errores en el navegador prácticamente te obligan a comprender qué está pasando realmente detrás de escena.
