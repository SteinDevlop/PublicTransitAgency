CREATE TABLE [dbo].[Usuario] (
    [ID]             INT           IDENTITY (1, 1) NOT NULL,
    [Nombre]         VARCHAR (200) NOT NULL,
    [Apellido]       VARCHAR (200) NOT NULL,
    [Identificacion] INT           NOT NULL,
    [Correo]         VARCHAR (200) NOT NULL,
    [Contrasena]     VARCHAR (15)  NOT NULL,
    [Celular]        INT           NULL,
    [IDRolUsuario]   INT           NOT NULL,
    [IDTurno]        INT           NOT NULL,
    [IDTarjeta]      INT           NULL,
    CONSTRAINT [PK_Usuario] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Usuario_Rol] FOREIGN KEY ([IDRolUsuario]) REFERENCES [dbo].[RolUsuario] ([ID]),
    CONSTRAINT [FK_Usuario_Turno] FOREIGN KEY ([IDTurno]) REFERENCES [dbo].[Turno] ([ID]),
    CONSTRAINT [UQ_Usuario_Correo] UNIQUE NONCLUSTERED ([Correo] ASC)
);


GO

