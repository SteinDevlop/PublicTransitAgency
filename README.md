# Public Transit Agency

## Description

The **Public Transit Agency** software development focuses on creating a modern software architecture for public transportation systems, transitioning from outdated, isolated systems. This solution employs a microservices architecture and a cloud data warehouse to enhance data sharing and analysis across departments. Key functionalities include fleet and route management, real-time vehicle monitoring, administration of drivers and operators, and a passenger information portal that provides real-time updates on schedules, routes, and availability, ultimately improving user experience and operational efficiency.

## Project Status

The project is currently in progress.

## Installation  

The **Public Transit Agency** requires Python 3.9 or later.

### **Implementation**

For the proper implementation of this development, you need to install the required dependencies listed in the requirements.txt file by running the following command:

    ```
    pip install -r requirements.tx
    ```
    
This archive has to have the following libraries:

    ```
    ```
For executing the application we will use:

    ```
    python main.py
    ```

### **Docker**

The development environment is configured through our `Dockerfile`, designed for use on Linux enviroment. It defines dependencies, configurations, and setup commands, ensuring a consistent and reproducible deployment.
## Estructure

```
📦 PublicTransitAgency
├── 📜 coverage.ini
├── 📜 Dockerfile
├── 📜 estructura.txt
├── 📜 LICENSE
├── 📜 pytest.ini
├── 📜 README.md
├── 📜 requirements.txt
├── 📜 sonar-project.properties
│
├── 📂 .github/workflows
│   ├── build.yml
│   ├── docker-image.yml
│   ├── python-app.yml
│
├── 📂 docs
│   ├── __init__.py
│
└── 📂 src
    ├── 📂 backend
    │   ├── 📂 app
    │   │   ├── config.py
    │   │   ├── main.py
    │   │   │
    │   │   ├── 📂 models
    │   │   │   ├── __init__.py
    │   │   │
    │   │   ├── 📂 routes
    │   │   │   ├── __init__.py
    │   │   │
    │   │   ├── 📂 services
    │   │   │   ├── __init__.py
    │
    ├── 📂 frontend
    │   ├── 📂 assets
    │   │   ├── __init__.py
    │   │
    │   ├── 📂 lib
    │   │   ├── __init__.py
    │   │
    │   ├── 📂 web
    │   │   ├── __init__.py
```
## Classes descriptions and funtions
### **User**
`User(self, user_id, name, email, password, role)` - Base class for all users.
- `login(self)` - Abstract method to log in.
- `logout(self)` - Abstract method to log out.

### **Administrator**
- `manage_routes(self)` - Manages transport routes.
- `manage_schedules(self)` - Manages transport schedules.
- `manage_users(self)` - Manages system users.
- `generate_reports(self)` - Generates system reports.

### **OperationalSupervisor**
- `assign_shifts(self)` - Assigns shifts to drivers.
- `monitor_units(self)` - Monitors transport units.
- `record_incidents(self)` - Records operational incidents.

### **Driver**
`Driver(self, user_id, name, email, password, role, license, assigned_shift)` - Represents a driver with a license and assigned shift.
- `check_shifts(self)` - Checks assigned shifts.
- `report_incident(self)` - Reports an incident.

### **PassengerUser**
- `check_schedules(self)` - Checks transport schedules.
- `make_payment(self)` - Makes a payment.
- `submit_complaint(self)` - Submits a complaint.

### **MaintenanceTechnician**
- `record_maintenance(self)` - Logs maintenance activities.
- `check_unit_history(self)` - Checks maintenance history of a unit.

### **Card**
`Card(self, card_id, type, balance)` - Represents a payment or access card.
- `use_card(self)` - Abstract method to use the card.

### **TransportUnit**
`TransportUnit(self, unit_id, type, capacity, status, current_location)` - Represents a transportation unit.
- `update_status(self)` - Updates the status of the unit.
- `send_alert(self)` - Sends an alert regarding the unit.

### **Route**
`Route(self, route_id, origin, destination, stops, estimated_duration)` - Defines a transport route.
- `update_route(self)` - Updates the route information.

### **Stop**
`Stop(self, stop_id, name, location)` - Represents a stop along a route.
- `register_stop(self)` - Registers a new stop.

### **Schedule**
`Schedule(self, schedule_id, route, departure_time, arrival_time)` - Manages transport schedules.
- `adjust_schedule(self)` - Adjusts the schedule timings.

### **Shift**
`Shift(self, shift_id, driver, unit, schedule)` - Assigns a driver and unit to a schedule.
- `assign_shift(self)` - Assigns a shift to a driver.
- `change_shift(self)` - Modifies the assigned shift.

### **GPS**
`GPS(self, unit, current_coordinates)` - Tracks a transport unit’s location.
- `get_location(self)` - Retrieves the current location.
- `send_alert(self)` - Sends an alert regarding GPS data.

### **Incident**
`Incident(self, incident_id, type, description, status)` - Records incidents related to transport operations.
- `register_incident(self)` - Logs a new incident.
- `update_status(self)` - Updates the status of an incident.

### **Maintenance**
`Maintenance(self, maintenance_id, unit, date, type, status)` - Manages vehicle maintenance records.
- `schedule_maintenance(self)` - Schedules maintenance for a unit.
- `update_status(self)` - Updates maintenance status.

### **Report**
`Report(self, report_id, type, generated_data)` - Generates various system reports.
- `generate_report(self)` - Creates a new report.
- `export(self)` - Exports the report data.

### **Notification**
`Notification(self, notification_id, message, recipient)` - Sends notifications to users.
- `send_notification(self)` - Sends a notification message.

### **Payment**
`Payment(self, payment_id, user, amount, payment_method)` - Processes user payments.
- `process_payment(self)` - Processes a payment transaction.
- `validate_ticket(self)` - Validates a transport ticket.
---


## Team

- Mario Alberto Julio Wilches

- Andrés Felipe Rubiano Marrugo

- Alejandro Pedro Steinman Cuesta
