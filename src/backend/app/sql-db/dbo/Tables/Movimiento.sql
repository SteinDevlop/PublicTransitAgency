CREATE TABLE [dbo].[Movimiento] (
    [ID]               INT IDENTITY (1, 1) NOT NULL,
    [IDTipoMovimiento] INT NOT NULL,
    [Monto]            INT NOT NULL,
    CONSTRAINT [PK_Movimiento] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Movimiento_TipoMovimiento] FOREIGN KEY ([IDTipoMovimiento]) REFERENCES [dbo].[TipoMovimiento] ([ID])
);


GO

