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