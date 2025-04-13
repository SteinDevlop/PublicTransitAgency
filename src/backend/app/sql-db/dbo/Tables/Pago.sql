CREATE TABLE [dbo].[Pago] (
    [IDMovimiento] INT NOT NULL,
    [IDPago]       INT NOT NULL,
    [IDTarjeta]    INT NOT NULL,
    [IDTransporte] INT NOT NULL,
    CONSTRAINT [FK_Pago_Movimiento] FOREIGN KEY ([IDMovimiento]) REFERENCES [dbo].[Movimiento] ([ID]),
    CONSTRAINT [FK_Pago_Precio] FOREIGN KEY ([IDPago]) REFERENCES [dbo].[Precio] ([ID])
);


GO

