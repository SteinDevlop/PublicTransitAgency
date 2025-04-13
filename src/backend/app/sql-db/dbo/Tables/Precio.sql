CREATE TABLE [dbo].[Precio] (
    [ID]               INT NOT NULL,
    [IDTipoTransporte] INT NOT NULL,
    [Monto]            INT NOT NULL,
    CONSTRAINT [PK_Precio] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Precio_TipoTransporte] FOREIGN KEY ([IDTipoTransporte]) REFERENCES [dbo].[TipoTransporte] ([ID])
);


GO

