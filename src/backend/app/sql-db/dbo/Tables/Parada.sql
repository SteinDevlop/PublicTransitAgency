CREATE TABLE [dbo].[Parada] (
    [ID]        INT           NOT NULL,
    [Ubicacion] VARCHAR (150) NOT NULL,
    [Nombre]    VARCHAR (100) NOT NULL,
    CONSTRAINT [PK_Parada] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO

