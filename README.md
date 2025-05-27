# Public Transit Agency

## Overview

**Public Transit Agency** is a comprehensive, modular solution for managing urban public transportation systems. The platform is designed to replace legacy systems, optimizing fleet management, routes, schedules, users, and daily operations through a microservices architecture and cloud-native technologies. Its goal is to improve operational efficiency, data transparency, and the experience for both users and operators/administrators.

The system provides features for managing transport units, drivers and operators, a passenger information portal with real-time updates, electronic payment processing, incident and maintenance management, and more.

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

> **Current Phase:** In Development

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
│       ├── assets
│       ├── lib              # Flutter source code
│       ├── templates
│       │   └── img
│       └── web
```

---

## 🧩 Class and Module Documentation

### Module: `models`

#### Users and Roles

- **User (abstract)**
  - Methods:
    - `login(self)`: User authentication.
    - `logout(self)`: Logout.

- **Administrator (User)**
  - Methods:
    - `manage_routes(self)`: Manage routes.
    - `manage_schedules(self)`: Manage schedules.
    - `manage_users(self)`: Manage users.
    - `generate_reports(self)`: Generate reports.

- **OperationalSupervisor (User)**
  - Methods:
    - `assign_shifts(self)`: Assign shifts to drivers.
    - `monitor_units(self)`: Monitor transport units.
    - `record_incidents(self)`: Record incidents.

- **Driver (User)**
  - Methods:
    - `check_shifts(self)`: Check assigned shifts.
    - `report_incident(self)`: Report incidents.

- **PassengerUser (User)**
  - Methods:
    - `check_schedules(self)`: Check schedules and routes.
    - `make_payment(self)`: Make electronic payments.
    - `submit_complaint(self)`: Submit complaints or suggestions.

- **MaintenanceTechnician (User)**
  - Methods:
    - `record_maintenance(self)`: Log maintenance activities.
    - `check_unit_history(self)`: Check unit maintenance history.

#### Transport Entities

- **Card**
  - Methods:
    - `use_card(self)`: Use and validate transport card.

- **TransportUnit**
  - Methods:
    - `update_status(self)`: Update unit status.
    - `send_alert(self)`: Send unit alerts.

- **Route**
  - Methods:
    - `update_route(self)`: Update route information.

- **Stop**
  - Methods:
    - `register_stop(self)`: Register a new stop.

- **Schedule**
  - Methods:
    - `adjust_schedule(self)`: Adjust schedules.

- **Shift**
  - Methods:
    - `assign_shift(self)`: Assign shift to driver.
    - `change_shift(self)`: Modify shift.

- **Incident**
  - Methods:
    - `register_incident(self)`: Register an incident.
    - `update_status(self)`: Update incident status.

- **Maintenance**
  - Methods:
    - `schedule_maintenance(self)`: Schedule maintenance.
    - `update_status(self)`: Update maintenance status.

- **Report**
  - Methods:
    - `generate_report(self)`: Generate reports.
    - `export(self)`: Export report data.

- **Notification**
  - Methods:
    - `send_notification(self)`: Send notifications to users.

- **Payment**
  - Methods:
    - `process_payment(self)`: Process payments.
    - `validate_ticket(self)`: Validate electronic tickets.

---

### Module: `routes`

Defines RESTful endpoints for system interaction, organized by resources (users, routes, units, payments, etc.) using FastAPI.

### Module: `logic`

Contains business logic, services, and validations for each entity and process in the system.

### Module: `data`

Implements data access, repositories, and integration with relational/non-relational databases.

### Module: `frontend/lib`

Flutter source code for the user interface, for both passengers and operators/administrators.

---

## 👥 Development Team

- **Mario Alberto Julio Wilches**
- **Andrés Felipe Rubiano Marrugo**
- **Alejandro Pedro Steinman Cuesta**

---

