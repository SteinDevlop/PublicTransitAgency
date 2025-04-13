# Public Transit Agency

## Overview

**Public Transit Agency** is a comprehensive, modular software solution aimed at modernizing public transportation systems. Built using a microservices architecture and leveraging cloud-native technologies, it replaces legacy systems with scalable, maintainable, and interoperable components.  

Key features include:

- Fleet and route management    
- Driver and operator administration  
- Passenger information portal with real-time schedule and availability updates

This platform is designed to enhance operational efficiency, data transparency, and overall user experience in urban transit environments.

---

## 📈 Project Status

> **Current Phase**: In Development  

[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_PublicTransitAgency&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_PublicTransitAgency)  
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=ISCODEVUTB_PublicTransitAgency&metric=coverage)](https://sonarcloud.io/summary/new_code?id=ISCODEVUTB_PublicTransitAgency)

---

## ⚙️ Installation & Setup

### 🐍 Requirements

- Python 3.9+
- Docker (for containerized environments)
- Flutter

### 🔧 Local Setup

1. Clone the repository  
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   > Required libraries include:
   ```text
   fastapi
   uvicorn
   jinja2
   pytest
   pytest-cov
   ```

### 🐳 Docker Support

Deployment and development environments are containerized using a custom `Dockerfile`.  
Compatible with Linux-based systems, the container includes all necessary configurations and dependencies for consistent environment replication.

---

## 🗂️ Project Structure

```
PUBLIC TRANSIT AGENCY
├───.github
│   └───workflows
├───docs
└───src
    ├───backend
    │   └───app
    │       ├───data
    │       ├───logic
    │       ├───models
    │       ├───routes
    │       ├───templates
    │       └───test
    └───frontend
        ├───assets
        ├───lib
        ├───templates
        │   └───img
        └───web
```

---

## 🧠 Class and Function Reference

Each system component is modeled using Python classes to reflect real-world entities:

### 👤 Users

#### `User`
- `login(self)`: Abstract method to authenticate user.
- `logout(self)`: Abstract method to log out.

#### `Administrator`
- `manage_routes(self)`: Manages transport routes.
- `manage_schedules(self)`: Manages transport schedules.
- `manage_users(self)`: Manages system users.
- `generate_reports(self)`: Generates system reports.

#### `OperationalSupervisor`
- `assign_shifts(self)`: Assigns shifts to drivers.
- `monitor_units(self)`: Monitors transport units.
- `record_incidents(self)`: Records operational incidents.

#### `Driver`
- `check_shifts(self)`: Checks assigned shifts.
- `report_incident(self)`: Reports an incident.

#### `PassengerUser`
- `check_schedules(self)`: Checks transport schedules.
- `make_payment(self)`: Makes a payment.
- `submit_complaint(self)`: Submits a complaint.

#### `MaintenanceTechnician`
- `record_maintenance(self)`: Logs maintenance activities.
- `check_unit_history(self)`: Checks maintenance history of a unit.

---

### 🚌 Transport Entities

#### `Card`
- `use_card(self)`: Abstract method to use the card.

#### `TransportUnit`
- `update_status(self)`: Updates the status of the unit.
- `send_alert(self)`: Sends an alert regarding the unit.

#### `Route`
- `update_route(self)`: Updates the route information.

#### `Stop`
- `register_stop(self)`: Registers a new stop.

#### `Schedule`
- `adjust_schedule(self)`: Adjusts the schedule timings.

#### `Shift`
- `assign_shift(self)`: Assigns a shift to a driver.
- `change_shift(self)`: Modifies the assigned shift.

#### `GPS`
- `get_location(self)`: Retrieves the current location.
- `send_alert(self)`: Sends an alert regarding GPS data.

#### `Incident`
- `register_incident(self)`: Logs a new incident.
- `update_status(self)`: Updates the status of an incident.

#### `Maintenance`
- `schedule_maintenance(self)`: Schedules maintenance for a unit.
- `update_status(self)`: Updates maintenance status.

#### `Report`
- `generate_report(self)`: Creates a new report.
- `export(self)`: Exports the report data.

#### `Notification`
- `send_notification(self)`: Sends a notification message.

#### `Payment`
- `process_payment(self)`: Processes a payment transaction.
- `validate_ticket(self)`: Validates a transport ticket.

---

## 👥 Development Team

- **Mario Alberto Julio Wilches**  
- **Andrés Felipe Rubiano Marrugo**  
- **Alejandro Pedro Steinman Cuesta**

---
