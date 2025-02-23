+++
date = '2025-02-23T16:14:13+05:30'
draft = false
title = 'Unit Testing in Dotnet Core With Nsubstitute'
tags = ['dotnet','testing']
categories = ['programming']
+++

As the name suggesting , Unit testing is a software testing where smallest units of the application such as methods are tested in the isolation, so that we can ensure our software is working as expected.

### Commonly used testing frameworks

- MSTest
- nUnit
- xUnit

### Mocking frameworks

Mocking framework is a library which allows us to mock the objects. For example, a **PeopleController** is injected with the **IPersonRepository.** While testing the PeopleController, we need the IPersonRepository. Mock frameworks comes to rescue in that situation. With the help of mock frameworks we can mock the IPersonRepository and mimic it’s behavior. Some popular mocking libraries are:

- Moq
- NSubstitue
- FakeItEasy

In this tutorial we are going to use the **XUnit** framework and **nSubstitute** library.

### Tech Used in this project

- .Net 8 web APIs (controller)
- Sqlite
- EntityFrameworkCore
- xUnit
- nSubstitue

### Let’s get started

Create a **sln** file (I have named it **PersonGithubActionsDemo**) with two projects

1. A .Net Core API project (I have named it **PersonGithubActionsDemo.Api**).

2. A xUnit project ( I have named it **PersonGithubActionsDemo.UnitTests**)

✅ Open the project in the **VsCode** editor.

**💻Source code:**

[https://github.com/rd003/PersonGithubActionsDemo](https://github.com/rd003/PersonGithubActionsDemo)

**🌿Branch:** unit-test

Please do not forget to visit the branch **‘unit-test’**, I might add some more code in the master branch.

### Folder structure

![unit testing with nsubstitute](/images/1_wxAcNpew2bhlVboDeN2EIw.jpg)

Folder structure of the application

### Let’s work with API Project

In this section, we are going to create the endpoints for the People.

### Domain classes (Our entities)

👉 Domain/Person.cs

```cs
using System.ComponentModel.DataAnnotations;

namespace PersonGithubActionsDemo.Api.Domain;

public class Person
{
    public int Id { get; set; }

    [Required]
    [MinLength(4)]
    [MaxLength(20)]
    public string Name { get; set; } = string.Empty;

    [MinLength(1)]
    [MaxLength(20)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;

    public Person()
    {

    }

    public Person(int id, string name, string email)
    {
        Id = id;
        Name = name;
        Email = email;
    }

}
```

This entity is going to persist in the database.

### 👉 Install nuget packages

In the Api project, install these packages

```sh
dotnet add package Microsoft.EntityFrameworkCore.Design

dotnet add package Microsoft.EntityFrameworkCore.Sqlite
```

### 👉 Data/PersonContext.cs

```cs
using Microsoft.EntityFrameworkCore;
using PersonGithubActionsDemo.Api.Domain;

namespace PersonGithubActionsDemo.Api.Data;

public class PersonContext : DbContext
{
    public PersonContext(DbContextOptions<PersonContext> options) : base(options)
    {

    }

    public DbSet<Person> People { get; set; }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        modelBuilder.Entity<Person>().ToTable("Person");

        modelBuilder.Entity<Person>().HasData(new List<Person>{
           new () {Id=1,Name="John",Email="john@example.com"},
           new () {Id=2,Name="Jim",Email="jim@example.com"}
        });
    }

}
```

In the method named **OnModelCreating,** we are seeding some data to the table **Person**.

### Migration

In the terminal run following command

```sh
dotnet ef migrations add init
```

It will generate the migration files. It can be followed by the database update command (dotnet ef database update), but we do not need it, we are going to do it programmatically.

### 👉appsettings.json

Add connection string in this file.

```json
"ConnectionStrings": {
 "default": "data source = Person.db"
 }
```

Person.db is the name of sqlite database, which will be created in the root directory.

### 👉Program.cs file

Add this line in the Program.cs file.

```cs
builder.Services
 .AddDbContext<PersonContext>
 (options => options.UseSqlite(builder.Configuration
 .GetConnectionString("default")));

// add these lines just above app.Run()

app.MapGet("/", () => "Hello World");

// It will automatically run the pending migration files

using (var scope = app.Services.CreateScope())
{
 var context = scope.ServiceProvider.GetService<PersonContext>();
 if (context.Database.GetPendingMigrations().Any())
 {
 context.Database.Migrate();
 }
}
```

I have mapped default (“/”) path with the string “Hello World!”, it is not necessary to add this line. When we run our project and visit the default path, this string will be displayed, which ensures our project is running as expected.

#### Run the application

Now you can run the project using (dotnet run), and browse the default url. You should see ‘Hello World” in the screen.

At this point, our migration has been applied and some data have been seeded in the database.

### Let’s Create DTOS

👉 DTOS/PersonCreateDTO.cs

```cs
using System.ComponentModel.DataAnnotations;

namespace PersonGithubActionsDemo.Api.DTOS;

public class PersonCreateDTO
{
    [Required]
    [MinLength(4)]
    [MaxLength(20)]
    public string Name { get; set; } = string.Empty;

    [MinLength(1)]
    [MaxLength(20)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;


    public PersonCreateDTO(string name, string email)
    {
        Name = name;
        Email = email;
    }
}
```

👉DTOS/PersonUpdateDTO.cs

```cs
using System.ComponentModel.DataAnnotations;

namespace PersonGithubActionsDemo.Api.DTOS;

public class PersonUpdateDTO
{
    public int Id { get; set; }

    [Required]
    [MinLength(4)]
    [MaxLength(20)]
    public string Name { get; set; } = string.Empty;

    [MinLength(1)]
    [MaxLength(20)]
    [EmailAddress]
    public string Email { get; set; } = string.Empty;


    public PersonUpdateDTO(int id, string name, string email)
    {
        Id = id;
        Name = name;
        Email = email;
    }

}
```

👉 DTOS/PersonReadDTO.cs

```cs
namespace PersonGithubActionsDemo.Api.DTOS;

public record PersonReadDTO(int Id, string Name, string Email);
```

### Mappers

I am going to create manual mappers in this project, you can also use libraries like automapper or mapster.

👉 Extensions/PersonMapper:

```cs
using System;
using PersonGithubActionsDemo.Api.Domain;
using PersonGithubActionsDemo.Api.DTOS;

namespace PersonGithubActionsDemo.Api.Extensions;

public static class PersonMapper
{
    public static Person ToPerson(this PersonCreateDTO model)
    {
        return new Person
        {
        Name = model.Name,
        Email = model.Email
        };
    }

    public static Person ToPerson(this PersonUpdateDTO model)    {
        return new Person
        {
            Id = model.Id,
            Name = model.Name,
            Email = model.Email
        };
    }

    public static PersonCreateDTO ToPersonCreateDto(this Person person)    {
        return new PersonCreateDTO(person.Name, person.Email);
    }

    public static PersonUpdateDTO ToPersonUpdateDto(this Person person)    {
        return new PersonUpdateDTO(person.Id, person.Name, person.Email);
    }

    public static PersonReadDTO ToPersonReadDto(this Person person)    {
        return new PersonReadDTO(person.Id, person.Name, person.Email);
    }
}
```

### Services:

👉 Services/IPersonService.cs

```cs
using PersonGithubActionsDemo.Api.Domain;

namespace PersonGithubActionsDemo.Api.Services;

public interface IPersonService
{
 public Task<Person> AddPersonAsync(Person person);
 public Task<Person> UpdatePersonAsync(Person person);
 public Task DeletePersonAsync(Person person);
 public Task<IEnumerable<Person>> GetPeopleAsync();
 public Task<Person?> GetPersonAsync(int id);
}
```

👉 Services/PersonService.cs

```cs
using Microsoft.EntityFrameworkCore;
using PersonGithubActionsDemo.Api.Data;
using PersonGithubActionsDemo.Api.Domain;

namespace PersonGithubActionsDemo.Api.Services;

public class PersonService : IPersonService
{
    private readonly PersonContext _context;
    public PersonService(PersonContext context)
    {
        _context = context;
    }
    public async Task<Person> AddPersonAsync(Person person)
    {
        _context.People.Add(person);
        await _context.SaveChangesAsync();
        return person;
    }

    public async Task<Person> UpdatePersonAsync(Person person)
    {
        _context.People.Update(person);
        await _context.SaveChangesAsync();
        return person;
    }

    public async Task DeletePersonAsync(Person person)
    {
        _context.People.Remove(person);
        await _context.SaveChangesAsync();
    }

    public async Task<IEnumerable<Person>> GetPeopleAsync() =>
      await _context.People.AsNoTracking().ToListAsync();

    public async Task<Person?> GetPersonAsync(int id) =>
      await _context.People.AsNoTracking().FirstOrDefaultAsync(p => p.Id == id);

}
```

Add this line in the Program.cs file.

👉 Program.cs

```cs
builder.Services.AddScoped<IPersonService, PersonService>();
```

### Controllers

👉 Controllers/PeopleController

```cs
using Microsoft.AspNetCore.Mvc;
using PersonGithubActionsDemo.Api.Domain;
using PersonGithubActionsDemo.Api.DTOS;
using PersonGithubActionsDemo.Api.Extensions;
using PersonGithubActionsDemo.Api.Services;

namespace PersonGithubActionsDemo.Api.Controllers;

[ApiController]
[Route("/api/[Controller]")]
public class PeopleController : ControllerBase
{
    private readonly IPersonService _personService;
    private readonly ILogger<PeopleController> _logger;

    public PeopleController(IPersonService personService, ILogger<PeopleController> logger)
    {
        _personService = personService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<IActionResult> GetPeople()
    {
        try
        {
            var people = (await _personService.GetPeopleAsync()).Select(p => p.ToPersonReadDto()).ToList();
            return Ok(people);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, ex.Message);
        }
    }

    [HttpGet("{id}", Name = "GetPerson")]
    public async Task<IActionResult> GetPerson(int id)
    {
        try
        {
            PersonReadDTO? person = (await _personService.GetPersonAsync(id))?.ToPersonReadDto();
            if (person == null)
            {
                return NotFound();
            }
            return Ok(person);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, ex.Message);
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeletePerson(int id)
    {
        try
        {
            Person? person = await _personService.GetPersonAsync(id);
            if (person == null)
            {
                return NotFound();
            }
            await _personService.DeletePersonAsync(person);
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, ex.Message);
        }
    }

    [HttpPost]
    public async Task<IActionResult> AddPerson(PersonCreateDTO person)
    {
        try
        {
            Person createdPerson = await _personService.AddPersonAsync(person.ToPerson());
            return CreatedAtRoute(nameof(GetPerson), new { id = createdPerson.Id }, createdPerson.ToPersonReadDto());
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, ex.Message);
        }
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdatePerson(int id, [FromBody] PersonUpdateDTO personToUpdate)
    {
        try
        {
            if (id != personToUpdate.Id)
            {
                return BadRequest("Id mismatch");
            }
            Person? person = await _personService.GetPersonAsync(id);
            if (person == null)
            {
                return NotFound();
            }
            await _personService.UpdatePersonAsync(personToUpdate.ToPerson());
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(500, ex.Message);
        }
    }

}
```

🌐 Now test the endpoints in the postman and make sure everything is working fine.

---

### Unit testing project

In this section we are going to work in the unit testing project.

### Install the Nuget Packages

```sh
dotnet add package NSubstitute

dotnet add package NSubstitute.Analyzers.CSharp
```

### Project reference

Add the reference of the api project, so that you can access the controller class.

### Create a testing Class

Create a new Class in the root of the application and name it `PeopleControllerTests`

```cs
👉 PeopleControllerTests.cs

public class PeopleControllerTests
{
}
```

Since the **PeopleController** injects **ILogger** and **IPersonService**, so we need to mimic their their behavior using **NSubstitute**. We also have a list of person, which is going to be utilized in test methods.

```cs
public class PeopleControllerTests
{
    private readonly IPersonService _personService;
    private readonly ILogger<PeopleController> _logger;
    private readonly PeopleController _controller;

    List<Person> people = new List<Person>
        {
            new Person(1, "John", "john@example.com"),
            new Person(2, "Jim", "jim@example.com"),
            new Person(3, "Rick","rick@example.com")
        };

    public PeopleControllerTests()
    {
        _personService = Substitute.For<IPersonService>(); // mocking IPersonService
        _logger = Substitute.For<ILogger<PeopleController>>(); // mocking ILogger
        _controller = new PeopleController(_personService, _logger);
    }

}
```

Make sure to import these packages at the top.

```cs
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using NSubstitute;
using NSubstitute.ExceptionExtensions;
using PersonGithubActionsDemo.Api.Controllers;
using PersonGithubActionsDemo.Api.Domain;
using PersonGithubActionsDemo.Api.DTOS;
using PersonGithubActionsDemo.Api.Services;
```

Let’s write our first test method.

```cs
    [Fact]
    public async Task GetPeople_ReturnsOkResult_WithPeopleList()
    {
        // Arrange
        _personService.GetPeopleAsync().Returns(people);

        // Act
        var result = await _controller.GetPeople();

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        var peopleList = Assert.IsType<List<PersonReadDTO>>(okResult.Value);
        Assert.True(peopleList.Count > 0);
    }
```

In this test we are ensuring that the **GetPeople** method return **OkResult** with the **people list**.

#### Run the test

Open the integrated terminal and run this command:

```sh
dotnet test
```

You will be seeing the passing result the terminal.

![test results](/images/1_ryB4F0vb2CGEgrMdj2eUUg.jpg)

Let’s write the remaining test, the name of the test methods are the self explanatory.

👉 GetPerson_ReturnOKResult_WithPerson

```cs
    [Fact]
    public async Task GetPerson_ReturnOKResult_WithPerson()
    {
        // Arrange
        int id = 1;
        var person = people.First(a => a.Id == id);
        _personService.GetPersonAsync(id).Returns(person);

        // Act
        var result = await _controller.GetPerson(id);

        // Assert
        var okResult = Assert.IsType<OkObjectResult>(result);
        var personResult = Assert.IsType<PersonReadDTO>(okResult.Value);
        Assert.Equal(id, personResult.Id);
    }
```

👉 GetPerson_ReturnsNotFound_WhenPersonDoesNotExist

```cs
    [Fact]
    public async Task GetPerson_ReturnsNotFound_WhenPersonDoesNotExist()
    {
        // Arrange
        int id = 1;

        // Act
        var result = await _controller.GetPerson(id);

        // Assert
        Assert.IsType<NotFoundResult>(result);
    }
```

👉 DeletePerson_ReturnsNoContentResult

```cs
    [Fact]
    public async Task DeletePerson_ReturnsNoContentResult()
    {
        // Arrange
        var id = 1;
        var person = people.First(a => a.Id == id);
        _personService.GetPersonAsync(id).Returns(person);

        // Act
        var result = await _controller.DeletePerson(id);

        // Assert
        Assert.IsType<NoContentResult>(result);
    }
```

👉 DeletePerson_ReturnsNotFoundResult_WhenPersonDoesNotExist

```cs
    [Fact]
    public async Task DeletePerson_ReturnsNotFoundResult_WhenPersonDoesNotExist()
    {
        // Arrange
        int id = 999; // ID that doesn't exist

        // Act
        var result = await _controller.DeletePerson(id);

        // Assert
        Assert.IsType<NotFoundResult>(result);
    }
```

👉 AddPerson_ReturnsCreatedAtRouteResult_WhenPersonAddedSuccessfully

```cs
    [Fact]
    public async Task AddPerson_ReturnsCreatedAtRouteResult_WhenPersonAddedSuccessfully()
    {
        // Arrange
        PersonCreateDTO personCreateDto = new PersonCreateDTO("John", "john@example.com");
        var person = people.FirstOrDefault(a => a.Name == "John" && a.Email == "john@example.com");
        _personService.AddPersonAsync(Arg.Any<Person>()).Returns(person);

        // Act
        var result = await _controller.AddPerson(personCreateDto);

        // Assert
        var createdAtRouteResult = Assert.IsType<CreatedAtRouteResult>(result);
        Assert.Equal(nameof(_controller.GetPerson), createdAtRouteResult.RouteName);
        Assert.Equal(1, createdAtRouteResult.RouteValues["id"]);

        var personReadDTO = Assert.IsType<PersonReadDTO>(createdAtRouteResult.Value);

        Assert.Equal(person.Id, personReadDTO.Id);
    }
```

👉 AddPerson_ReturnsStatusCodeResult_WhenServiceThrowsException

```cs
    [Fact]
    public async Task AddPerson_ReturnsStatusCodeResult_WhenServiceThrowsException()
    {
        // Arrange
        var personCreateDTO = new PersonCreateDTO("John", "john@example.com");
        _personService.AddPersonAsync(Arg.Any<Person>()).Throws<Exception>();

        // Act
        var result = await _controller.AddPerson(personCreateDTO);

        // Assert
        var statusCodeResult = Assert.IsType<ObjectResult>(result);
        Assert.Equal(500, statusCodeResult.StatusCode);
    }
```

👉 UpdatePerson_ReturenNoContent_WhenPersonUpdated

```cs
    [Fact]
    public async Task UpdatePerson_ReturenNoContent_WhenPersonUpdated()
    {
        // Arrange
        int id = 1;
        var personUpdateDto = new PersonUpdateDTO(id, "John", "john@example.com");
        var person = people.First(a => a.Id == personUpdateDto.Id);
        _personService.GetPersonAsync(id).Returns(person);

        // Act
        var result = await _controller.UpdatePerson(id, personUpdateDto);

        // Assert
        Assert.IsType<NoContentResult>(result);
    }
```

👉 UpdatePerson_ReturnsBadRequest_WhenIdMismatch

```cs
    [Fact]
    public async Task UpdatePerson_ReturnsBadRequest_WhenIdMismatch()
    {
        // Arrange
        int id = 1;
        PersonUpdateDTO personToUpdate = new PersonUpdateDTO(2, "John", "john@example.com");

        // Act
        var result = await _controller.UpdatePerson(id, personToUpdate);

        // Assert
        var badRequestResult = Assert.IsType<BadRequestObjectResult>(result);
        Assert.Equal("Id mismatch", badRequestResult.Value);
    }
```

👉 UpdatePerson_ReturnsNotFound_WhenPersonNotFound

```cs
    [Fact]
    public async Task UpdatePerson_ReturnsNotFound_WhenPersonNotFound()
    {
        // Arrange
        int id = 1;
        PersonUpdateDTO personToUpdate = new PersonUpdateDTO(id, "John", "john@example.com");
        _personService.GetPersonAsync(Arg.Any<int>()).Returns((Person)null);

        // Act
        var result = await _controller.UpdatePerson(id, personToUpdate);

        // Assert
        Assert.IsType<NotFoundResult>(result);
    }
```

[Canonical link](https://medium.com/@ravindradevrani/unit-testing-in-net-core-with-n-substitute-d05ea335dde2)
