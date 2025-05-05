+++
date = '2025-05-04T17:00:00+05:30'
draft = false
title = 'Bulk insert in dapper with table valued parameter'
tags = ['dotnet','dapper']
categories = ['programming']
+++

![How to insert bulk data in dapper?](/images/bulk.webp)

There might be instances when you want to insert bulk data. For an instance, you want to create an order, where you need to add multiple items. Let's see how can we insert bulk data in c# using dapper.

Note: It is only good for adding bunch of rows. But if you are looking for adding hundreds of rows then better to use other approaches. There are many, if you look out.

**💻 You can get source code from [👉here](https://github.com/rd003/DotnetPracticeDemos/tree/master/DapperBulkInsertDemo)** 

## Database Structure

Let's look into our database structure first:

```sql
USE master
GO

CREATE TABLE Person
(
    PersonId int identity (1,1),
    FirstName NVARCHAR(20),
    LastName NVARCHAR(20)

    constraint PK_Person_Id primary key (PersonId) 
)
GO
```

## Creating a table-valued paramter

We need to create a custom type of `table` type aka `table-valued parameter`. It is needed to pass rows through stored procedure parameters.

```sql
CREATE TYPE CreatePersonTableType as TABLE
(
    FirstName NVARCHAR(20),
    LastName NVARCHAR(20)
);
```

I know it's bad name. Use the name which suits you better.

## Stored Procedure

```sql
CREATE PROCEDURE usp_AddPeople
    @PersonData AS CreatePersonTableType READONLY
AS
BEGIN
  SET NOCOUNT ON;

  INSERT INTO Person(FirstName,LastName)
  SELECT FirstName,LastName FROM @PersonData;
 
END   
```

## Accessing it with C#

Make sure you have installed these packages: `Dapper` and `Microsoft.Data.SqlClient`.

```cs
    // Data to insert
    List<Person> people = [
      new Person{FirstName="John",LastName="Doe"},
      new Person{FirstName="Jane",LastName="Doe"},
      new Person{FirstName="Mohan",LastName="Singh"},
      new Person{FirstName="Nitin",LastName="Kumar"}
    ];

    DataTable personTable = new();
    personTable.Columns.Add("FirstName", typeof(string));
    personTable.Columns.Add("LastName", typeof(string));

    // Populate datatable with person data

    foreach (var person in people)
    {
      personTable.Rows.Add(person.FirstName, person.LastName);
    }

    using IDbConnection connection = new SqlConnection(_constr);

    var parameters = new DynamicParameters();
    parameters.Add("@PersonData", personTable, DbType.Object, ParameterDirection.Input);

    await connection.ExecuteAsync(
      "usp_AddPeople",
      parameters,
      commandType: CommandType.StoredProcedure
    );
```

