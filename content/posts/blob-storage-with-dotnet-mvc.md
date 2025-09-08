+++
date = '2025-09-08T12:49:37+05:30'
draft = false
title = 'Azure Blob Storage : CRUD With AspNetCore Mvc & SQL Server'
tags= ["dotnet","azure"]
categories = ["programming","cloud"]
+++

![Azure blob storage crud operations with .net core mvc and sql server](/images/blobstorage/azure-blob-storage-crud.png)

`Azure blob storage` is a storage solution provided by microsoft. You can store data like images, audio, video, json files, zip files etc etc in the azure.

## What are we going to learn?

- How to create a web application that stores and manipulate the images in the cloud.
- We will perform all the CRUD (create, read, update and delete) operations.

## Tech used 

- .NET Core 9 (MVC app)
- SQL server 2022
- Azure storage account

## High level overview

- We will save `image url` in the database and images in the `storage account(blob container)`

---

## Let's create an storage account first

Step 1:
![create azure storage account 1](/images/blobstorage/blob_1.png)

Step 2:
![create azure storage account 2](/images/blobstorage/blob_2.png)

Step 3:
![create azure storage account 3](/images/blobstorage/blob_3.png)

Click on the next and go to advanced section.

Stepe 4:
![create azure storage account 4](/images/blobstorage/blob_4.png)

Match your options with mine. Click on `Review+Create` then create an account.

We are done here.

---

## Create a new ASP.NET Core MVC application

Create a new `ASP.NET Core MVC` project. I am not going to do it, please [follow this](ASP.NET Core MVC), if you don't know how to create one.

📢 I might be missing something in this blog post. If you find something missing please checkout the source code.

💻 [Source code](https://github.com/rd003/DotnetPracticeDemos/tree/master/AzureBlobDemo)

## appsettings

Add these lines in the `appsettings.json`

```js
"AzureBlobStorage": {
    "ConnectionString": "",
    "ContainerName": "",
    "StorageAccountName": "",
    "StorageAccountKey": ""
  }
```  

**📢 Note:** Let's leave these things empty and set it in the `secrets-manager`. Secrets manager stores secrets in the machine not in the project. In this way we can keep our secrets safe. In production, put those secrets in the environment variables of azure app services (where your web app is deployed).

## Secrets

Right click on a project, click on "Manage Secrets". It will open the `secret.json` file

```js
{
   "AzureBlobStorage": {
    "ConnectionString":"",
    "ContainerName": "images", // this does not exists yet, will be created through code
    "StorageAccountName":"",
    "StorageAccountKey": ""
  },
}
```

You can find all the information here:

![Azure storage account keys](/images/blobstorage/blob_keys.png)

## Packages 

```sh
Azure.Storage.Blobs
```

## Options/BlobStorageOptions.cs

```cs
namespace AzureBlobDemo.Options;

public class BlobStorageOptions
{
    public string? ConnectionString { get; set; }
    public string? ContainerName { get; set; }
    public string? StorageAccountName { get; set; }
    public string? StorageAccountKey { get; set; }

}
```

We are using `options pattern` to retrieve the configuration value.

## Program.cs

```cs
builder.Services.AddOptions<BlobStorageOptions>()
                .BindConfiguration("AzureBlobStorage");
```

## IBlobStorageService

```cs
// Services/IBlobStorageService.cs
namespace AzureBlobDemo.Services;

public interface IBlobStorageService
{
    Task<string> UploadFileAsync(IFormFile file, string? fileNameWithExtension = "");

    Task DeleteBlobAsync(string blobUrl);
}
```

## BlobStorageService

```cs
// Services/BlobStorageService.cs

using Azure.Storage.Blobs;
using Azure.Storage.Blobs.Models;
using AzureBlobDemo.Options;
using Microsoft.Extensions.Options;

namespace AzureBlobDemo.Services;

public class BlobStorageServie : IBlobStorageService
{
    private readonly BlobStorageOptions _blobStorage;

    public BlobStorageServie(IOptions<BlobStorageOptions> options)
    {
        _blobStorage = options.Value;
    }

    public async Task<string> UploadFileAsync(IFormFile file, string? fileNameWithExtension = "")
    {
        if (string.IsNullOrEmpty(fileNameWithExtension))
        {
            var fileExtension = Path.GetExtension(file.FileName)?.ToLowerInvariant();
            fileNameWithExtension = Guid.NewGuid().ToString("N") + fileExtension;
        }
        BlobContainerClient containerClient = new(_blobStorage.ConnectionString, _blobStorage.ContainerName);

        await containerClient.CreateIfNotExistsAsync();

        await containerClient.SetAccessPolicyAsync(PublicAccessType.Blob);

        BlobClient blobClient = containerClient.GetBlobClient(fileNameWithExtension);

        await using var stream = file.OpenReadStream();

        await blobClient.UploadAsync(stream, true);

        return blobClient.Uri.ToString();
    }

    public async Task DeleteBlobAsync(string blobUrl)
    {
        string blobName = Path.GetFileName(blobUrl);
        if (string.IsNullOrEmpty(blobName))
        {
            throw new InvalidOperationException("Invalid blob url");
        }
        BlobContainerClient containerClient = new(_blobStorage.ConnectionString, _blobStorage.ContainerName);

        BlobClient blobClient = containerClient.GetBlobClient(blobName);

        await blobClient.DeleteIfExistsAsync(snapshotsOption: DeleteSnapshotsOption.IncludeSnapshots);
    }

}

```

## Register Blobstorage service in program.cs

```cs
builder.Services.AddSingleton<IBlobStorageService, BlobStorageServie>();
```

--- 

In this section, we will be connecting with database, so we'll create Models, Dtos and AppDbContext

First, install the required nuget packages:

```sh
Microsoft.EntityFrameworkCore.SqlServer
```

And

```sh
## For Visual studio users
Microsoft.EntityFrameworkCore.Tools

## For .NET CLI users
Microsoft.EntityFrameworkCore.Tools.Design
```

## Domain model 

This class represents the entity in the sql server database.

```cs
// Models/Person.cs
using System.ComponentModel.DataAnnotations;

namespace AzureBlobDemo.Models;

public class Person
{
    public int PersonId { get; set; }

    [Required]
    [MaxLength(30)]
    public string FirstName { get; set; } = null!;

    [Required]
    [MaxLength(30)]
    public string LastName { get; set; } = null!;

    [Required]
    [MaxLength(250)]
    public string ProfilePicture { get; set; } = null!;
}
```

📢 `ProfilePicture` will hold the blob container's image url.

### DTOs

PersonDto:

```cs
// Models/PersonDto.cs

using System.ComponentModel.DataAnnotations;

namespace AzureBlobDemo.Models;

public class PersonDto
{
    [Required]
    [MaxLength(30)]
    public string FirstName { get; set; } = null!;

    [Required]
    [MaxLength(30)]
    public string LastName { get; set; } = null!;

    [Required]
    public IFormFile File { get; set; } = null!;

    public string? SuccessMessage { get; set; }
    public string? ErrorMessage { get; set; }
}
```

PersonUpdateDto:

```cs
// Models/PersonUpdateDto.cs

using System.ComponentModel.DataAnnotations;

namespace AzureBlobDemo.Models;

public class PersonUpdateDto
{
    public int PersonId { get; set; }

    [Required]
    [MaxLength(30)]
    public string FirstName { get; set; } = null!;

    [Required]
    [MaxLength(30)]
    public string LastName { get; set; } = null!;

    [Required]
    public string ProfilePicture { get; set; } = null!;

    public IFormFile? File { get; set; }

    public string? SuccessMessage { get; set; }
    public string? ErrorMessage { get; set; }
}
```

## AppDbContext

```cs
// Models/AppDbContext.cs

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {

    }

    public DbSet<Person> People { get; set; }
}
```

## Database connection string

Appsettings.json

```json
"ConnectionStrings": {
  "Default": "Server=localhost,1433;Database=PersonDb;User Id= <your_username>; Password=<your password>; Trust Server Certificate=true"
}
```

## Let's register AppDbContext in a Program.cs

```cs
var connectionString = builder.Configuration.GetConnectionString("Default");
builder.Services.AddDbContext<AppDbContext>(op => op.UseSqlServer(connectionString));
```

--- 

## Controllers

- Create a controller with name `PersonController`

- Inject required services to it

```cs
public class PersonController : Controller
{
    private readonly AppDbContext _dbcontext;
    private readonly IBlobStorageService _blobStorage;

    public PersonController(AppDbContext dbcontext, IBlobStorageService blobStorage)
    {
        _dbcontext = dbcontext;
        _blobStorage = blobStorage;
    }

    // Index method

    // CreatePerson (get method)

    // CreatePerson (post method)

    // EditPerson (get method)

    // EditPerson (post method)

    // DeletePerson (method)
}
```
Let's define each method.

### Index method

```cs
 public async Task<IActionResult> Index()
 {
     var people = await _dbcontext.People.ToListAsync();
     return View(people);
 }
```

### CreatePerson (get method)

```cs
 public IActionResult CreatePerson()
 {
     return View(new PersonDto());
 }
```

### CreatePerson (post method)

```cs
[HttpPost]
public async Task<IActionResult> CreatePerson(PersonDto personToCreate)
{
    if (!ModelState.IsValid)
    {
        return View(personToCreate);
    }
    try
    {
        if (personToCreate.File.Length > 300 * 1024)
        {
            personToCreate.ErrorMessage = "File can not exceed 300kb length";
            return View(personToCreate);
        }

        var allowedExtensions = new[] { ".jpg", ".jpeg", ".png" };
        var fileExtension = Path.GetExtension(personToCreate.File.FileName)?.ToLowerInvariant();

        if (!allowedExtensions.Contains(fileExtension))
        {
            personToCreate.ErrorMessage = "You can only upload .jpg, .jpeg, .png files";
            return View(personToCreate);
        }

        string profilePicUrl = await _blobStorage.UploadFileAsync(personToCreate.File);

        var person = new Person
        {
            FirstName = personToCreate.FirstName,
            LastName = personToCreate.LastName,
            ProfilePicture = profilePicUrl
        };
        _dbcontext.Add(person);
        await _dbcontext.SaveChangesAsync();
        personToCreate.SuccessMessage = "Saved successfully";
    }
    catch (Exception ex)
    {
        personToCreate.ErrorMessage = ex.Message;
        Console.WriteLine(ex.Message);
    }
    return View(personToCreate);
}
```

### EditPerson (get method)

```cs
public async Task<IActionResult> EditPerson(int id)
{
    var person = await _dbcontext.People.FindAsync(id);
    if (person is null) throw new InvalidOperationException("Person does not exists");

    var personUpdateDto = new PersonUpdateDto
    {
        PersonId = person.PersonId,
        FirstName = person.FirstName,
        LastName = person.LastName,
        ProfilePicture = person.ProfilePicture
    };
    return View(personUpdateDto);
}
```

### EditPerson (post method)

```cs
[HttpPost]
public async Task<IActionResult> EditPerson(PersonUpdateDto personToUpdate)
{
    if (!ModelState.IsValid)
    {
        return View(personToUpdate);
    }
    try
    {
        if (personToUpdate.File != null)
        {

            if (personToUpdate.File.Length > 300 * 1024)
            {
                personToUpdate.ErrorMessage = "File can not exceed 300kb length";
                return View(personToUpdate);
            }

            var allowedExtensions = new[] { ".jpg", ".jpeg", ".png" };

            var fileExtension = Path.GetExtension(personToUpdate.File.FileName)?.ToLowerInvariant();

            if (string.IsNullOrEmpty(fileExtension) || !allowedExtensions.Contains(fileExtension))
            {
                personToUpdate.ErrorMessage = "You can only upload .jpg, .jpeg, .png files";
                return View(personToUpdate);
            }
            string oldPictureName = personToUpdate.ProfilePicture;
            personToUpdate.ProfilePicture = await _blobStorage.UploadFileAsync(personToUpdate.File, oldPictureName);
        }

        var person = new Person
        {
            PersonId = personToUpdate.PersonId,
            FirstName = personToUpdate.FirstName,
            LastName = personToUpdate.LastName,
            ProfilePicture = personToUpdate.ProfilePicture!
        };
        _dbcontext.Update(person);
        await _dbcontext.SaveChangesAsync();
        personToUpdate.SuccessMessage = "Saved successfully";
    }
    catch (Exception ex)
    {
        personToUpdate.ErrorMessage = ex.Message;
        Console.WriteLine(ex.Message);
    }
    return View(personToUpdate);
}
```

### DeletePerson (method)

```cs
public async Task<IActionResult> DeletePerson(int id)
{
    var transaction = await _dbcontext.Database.BeginTransactionAsync();
    try
    {
        var person = await _dbcontext.People.FindAsync(id);
        if (person == null)
        {
            throw new InvalidOperationException("No person found to delete.");
        }
        var blobUrl = person.ProfilePicture;
        _dbcontext.People.Remove(person);
        _dbcontext.SaveChanges();
        await _blobStorage.DeleteBlobAsync(blobUrl);
        await transaction.CommitAsync();
    }
    catch (Exception ex)
    {
        Console.WriteLine(ex.Message);
        await transaction.RollbackAsync();
    }
    return RedirectToAction(nameof(Index));
}
```

## Views for each controller method

- Create a new folder/directory named `Person` inside `Views`
- Create three views : `CreatePerson.cshtml`, `EditPerson.cshtml` and `Index.cshtml`
- These views represents their coressponding controller methods

Let's define each of them

### CreatePerson.cshtml

```html
@model PersonDto
@{
    ViewData["Title"] = "Add person";
}

<div style="width: 50%;">
    <h1>Save person</h1>
    <a class="btn btn-info mb-2" href="/Person/Index">Show all</a>

    @if (!string.IsNullOrEmpty(Model.SuccessMessage))
    {
        <div class="alert alert-success">@Model.SuccessMessage</div>
    }


    @if (!string.IsNullOrEmpty(Model.ErrorMessage))
    {
        <div class="alert alert-success">@Model.ErrorMessage</div>
    }

    <form asp-action="CreatePerson" method="post" enctype="multipart/form-data">

        <div class="mb-3">
            <label>FirstName*</label>
            <input type="text" class="form-control" asp-for="FirstName">
            <span asp-validation-for="FirstName" class="text-danger"></span>
        </div>

        <div class="mb-3">
            <label>LastName*</label>
            <input type="text" class="form-control" asp-for="LastName">
            <span asp-validation-for="LastName" class="text-danger"></span>
        </div>

        <div class="mb-3">
            <label>Profile Pic*</label>
            <input type="file" class="form-control" asp-for="File">
            <span asp-validation-for="File" class="text-danger"></span>
        </div>

        <div class="mb-3">
            <button type="submit" class="btn btn-primary">Save</button>
        </div>

    </form>

</div>
```

### EditPerson.cshtml

```html
@model PersonUpdateDto
@{
    ViewData["Title"] = "Update person";
}

<div style="width: 50%;">
    <h1>Update person</h1>
    <a class="btn btn-info mb-2" href="/Person/Index">Show all</a>

    @Html.ValidationSummary()

    @if (!string.IsNullOrEmpty(Model.SuccessMessage))
    {
        <div class="alert alert-success">@Model.SuccessMessage</div>
    }


    @if (!string.IsNullOrEmpty(Model.ErrorMessage))
    {
        <div class="alert alert-success">@Model.ErrorMessage</div>
    }

    <form asp-action="EditPerson" method="post" enctype="multipart/form-data">
        <input type="hidden" asp-for="PersonId" />
        <input type="hidden" asp-for="ProfilePicture" />
        <div class="mb-3">
            <label>FirstName*</label>
            <input type="text" class="form-control" asp-for="FirstName">
            <span asp-validation-for="FirstName" class="text-danger"></span>
        </div>

        <div class="mb-3">
            <label>LastName*</label>
            <input type="text" class="form-control" asp-for="LastName">
            <span asp-validation-for="LastName" class="text-danger"></span>
        </div>

        <div class="mb-3">
            <label>Profile Pic</label>
            @if (!string.IsNullOrEmpty(Model.ProfilePicture))
            {
                <img class="mb-1" style="width:100px;height:80px" src="@Model.ProfilePicture" />
            }
            <input type="file" class="form-control" asp-for="File">

        </div>

        <div class="mb-3">
            <button type="submit" class="btn btn-primary">Save</button>
        </div>

    </form>

</div>
```

### Index.cshtml

```html
@model IEnumerable<Person>
@{
    ViewData["Title"] = "People";
}

<h1>People</h1>

<a class="btn btn-info mb-2" href="/Person/CreatePerson">Add more</a>

<table class="table table-striped table-bordered">

    <thead>
        <tr>
            <th>FirstName</th>
            <th>LastName</th>
            <th>Picture</th>
            <th>Actions</th>
        </tr>
    </thead>

    <tbody>
        @foreach (var person in Model)
        {
            <tr>
                <td>@person.FirstName</td>
                <td>@person.LastName</td>
                <td>
                    @if (string.IsNullOrEmpty(person.ProfilePicture))
                    {
                        <span>No Image</span>
                    }
                    else
                    {
                        <img style="width:120px;height:90px" src="@person.ProfilePicture" />
                    }
                </td>
                <td>
                    <a href="/Person/EditPerson?id=@person.PersonId" class="btn btn-success">Edit</a>
                    <a onclick="return window.confirm('Are you sure to delete?')"
                        href="/Person/DeletePerson?id=@person.PersonId" class="btn btn-danger">Delete</a>
                </td>
            </tr>
        }
    </tbody>

</table>

```

You can see your stored images here

![blob container](/images/blobstorage/blob_blob_container.png)

---


