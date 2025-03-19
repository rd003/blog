+++
date = '2025-03-19T17:25:31+05:30'
draft = false
title = 'Inserting bulk records (1 million) in SQL Server'
tags = ['sql']
categories = ['database']
+++

## Creating a database

```sql
USE master
GO

DROP DATABASE IF EXISTS BookMillion
GO

CREATE DATABASE BookMillion
GO

USE [BookMillion]
GO

CREATE TABLE [dbo].[Book](
	[Id] [int] IDENTITY(1,1) NOT NULL,
	[Title] [nvarchar](100) NULL,
	[Author] [nvarchar](100) NOT NULL,
	[Country] [nvarchar](100) NULL,
	[ImageLink] [nvarchar](100) NULL,
	[Language] [nvarchar](20) NULL,
	[Link] [nvarchar](200) NULL,
	[Pages] [int] NULL,
	[Year] [int] NULL,
	[Price] [int] NULL

	CONSTRAINT PK_Book_Id PRIMARY KEY (Id)
)
GO
```

## Bulk insert using recursive cte

```sql
USE [BookMillion]
GO

WITH Numbers AS (
SELECT 1 AS N
UNION ALL
SELECT N + 1
FROM Numbers
WHERE N < 1000000
)
insert into Book (Title,Author,Country,[Language],ImageLink,Link,Pages,Price,[Year])
select
'Book'+ cast(N as varchar),
'Author'+ cast(N as varchar),
'Country'+ cast(N as varchar),
'Language'+ cast(N as varchar),
'ImageLink'+ cast(N as varchar),
'Link'+ cast(N as varchar),
ABS(CHECKSUM(NEWID())) % 901 + 100, -- Pages between 100-1000
ABS(CHECKSUM(NEWID())) % 901 + 100, -- Price between 100-1000
ABS(CHECKSUM(NEWID())) % 825 + 1200 -- Year between 1200-2024
from Numbers

option (maxrecursion 0)

GO
```
