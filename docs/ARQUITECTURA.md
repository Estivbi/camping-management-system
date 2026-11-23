# Camping Management System — Documento de arquitectura y plan de implementación

> Documento pensado para ser entregado a un agente de desarrollo (Antigravity).
> Léelo completo antes de tocar código. Trabaja por fases, en orden, y no avances de fase sin cumplir los criterios de aceptación de la anterior.

---

## 1. Objetivo del producto

Software SaaS de gestión para **campings en España** (inspirado en el software que usan los campings franceses), con tres caras sobre un mismo núcleo:

| Cara | Usuario | Dispositivo | Descripción |
|---|---|---|---|
| **Backoffice** | Recepción, dirección, limpieza | Escritorio / tablet | Gestión de alojamientos, reservas, tarifas, huéspedes, facturación, actividades |
| **PWA del campista** | Huésped durante y antes de la estancia | Móvil | Ver reserva, pre-check-in (registro de viajeros), actividades, avisos, info del camping |
| **Reserva online** | Cliente nuevo | Móvil / web | Buscar disponibilidad, reservar y pagar. Debe poder integrarse en la web del camping |

Cliente objetivo: campings pequeños y medianos. Prioridades de producto: facilidad de uso en móvil para recepción, precio contenido y cumplimiento legal español resuelto de serie.

## 2. Estado actual del repositorio (punto de partida)

- `backend/`: FastAPI + PostgreSQL con `psycopg2` y SQL escrito a mano. JWT con `python-jose` y `passlib`. Solo existe CRUD de **actividades** (`routes/actividad.py`) y usuarios/login. `routes/reserva.py` está vacío.
- `admin/`: Angular 20 (standalone components), Angular Material + PrimeNG. Login, layout con sidebar y dashboard con datos de muestra. `reservations.ts` y `users.ts` son stubs.
- Problemas conocidos a corregir en la Fase 0:
  - `SECRET_KEY` hardcodeada en `backend/utils/auth.py`.
  - Cada consulta abre una conexión nueva (`db.py`), sin pool.
  - CORS solo para `localhost:4200`.
  - Sin roles, sin multi-tenant, sin tests, sin migraciones.
  - El concepto "reserva" está ligado a una actividad; el negocio real es la reserva de **alojamiento (estancia)**.

## 3. Decisiones de arquitectura

1. **Se mantiene Python (FastAPI) y PostgreSQL.** No se reescribe en otro lenguaje.
2. **Monolito modular**, no microservicios. Un solo despliegue de backend con módulos internos desacoplados.
3. **Multi-tenant desde el principio**: cada camping es un `tenant`. Todas las tablas de negocio llevan `camping_id`. Aislamiento reforzado con Row Level Security (RLS) de PostgreSQL además del filtrado en la capa de aplicación.
4. **API-first**: contrato OpenAPI generado por FastAPI; los frontends consumen clientes tipados generados a partir de él.
5. **Monorepo**:
   ```
   /
   ├── backend/                # FastAPI
   ├── apps/
   │   ├── backoffice/         # Angular (migrar el actual /admin)
   │   ├── guest-pwa/          # PWA del campista (Angular + @angular/pwa)
   │   └── booking/            # Reserva online pública (ver nota)
   ├── packages/
   │   └── api-client/         # Cliente TypeScript generado desde OpenAPI
   ├── docs/
   └── docker-compose.yml
   ```
   Nota sobre `booking/`: la página pública necesita SEO y carga rápida. Se acepta empezar como una ruta pública dentro de `guest-pwa` y separarla después si hace falta (Next.js o widget embebible).
6. **Tareas en segundo plano** (emails, recordatorios, envío del registro de viajeros, generación de facturas): cola de trabajos (ARQ o Celery con Redis).
7. **Configuración por entorno** con `pydantic-settings` y `.env`. Ningún secreto en el código.

## 4. Stack objetivo

**Backend:** Python 3.12, FastAPI, SQLAlchemy 2.0 (async) + Alembic, Pydantic v2, `pydantic-settings`, PostgreSQL 16, Redis, ARQ (o Celery), pytest, Ruff, mypy.
**Frontend:** Angular 20 con standalone components y signals; Angular Material; `@angular/pwa` (service worker, manifest); i18n (ES, EN, FR, DE, NL como mínimo); cliente API generado con `openapi-typescript` o `openapi-generator`.
**Infra:** Docker Compose para desarrollo; despliegue objetivo: backend en contenedor, PostgreSQL gestionado, frontends estáticos en CDN.

## 5. Estructura del backend (módulos)

```
backend/app/
├── core/            # config, seguridad, db, dependencias, errores, logging
├── modules/
│   ├── tenants/     # campings (tenants) y su configuración
│   ├── auth/        # login staff, acceso huésped por enlace mágico / código de reserva
│   ├── users/       # personal del camping y roles
│   ├── accommodations/  # tipos de alojamiento y unidades (parcelas, bungalows, mobil-homes)
│   ├── pricing/     # temporadas, tarifas, suplementos, impuestos
│   ├── bookings/    # disponibilidad, reservas de estancia, estados
│   ├── guests/      # huéspedes y registro de viajeros
│   ├── payments/    # pasarela de pago (Redsys / Stripe), depósitos
│   ├── invoicing/   # facturas
│   ├── activities/  # actividades y sus reservas (ya existe, migrar)
│   ├── notifications/   # email y push
│   └── reporting/   # estadísticas y ocupación
└── main.py
```

Cada módulo contiene: `models.py`, `schemas.py`, `service.py` (lógica de negocio), `router.py`, `tests/`. Los routers no contienen lógica de negocio; los módulos se comunican por sus servicios, no accediendo a tablas ajenas.

## 6. Modelo de datos (núcleo)

Todas las tablas salvo `tenants` llevan `camping_id` (FK a `tenants.id`), `created_at`, `updated_at`. Usar UUID como clave primaria.

- **tenants**: nombre, slug, zona horaria, moneda, idiomas activos, datos fiscales, logo, colores.
- **users**: camping_id, email, password_hash, rol (`owner`, `admin`, `reception`, `housekeeping`), activo.
- **accommodation_types**: nombre, categoría (`pitch`, `bungalow`, `mobilhome`, `tent`…), capacidad máxima, descripción, fotos.
- **accommodation_units**: type_id, código/nombre (ej. "Parcela 42"), zona, coordenadas en el plano, estado operativo.
- **seasons**: nombre, fecha_inicio, fecha_fin, prioridad.
- **rates**: type_id, season_id, precio por noche, mínimo de noches, suplementos por persona/mascota/vehículo.
- **guests**: datos de contacto y documentación (ver sección 8 sobre datos personales).
- **bookings**: unit_id, titular (guest_id), fecha_entrada, fecha_salida, nº adultos/menores, estado (`pending`, `confirmed`, `checked_in`, `checked_out`, `cancelled`, `no_show`), importe total, código de reserva, origen (`backoffice`, `online`).
- **booking_guests**: relación reserva ↔ huéspedes (todos los viajeros).
- **payments**: booking_id, importe, método, estado, id de pasarela.
- **invoices**: booking_id, número correlativo por camping, líneas, impuestos, totales.
- **activities** y **activity_bookings**: migrar lo existente añadiendo `camping_id`; la reserva de actividad referencia opcionalmente a una `booking`.
- **notifications**: destinatario, canal, tipo, estado, plantilla.

**Regla crítica de disponibilidad:** una unidad no puede tener dos reservas activas con fechas solapadas. Garantizarlo **en base de datos** con una constraint de exclusión (`EXCLUDE USING gist` con `daterange` sobre `unit_id`, excluyendo reservas canceladas), no solo en código. Cubrir con tests de concurrencia.

## 7. Seguridad

- JWT de corta duración + refresh token. Secretos solo por variables de entorno.
- Hash de contraseñas con bcrypt o argon2.
- Autorización por rol con dependencia reutilizable (`require_role(...)`).
- El `camping_id` se obtiene del token del usuario autenticado, **nunca** del cuerpo o la URL que envía el cliente.
- RLS de Postgres activada en todas las tablas con `camping_id`.
- Acceso de huésped: enlace mágico o código de reserva + apellido, con rate limiting. Sin contraseña.
- Rate limiting en login y endpoints públicos. CORS configurable por entorno.
- Validación estricta con Pydantic; consultas siempre parametrizadas (con SQLAlchemy no se concatena SQL).
- Logs de auditoría para acciones sensibles (cambios de reserva, cobros, acceso a datos de huéspedes).

## 8. Cumplimiento legal (España)

> Esta sección recoge requisitos conocidos. **Antes de implementar y de prometerlos a clientes, verificar los requisitos y plazos vigentes** con fuentes oficiales o un asesor; la normativa cambia.

- **Registro de viajeros** (Real Decreto 933/2021, comunicación al Ministerio del Interior vía SES.Hospedajes): el sistema debe recoger los datos exigidos de cada viajero y permitir su comunicación. Diseñar el modelo de `guests` y el pre-check-in pensando en esto. Dejar la integración tras una interfaz (`TravelerRegistryGateway`) para poder implementarla o simularla por separado.
- **RGPD**: base legal y consentimientos, minimización de datos, derecho de acceso y supresión, plazo de conservación, cifrado en reposo de documentos de identidad, y rol de **encargado del tratamiento** (el camping es el responsable; este software es el encargado).
- **Facturación**: numeración correlativa por camping y preparación para Verifactu / factura electrónica. Dejar la emisión tras una interfaz (`InvoiceProvider`).
- **IVA y tasas turísticas**: configurables por camping y por zona.

## 9. PWA del campista (requisitos)

1. Acceso con enlace mágico o código de reserva.
2. Ver y gestionar su reserva.
3. **Pre-check-in**: rellenar online los datos de todos los viajeros antes de llegar.
4. Información del camping (normas, horarios, mapa, contacto) disponible **offline**.
5. Actividades: ver y reservar plazas.
6. Notificaciones push (avisos del camping).
7. Multi-idioma con detección automática.
8. Instalable (manifest, iconos, service worker), puntuación Lighthouse PWA correcta.

## 10. Backoffice (requisitos del MVP)

1. Plano o listado de unidades con estado de ocupación.
2. **Calendario de reservas** (vista tipo Gantt por unidad) con crear, mover y cancelar.
3. Ficha de reserva: huésped, viajeros, pagos, notas, historial.
4. Check-in y check-out rápidos, usables en tablet.
5. Gestión de tarifas, temporadas y alojamientos.
6. Dashboard con datos reales (ocupación, llegadas y salidas del día, ingresos).
7. Gestión de personal y roles.

## 11. Plan por fases

### Fase 0 — Cimientos (hacer primero)
- Reorganizar en monorepo; mover `admin/` a `apps/backoffice/`.
- Docker Compose (Postgres, Redis, backend).
- Backend: `pydantic-settings` + `.env.example`; eliminar la clave hardcodeada; SQLAlchemy 2 + Alembic con migración inicial; pool de conexiones; estructura modular.
- Migrar usuarios y actividades al nuevo esquema con `camping_id`.
- Roles y `require_role`.
- Pytest + CI (lint, tipos, tests).
- **Aceptación:** `docker compose up` levanta todo; las migraciones se aplican en una base vacía; login funciona con roles; tests verdes en CI; no queda ningún secreto en el repo.

### Fase 1 — Núcleo de reservas
- Módulos `accommodations`, `pricing`, `bookings`, `guests`.
- Constraint de exclusión para solapamientos y tests de concurrencia.
- Cálculo de precio por estancia (temporadas, suplementos, mínimo de noches).
- Backoffice: listado de unidades, calendario, alta y edición de reservas, check-in/out.
- **Aceptación:** no es posible crear dos reservas solapadas ni por API ni por carrera de peticiones; el precio calculado coincide con tests definidos por temporadas; el flujo completo alta → check-in → check-out funciona desde el backoffice.

### Fase 2 — PWA del campista y pre-check-in
- Acceso por enlace mágico, vista de reserva, formulario de pre-check-in, información offline, i18n.
- Interfaz `TravelerRegistryGateway` con implementación simulada.
- **Aceptación:** un huésped completa el pre-check-in desde el móvil; la app se instala y muestra información offline; Lighthouse PWA sin errores críticos.

### Fase 3 — Pagos, facturación y notificaciones
- Pasarela de pago (Stripe o Redsys) con depósito y pago final; webhooks idempotentes.
- Facturas con numeración correlativa; interfaz `InvoiceProvider`.
- Emails transaccionales (confirmación, recordatorio de pre-check-in) y push.
- **Aceptación:** reserva online completa con pago de prueba; factura generada; emails enviados por la cola.

### Fase 4 — Reserva online pública y multi-camping
- Página pública de reserva con disponibilidad en tiempo real; widget embebible.
- Alta de nuevos campings (onboarding), tema por camping (logo y colores).
- Estadísticas y reporting.
- **Aceptación:** un segundo camping de prueba funciona de forma aislada del primero (verificado con tests de aislamiento entre tenants).

## 12. Reglas de trabajo para el agente

- Trabaja en una **rama por fase** y haz commits pequeños y descriptivos. No hagas push a `main` ni abras PR sin que te lo pidan.
- Antes de cada fase, lista los archivos que vas a crear o cambiar y confirma el alcance.
- Cada funcionalidad nueva lleva **tests**. No se da por terminada una tarea con tests en rojo.
- No añadas dependencias sin justificarlo. No introduzcas librerías de pago ni servicios externos sin avisar.
- No hardcodees secretos, URLs de entornos ni credenciales. Todo por variables de entorno, con `.env.example` actualizado.
- Todo acceso a datos de negocio filtra por `camping_id`; añade siempre un test de aislamiento entre tenants.
- No implementes integraciones legales (registro de viajeros, Verifactu) como si fueran definitivas: déjalas tras interfaces con una implementación simulada y márcalas como pendientes de validación.
- Si algo del documento es ambiguo o choca con el código existente, **pregunta** antes de decidir.
- Mantén actualizados `README.md` y `docs/` al terminar cada fase.

## 13. Fuera de alcance por ahora

Channel manager (Booking, Airbnb), TPV de bar y tienda, gestión de limpieza avanzada, programa de fidelización, app nativa. Se valoran tras validar el MVP con campings piloto.

## 14. Preguntas abiertas (a resolver con la persona responsable del producto)

1. ¿Cuál es el software francés de referencia y qué módulos concretos se quieren emular?
2. Pasarela de pago preferida: ¿Stripe o Redsys?
3. ¿Despliegue en un proveedor concreto?
4. ¿Hay uno o dos campings piloto identificados?
5. Idiomas obligatorios en el lanzamiento.
