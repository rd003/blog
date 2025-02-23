+++
date = '2025-02-23T17:04:04+05:30'
draft = false
title = 'Integration Testing in Dotnet With InMemory Db'
tags = ['dotnet','testing']
categories = ['programming']
+++

**Integration testing** is a software testing technique, where individual units of a program are integrated together and tested as a group for interacting harmoniously with each other. It concerns the testing of interactions and interfaces between modules, components, or systems to see if they behave as expected once integrated.

> 📢 Always use real database for integration testing instead of InMemory Db.

### Purpose

- This is to ensure that various components or modules behave according to expectation.
- In the case of integration, to find out whether there are problems concerning interfaces or inconsistencies in data.
- Verifying whether it meets the set specifications and functionality of an integrated system.

### Tech Used in this project

- .Net 8 web APIs (controller)
- Sqlite
- EntityFrameworkCore
- xUnit
- In Memory Database (for testing)

### Let’s get started

Create a **sln** file (I have named it **PersonGithubActionsDemo**) with two projects

1. A **.Net Core API** project (I have named it **PersonGithubActionsDemo.Api**).

2. A **xUnit** project ( I have named it **PersonGithubActionsDemo.IntegrationTests**)

✅ Open the project in the **VsCode** editor.

### 💻Source code:

[https://github.com/rd003/PersonGithubActionsDemo](https://github.com/rd003/PersonGithubActionsDemo)

**🌿Branch:** integration-test

Please do not forget to visit the branch **‘integration-test’**, I might add some more code in the master branch.

### Folder structure

![folder structure](/images/1_uhcdlFi89dON8oTsiyE6uQ.jpg)

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

It will generate the migration files. It can be followed by the database update command (`dotnet ef database update`), but we do not need it, we are going to do it programmatically.

### 👉appsettings.json

Add connection string in this file.

```json
"ConnectionStrings": {
 "default": "data source = Person.db"
 }
```

`Person.db` is the name of `sqlite` database, which will be created in the root directory.

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
 if (context.Database.ProviderName != "Microsoft.EntityFrameworkCore.InMemory" && context.Database.GetPendingMigrations().Any())
 {
    context.Database.Migrate();
 }
}
```

I have mapped default (“/”) path with the string **“Hello World!”,** it is not necessary to add this line. When we run our project and visit the default path, this string will be displayed, which ensures our project is running as expected.

`if (context.Database.ProviderName != "Microsoft.EntityFrameworkCore.InMemory" && context.Database.GetPendingMigrations().Any())`

Let’s look at this condition, migrations will applied only when we meet this condition. If we do not put this condition (`context.Database.ProviderName != “Microsoft.EntityFrameworkCore.InMemory”`), the application will give error when we works with integration tests, because we are using **In-Memory** Db in the integration tests, and migrations won’t work with **in-memory** database.

### Run the application

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

I am going to create manual mappers in this project, you can also use libraries like **Automapper** or **Mapster**.

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

    public static Person ToPerson(this PersonUpdateDTO model)
    {
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

### Controllers:

👉 Controllers/PeopleController

```cs
using Microsoft.AspNetCore.Mvc;
using PersonGithubActionsDemo.Api.Domain;
using PersonGithubActionsDemo.Api.DTOS;
using PersonGithubActionsDemo.Api.Extensions;
using PersonGithubActionsDemo.Api.Services;namespace PersonGithubActionsDemo.Api.Controllers;

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

### Integration testing project

In this section we are going to work in the integration testing project.

### Install the Nuget Packages

```sh
dotnet add package Microsoft.AspNetCore.Mvc.Testing

dotnet add package Microsoft.EntityFrameworkCore.InMemory
```

The `Microsoft.AspNetCore.Mvc.Testing` class allow us to use the functionality of **WebApplicationFactory**.

### Project reference

Add the reference of the API project, so that you can access the controller class.

### ⚠️ Update Program.cs file

We need to use the **Program** class in our integration test project, but **Program** class is internal by default. So we need to make it public somehow. One way is, define a public partial class. So add this lines at the end of your **Program** class.

```cs
app.Run();

// add this line
public partial class Program { }
```

### Custom WebApplication factory

Create a new class at the root directory named `MyWebApplicationFactory` .

👉 **MyWebApplicationFactory.cs**

```cs
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using PersonGithubActionsDemo.Api.Data;

namespace PersonGithubActionsDemo.IntegrationTests;

public class MyWebApplicationFactory : WebApplicationFactory
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            var descriptor = services.SingleOrDefault(
            d => d.ServiceType == typeof(DbContextOptions<PersonContext>));
            if (descriptor != null)
            {
                services.Remove(descriptor);
            }
            services.AddDbContext<PersonContext>(options =>
            {
                options.UseInMemoryDatabase("InMemoryDbForTesting");
            });

            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            using var appContext = scope.ServiceProvider.GetRequiredService<PersonContext>();
            try
            {
                appContext.Database.EnsureDeleted();
                appContext.Database.EnsureCreated();
            }
            catch (Exception ex)
            {
                throw;
            }
        });
    }
}
```

- First we find the existing database context, which is setup with sqlite database and delete it.
- Then we are adding the database context with in-memory database.
- Since this class is accessed each time, so we are ensuring to delete the database and recreate it.

### Testing class

Create a new class named `PeopleControllerTests` and implement the `IClassFixture<MyWebApplicationFactory<Program>>`.

👉 **PeopleControllerTests.cs**

```cs
public class PeopleControllerTests : IClassFixture<MyWebApplicationFactory>
{

}
```

Create and assign the private readonly fields of type `MyWebApplicationFactory<Program>`and `HttpClient` .

```cs
public class PeopleControllerTests : IClassFixture<MyWebApplicationFactory>
{
    private readonly MyWebApplicationFactory _factory;
    private readonly HttpClient _client;

    public PeopleControllerTests(MyWebApplicationFactory factory)
    {
        _factory = factory;
        _client = _factory.CreateClient();
    }
}
```

### Write our first test case

```cs
    [Fact]
    public async Task GetPeople_ReturnsOkResponse()
    {
        // Arrange

        //Act
        var response = await _client.GetAsync("api/People");

        // Act
        response.EnsureSuccessStatusCode(); // Status Code 2xx
        var reponseString = await response.Content.ReadAsStringAsync();
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        var people = JsonSerializer.Deserialize<List<PersonReadDTO>>(reponseString, options);

        // Assert
        Assert.NotNull(people);
        Assert.NotEmpty(people);
    }
```

In the integration testing we do not mock the service, rather we make the actual http call. In this test case, we are ensuring the method named ‘GetPeople’:

- Must return 2xx status code (`response.EnsureSuccessStatusCode();`), will return 200 in our case.
- `people` list should not be null.
- `people` list should not be empty.

**Note:** We do not need to seed the data, since we are seeding it the section **OnModelCreating** (**PersonContext** class).

### 🌐 Run the test cases

Open your integrate terminal and run the command `dotnet test` as a result you should see this.

![Passing test case](/images/1_zyA0Zbn_jIfwGJCuBZYAqQ.jpg)

Similarly we can write other test cases.

👉 GetPerson_ReturnsOk_WhenPersonExists

```cs
    [Fact]
    public async Task GetPerson_ReturnsOk_WhenPersonExists()
    {
        // Arrange:

        // Act
        var response = await _client.GetAsync("api/People/1");

        // Assert
        response.EnsureSuccessStatusCode(); // Status Code 2xx

        var responseString = await response.Content.ReadAsStringAsync();
        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        var person = JsonSerializer.Deserialize<PersonReadDTO>(responseString, options);
        Assert.NotNull(person);
        Assert.Equal(1, person.Id);
    }
```

👉 GetPerson_ReturnsNotFound_WhenPersonDoesNotExist()

```cs
    [Fact]
    public async Task GetPerson_ReturnsNotFound_WhenPersonDoesNotExist()
    {
        // Arrange

        // Act
        var response = await _client.GetAsync("/api/People/999"); // record with this id does not exists

        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
```

👉 AddPerson_ReturnsCreatedAtRoute

```cs
    [Fact]
    public async Task AddPerson_ReturnsCreatedAtRoute()
    {
        // Arrange
        var newPerson = new Person(0, "Rick", "rick@example.com");
        var content = new StringContent(JsonSerializer.Serialize(newPerson), Encoding.UTF8, "application/json");

        // Act
        var response = await _client.PostAsync("/api/people", content);
        response.EnsureSuccessStatusCode();  // status code 2xx

        var jsonResponse = await response.Content.ReadAsStringAsync();

        var options = new JsonSerializerOptions
        {
            PropertyNameCaseInsensitive = true
        };
        var createdPerson = JsonSerializer.Deserialize<PersonReadDTO>(jsonResponse, options);

        // Assert
        Assert.NotNull(createdPerson);
        Assert.Equal("Rick", createdPerson.Name);
        Assert.Equal("rick@example.com", createdPerson.Email);
    }
```

👉UpdatePerson_ReturnsNoContent_WhenUpdateIsSuccessful()

```cs
    [Fact]
    public async Task UpdatePerson_ReturnsNoContent_WhenUpdateIsSuccessful()
    {
        // Arrange
        var personToUpdate = new Person(1, "John Doe", "johndoe@example.com");
        var content = new StringContent(JsonSerializer.Serialize(personToUpdate), Encoding.UTF8, "application/json");

        // Act
        var response = await _client.PutAsync("/api/people/1", content);
        response.EnsureSuccessStatusCode();  // status code 2xx

        // Assert
        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);
    }
```

👉 UpdatePerson_ReturnsBadRequest_WhenIdMismatch()

```cs
    [Fact]
    public async Task UpdatePerson_ReturnsBadRequest_WhenIdMismatch()
    {
        // Arrange
        var personToUpdate = new Person(1, "John Doe", "johndoe@example.com");
        var content = new StringContent(JsonSerializer.Serialize(personToUpdate), Encoding.UTF8, "application/json");

        // Act
        var response = await _client.PutAsync("/api/people/2", content);

        // Assert
        Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);
    }
```

👉 UpdatePerson_ReturnsNotFound_WhenPersonDoesNotExist()

```cs
    [Fact]
    public async Task UpdatePerson_ReturnsNotFound_WhenPersonDoesNotExist()
    {
        // Arrange
        var personToUpdate = new Person(999, "Jack", "jack@example.com");
        var content = new StringContent(JsonSerializer.Serialize(personToUpdate), Encoding.UTF8, "application/json");

        // Act
        var response = await _client.PutAsync("/api/people/999", content);

        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);
    }
```

👉 DeletePerson_ReturnsNoContent_WhenDeletionIsSuccessfull

```cs
    [Fact]
    public async Task DeletePerson_ReturnsNoContent_WhenDeletionIsSuccessfull()
    {
        // Arrange

        // Act
        var response = await _client.DeleteAsync("api/people/1");

        // Assert
        response.EnsureSuccessStatusCode(); // Status Code 2xx
        Assert.Equal(HttpStatusCode.NoContent, response.StatusCode);
    }
```

👉 DeletePerson_ReturnsNotFound_WhenPersonDoesNotExist

```cs
    [Fact]
    public async Task DeletePerson_ReturnsNotFound_WhenPersonDoesNotExist()
    {
        // Arrange

        // Act
        var response = await _client.DeleteAsync("api/people/999");

        // Assert
        Assert.Equal(HttpStatusCode.NotFound, response.StatusCode);

    }
```

---

### Authentication and Authorization

If your controller has authorized attribute as described below

```cs
[ApiController]
[Route("/api/[Controller]")]
[Authorize]
public class PeopleController : ControllerBase
{
}
```

And you are testing any method of this controller, then you will get 401 status code with error. We can also have variation of authorization like `[Authorize(Roles =”Admin”)]` or `[Authorize(Roles =”Account,Manager”)]` . We are going to cover all of these scenarios.

Create a class named **TestAuthHandler** in the root of the integration project and write this code in the TestAuthHander class.

```cs
using Microsoft.AspNetCore.Authentication;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using System.Security.Claims;
using System.Text.Encodings.Web;

namespace BookStoreFullStackNg.IntegratedTests;

public class TestAuthHandler : AuthenticationHandler<AuthenticationSchemeOptions>
{
    public const string TestUserRolesHeader = "X-TestUserRoles";
    public TestAuthHandler(IOptionsMonitor<AuthenticationSchemeOptions> options, ILoggerFactory logger,
    UrlEncoder encoder, ISystemClock clock)
    : base(options, logger, encoder, clock)
    {
    }

    protected override Task<AuthenticateResult> HandleAuthenticateAsync()
    {
        var rolesHeader = Request.Headers[TestUserRolesHeader].FirstOrDefault() ?? "User";
        var roles = rolesHeader.Split(new[] { ',' }, StringSplitOptions.RemoveEmptyEntries);

        var claims = new List<Claim> { new Claim(ClaimTypes.Name, "TestUser") };

        // Add role claims after trimming whitespace
        foreach (var role in roles)
        {
            claims.Add(new Claim(ClaimTypes.Role, role.Trim()));
        }

        var identity = new ClaimsIdentity(claims, "TestScheme");
        var principal = new ClaimsPrincipal(identity);
        var ticket = new AuthenticationTicket(principal, "TestScheme");

        return Task.FromResult(AuthenticateResult.Success(ticket));

    }

}
```

Modify the `MyWebApplicationFactory` and add these lines.

```cs
// Add a test authentication scheme
services.AddAuthentication(options =>
{
options.DefaultAuthenticateScheme = "TestScheme";
options.DefaultChallengeScheme = "TestScheme";
})
.AddScheme<AuthenticationSchemeOptions, TestAuthHandler>("TestScheme", options => { });
```

Full code:

```cs
public class MyWebApplicationFactory<TEntryPoint> : WebApplicationFactory<Program> where TEntryPoint : Program
{
    protected override void ConfigureWebHost(IWebHostBuilder builder)
    {
        builder.ConfigureServices(services =>
        {
            var descriptor = services.SingleOrDefault(
            d => d.ServiceType == typeof(DbContextOptions<PersonContext>));
            if (descriptor != null)
            {
                services.Remove(descriptor);
            }
            services.AddDbContext<PersonContext>(options =>
            {
                options.UseInMemoryDatabase("InMemoryDbForTesting");
            });

            // Add a test authentication scheme
            // new code starts here
            services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = "TestScheme";
                options.DefaultChallengeScheme = "TestScheme";
            })
            .AddScheme<AuthenticationSchemeOptions, TestAuthHandler>("TestScheme", options => { });
            // new code ends here

            var sp = services.BuildServiceProvider();
            using var scope = sp.CreateScope();
            using var appContext = scope.ServiceProvider.GetRequiredService<PersonContext>();
            try
            {
                appContext.Database.EnsureDeleted();
                appContext.Database.EnsureCreated();
            }
            catch (Exception ex)
            {
                throw;
            }
        });
    }
}
```

You need to set the value of `TestUserRolesHeader` in every controller method.

```cs
[Fact]
public async Task GetPeople_ReturnsOkResponse()
{
        // Arrange

       _client.DefaultRequestHeaders
              .Add(TestAuthHandler.TestUserRolesHeader, "Admin"); //You can also replace Admin with other values like Account or Manager

        //Act
        // remain code
        // remaining code is removed for the sake of brevity
}
```

Make sure to the the same in every method.

---

### Adding Github Actions integration workflow

This section is not directly related to this post, but you will be benifited if you know this. We are going to apply workflow of CI/CD (github actions). It is very simple and straight forward, so I thought to include it here.

Create a folder named “.github” in the root directory, create a folder named “workflows” inside the “.github” directory. Create a new file named “integration.yaml” inside the “workflows” directory and write these lines in the yaml file.

```yml
name: Integration

on:
push:
branches: ["master"]
pull_request:
branches: ["master"]

jobs:
build:
runs-on: ubuntu-latest

    steps:
       - uses: actions/checkout@v4
       - name: Setup .NET
        uses: actions/setup-dotnet@v4
        with:
          dotnet-version: 8.0.x
       - name: Restore dependencies
        run: dotnet restore ./PersonGithubActionsDemo.sln
       - name: Build
        run: dotnet build ./PersonGithubActionsDemo.sln  --no-restore
       - name: Test
        run: dotnet test ./PersonGithubActionsDemo.sln  --no-build  --verbosity normal
```

Your test will automatically run whenever you make a pull request or push you changes to master branch in github.

---

[Canonical link](https://medium.com/@ravindradevrani/integration-testing-in-aspnetcore-5e946def188f)
