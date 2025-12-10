+++
date = '2025-02-23T18:00:17+05:30'
draft = false
title = 'Dotnet Core Api CRUD With Dapper and PostgreSql'
tags = ['dotnet','dapper']
categories = ['programming']
image = '/images/1_rpGj8zPS6MI2E6ePNKFT0g.png'
+++

<!-- ![dapper and postgres](/images/1_rpGj8zPS6MI2E6ePNKFT0g.png) -->

#### 💻Source Code: [https://github.com/rd003/PostgressDapperDemo](https://github.com/rd003/PostgressDapperDemo)

### Tools and technology used

- VS Code (editor)
- .Net 8
- Postgres
- Dapper

Let’s get started with creating the database first.

create database PersonDb;

Now, create a table within the database.

```sql
create table Person
(
 Id serial primary key,
 Name varchar(30) not null,
 Email varchar(30) not null
);
```

To create a new project you need to run these commands in a sequence.

```sh
> dotnet new sln -o PostgressDapperDemo

> cd PostgressDapperDemo

> dotnet sln add .\PostgressDapperDemo\

> code . #this command will open this project in the vs code
```

### Nuget packages

Install the following nuget packages.

```sh
dotnet add package Dapper
dotnet add package Npgsql
```

### Models

Create a new folder named `Models` and create another folder inside the `Models` folder and name it `Domain`. Create a class named `Person` within the `Domain` folder.

```cs
namespace PostgressDapperDemo.Models.Domain;

public class Person
{
 public int Id { get; set; }
 public string Name { get; set; } = string.Empty;
 public string Email { get; set; } = string.Empty;
}
```

### DTOs

DTO stands for **Data Transfer Object**. These are the classes which exposed to the clients. Because, client always do not need to know all the properties of the class. For example, in a post request client won’t pass the property named **Id**. It would create unnecessary confusion if we include the **Id** property in the post request model. That is why we need data transfer objects.

Create a new folder named `DTOs` inside the `Models` folder. Create a class named `PersonCreateDto` inside the `DTOs` folder.

```cs
using System.ComponentModel.DataAnnotations;

namespace PostgressDapperDemo.Models.DTOs;

public class PersonCreateDto
{
    [Required]
    [MaxLength(30)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    [MaxLength(30)]
    public string Email { get; set; } = string.Empty;
}
```

Inside the `DTOs` folder create a new class named `PersonUpdateDto` .

```cs
using System;
using System.ComponentModel.DataAnnotations;

namespace PostgressDapperDemo.Models.DTOs;

public class PersonUpdateDto
{
    public int Id { get; set; }

    [Required]
    [MaxLength(30)]
    public string Name { get; set; } = string.Empty;

    [Required]
    [EmailAddress]
    [MaxLength(30)]
    public string Email { get; set; } = string.Empty

}
```

Create a new class named `PersonDisplayDto` inside the `DTOs` folder.

```cs
using System;

namespace PostgressDapperDemo.Models.DTOs;

public class PersonDisplayDto
{

    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public string Email { get; set; } = string.Empty;

}
```

**Person** and **PersonDisplayDto** class seems same. In this scenario, we do not require to create a new DTO class. This does not make any sense,when both classes are same. You can skip this if you want. If the **Person** class have more properties and you do not want to expose those properties to the client, then creating a new DTO class would make more sense. Anyway I am still going to create the **PersonDisplayDto** class.

### Mappers

To convert **Domain** models to **DTOs** and vise-versa, we need some kind of mapping. Either we can use the mapping library (eg. automapper) or we can create our own mappers. We are going to create our own mapper.

Create a new folder/directory named `Mappers`. Create a class named `PersonMapper` within the Mappers folder.

```cs
using PostgressDapperDemo.Models.Domain;
using PostgressDapperDemo.Models.DTOs;

namespace PostgressDapperDemo.Mappers;

public static class PersonMapper
{
    public static Person ToPerson(this PersonCreateDto person) {
        return new Person
        {
            Name = person.Name,
            Email = person.Email
        };
    }

    public static Person ToPerson(this PersonUpdateDto person)    {
        return new Person
        {
            Id = person.Id,
            Name = person.Name,
            Email = person.Email
        };
    }

    public static PersonDisplayDto ToPersonDisplay(this Person person)    {
        return new PersonDisplayDto
        {
            Id = person.Id,
            Name = person.Name,
            Email = person.Email
        };
    }

}
```

### Connection String

Open the **appsettings.json** file and define the connection string there.

```json
"ConnectionStrings": {
 "default": "Host=localhost;Port=5432;Database=persondb;Username=postgres;Password=p@55w0rd;"
 },
```

In the connection string, you need to change the value of the **Password** accordingly.

### Repository

Now we need a class that would contain all the database related operations. Create a folder named `Repositories` and create an interface named `IPersonRepository` within the **Repositories** folder.

```cs
using PostgressDapperDemo.Models.Domain;

namespace PostgressDapperDemo.Repositories;

public interface IPersonRepository
{
 Task<Person> CreatePersonAsync(Person person);
 Task<Person> UpdatePersonAsync(Person person);
 Task DeletePersonAsync(int id);
 Task<IEnumerable<Person>> GetAllPersonAsync();
 Task<Person?> GetPersonByIdAsync(int id);
}
```

Create a class named `PersonRepository` within the Repositories folder.

```cs
    using Dapper;
    using Npgsql;
    using PostgressDapperDemo.Models.Domain;

    namespace PostgressDapperDemo.Repositories;

    public class PersonRepository : IPersonRepository
    {
    private string _connectionString = "";
    private IConfiguration _configuration;

    public PersonRepository(IConfiguration configuration)
    {
        _configuration = configuration;
        _connectionString = _configuration.GetConnectionString("default");
    }

    public async Task<Person> CreatePersonAsync(Person person)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        var createdId = await connection.ExecuteScalarAsync<int>("INSERT INTO person (name, email) VALUES (@name, @email); SELECT LASTVAL();", person);
        person.Id = createdId;
        return person;
    }

    public async Task<Person> UpdatePersonAsync(Person person)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        await connection.ExecuteAsync("UPDATE person SET name = @name, email = @email WHERE id = @id", person);
        return person;
    }

    public async Task DeletePersonAsync(int id)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        await connection.ExecuteAsync("DELETE FROM person WHERE id = @id", new { id });
    }

    public async Task<IEnumerable<Person>> GetAllPersonAsync()
    {
        using var connection = new NpgsqlConnection(_connectionString);
        return await connection.QueryAsync<Person>("SELECT \* FROM person");
    }

    public async Task<Person?> GetPersonByIdAsync(int id)
    {
        using var connection = new NpgsqlConnection(_connectionString);
        return await connection.QueryFirstOrDefaultAsync<Person>("SELECT \* FROM person WHERE id = @id", new { id });
    }

}
```

### Registering IPersonRepository

To inject `IPersonRepository` in the **controller**, we need to register this service in the `Program.cs` file.

```cs
builder.Services.AddScoped<IPersonRepository, PersonRepository>();
```

### Controller

Create a new file named `PeopleController` inside the `Controllers` folder.  
Initial controller will look like this.

```cs
using Microsoft.AspNetCore.Mvc;

namespace PostgressDapperDemo.Controllers;

[Route("api/[controller]")]
[ApiController]
public class PeopleController : ControllerBase
{
}
```

Now we are going to inject necessary services into this controller.

```cs
using Microsoft.AspNetCore.Mvc;
using PostgressDapperDemo.Repositories;

namespace PostgressDapperDemo.Controllers;

[Route("api/[controller]")]
[ApiController]
public class PeopleController : ControllerBase
{
    private readonly IPersonRepository _personRepository;
    private readonly ILogger<PeopleController> _logger;

    public PeopleController(IPersonRepository personRepository, ILogger<PeopleController> logger)
    {
        _personRepository = personRepository;
        _logger = logger;
    }

}
```

Define the **GetPerson** method in the controller.

```cs
[HttpGet("{id}", Name = "GetPerson")]
public async Task<IActionResult> GetPerson(int id)
{
    try
    {
        var person = await _personRepository.GetPersonByIdAsync(id);
        if (person == null)
        {
            return NotFound();
        }
        return Ok(person.ToPersonDisplay());
    }
    catch (Exception ex)
    {
        _logger.LogError($"Error getting person: {ex.Message}");
        return StatusCode(StatusCodes.Status500InternalServerError);
    }
}
```

Define the **CreatePerson** method.

```cs
 [HttpPost]
 public async Task<IActionResult> CreatePerson(PersonCreateDto personCreateDto)
 {
    try
    {
        var person = personCreateDto.ToPerson();
        await _personRepository.CreatePersonAsync(person);
        return CreatedAtRoute(nameof(GetPerson), new { id = person.Id }, person.ToPersonDisplay());
    }
    catch (Exception ex)
    {
        _logger.LogError($"Error creating person: {ex.Message}");
        return StatusCode(StatusCodes.Status500InternalServerError);
    }
 }
```

#### The put method

```cs
[HttpPut("{id}")]
public async Task<IActionResult> UpdatePerson(int id, [FromBody] PersonUpdateDto person)
{
    try
    {
        if (id != person.Id)
        {
            return BadRequest("Id mismatch");
        }
        var existingPerson = await _personRepository.GetPersonByIdAsync(id);
        if (existingPerson == null)
        {
            return NotFound();
        }
        var personToUpdate = person.ToPerson();
        await _personRepository.UpdatePersonAsync(personToUpdate);
        return NoContent();
    }
    catch (Exception ex)
    {
        _logger.LogError($"Error updating person: {ex.Message}");
        return StatusCode(StatusCodes.Status500InternalServerError);
    }
}
```

#### The delete method

```cs
[HttpDelete("{id}")]
public async Task<IActionResult> DeletePerson(int id)
{
    try
    {
        var person = await _personRepository.GetPersonByIdAsync(id);
        if (person == null)
        {
            return NotFound();
        }
        await _personRepository.DeletePersonAsync(id);
        return NoContent();
    }
    catch (Exception ex)
    {
        _logger.LogError($"Error deleting person: {ex.Message}");
        return StatusCode(StatusCodes.Status500InternalServerError);
    }
}
```

#### The get all method

```cs
[HttpGet]
public async Task<IActionResult> GetAllPeople()
{
    try
    {
        var people = await _personRepository.GetAllPersonAsync();
        var peopleToReturn = people.Select(p => p.ToPersonDisplay()).ToList();
        return Ok(peopleToReturn);
    }
    catch (Exception ex)
    {
        _logger.LogError($"Error getting all people: {ex.Message}");
        return StatusCode(StatusCodes.Status500InternalServerError);
    }
}
```

### Running the application

To run the application, run the command `dotnet run` in the terminal. You will see something like below in the terminal.

![terminal](/images/1_MrNhTeVXU9i3AKAF9dQKDA.jpg)

In the web browser enter the following url `[http://localhost:5217/swagger](http://localhost:5217/swagger)` . Mine is listening on the `[http://localhost:5217/swagger](http://localhost:5217/swagger)` , but your will be different, so adjust accordingly.

#### Post request

![post1](/images/1_zy1msUvZjCRSh9XWfI_g5w.jpg)

request

![post2](/images/1_6njNJ3oBYM-VrABrfCWcng.jpg)

response

With the help of swagger UI you can test other API endpoints.

---

[Canonical link](https://medium.com/@ravindradevrani/dotnet-core-api-crud-with-dapper-and-postgresql-3f2532987ba3)
