CREATE TABLE [dbo].[Tarjeta] (
    [ID]            INT IDENTITY (1, 1) NOT NULL,
    [IDUsuario]     INT NOT NULL,
    [Saldo]         INT NOT NULL,
    [IDTipoTarjeta] INT NOT NULL,
    CONSTRAINT [PK_Tarjeta] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Tarjeta_TipoTarjeta] FOREIGN KEY ([IDTipoTarjeta]) REFERENCES [dbo].[TipoTarjeta] ([ID]),
    CONSTRAINT [FK_Tarjeta_Usuario] FOREIGN KEY ([IDUsuario]) REFERENCES [dbo].[Usuario] ([ID]),
    CONSTRAINT [UQ_Tarjeta_Usuario] UNIQUE NONCLUSTERED ([IDUsuario] ASC)
);


GO

