# Now Ecosystem Registry

Directorio central de módulos del ecosistema Now. Actúa como punto de resolución de endpoints, control de autorización y log de errores.

## Stack

- **FastAPI** — API REST
- **Supabase** — Base de datos (tablas pendientes de crear)
- **Python 3.11+**

## Setup

```bash
cp .env.example .env
# Editar .env con tus credenciales de Supabase y la clave del Registry

pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

## Autenticación

Todos los endpoints requieren el header:

```
X-Registry-Key: <REGISTRY_API_KEY>
```

Rutas exentas: `/`, `/health`, `/docs`, `/openapi.json`, `/redoc`.

## Endpoints

### Módulos

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/modules/register` | Registra un módulo con sus operaciones y dependencias |
| `GET` | `/modules/{moduleId}/resolve/{operationName}` | Devuelve el endpoint concreto de una operación |
| `GET` | `/modules/status` | Estado de todos los módulos registrados |

#### POST /modules/register

```json
{
  "moduleId": "engagement",
  "baseUrl": "https://engagement.example.com",
  "version": "1.0.0",
  "operations": [
    { "name": "getEngagement", "path": "/engagement/{id}", "method": "GET" }
  ],
  "dependencies": ["auth", "users"],
  "metadata": {}
}
```

#### GET /modules/{moduleId}/resolve/{operationName}

```json
{
  "endpoint": "https://engagement.example.com/engagement/{id}",
  "method": "GET"
}
```

### Autorización

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/auth/check` | Verifica si un usuario está autorizado para una operación |
| `POST` | `/auth/grant` | Concede autorización de un usuario a un módulo |

#### POST /auth/check

```json
{
  "requestingModule": "reports",
  "owningModule": "engagement",
  "userId": "user-123",
  "operation": "getEngagement"
}
```

Respuesta: `{ "authorized": true }`

#### POST /auth/grant

```json
{
  "userId": "user-123",
  "module": "engagement",
  "operations": ["getEngagement", "listEngagements"],
  "grantedBy": "admin"
}
```

### Errores

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/errors/log` | Registra un error de cualquier módulo |

#### POST /errors/log

```json
{
  "moduleId": "engagement",
  "errorCode": "DB_CONNECTION_FAILED",
  "message": "Cannot connect to database",
  "severity": "critical",
  "userId": "user-123",
  "context": { "retries": 3 }
}
```

## Tablas Supabase (pendientes)

```sql
-- modules
create table modules (
  "moduleId" text primary key,
  "baseUrl" text not null,
  version text not null,
  operations jsonb not null default '[]',
  dependencies text[] not null default '{}',
  metadata jsonb not null default '{}',
  registered_at timestamptz not null default now()
);

-- authorizations
create table authorizations (
  id uuid primary key default gen_random_uuid(),
  "userId" text not null,
  module text not null,
  operations text[] not null default '{}',
  granted_by text,
  granted_at timestamptz not null default now(),
  unique ("userId", module)
);

-- error_logs
create table error_logs (
  id uuid primary key default gen_random_uuid(),
  "moduleId" text not null,
  "errorCode" text,
  message text not null,
  stack text,
  context jsonb not null default '{}',
  severity text not null default 'error',
  "userId" text,
  occurred_at timestamptz not null default now()
);
```
