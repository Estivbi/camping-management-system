# 🏕️ Camping Management System

Sistema completo de gestión para campings con backend en FastAPI, frontend en Angular y base de datos PostgreSQL.

## 🚀 Características

- **Backend**: FastAPI con PostgreSQL
- **Frontend**: Angular con Material Design
- **Autenticación**: JWT tokens
- **Base de datos**: PostgreSQL con Docker
- **Arquitectura**: API REST + SPA

## 📋 Funcionalidades

### ✅ Implementadas
- [x] Autenticación JWT
- [x] Registro y login de usuarios
- [x] Panel de administración Angular
- [x] Conexión frontend-backend
- [x] Base de datos PostgreSQL

### 🚧 En Desarrollo
- [ ] Dashboard principal
- [ ] Gestión de actividades
- [ ] Gestión de reservas
- [ ] Sistema de notificaciones
- [ ] Estadísticas y reportes

## 🛠️ Tecnologías

### Backend
- **FastAPI** - Framework web moderno y rápido
- **PostgreSQL** - Base de datos relacional
- **JWT** - Autenticación segura
- **Docker** - Contenedorización de servicios

### Frontend
- **Angular 17** - Framework de aplicaciones web
- **Angular Material** - Componentes de UI
- **TypeScript** - Lenguaje tipado
- **SCSS** - Estilos avanzados

## 📦 Instalación

### Prerrequisitos
- Python 3.11+
- Node.js 18+
- Docker y Docker Compose
- Git

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/camping-management-system.git
cd camping-management-system
```

### 2. Configurar el Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Levantar la Base de Datos
```bash
docker-compose up -d
```

### 4. Configurar el Frontend
```bash
cd admin
npm install
```

## 🚀 Ejecución

### Backend
```bash
cd backend
make run
# O manualmente:
# uvicorn main:app --reload
```

### Frontend
```bash
cd admin
npx ng serve
```

### Base de Datos
```bash
docker-compose up -d
```

## 🌐 URLs

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs
- **Base de datos**: localhost:5432

## 📊 Estructura del Proyecto

```
camping-project/
├── backend/                 # FastAPI Backend
│   ├── main.py             # Punto de entrada
│   ├── db.py               # Configuración de BD
│   ├── models/             # Lógica de datos
│   ├── routes/             # Endpoints API
│   ├── schemas/            # Validación de datos
│   ├── utils/              # Utilidades
│   └── docker-compose.yml  # Configuración Docker
├── admin/                  # Angular Frontend
│   ├── src/
│   │   ├── app/
│   │   │   ├── components/ # Componentes Angular
│   │   │   ├── services/   # Servicios
│   │   │   └── ...
│   │   └── ...
│   └── ...
├── TODO.md                 # Tareas pendientes
└── README.md              # Este archivo
```

## 🔧 Configuración

### Variables de Entorno
Crea un archivo `.env` en la carpeta `backend`:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=Camping
DB_USER=postgres
DB_PASS=postgres
SECRET_KEY=tu_clave_secreta_super_segura
```

### Base de Datos
Las tablas se crean automáticamente. Para crear manualmente:

```sql
-- Tabla de usuarios (ya creada)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 📚 API Endpoints

### Autenticación
- `POST /token` - Login
- `POST /api/users/register` - Registro
- `GET /api/users/me` - Perfil del usuario

### Próximos Endpoints
- `GET /api/activities` - Listar actividades
- `POST /api/activities` - Crear actividad
- `GET /api/reservations` - Listar reservas
- `POST /api/reservations` - Crear reserva

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 👥 Autores

- **Carolina** - *Desarrollo inicial* - [Tu GitHub]

## 🙏 Agradecimientos

- FastAPI por el excelente framework
- Angular por las herramientas de desarrollo
- PostgreSQL por la base de datos robusta

---

⭐ Si te gusta este proyecto, ¡dale una estrella en GitHub! 