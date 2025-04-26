-- Table: Movement
CREATE TABLE dbo.Movement (
    ID int IDENTITY(1,1) NOT NULL,
    MovementTypeID int NOT NULL,
    Amount int NOT NULL,
    CONSTRAINT PK_Movement PRIMARY KEY (ID)
);

ALTER TABLE dbo.Movement 
ADD CONSTRAINT FK_Movement_MovementType 
FOREIGN KEY (MovementTypeID) REFERENCES .dbo.MovementType(ID);

-- Table: MovementType
CREATE TABLE dbo.MovementType (
    ID int NOT NULL,
    MovementType varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_MovementType PRIMARY KEY (ID)
);
-- Table: Payment
CREATE TABLE dbo.Payment (
    MovementID int NOT NULL,
    PaymentID int NOT NULL,
    CardID int NOT NULL,
    TransportID int NOT NULL
);

ALTER TABLE dbo.Payment 
ADD CONSTRAINT FK_Payment_Movement FOREIGN KEY (MovementID) REFERENCES .dbo.Movement(ID),
    CONSTRAINT FK_Payment_Payment FOREIGN KEY (PaymentID) REFERENCES .dbo.Price(ID),
    CONSTRAINT FK_Payment_Card FOREIGN KEY (CardID) REFERENCES .dbo.Card(ID),
    CONSTRAINT FK_Payment_Transport FOREIGN KEY (TransportID) REFERENCES .dbo.TransportUnit(ID);

-- Table: Price
CREATE TABLE dbo.Price (
    ID int NOT NULL,
    TransportTypeID int NOT NULL,
    Amount int NOT NULL,
    CONSTRAINT PK_Price PRIMARY KEY (ID)
);

ALTER TABLE dbo.Price 
ADD CONSTRAINT FK_Price_TransportType FOREIGN KEY (TransportTypeID) REFERENCES .dbo.TransportType(ID);

-- Table: TransportType
CREATE TABLE dbo.TransportType (
    ID int NOT NULL,
    TransportType varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_TransportType PRIMARY KEY (ID)
);

-- Table: MaintenanceStatus
CREATE TABLE dbo.MaintenanceStatus (
    ID int NOT NULL,
    StatusType varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_MaintenanceStatus PRIMARY KEY (ID)
);

-- Table: Maintenance
CREATE TABLE dbo.Maintenance (
    ID int IDENTITY(1,1) NOT NULL,
    StatusID int NOT NULL,
    Type varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Date date NOT NULL,
    TransportUnitID int NOT NULL,
    CONSTRAINT PK_Maintenance PRIMARY KEY (ID)
);

ALTER TABLE dbo.Maintenance 
ADD CONSTRAINT FK_Maintenance_Status FOREIGN KEY (StatusID) REFERENCES .dbo.MaintenanceStatus(ID),
    CONSTRAINT FK_Maintenance_TransportUnit FOREIGN KEY (TransportUnitID) REFERENCES .dbo.TransportUnit(ID);

-- Table: TransportUnit
CREATE TABLE dbo.TransportUnit (
    ID int IDENTITY(1,1) NOT NULL,
    Location varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Capacity int NOT NULL,
    RouteID int NOT NULL,
    TransportTypeID int NOT NULL,
    CONSTRAINT PK_TransportUnit PRIMARY KEY (ID)
);

ALTER TABLE dbo.TransportUnit 
ADD CONSTRAINT FK_TransportUnit_Route FOREIGN KEY (RouteID) REFERENCES .dbo.Route(ID),
    CONSTRAINT FK_TransportUnit_TransportType FOREIGN KEY (TransportTypeID) REFERENCES .dbo.TransportType(ID);
-- Table: Incident
CREATE TABLE dbo.Incident (
    ID int NOT NULL,
    TicketID int NOT NULL,
    Description varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Type varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    TransportUnitID int NOT NULL,
    CONSTRAINT PK_Incident PRIMARY KEY (ID),
    CONSTRAINT UQ_Incident_Ticket UNIQUE (TicketID)
);

ALTER TABLE dbo.Incident 
ADD CONSTRAINT FK_Incident_Ticket FOREIGN KEY (TicketID) REFERENCES .dbo.Ticket(ID);

-- Table: Ticket
CREATE TABLE dbo.Ticket (
    ID int NOT NULL,
    IncidentStatus varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_Ticket PRIMARY KEY (ID)
);

-- Table: Route
CREATE TABLE dbo.Route (
    ID int NOT NULL,
    ScheduleID int NOT NULL,
    Name varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_Route PRIMARY KEY (ID)
);

ALTER TABLE dbo.Route 
ADD CONSTRAINT FK_Route_Schedule FOREIGN KEY (ScheduleID) REFERENCES .dbo.Schedule(ID);

-- Table: Schedule
CREATE TABLE dbo.Schedule (
    ID int NOT NULL,
    Arrival time NOT NULL,
    Departure time NOT NULL,
    CONSTRAINT PK_Schedule PRIMARY KEY (ID)
);

-- Table: CardType
CREATE TABLE dbo.CardType (
    ID int NOT NULL,
    Type varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_CardType PRIMARY KEY (ID)
);

-- Table: Card
CREATE TABLE dbo.Card (
    ID int IDENTITY(1,1) NOT NULL,
    UserID int NOT NULL,
    Balance int NOT NULL,
    CardTypeID int NOT NULL,
    CONSTRAINT PK_Card PRIMARY KEY (ID),
    CONSTRAINT UQ_Card_User UNIQUE (UserID)
);

ALTER TABLE dbo.Card 
ADD CONSTRAINT FK_Card_User FOREIGN KEY (UserID) REFERENCES .dbo.UserAccount(ID),
    CONSTRAINT FK_Card_CardType FOREIGN KEY (CardTypeID) REFERENCES .dbo.CardType(ID);

-- Table: UserAccount
CREATE TABLE dbo.UserAccount (
    ID int IDENTITY(1,1) NOT NULL,
    FirstName varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    LastName varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Identification int NOT NULL,
    Email varchar(200) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Password varchar(15) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    PhoneNumber int NULL,
    UserRoleID int NOT NULL,
    ShiftID int NOT NULL,
    CardID int NULL,
    CONSTRAINT PK_UserAccount PRIMARY KEY (ID),
    CONSTRAINT UQ_UserAccount_Email UNIQUE (Email)
);

ALTER TABLE dbo.UserAccount 
ADD CONSTRAINT FK_UserAccount_Role FOREIGN KEY (UserRoleID) REFERENCES .dbo.UserRole(ID),
    CONSTRAINT FK_UserAccount_Shift FOREIGN KEY (ShiftID) REFERENCES .dbo.Shift(ID),
    CONSTRAINT FK_UserAccount_Card FOREIGN KEY (CardID) REFERENCES .dbo.Card(ID);

-- Table: UserRole
CREATE TABLE dbo.UserRole (
    ID int NOT NULL,
    Role varchar(20) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_UserRole PRIMARY KEY (ID)
);

-- Table: Shift
CREATE TABLE dbo.Shift (
    ID int NOT NULL,
    ShiftType varchar(30) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_Shift PRIMARY KEY (ID)
);

-- Table: RouteStop
CREATE TABLE dbo.RouteStop (
    StopID int NOT NULL,
    RouteID int NOT NULL,
    CONSTRAINT PK_RouteStop PRIMARY KEY (StopID, RouteID)
);

ALTER TABLE dbo.RouteStop 
ADD CONSTRAINT FK_RouteStop_Stop FOREIGN KEY (StopID) REFERENCES .dbo.Stop(ID),
    CONSTRAINT FK_RouteStop_Route FOREIGN KEY (RouteID) REFERENCES .dbo.Route(ID);

-- Table: Stop
CREATE TABLE dbo.Stop (
    ID int NOT NULL,
    Location varchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    Name varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
    CONSTRAINT PK_Stop PRIMARY KEY (ID)
);
