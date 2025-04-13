CREATE TABLE [dbo].[RutaParada] (
    [IDParada] INT NOT NULL,
    [IDRuta]   INT NOT NULL,
    CONSTRAINT [PK_RutaParada] PRIMARY KEY CLUSTERED ([IDParada] ASC, [IDRuta] ASC),
    CONSTRAINT [FK_RutaParada_Parada] FOREIGN KEY ([IDParada]) REFERENCES [dbo].[Parada] ([ID]),
    CONSTRAINT [FK_RutaParada_Ruta] FOREIGN KEY ([IDRuta]) REFERENCES [dbo].[Ruta] ([ID])
);


GO

