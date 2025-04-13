CREATE TABLE [dbo].[Ticket] (
    [ID]               INT          NOT NULL,
    [EstadoIncidencia] VARCHAR (20) NOT NULL,
    CONSTRAINT [PK_Ticket] PRIMARY KEY CLUSTERED ([ID] ASC)
);


GO

