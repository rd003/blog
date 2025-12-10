+++
date = '2025-02-23T13:21:42+05:30'
draft = false
title = ".Net Core API CRUD With PostgreSql"
tags = ['dotnet']
categories = ['programming']
image = '/images/1_NnvApuXzGsE_9Q2TEJPjWA.png'
+++

<!-- ![aspnet core apis crud](/images/1_NnvApuXzGsE_9Q2TEJPjWA.png) -->

When we create an application with .NET, we tend to use the Microsoft tech stack like Visual Studio IDE, Microsoft SQL Server, Windows Operating System, and Azure. However, things have changed since the introduction of .NET Core. We are no longer bound to a specific operating system and database.

In this blog post, we will learn how to create a Web API CRUD (Create, Read, Update, Delete) application using .NET Core and a Postgres database.

### Disclaimer

In this blog post, I won’t be teaching you the REST API basics or basics of .NET APIs. I will simply walk you through the steps to create the application. However, I have tried to explain all the important concepts used in this tutorial, why I have used them and what are their alternatives. I am also not following the industry standard best practices, I have tried to make this tutorial as simple as possible.

💻 Source Code : [https://github.com/rd003/DotnetApiPostgres](https://github.com/rd003/DotnetApiPostgres)

### Tools

- .Net SDK (I am using .net 8, which is latest at the time I am writing this blog post. If you have already installed visual studio then you dont need to install .net sdks.)
- Postgres database (I am running postgres in docker container)
- Vs Code (text editor)
- Entity Framework Core (ORM)
- REST Client extension for vs code, for testing APIS (Optional). You can also use swagger UI( which is integrated with this project) or POSTMAN.

### Let’s get started💻

First and foremost, we need to create a project. Please execute these commands one by one.

```sh
dotnet new sln -o DotnetApiPostgres

cd DotnetApiPostgres

dotnet new webapi --use-controllers -n "DotnetApiPostgres.Api"

dotnet sln add .\DotnetApiPostgres.Api\DotnetApiPostgres.Api.csproj
```

At this point, your project has been created. To open it in VSCode, use the following command:

```sh
code .
```

### Installing the required nuget packages

At this point, you project has been opened in vs code. Follow these steps:

- Open the integrated terminal by pressing the **ctrl** and **\`** buttons together.
- Change the directory to “DotnetApiPostgres.Api”

```sh
cd DotnetApiPostgres.Api
```

- Now execute these commands one by one.

```sh
dotnet add package Npgsql.EntityFrameworkCore.PostgreSQL

dotnet add package Microsoft.EntityFrameworkCore.Design
```

To confirm whether these packages are installed or not, you can check inside the **DotApiPostgres.Api.csproj** file. You will see their package reference.

![DotApiPostgres.Api.csproj](/images/1_iGwXYCxt71GFhAENMXHe_A.jpg)

### Project structure

![project structure](/images/1_Au1nSOHkth5PoKtvL9ZuNQ.jpg)

### Models

Create a folder named “Models” inside the “DotnetApiPostgres.Api”. Inside this folder create a file named “Person.cs”. Write following code inside the Person.cs file.

👉 Models -> Person.cs

```cs
// Models.
using System.ComponentModel.DataAnnotations;

using System.ComponentModel.DataAnnotations.Schema;

namespace DotnetApiPostgres.Api.Models;

[Table("Person")]
public class Person
{
 public int Id { get; set; }

    [Column(TypeName = "varchar(30)")]
    [Required]
    public required string Name { get; set; }
}
```

It is our domain model that persists in the database. The Table attribute forces the table to be named ‘Person’, otherwise, the table name would be the same as the DbSet property name. For example, if our DbSet property is named ‘People’, and we don’t explicitly define the table name in the **Table** attribute, the table name in the database will be ‘People’. The DbSet property defines the name of the entity (table) in the database. If you want a different entity name than the DbSet property, define a Table(“table name”) attribute at the top of the class.

👉 Models -> ApplicationDbContext.cs

```cs
using DotnetApiPostgres.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace DotnetApiPostgres.Api;

public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {

    }

    public DbSet<Person> People { get; set; }

}
```

👉 appsettings.development.json

```json
"ConnectionStrings": {
 "default": "Host=localhost;Port=5432;Database=PersonDb;Username=your_user_name;Password=your_secret_password"
 }
```

Connection string may differ on your system. Please make sure to check your port number, username and password, other wise you will face error while using “dotnet ef database update” command.

👉 Program.cs

We need to register our `ApplicationDbContext` service.

```cs
string connectionString = builder.Configuration.GetConnectionString("default");

builder
.Services
.AddDbContext<ApplicationDbContext\>(op => op.UseNpgsql(connectionString));
```

### Migrations

Till now, we haven’t generated a database. For that, we need the migration commands. In .net cli, we need a tool for manipulating migration commands. Follow this command to install ef tool if not already installed.

```sh
dotnet tool install --global dotnet-ef
```

This tool is installed globally, you don’t need to install it in future.

If you already have installed it, consider to update it, it might be outdated.

```sh
dotnet tool update \--global dotnet-ef
```

Now, we can create our migration file.

👉 create migration

```sh
dotnet ef migrations add "init"
```

This command will generate migration files inside the Migrations folder. Migration file contains set of instructions to generate or modify the database.

👉 update database

```sh
dotnet ef database update
```

After running this command, EF Core tools will generate the database with the table(s). Sometimes, this step can become very frustrating. If your connection string is incorrect or your database engine is not running, you may encounter an error. I myself faced an error while writing this blog post. My connection string was incorrect, containing a typo that was difficult to spot, and it took a considerable amount of time to find. If you find yourself in the same situation, ensure that your connection string is correct, verify that your database is running, and try opening it via the terminal or a GUI tool.

### DTOs

We do not want to expose our actual class, Person, to clients. Instead, we need a kind of mediator class for that purpose, known as Data Transfer Objects (DTOs). Currently, our class only has two fields, so creating DTOs may not seem necessary. However, consider a situation where our domain class has many fields and we do not want to expose all of them to the client. In such cases, DTOs will be useful.

Create a folder named ‘DTO’ inside the ‘Models’ folder. Create a flie named ‘CreatePersonDTO.cs’ inside the ‘Models’ folder

👉 Models -> DTOS -> CreatePersonDTO.cs

```cs
using System.ComponentModel.DataAnnotations;

namespace DotnetApiPostgres.Api.Models.DTO;

public class CreatePersonDTO
{
    [Required]
    public required string Name { get; set; }

    public static Person ToPerson(CreatePersonDTO createPersonDto)
    {
        return new Person
        {
            Name = createPersonDto.Name
        };
    }
}
```

You might be wondering what the static method `ToPerson()` is doing in our DTO class. Well, at some point, we need to convert our DTO class to a domain class and vice versa. We need a converter for that purpose. I have created a manual mapper. However, you also can create a separate class for the manual mapper, which follows the principle of separation of concerns and makes your Domain and DTO classes much cleaner.

In case you don’t want to do manual mapping, there are multiple libraries available, like **AutoMapper**, **Mapster**, etc. The overhead of manual mapping can be hugely reduced by using those. Note that some performance overhead is introduced by the mapping libraries. Mapping itself is a complex and debatable topic. I don’t want to start a debate here. Do further research on mapping if you are going to use it in a production-grade, large-scale project.

👉 Models -> DTOS -> UpdatePersonDTO.cs

```cs
using System.ComponentModel.DataAnnotations;

namespace DotnetApiPostgres.Api.Models.DTO;

public class UpdatePersonDTO
{
    public int Id { get; set; }

    [Required]
    public required string Name { get; set; }

    public static Person ToPerson(UpdatePersonDTO updatePersonDto)
    {
        return new Person
        {
            Id = updatePersonDto.Id,
            Name = updatePersonDto.Name
        };
    }

}
```

👉Models -> DTOS -> GetPersonDto.cs

```cs
namespace DotnetApiPostgres.Api.Models.DTO;

public class GetPersonDto
{
    public int Id { get; set; }
    public required string Name { get; set; }

    public static Person ToPerson(GetPersonDto getPersonDto)
    {
        return new Person
        {
            Id = getPersonDto.Id,
            Name = getPersonDto.Name
        };
    }

}
```

👉 We also need to update the **Person.cs** file, where we will define a mapper method. We need a mapper that converts a **Person** object to a **GetPersonDto**.

Models -> Person.cs

```cs
// other existing using statements
using DotnetApiPostgres.Api.Models.DTO;

[Table("Person")]
public class Person
{
    // existing code here

    // added code
    public static GetPersonDto ToGetPersonDto(Person person)
    {
        return new GetPersonDto
        {
            Id = person.Id,
            Name = person.Name
        };
    }

}
```

### Services

We need a class where we can define methods that interact with the database, such as adding, updating, deleting, and retrieving all persons.

Create a new folder named “Services” inside the “DotnetApiPostgres.Api” project. In this folder, create a new file named “PersonService.cs”.

👉 Services -> PersonService.cs

Usually, we create interfaces in a separate file, but for the sake of simplicity, I am going to create it in the **PersonService.cs** file. I have defined both the interface and the implementation class in the same file.

```cs
public interface IPersonService
{
 Task<GetPersonDto> AddPersonAsync(CreatePersonDTO personToCreate);
 Task UpdatePersonAsync(UpdatePersonDTO personToUpdate);
 Task DeletePersonAsync(Person person);
 Task<GetPersonDto?> FindPersonByIdAsync(int id);
 Task<IEnumerable<GetPersonDto>> GetPeopleAsync();
}
public sealed class PersonService : IPersonService
{

}
```

I have used the `sealed` keyword, which means this class cannot be inherited. However, this is optional, and you can create a normal class if you prefer.

Next, let’s inject `ApplicationDbContext` into the `PersonService` class.

```cs
public sealed class PersonService : IPersonService
{
    private readonly ApplicationDbContext _context;

    public PersonService(ApplicationDbContext context)
    {
        _context = context;
    }

}
```

Let’s implement the methods of the **IPersonService** interface one by one. First, we are going to implement the **AddPersonAsync** method.

👉 AddPersonAsync

```cs
public async Task<GetPersonDto> AddPersonAsync(CreatePersonDTO personToCreate)
 {
 Person person = CreatePersonDTO.ToPerson(personToCreate);
 _context.People.Add(person);
 await _context.SaveChangesAsync();
 return Person.ToGetPersonDto(person);
 }
```

👉 UpdatePersonAsync

```cs
public async Task UpdatePersonAsync(UpdatePersonDTO personToUpdate)
{
    Person person = UpdatePersonDTO.ToPerson(personToUpdate);
    _context.People.Update(person);
    await _context.SaveChangesAsync();
}
```

👉 DeletePersonAsync

```cs
public async Task DeletePersonAsync(Person person)
{
 _context.People.Remove(person);
 await _context.SaveChangesAsync();
}
```

👉 FindPersonByIdAsync

```cs
public async Task<GetPersonDto?> FindPersonByIdAsync(int id)
{
 Person? person = await _context.People.Where(x => x.Id == id).AsNoTracking().FirstOrDefaultAsync();
 if (person == null)
 {
 return null;
 }
 return Person.ToGetPersonDto(person);
}
```

👉 GetPeopleAsync

```cs
public async Task<IEnumerable<GetPersonDto\>> GetPeopleAsync()
{
 IEnumerable<Person\> people \= await _context.People.AsNoTracking().ToListAsync();
 return people.Select(Person.ToGetPersonDto);
}
```

### Registering PersonService in DI container

To inject the **IPersonService** into the **PersonController**, we need to register it in the DI Container. Open the **Program.cs** file and add the following line.

👉 Program.cs

```cs
builder.Services.AddTransient<IPersonService, PersonService>();
```

### Controllers

Create a file named “PeopleController.cs” inside the “Controllers” folder

👉 Controllers -> PeopleController

```cs
[Route("api/people")]
[ApiController]
public class PeopleController : ControllerBase
{

}
```

Inject **IPersonService** and **ILogger** into this controller through constructor injection.

```cs
[Route("api/people")]
[ApiController]
public class PeopleController : ControllerBase
{
    private readonly IPersonService _personService;
    private readonly ILogger<PeopleController> _logger;

    public PeopleController(IPersonService personService, ILogger<PeopleController> logger)
    {
        _personService = personService;
        _logger = logger;
    }
}
```

Next , we will create our endoints one by one.

#### 👉 Create Person

```cs
 [HttpPost]
 public async Task<IActionResult> AddPersonAsync(CreatePersonDTO personToCreate)
 {
 try
 {
 var person = await _personService.AddPersonAsync(personToCreate);
 return Ok(person);
 }
 catch (Exception ex)
 {
 _logger.LogError(ex.Message);
 return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
 }
 }
```

#### 👉 Update Person

```cs
 [HttpPut("{id}")]
 public async Task<IActionResult> UpdatePersonAsync(int id, UpdatePersonDTO personToUpdate)
 {
 if (id != personToUpdate.Id)
 {
 return BadRequest($"id in parameter and id in body is different. id in parameter: {id}, id in body: {personToUpdate.Id}");
 }
 try
 {
 GetPersonDto? person = await _personService.FindPersonByIdAsync(id);
 if (person == null)
 {
 return NotFound();
 }
 await _personService.UpdatePersonAsync(personToUpdate);
 return NoContent();
 }
 catch (Exception ex)
 {
 _logger.LogError(ex.Message);
 return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
 }
 }
```

#### 👉 Delete Person

```cs
 [HttpDelete("{id}")]
 public async Task<IActionResult> DeleteByIdAsync(int id)
 {
 try
 {
 GetPersonDto? person = await _personService.FindPersonByIdAsync(id);
 if (person == null)
 {
 return NotFound();
 }
 await _personService.DeletePersonAsync(GetPersonDto.ToPerson(person));
 return NoContent();
 }
 catch (Exception ex)
 {
 _logger.LogError(ex.Message);
 return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
 }
 }
```

#### 👉 Get Person By Id

```cs
 [HttpGet("{id}")]
 public async Task<IActionResult> GetPersonByIdAsync(int id)
 {
 try
 {
 GetPersonDto? person = await _personService.FindPersonByIdAsync(id);
 if (person == null)
 {
 return NotFound();
 }
 return Ok(person);
 }
 catch (Exception ex)
 {
 _logger.LogError(ex.Message);
 return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
 }
 }
```

#### 👉 Get All Person

```cs
 [HttpGet]
 public async Task<IActionResult> GetPeopleAsync()
 {
 try
 {
 IEnumerable<GetPersonDto> peoples = await _personService.GetPeopleAsync();
 return Ok(peoples);
 }
 catch (Exception ex)
 {
 _logger.LogError(ex.Message);
 return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
 }
 }
```

### Testing APIs

I am using the REST Client for testing, but you can also use Swagger or Postman. Install the [VS Code extension for the REST Client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

Create a new folder named **‘HttpFiles’** inside the **‘DotnetApiPostgres.Api’** project. Within the **‘HttpFiles’** directory, create a new file named **‘create-person.http’**. The resulting folder structure for ‘HttpFiles’ is as follows:

![http file structure](/images/1_e25uPmll7G-8cYlu03OZLg.jpg)

folder structure of .http files

👉 HttpFiles -> create-person.http

```json
POST https://localhost:7294/api/people/ HTTP/1.1
Content-Type: application/json

{
 "name": "Jane Doe"
}
```

Now you need to run the project.

```bash
dotnet run
```

![create person test](/images/1_pH2VvTk1EZgm5ogH0JumqA.jpg)

Create person endpoint request with rest client

Similarly you can create other .http files.

👉 HttpFiles -> update-person.http

```json
Put https://localhost:7294/api/people/4 HTTP/1.1
Content-Type: application/json

{
 "id":4,
 "name": "John 2"
}
```

👉 HttpFiles -> delete-person.http

```json
Delete https://localhost:7294/api/people/5 HTTP/1.1
```

👉 HttpFiles -> get-person.http

```json
GET https://localhost:7294/api/people/1 HTTP/1.1
```

👉 HttpFiles -> get-people.http

```json
GET https://localhost:7294/api/people HTTP/1.1
```

[💻Source Code](https://github.com/rd003/DotnetApiPostgres)

---

[Canonical link](https://medium.com/@ravindradevrani/asp-net-core-api-crud-with-postgres-71544c94b8c7)
