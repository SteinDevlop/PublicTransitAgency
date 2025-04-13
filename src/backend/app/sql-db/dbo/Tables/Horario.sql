CREATE TABLE [dbo].[Horario] (
    [ID]      INT      NOT NULL,
    [Llegada] TIME (7) NOT NULL,
    [Salida]  TIME (7) NOT NULL,
    CONSTRAINT [PK_Horario] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO

