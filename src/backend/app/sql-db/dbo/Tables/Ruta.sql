CREATE TABLE [dbo].[Ruta] (
    [ID]        INT           NOT NULL,
    [IDHorario] INT           NOT NULL,
    [Nombre]    VARCHAR (100) NOT NULL,
    CONSTRAINT [PK_Ruta] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Ruta_Horario] FOREIGN KEY ([IDHorario]) REFERENCES [dbo].[Horario] ([ID])
);


GO

