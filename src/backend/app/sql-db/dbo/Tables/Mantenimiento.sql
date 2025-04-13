CREATE TABLE [dbo].[Mantenimiento] (
    [ID]                 INT           IDENTITY (1, 1) NOT NULL,
    [IDEstado]           INT           NOT NULL,
    [Tipo]               VARCHAR (100) NOT NULL,
    [Fecha]              DATE          NOT NULL,
    [IDUnidadTransporte] INT           NOT NULL,
    CONSTRAINT [PK_Mantenimiento] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Mantenimiento_Estado] FOREIGN KEY ([IDEstado]) REFERENCES [dbo].[EstadoMantenimiento] ([ID]),
    CONSTRAINT [FK_Mantenimiento_UnidadTransporte] FOREIGN KEY ([IDUnidadTransporte]) REFERENCES [dbo].[UnidadTransporte] ([ID])
);


GO

