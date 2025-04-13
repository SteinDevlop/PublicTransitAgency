CREATE TABLE [dbo].[Incidencia] (
    [ID]          INT           NOT NULL,
    [IDTicket]    INT           NOT NULL,
    [Descripcion] VARCHAR (100) NOT NULL,
    [Tipo]        VARCHAR (20)  NOT NULL,
    [IDUnidad]    INT           NOT NULL,
    CONSTRAINT [PK_Incidencia] PRIMARY KEY CLUSTERED ([ID] ASC),
    CONSTRAINT [FK_Incidencia_Ticket] FOREIGN KEY ([IDTicket]) REFERENCES [dbo].[Ticket] ([ID]),
    CONSTRAINT [UQ_Incidencia_Ticket] UNIQUE NONCLUSTERED ([IDTicket] ASC)
);


GO

