CREATE TABLE [dbo].[UnidadTransporte] (
    [ID]               INT           IDENTITY (1, 1) NOT NULL,
    [Ubicacion]        VARCHAR (200) NOT NULL,
    [Capacidad]        INT           NOT NULL,
    [IDRuta]           INT           NOT NULL,
    [IDTipoTransporte] INT           NOT NULL,
    CONSTRAINT [PK_UnidadTransporte] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_UnidadTransporte_Ruta] FOREIGN KEY ([IDRuta]) REFERENCES [dbo].[Ruta] ([ID]),
    CONSTRAINT [FK_UnidadTransporte_TipoTransporte] FOREIGN KEY ([IDTipoTransporte]) REFERENCES [dbo].[TipoTransporte] ([ID])
);


GO

