+++
date = '2025-02-19T17:40:41+05:30'
title = 'Write dapper effectively with generic methods'
tags= ["dotnet","dapper"]
categories = ["programming"]
canonical_url = "https://medium.com/@ravindradevrani/write-dapper-effectively-with-generic-methods-f3aa257cc3a3"
+++

![Dapper tutorial with dotnet core](/images/effective_dapper/dapper_dotnet7_feature_image.png)

**Dapper** is a micro ORM for database connectivity in
dotnet and it's been around for quite a while. It is loved by most of
the developers because of its simplicity and performance.

### **Why dapper?**

With the help of dapper you can quickly access the data without writing
too much code. It performs very well because we directly write queries
and executes them. Developers who loves to work with queries and for the
projects, where performance really matters where you wants to write very
optimized queries, dapper can be the good choice.

When we write a code and try to understand a topic then things get more
clear. So I am not saying any thing more about dapper now you can visit
to their official [github
repository](https://github.com/DapperLib/Dapper), you can learn much more about dapper
from there.

{{< youtube id="Y6EbAPiN7gs" title="Dapper" autoplay="false" >}}

In this article we will create a .Net 7 API project and we will perform
CRUD (create, read, update, delete) operations. Now let's get started.

Create a new project in your microsoft visual studio IDE. Select a
project type as **ASP.NET Core Web Api** as you can see in the picture
below.

![project_type](/images/effective_dapper/project_type.jpg)

Name of project will be **DapperDemoApi** and name of solution would be
**DapperDemo** because we will add one more project to this solution, so
it will be a good practice to keep solution and project name different.

![Project_Name](/images/effective_dapper/Project_Name.jpg)

Now click on next and keep these options checked as listed below

![project_version](/images/effective_dapper/project_version.jpg)

Note : Tf you are using versions .NET 6+ this code will work fine

Now we have created a solution with an api project successfully. **DapperDemoApi** will contain **_api endpoints_** only. It will not contain any _database related_ _operations_. We will create a new
project (type of ClassLibrary) for db operations. Now we can follow the single responsibility principle, **DapperDemoApi** project will contain only api part and **DapperDemoData** will contain the _database_ and _business logic._

Let's create a ClassLibrary project for business logic. So **right click** on the solution as shown below.

![solution_explorer](/images/effective_dapper/solution_explorer.jpg)

After that follow instruction given below to create a new
**_ClassLibrary_** project

![img1](/images/effective_dapper/img1.jpg)

![img2](/images/effective_dapper/img2.jpg)

![img3](/images/effective_dapper/img3.jpg)

Now click on next and it will be added to solution. Your solution
explorer should look like this 👇

![img4](/images/effective_dapper/img4.jpg)

Finally we have completed the initial project setup 👏👏👏.
We need to install a nuget package to **DapperDemoData** project. So got
to **Tools \> Nuget package Manager \> Package manager console** and add
these packages.

- `dapper`
- `Microsoft.Extensions.Configuration.Abstractions`
- `Microsoft.Data.SqlClient`

> Please look at these screenshot carefully

![img5](img5.jpg)

![img6](img6.jpg)

Now its time to create database. So open sql server management studio and run these commands.

```sql
CREATE DATABASE [DapperDemo]

USE [DapperDemo]

CREATE TABLE [dbo].[Person](
 [Id] [int] PRIMARY KEY IDENTITY,
 [Name] [nvarchar](30) NOT NULL,
 [Email] [nvarchar](50) NOT NULL
)
```

Open **_appsettings.json_** file and add connection string to it

```json
"ConnectionStrings": {
    "default": "data source=your_sql_server_instance ;initial catalog=DapperDemo;integrated security=true;encrypt=false"
  }
```

You can find **_data source =_ your_sql_server_instance** by following
screenshot

![server_name](/images/effective_dapper/server_name.jpg)

Create a new interface _IDataAccess.cs_ **(DapperDemoData \> Data \>
IDataAccess.cs)**

```cs
 public interface IDataAccess
    {
        Task<IEnumerable<T>> GetData<T, P>(string query, P parameters,
             string connectionId = "default"
            );
        Task SaveData<P>
            (string query, P parameters, string connectionId = "default");
    }
```

Create a new class _DataAccess.cs_ (DapperDemoData \> Data \>
DataAccess.cs)

```cs
 public class DataAccess : IDataAccess
    {
        private readonly IConfiguration _config;

        public DataAccess(IConfiguration config)
        {
            _config = config;
        }

        // this method will retuarn a list of type T
        public async Task<IEnumerable<T>> GetData<T, P>(string query, P parameters,
             string connectionId = "default"
            )
        {
            using IDbConnection connection =
                new SqlConnection(_config.GetConnectionString(connectionId));
            return await connection.QueryAsync<T>(query, parameters);

        }

        //This method will not return anything
        public async Task SaveData<P>
            (string query, P parameters, string connectionId = "default")
        {
           using IDbConnection connection =
                new SqlConnection(_config.GetConnectionString(connectionId));
            await connection.ExecuteAsync(query, parameters);

        }


    }
```

Now let's understand what this class is doing. This class have two
generic methods and with these two methods we can manage all the
database operations. The first method is :

```cs
public async Task<IEnumerable<T>> GetData<T, P>(string query, P parameters,
 string connectionId = "default"
 )
```

This method takes a sql query as a string parameter and dynamic object
as a parameter and it will return a list of data. We will use this
method for fetching data.

The second method is below.👇

```cs
public async Task SaveData<P>
            (string query, P parameters, string connectionId = "default")
```

This method also takes a sql query as a string parameter and dynamic
object as a parameters but it will not return any thing. It is used for
saving the data to database.

Now create a model for person table. Create a new class Person.cs
(**DapperDemoData \> Models \> Person.cs)**

```cs
public class Person
    {
        public int Id { get; set; }
        [Required]
        public string Name{ get; set; }
        [Required]
        public string Email{ get; set; }
    }
```

We need a class which contain business logic for Person related
activities. This class will be named as **PersonRepository.**

Now create a folder **Repository (** **DapperDemoData\> Repository).**

Create a new interface **_IPersonRepository.cs_ (** **DapperDemoData\>
Repository\> IPersonRepository.cs)**

```cs
 public interface IPersonRepository
    {
        Task<bool> AddPerson(Person person);
        Task<bool> UpdatePerson(Person person);
        Task<Person> GetPersonById(int id);
        Task<bool> DeletePerson(int id);
        Task<IEnumerable<Person>> GetPeople();
    }
```

Create a new class **_PersonRepository.cs_ (** **DapperDemoData\>
Repository\> PersonRepository.cs)** which will implement the
**_IPersonRepository_** interface.

Inject **_IDataAccess_** service to this class as a constructor
injection.

```cs
private readonly IDataAccess _db;
public PersonRepository(IDataAccess db)
{
    _db= db;
}
```

Now we will create a new method for **adding** new person to database.

```cs
 public async Task<bool> AddPerson(Person person)
        {
            try
            {
                string query = "insert into dbo.person(name,email) values(@Name,@Email)";
                await _db.SaveData(query, new { Name = person.Name, Email = person.Email });
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }
```

Add another method for **updating** the person record.

```cs
public async Task<bool> UpdatePerson(Person person)
        {
            try
            {
                string query = "update dbo.person set name=@Name,email=@email where id=@Id";
                await _db.SaveData(query, person);
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }
```

Add a method for **deleting** a person record from database. Although we
never delete a record from database, we only sets it as IsArchived or
IsDeleted. But to understand , how deletion works, I am going to explain
it here. Do not follow this approach in real life applications.

```cs
 public async Task<bool> DeletePerson(int id)
        {
            try
            {
                string query = "delete from dbo.person where id = @Id";
                await _db.SaveData(query, new {Id=id});
                return true;
            }
            catch (Exception ex)
            {
                return false;
            }
        }
```

Add a new method for getting the **people list** from database.

```cs
 public async Task<IEnumerable<Person>> GetPeople()
        {
            string query = "select * from dbo.person";
            var people = await _db.GetData<Person, dynamic>(query, new { });
            return people;
        }
```

Now we will write our last method that will bring us **person's data by
id.**

```cs
  public async Task<Person> GetPersonById(int id)
        {
            string query = "select * from dbo.person where id=@Id";
            IEnumerable<Person> people = await _db.GetData<Person, dynamic>(query, new {Id=id});
            return people.FirstOrDefault();
        }
```

Now we have successfully created our **Create, Read, Update** and
**Delete** methods for person.

Now lets create a **PersonController** and make some apis for consuming
the person repository.

```cs
namespace DapperDemoApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PersonController : ControllerBase
    {

    }
}
```

Now we need to inject the **PersonRepository** into **PersonController**
For that we have to **add the reference** of **DapperDemoData** project.

RightClick on **DapperDemoApi** and follow these instruction shown in
screenshots 👇👇

![project_reference](/images/effective_dapper/project_reference.jpg)

Now **check the box** as shown in below image and press **Ok** button on
bottom-right corner on this dialogbox.

![project_reference_2](/images/effective_dapper/project_reference_2.jpg)

Now we can inject **PersonRepository** into **PersonController**

```cs
using DapperDemoData.Models;
using DapperDemoData.Repository;

namespace DapperDemoApi.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PersonController : ControllerBase
    {
      private readonly IPersonRepository _personRepository;
        public PersonController(IPersonRepository personRepository)
        {
            _personRepository = personRepository;
        }
    }
}
```

Now Lets create **Get**, **GetById**, **Create**, **Update** and
**Delete** functionality in this controller. We will start with a
**Get** method which will return the list of all the people.

```cs
 [HttpGet]
 public async Task<IActionResult> Get()
 {
    var people = await _personRepository.GetPeople();
    return Ok(people);
 }
```

Lets create GetById ( api/Person/{id})method for person.

```cs
        // GET api/Person/5
        [HttpGet("{id}")]
        public async Task<IActionResult> Get(int id)
        {
            var person = await _personRepository.GetPersonById(id);
            if (person is null)
                return NotFound();
            return Ok(person);
        }
```

Post method for person (api/Person)

```cs
        [HttpPost]
        public async Task<IActionResult> Post(Person person)
        {
            if (!ModelState.IsValid)
                return BadRequest("Invalid data");
            var result = await _personRepository.AddPerson(person);
            if(!result)
                return BadRequest("could not save data");
            return Ok();
        }
```

Put method for person (api/Person)

```cs
        [HttpPut("{id}")]
        public async Task<IActionResult> Put(int id, [FromBody] Person newPerson)
        {
            if (!ModelState.IsValid)
                return BadRequest("Invalid data");
            var person = await _personRepository.GetPersonById(id);
            if (person is null)
                return NotFound();
            newPerson.Id = id;
            var result = await _personRepository.UpdatePerson(newPerson);
            if (!result)
                return BadRequest("could not save data");
            return Ok();
        }
```

Delete method for person (api/Person/{id})

```cs
        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(int id)
        {
            var person = await _personRepository.GetPersonById(id);
            if (person is null)
                return NotFound();
            var result = await _personRepository.DeletePerson(id);
            if (!result)
                return BadRequest("could not save data");
            return Ok();
        }
```

Now we can can thest these api endpoint with integrated swagger UI
(although you can also use postman). Run this project and you will see
this as a result.

![swagger](/images/effective_dapper/swagger.jpg)

Now lets test Person\> **post** endpoint.

![swagger_post](/images/effective_dapper/swagger_post.jpg)

You will get **200** status code in return.

I have added some records and now we can test **get** endpoint. You can
see the response below.

![swagger_get](/images/effective_dapper/swagger_get.jpg)

Now you can test other endpoints also.

So that was all about dapper and how to use it with .net 7 APIs. I hope
everything is clear to you now.

[📎Source code](https://drive.google.com/file/d/1S_CLW90HkZxnrcFmerTKHxFhtxRTfbaW/view)

[Canonical
link](https://medium.com/@ravindradevrani/write-dapper-effectively-with-generic-methods-f3aa257cc3a3)
