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