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

## 👥 Development Team

- **Mario Alberto Julio Wilches**
- **Andrés Felipe Rubiano Marrugo**
- **Alejandro Pedro Steinman Cuesta**

---

