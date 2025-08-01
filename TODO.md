# TODO - Camping Management System

## 🎯 Estado del Proyecto
- ✅ Backend FastAPI con PostgreSQL funcionando
- ✅ Autenticación JWT implementada
- ✅ Frontend Angular con login funcionando
- ✅ Conexión frontend-backend establecida

---

## 🚀 Próximas Tareas

### 📊 1. Dashboard Principal (Angular)
- [ ] **Panel con navegación lateral**
  - [ ] Crear layout con sidebar
  - [ ] Implementar menú de navegación
  - [ ] Agregar breadcrumbs
  - [ ] Diseño responsivo

- [ ] **Resumen de estadísticas**
  - [ ] Cards con métricas principales
  - [ ] Gráficos de reservas por día/semana
  - [ ] Estadísticas de ocupación
  - [ ] Ingresos del camping

- [ ] **Menú para acceder a diferentes secciones**
  - [ ] Enlace a Gestión de Actividades
  - [ ] Enlace a Gestión de Reservas
  - [ ] Enlace a Gestión de Usuarios
  - [ ] Enlace a Notificaciones

### 🏕️ 2. Funcionalidades del Camping (Frontend)

#### 📋 Gestión de Actividades
- [ ] **Lista de actividades**
  - [ ] Tabla con actividades disponibles
  - [ ] Filtros por tipo, fecha, estado
  - [ ] Búsqueda de actividades
  - [ ] Paginación

- [ ] **Crear/Editar actividades**
  - [ ] Formulario para nueva actividad
  - [ ] Editar actividad existente
  - [ ] Subir imágenes de actividades
  - [ ] Configurar capacidad y horarios

- [ ] **Gestión de reservas de actividades**
  - [ ] Ver reservas por actividad
  - [ ] Aprobar/rechazar reservas
  - [ ] Cancelar actividades

#### 📅 Gestión de Reservas
- [ ] **Vista general de reservas**
  - [ ] Calendario de reservas
  - [ ] Lista de reservas pendientes
  - [ ] Filtros por fecha, estado, tipo

- [ ] **Detalles de reserva**
  - [ ] Información del huésped
  - [ ] Servicios contratados
  - [ ] Estado de pago
  - [ ] Historial de cambios

- [ ] **Gestión de estados**
  - [ ] Aprobar reservas
  - [ ] Cancelar reservas
  - [ ] Modificar fechas
  - [ ] Notificar cambios

#### 👥 Gestión de Usuarios
- [ ] **Lista de usuarios registrados**
  - [ ] Tabla con información de usuarios
  - [ ] Filtros por tipo de usuario
  - [ ] Búsqueda de usuarios

- [ ] **Perfil de usuario**
  - [ ] Ver información detallada
  - [ ] Historial de reservas
  - [ ] Actividades realizadas
  - [ ] Preferencias

- [ ] **Gestión de permisos**
  - [ ] Roles de usuario (admin, staff, guest)
  - [ ] Asignar permisos
  - [ ] Bloquear/desbloquear usuarios

#### 🔔 Notificaciones
- [ ] **Panel de notificaciones**
  - [ ] Lista de notificaciones enviadas
  - [ ] Crear nueva notificación
  - [ ] Plantillas de notificaciones

- [ ] **Envío de notificaciones**
  - [ ] Notificación individual
  - [ ] Notificación masiva
  - [ ] Programar notificaciones
  - [ ] Notificaciones automáticas

### ⚙️ 3. Backend - Rutas Pendientes

#### 📋 Actividades
- [ ] `GET /api/activities` - Listar actividades
- [ ] `POST /api/activities` - Crear actividad
- [ ] `PUT /api/activities/{id}` - Actualizar actividad
- [ ] `DELETE /api/activities/{id}` - Eliminar actividad
- [ ] `GET /api/activities/{id}/reservations` - Reservas de una actividad

#### 📅 Reservas
- [ ] `GET /api/reservations` - Listar reservas
- [ ] `POST /api/reservations` - Crear reserva
- [ ] `PUT /api/reservations/{id}` - Actualizar reserva
- [ ] `DELETE /api/reservations/{id}` - Cancelar reserva
- [ ] `GET /api/reservations/user/{user_id}` - Reservas de un usuario

#### 🔔 Notificaciones
- [ ] `GET /api/notifications` - Listar notificaciones
- [ ] `POST /api/notifications` - Enviar notificación
- [ ] `GET /api/notifications/user/{user_id}` - Notificaciones de un usuario
- [ ] `PUT /api/notifications/{id}/read` - Marcar como leída

#### 📊 Estadísticas
- [ ] `GET /api/stats/overview` - Estadísticas generales
- [ ] `GET /api/stats/reservations` - Estadísticas de reservas
- [ ] `GET /api/stats/activities` - Estadísticas de actividades
- [ ] `GET /api/stats/revenue` - Estadísticas de ingresos

### 🗄️ 4. Base de Datos - Tablas Pendientes

#### 📋 Tabla de Actividades
```sql
CREATE TABLE activities (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    capacity INTEGER NOT NULL,
    price DECIMAL(10,2),
    duration INTEGER, -- en minutos
    location VARCHAR(100),
    image_url VARCHAR(255),
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 📅 Tabla de Reservas
```sql
CREATE TABLE reservations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_id INTEGER REFERENCES activities(id),
    reservation_date DATE NOT NULL,
    start_time TIME,
    end_time TIME,
    status VARCHAR(20) DEFAULT 'pending', -- pending, confirmed, cancelled
    total_price DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 🔔 Tabla de Notificaciones
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    title VARCHAR(100) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(20), -- info, warning, success, error
    is_read BOOLEAN DEFAULT false,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🎨 5. Mejoras de UX/UI
- [ ] **Tema personalizable**
  - [ ] Colores del camping
  - [ ] Logo personalizable
  - [ ] Imágenes de fondo

- [ ] **Responsive design**
  - [ ] Optimizar para móviles
  - [ ] Tablet layout
  - [ ] Desktop layout

- [ ] **Animaciones y transiciones**
  - [ ] Loading states
  - [ ] Smooth transitions
  - [ ] Feedback visual

### 🔒 6. Seguridad y Optimización
- [ ] **Variables de entorno**
  - [ ] SECRET_KEY en .env
  - [ ] Configuración de producción
  - [ ] Logs de seguridad

- [ ] **Validaciones**
  - [ ] Validación de formularios
  - [ ] Sanitización de datos
  - [ ] Rate limiting

- [ ] **Testing**
  - [ ] Unit tests para backend
  - [ ] E2E tests para frontend
  - [ ] API tests

---

## 📝 Notas
- Priorizar el dashboard principal para tener una interfaz completa
- Implementar funcionalidades una por una, probando cada una
- Mantener consistencia en el diseño y UX
- Documentar APIs y componentes importantes

---

## 🎯 Objetivos a Corto Plazo
1. **Dashboard principal** - Semana 1
2. **Gestión de actividades** - Semana 2
3. **Gestión de reservas** - Semana 3
4. **Notificaciones** - Semana 4 