# Public Transit Agency

## Overview

**Public Transit Agency** is a comprehensive, modular solution for managing urban public transportation systems. The platform is designed to replace legacy systems, optimizing fleet management, routes, schedules, users, and daily operations through a microservices architecture and cloud-native technologies. Its goal is to improve operational efficiency, data transparency, and the experience for both users and operators/administrators.

The system provides features for managing transport units, drivers and operators, a passenger information portal with real-time updates, electronic payment processing, incident and maintenance management, and more.

Backend link: [publictransitagency-production.up.railway.app](https://publictransitagency-production.up.railway.app/docs)
Frontend link: [publictransitagency-frontend-production.up.railway.app](https://publictransitagency-frontend-production.up.railway.app/#/home)
---

## 🚦 Main Functional Requirements

1. **User and Role Management**
   - Registration, authentication, and administration of users with different roles: Administrator, Operational Supervisor, Driver, Maintenance Technician, and Passenger.
   - Role-based permissions for accessing and operating different system features.

2. **Fleet and Unit Management**
   - Registration, updating, and monitoring of transport units (buses, trams, etc.).
   - Assignment of units to routes and shifts.

3. **Route and Stop Management**
   - Creation, editing, and deletion of routes and stops.
   - Visualization of active routes and their real-time status.

4. **Schedule and Shift Management**
   - Definition and adjustment of operation schedules.
   - Assignment and modification of driver shifts.

5. **Passenger Portal**
   - Real-time consultation of schedules, routes, and availability.
   - Purchase and validation of electronic tickets.
   - Submission of complaints and suggestions.

6. **Incident and Maintenance Management**
   - Registration and tracking of operational and technical incidents.
   - Scheduling and logging of preventive and corrective maintenance activities.

7. **Reports and Notifications**
   - Generation of operational and administrative reports.
   - Sending notifications to users and operators.

---

## 📈 Project Status

> **Current Phase:** Completed

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_PublicTransitAgency&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_PublicTransitAgency)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_PublicTransitAgency&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_PublicTransitAgency)

---

## ⚙️ Installation & Setup

### Requirements

- Python 3.9+
- Docker (for containerized environments)
- Flutter (for mobile/web frontend)

### Local Setup

1. Clone the repository.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   > Required libraries include:
   ```text
   fastapi
   uvicorn
   jose
   typing
   pytest
   pytest-cov
   ```

### Docker Support

Development and deployment environments are containerized using a custom `Dockerfile`, compatible with Linux systems. It includes all necessary configurations and dependencies for consistent environment replication.

---

## 🗂️ Project Structure

```
PUBLIC TRANSIT AGENCY
├── .github
│   └── workflows
├── docs
├── src
│   ├── backend
│   │   └── app
│   │       ├── data         # Data access and repositories
│   │       ├── logic        # Business logic and services
│   │       ├── models       # Domain and ORM models
│   │       ├── routes       # FastAPI endpoints and controllers
│   │       ├── templates    # Jinja2 templates for views
│   │       └── tests        # Unit and integration tests
│   └── frontend
│       ├── android          # Android-specific files
│       ├── assets           # Static assets (e.g., images)
│       ├── build            # Build outputs
│       ├── ios              # iOS-specific files
│       ├── lib              # Flutter source code
│       ├── linux            # Linux-specific files
│       ├── macos            # macOS-specific files
│       ├── static           # Static files (CSS, JS, etc.)
│       ├── templates        # HTML templates
│       ├── web              # Web-specific files
│       └── windows          # Windows-specific files
```

---

## 🧩 Microservices and Models Documentation

### Module: `models`

#### User Model
- **Entity Name**: `Usuario`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `Identificacion`: INTEGER
  - `Nombre`: VARCHAR(100)
  - `Apellido`: VARCHAR(100)
  - `Correo`: VARCHAR(100)
  - `Contrasena`: VARCHAR(100)
  - `IDRolUsuario`: INTEGER
  - `IDTurno`: INTEGER
  - `IDTarjeta`: INTEGER
- **Out**:
  - Inherits all fields from `UserCreate`.

#### Type Transport Model
- **Entity Name**: `tipotransporte`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `TipoTransporte`: VARCHAR(20)
- **Out**:
  - Inherits all fields from `TypeTransportCreate`.

#### Type Movement Model
- **Entity Name**: `TipoMovimiento`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `TipoMovimiento`: VARCHAR(20)
- **Out**:
  - Inherits all fields from `TypeMovementCreate`.

#### Type Card Model
- **Entity Name**: `tipotarjeta`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `Tipo`: VARCHAR(20)
- **Out**:
  - Inherits all fields from `TypeCardCreate`.

#### Transport Unit Model
- **Entity Name**: `UnidadTransporte`
- **In**:
  - `Ubicacion`: VARCHAR(200)
  - `Capacidad`: INT
  - `IDRuta`: INT
  - `IDTipo`: INT
  - `ID`: VARCHAR(20)

#### Ticket Model
- **Entity Name**: `Ticket`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `EstadoIncidencia`: VARCHAR(20) NOT NULL

#### Stops Model
- **Entity Name**: `Parada`
- **In**:
  - `ID`: INT PRIMARY KEY
  - `Ubicacion`: VARCHAR NOT NULL
  - `Nombre`: VARCHAR NOT NULL

#### Shift Model
- **Entity Name**: `Turno`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `TipoTurno`: VARCHAR(30) NOT NULL

#### Schedule Model
- **Entity Name**: `horario`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `Llegada`: TIME NOT NULL
  - `Salida`: TIME NOT NULL

#### Route-Stop Relationship Model
- **Entity Name**: `RutaParada`
- **In**:
  - `IDRuta`: INT NOT NULL
  - `IDParada`: INT NOT NULL

#### Route Model
- **Entity Name**: `Rutas`
- **In**:
  - `ID`: INT PRIMARY KEY
  - `IDHorario`: INT NOT NULL
  - `Nombre`: VARCHAR(255) NOT NULL

#### Role-User Model
- **Entity Name**: `RolUsuario`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `Rol`: VARCHAR(20)
- **Out**:
  - Inherits all fields from `RolUserCreate`.

#### Price Model
- **Entity Name**: `Precio`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `IDTipoTransporte`: INTEGER
  - `Monto`: FLOAT
- **Out**:
  - Inherits all fields from `PriceCreate`.

#### PQR Model
- **Entity Name**: `PQR`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `identificationuser`: INTEGER
  - `type`: VARCHAR
  - `description`: VARCHAR
  - `fecha`: VARCHAR
- **Out**:
  - Inherits all fields from `PQRCreate`.

#### Payment Model
- **Entity Name**: `Pago`
- **In**:
  - `IDMovimiento`: INTEGER NOT NULL
  - `IDPrecio`: INTEGER NOT NULL
  - `IDTarjeta`: INTEGER NOT NULL
  - `IDUnidad`: VARCHAR(20) NOT NULL DEFAULT 'EMPTY'
  - `ID`: INTEGER NOT NULL

#### Movement Model
- **Entity Name**: `Movimiento`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `IDTipoMovimiento`: INTEGER
  - `Monto`: FLOAT
- **Out**:
  - Inherits all fields from `MovementCreate`.

#### Maintenance Model
- **Entity Name**: `mantenimientoins`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `id_status`: INTEGER
- **Out**:
  - Inherits all fields from `MaintenanceCreate`.

#### Maintenance Status Model
- **Entity Name**: `EstadoMantenimiento`
- **In**:
  - `ID`: INT NOT NULL PRIMARY KEY
  - `TipoEstado`: VARCHAR(100) NOT NULL

#### Incidence Model
- **Entity Name**: `Incidencia`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `IDTicket`: INTEGER NOT NULL
  - `Descripcion`: VARCHAR(255) NOT NULL
  - `Tipo`: VARCHAR(50) NOT NULL
  - `IDUnidad`: VARCHAR(50) NOT NULL

#### Card Model
- **Entity Name**: `TarjetaIns`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `IDUsuario`: INTEGER
  - `IDTipoTarjeta`: INTEGER
  - `Saldo`: INTEGER
- **Out**:
  - Inherits all fields from `CardCreate`.

#### Behavior Model
- **Entity Name**: `Rendimiento`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `cantidadrutas`: INTEGER
  - `horastrabajadas`: INTEGER
  - `observaciones`: VARCHAR
  - `fecha`: VARCHAR
- **Out**:
  - Inherits all fields from `BehaviorCreate`.

#### Assistance Model
- **Entity Name**: `Asistencia`
- **In**:
  - `ID`: INTEGER PRIMARY KEY
  - `iduser`: INTEGER
  - `horainicio`: VARCHAR
  - `horafinal`: VARCHAR
  - `fecha`: VARCHAR
- **Out**:
  - Inherits all fields from `AsistanceCreate`.

---

### Module: `routes`

#### User Service
- **Endpoints**:
  - `GET /user/users`: Retrieve all users.
  - `GET /user/usuario`: Retrieve a user by ID.
  - `POST /user/create`: Create a new user.
  - `POST /user/update`: Update an existing user.
  - `POST /user/delete`: Delete a user by ID.

#### Price Service
- **Endpoints**:
  - `GET /price/pasajero/prices`: Retrieve all prices for passengers.
  - `POST /price/create`: Create a new price.
  - `POST /price/update`: Update an existing price.
  - `POST /price/delete`: Delete a price by ID.

#### Maintenance Service
- **Endpoints**:
  - `GET /maintainancements`: Retrieve all maintenance records.
  - `POST /maintainance/create`: Add a new maintenance record.
  - `POST /maintainance/update`: Update an existing maintenance record.
  - `POST /maintainance/delete`: Delete a maintenance record by ID.

#### Assistance Service
- **Endpoints**:
  - `GET /asistance/asistencias`: Retrieve all assistance records.
  - `GET /asistance/user`: Retrieve assistance records by user ID.
  - `POST /asistance/create`: Create a new assistance record.
  - `POST /asistance/update`: Update an existing assistance record.
  - `POST /asistance/delete`: Delete an assistance record by ID.

#### Behavior Service
- **Endpoints**:
  - `GET /behavior/supervisor/behaviors`: Retrieve all behaviors for supervisors.
  - `GET /behavior/administrador/behaviors`: Retrieve all behaviors for administrators.
  - `POST /behavior/create`: Create a new behavior record.
  - `POST /behavior/update`: Update an existing behavior record.
  - `POST /behavior/delete`: Delete a behavior record by ID.

#### Movement Service
- **Endpoints**:
  - `GET /movement/pasajero/movements`: Retrieve all movements for passengers.
  - `POST /movement/create`: Create a new movement.
  - `POST /movement/update`: Update an existing movement.
  - `POST /movement/delete`: Delete a movement by ID.

#### Card Service
- **Endpoints**:
  - `GET /card/tarjetas`: Retrieve all cards.
  - `GET /card/tarjeta`: Retrieve a card by ID.
  - `POST /card/create`: Create a new card.
  - `POST /card/update`: Update an existing card.
  - `POST /card/delete`: Delete a card by ID.

#### Route Service
- **Endpoints**:
  - `GET /routes/`: Retrieve all routes.
  - `GET /routes/{ID}`: Retrieve a route by ID.
  - `POST /routes/create`: Create a new route.
  - `POST /routes/update`: Update an existing route.
  - `POST /routes/delete`: Delete a route by ID.

#### Stop Service
- **Endpoints**:
  - `GET /stops/`: Retrieve all stops.
  - `GET /stops/{id}`: Retrieve a stop by ID.
  - `POST /stops/create`: Create a new stop.
  - `POST /stops/update`: Update an existing stop.
  - `POST /stops/delete`: Delete a stop by ID.

#### Schedule Service
- **Endpoints**:
  - `GET /schedules/`: Retrieve all schedules.
  - `GET /schedules/{id}`: Retrieve a schedule by ID.
  - `POST /schedules/create`: Create a new schedule.
  - `POST /schedules/update`: Update an existing schedule.
  - `POST /schedules/delete`: Delete a schedule by ID.

#### Shift Service
- **Endpoints**:
  - `GET /shifts/`: Retrieve all shifts.
  - `GET /shifts/{id}`: Retrieve a shift by ID.
  - `POST /shifts/create`: Create a new shift.
  - `POST /shifts/update`: Update an existing shift.
  - `POST /shifts/delete`: Delete a shift by ID.

#### Payment Service
- **Endpoints**:
  - `GET /payments/`: Retrieve all payments.
  - `GET /payments/{ID}`: Retrieve a payment by ID.
  - `POST /payments/create`: Create a new payment.
  - `POST /payments/update`: Update an existing payment.
  - `POST /payments/delete`: Delete a payment by ID.

#### Ticket Service
- **Endpoints**:
  - `GET /tickets/`: Retrieve all tickets.
  - `GET /tickets/{ID}`: Retrieve a ticket by ID.
  - `POST /tickets/create`: Create a new ticket.
  - `POST /tickets/update`: Update an existing ticket.
  - `POST /tickets/delete`: Delete a ticket by ID.

#### Incidence Service
- **Endpoints**:
  - `GET /incidences/`: Retrieve all incidences.
  - `GET /incidences/{ID}`: Retrieve an incidence by ID.
  - `POST /incidences/create`: Create a new incidence.
  - `POST /incidences/update`: Update an existing incidence.
  - `POST /incidences/delete`: Delete an incidence by ID.

#### Report Service
- **Endpoints**:
  - `GET /reporte/supervisor`: Generate a supervisor report.
  - `GET /reporte/alert-tec`: Generate a technical alert report.

#### Planner Service
- **Endpoints**:
  - `POST /planificador/ubicaciones`: Get route planning based on start and end locations.

#### Maintenance Status Service
- **Endpoints**:
  - `GET /maintainance_status/`: Retrieve all maintenance statuses.
  - `GET /maintainance_status/{id}`: Retrieve a maintenance status by ID.
  - `POST /maintainance_status/create`: Create a new maintenance status.
  - `POST /maintainance_status/update`: Update an existing maintenance status.
  - `POST /maintainance_status/delete`: Delete a maintenance status by ID.

#### Route-Stop Relationship Service
- **Endpoints**:
  - `GET /ruta_parada/`: Retrieve all route-stop relationships.
  - `GET /ruta_parada/{id_parada}`: Retrieve route-stop relationships by stop ID.
  - `POST /rutaparada/create`: Create a new route-stop relationship.
  - `POST /rutaparada/update`: Update an existing route-stop relationship.
  - `POST /rutaparada/delete`: Delete a route-stop relationship by ID.

#### Transport Unit Service
- **Endpoints**:
  - `GET /transport_units/`: Retrieve all transport units.
  - `GET /transport_units/{ID}`: Retrieve a transport unit by ID.
  - `POST /transport_units/create`: Create a new transport unit.
  - `POST /transport_units/update`: Update an existing transport unit.
  - `POST /transport_units/delete`: Delete a transport unit by ID.

#### Type of Transport Service
- **Endpoints**:
  - `GET /typetransports`: Retrieve all types of transport.
  - `POST /typetransport/create`: Create a new type of transport.
  - `POST /typetransport/update`: Update an existing type of transport.
  - `POST /typetransport/delete`: Delete a type of transport by ID.

#### Type of Movement Service
- **Endpoints**:
  - `GET /typemovements`: Retrieve all types of movements.
  - `POST /typemovement/create`: Create a new type of movement.
  - `POST /typemovement/update`: Update an existing type of movement.
  - `POST /typemovement/delete`: Delete a type of movement by ID.

#### Role-User Service
- **Endpoints**:
  - `GET /rolusers`: Retrieve all roles for users.
  - `POST /roluser/create`: Create a new role for a user.
  - `POST /roluser/update`: Update an existing role for a user.
  - `POST /roluser/delete`: Delete a role for a user by ID.

#### PQR Service
- **Endpoints**:
  - `GET /pqr/pqrs`: Retrieve all PQR records.
  - `POST /pqr/create`: Create a new PQR record.
  - `POST /pqr/update`: Update an existing PQR record.
  - `POST /pqr/delete`: Delete a PQR record by ID.

---

## 👥 Development Team

- **Mario Alberto Julio Wilches**
- **Andrés Felipe Rubiano Marrugo**
- **Alejandro Pedro Steinman Cuesta**

---

