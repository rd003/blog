+++
date = '2025-02-24T17:49:15+05:30'
draft = false
title = 'Database Firsts Approach In EF Core'
tags = ['dotnet','ef-core']
categories = ['programming']
image = '/images/1_FCYljdej4D2tgcBhiEErAw.jpg'
+++

<!-- ![Database first approach with DotNet Core](/images/1_FCYljdej4D2tgcBhiEErAw.jpg) -->

I have used `database first` approach in the .NET Framework 4.X. But It is the first time I am trying to use Db First approach in the .NET Core (I am using .net 9). Microsoft refers it ['Scaffolding (Reverse Engineering)'](https://learn.microsoft.com/en-us/ef/core/managing-schemas/scaffolding/?tabs=dotnet-core-cli). Personally I prefer `Dapper` for DB First approach. May be you have an existing database and you want to use it with ENTITY FRAMEWORK, then this approach might be helpful. I am playing around it and documenting it and sharing that journey with you. Let's see what it offers.

## T-SQL script

Let’s create a database with a table.

```sql
use master;
go

drop database if exists PersonDb;
go

create database PersonDb;
go

use PersonDb;
go

Create table People
(
 PersonID int identity(1,1),
 PersonName nvarchar(50) not null,
 PersonEmail Nvarchar(50) not null

Constraint PK_People_PersonId primary key (PersonID)
);
go

Create unique nonclustered index IX_People_Email on People(PersonEmail);
go

insert into People(PersonName,PersonEmail)
values
('Ravindra','ravindra@gmail.com'),
('Ramesh','ramesh@gmail.com'),
('Harish','harish@gmail.com'),
('Saraswati','saraswati@gmail.com');

go
```

## Create a new project

```sh
dotnet new webapi -n DbFirstDemo
```

## Nuget packages

Run these command in a sequence:

```sh
# change the directory

cd DbFirstDemo

# 1
dotnet add package Microsoft.EntityFrameworkCore.Design

# 2
dotnet add package Microsoft.EntityFrameworkCore.SqlServer

# 3
dotnet ef dbcontext scaffold "server=RAVINDRA\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false" Microsoft.EntityFrameworkCore.SqlServer --output-dir Models
```

**Note:** Replace the value of `server` with your server name.

It creates, two classes named `Person.cs` and `PersonDbContext.cs` in the `Models`.

```cs
// Models/Person.cs

using System;
using System.Collections.Generic;

namespace DbFirstDemo.Models;

public partial class Person
{
    public int PersonId { get; set; }

    public string PersonName { get; set; } = null!;

    public string PersonEmail { get; set; } = null!;

}

// Models/PersonDbContext.cs

using System;
using System.Collections.Generic;
using Microsoft.EntityFrameworkCore;

namespace DbFirstDemo.Models;

public partial class PersonDbContext : DbContext
{
    public PersonDbContext()
    {
    }

    public PersonDbContext(DbContextOptions<PersonDbContext> options)
        : base(options)
    {
    }

    public virtual DbSet<Person> People { get; set; }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)

#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name\= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
 => optionsBuilder.UseSqlServer("server=RAVINDRA\\\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false");

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.Entity<Person>(entity =>
        {
            entity.HasKey(e => e.PersonId).HasName("PK\_People\_PersonId");

            entity.HasIndex(e => e.PersonEmail, "IX\_People\_Email").IsUnique();

            entity.Property(e => e.PersonId).HasColumnName("PersonID");
            entity.Property(e => e.PersonEmail).HasMaxLength(50);
            entity.Property(e => e.PersonName).HasMaxLength(50);
        });

        OnModelCreatingPartial(modelBuilder);
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);

}
```

It’s Amazing.. right!

However, I would recommend you to move your connectionstring to the `appsettings.json`. We are also getting a warning about that. So remove these lines from `PersonDbContext`:

```txt
protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name\= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
 => optionsBuilder.UseSqlServer("server=RAVINDRA\\\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false");
```

Add connection string in the `appsettings.json`

```json
"ConnectionStrings": {
 "default":"server=RAVINDRA\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false"
 }
```

**Note:** Replace the value of `server` with your server name, you can get it from SqlServer Management Studio.

Also add these lines in the `Program.cs`

```cs
string connectionString = builder.Configuration.GetConnectionString("default");

builder.Services.AddDbContext<PersonDbContext>(o => o.UseSqlServer(connectionString));
```

To confirm if everything works fine. Let’s create an endpoint. Add these lines to `Program.cs`:

```cs
app.MapGet("/people", async (PersonDbContext context) =>
{
 var peoples = await context.People
 .Select(p => new Person
 {
 PersonId = p.PersonId,
 PersonEmail = p.PersonEmail,
 PersonName = p.PersonName
 })
 .ToListAsync();
 return Results.Ok(peoples);
}
```

Test the `GET` endpoint `http://localhost:5094/people` in the browser (or any of your favourate tool). It gives the following result:

Note: Replace `localhost:5094` with your address.

```json
[
  {
    "personId": 1,
    "personName": "Ravindra",
    "personEmail": "ravindra@gmail.com"
  },
  {
    "personId": 2,
    "personName": "Ramesh",
    "personEmail": "ramesh@gmail.com"
  },
  {
    "personId": 3,
    "personName": "Harish",
    "personEmail": "harish@gmail.com"
  },
  {
    "personId": 4,
    "personName": "Saraswati",
    "personEmail": "saraswati@gmail.com"
  }
]
```

---

Let’s Explore🔎 it a bit more. I want to add one more property to the `Person`. Let's add it in sql server:

```sql
alter table People add Age int;
go
```

How can we synch it with .net application. We have three ways to achieve it:

1. Re-scaffolding.
2. Manually update the property and sync to the database.
3. Switch to the approach using migrations (code first approach).

## 1. Re-scaffolding

Now let’s run this command:

```sh
dotnet ef dbcontext scaffold "server=RAVINDRA\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false" Microsoft.EntityFrameworkCore.SqlServer --output-dir Models
```

Right now I am getting this error:

```bash
The following file(s) already exist in directory 'C:\\Users\\RD\\Documents\\Projects\\Dotnet\\DotnetPracticeDemos\\DbFirstDemo\\Models': PersonDbContext.cs,Person.cs. Use the Force flag to overwrite these files.
```

Let’s add a `force` flag to it:

```bash
dotnet ef dbcontext scaffold "server=RAVINDRA\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false" Microsoft.EntityFrameworkCore.SqlServer --output-dir Models --force
```

It is a success. Let’s check our `Person` and `PersonDbContext` classes.

```cs
// Models/Person.cs

using System;
using System.Collections.Generic;

namespace DbFirstDemo.Models;

public partial class Person
{
    // Existing code.
    //Code is removed for brevity

    public int? Age { get; set; } // new property is  added

}

public partial class PersonDbContext : DbContext
{
    // ..... existing code

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)

#warning To protect potentially sensitive information in your connection string, you should move it out of source code. You can avoid scaffolding the connection string by using the Name\= syntax to read it from configuration - see https://go.microsoft.com/fwlink/?linkid=2131148. For more guidance on storing connection strings, see https://go.microsoft.com/fwlink/?LinkId=723263.
 => optionsBuilder.UseSqlServer("server=RAVINDRA\\MSSQLSERVER01;database=PersonDb;Integrated Security=true;encrypt=false");

     // remaining existing code

}
```

`Person` and `PersonDbContext` classes are recreated. The block of code we have removed from `PersonDbContext` is added again. This will happen always whenever we make changes to the database. By Re-Scaffolding we will lost our changes of the classes, those are generated by scaffolding (Person and PersonDbContext in our case). Make sure not to make any changes in the scaffolded classes, instead create a partial class and make changes there.

## 2. Manually update the property

Let’s add one more field to the database.

```sql
alter table People
add ContactNumber nvarchar(20);
go
```

Open the `Person.cs` file and add this property:

```cs
public partial class Person
{
    // Existing code here (removed for brevity)

    [MaxLength(20)]
    public string? ContactNumber { get; set; } = null!;
}
```

Right now, it is just a single property. What if we add one or more tables. Then we have add them here and manually sync it. We have to keep database and .net code in sync. That is tedious and error prone. I personally think, this process is very bad.

## 3. Switch to the code first

Let’s add one more class to `Models` folder.

```cs
namespace DbFirstDemo.Models;

public class Category
{
 public int CategoryID { get; set; }
 public string CategoryName { get; set; } = string.Empty;
}
```

Add this line to `PersonDbContext` :

```cs
public DbSet<Category> Categories { get; set; }
```

Now, we need to apply migrations. So run these command in a sequence in the integrated terminal:

```sh
#1
dotnet ef migrations add InitialCreate

#2
dotnet ef database update
```

At this point. I am getting an error:

There is already an object named 'People' in the database.

It is a kind of obvious. When you look at your migration file in the `Migrations` folder, you will notice that, EF is trying to add tables `Categories` and `People` to the database. But we already have a `People` table in the database.

Also, open your database and you will find a table with name `__EFMigrationsHistory` is created in the `PersonDb`. This table does not have any data yet.

👉 Now we need to remove the migration file.

```sh
dotnet ef migrations remove
```

At this moment, all of files from the `Migrations` folder has deleted.

Open the `PersonDbContext` file and comment the line `public DbSet<Category> Categories { get; set; }` as shown below:

```cs
public partial class PersonDbContext : DbContext
{
    // code is remove for brevity

    public virtual DbSet<Person> People { get; set; }

    //public DbSet<Category> Categories { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // code is removed for brevity
    }

    partial void OnModelCreatingPartial(ModelBuilder modelBuilder);

}
```

Run the command `dotnet ef migrations add InitialCreate` to genearate a migration file.

Now, open your migration file and remove every line from `Up` and `Down` method

```cs
public partial class InitialCreate : Migration
{
    /// <inheritdoc />
    protected override void Up(MigrationBuilder migrationBuilder)
    {

    }

    /// <inheritdoc />
    protected override void Down(MigrationBuilder migrationBuilder)
    {

    }
}
```

Now, run the command `dotnet ef database update`. This command won't make any change to the database. But if you notice the `terminal`, you will find something like this:

```bash
Microsoft.EntityFrameworkCore.Database.Command[20101]
 Executed DbCommand (4ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
 INSERT INTO [__EFMigrationsHistory] ([MigrationId], [ProductVersion])
 VALUES (N'20250204113847_InitialCreate', N'9.0.1');
```

If you verify it in the database, you will notice that the table `__EFMigrationsHistory` is not empty anymore and it has one row with value `'20250204113847_InitialCreate','9.0.1'`.

👉 Uncomment this line `public DbSet<Category> Categories { get; set; }` from the `PersonDbContext`.

👉 Run these commands in a sequence:

```sh
# 1

dotnet ef migrations add CategoryAdded

#2
dotnet ef database update
```

Now, we have completely synched to the database and successfully moved to the Code-First approach.

---

[Canonical link](https://medium.com/@ravindradevrani/database-first-approach-with-dotnet-core-7a62a3e8f008)
