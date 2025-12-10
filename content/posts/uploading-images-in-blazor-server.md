+++
date = '2025-02-20T18:25:51+05:30'
draft = false
title = 'Uploading Images in Blazor Server'
tags = ['dotnet','blazor']
category=['programming']
image = '/images/upload_files_in_blazor.png'
+++

<!-- ![upload files in blazor server](/images/upload_files_in_blazor.png) -->

In this blog post we are going to learn how to upload files in the blazor server application. I am going to upload **images** in this tutorial but you can upload **any file** (i have created **reusable code**).

💻Source Code: [https://github.com/rd003/BlazorFile/](https://github.com/rd003/BlazorFile/)

## High level overview

We will upload images to a **folder of a local machine** ( on a production you have to use cloud storage) with a unique name (e.g. `sd$3abccc3$1.png` ), that name is going to save in database.

**note:** File name in the folder & database must be **in sync** and always be **unique**.

## Database and ORM

- We will use `ms sql server` database and `dapper` micro orm.

## Database Design

```sql
create database BlazorFileDemo;
go

use  BlazorFileDemo;
go

create table ImageFile
(
 Id int primary key identity,
 ImageName nvarchar(200) not null
);
go
```

---

## Blazor server project

Create new blazor server app with a template “Blazor server app empty”

![new_blzr_server_project](/images/1_MZ5EQbm20XwzawTAf6cuzQ.jpg)

blazor server app empty

**👉 Project Name :**

`**BlazorFile**`

If you have created the project successfully then move ahead.

---

## Database connectivity

In this section how we can insert record and retrieve record to/from a database.

**Required packages:** Install these packages from nuget

👉 Dapper

👉 Microsoft.Data.SqlClient

## ConnectionString

```json
// appsettings.json
"ConnectionStrings": {
 "default": "data source=RAVINDRA\\\MSSQLSERVER01 ;initial catalog=BlazorFileDemo;integrated security=true;encrypt=false"
 }

```

## Models

```cs
\\ Models/ImageFile.cs

namespace BlazorFile.Models
{
public class ImageFile
{
public int Id { get; set; }
public string ImageName { get; set; }
}
}
```

## Image Upload Repository

Create a new directory **Repositories**. Inside this directory create a new class **ImageUploadRepository.cs.**

First we will create an interface. I am going to create interface and class inside a single file , since it is a demo project. I recommend you to create it a new file with Name **IImageUploadRepository.cs**

```cs
// ImageUploadRepository.cs

using BlazorFile.Models;

namespace BlazorFile.Repositories;
public interface IImageUploadRepository
{
Task UploadImageToDb(ImageFile image);
Task&lt;IEnumerable<ImageFile&gt;> GetImages();
}
```

Now we will implement this interface

```cs
// ImageUploadRepository.cs

using BlazorFile.Models;
using Dapper;
using Microsoft.Data.SqlClient;
using System.Data;

namespace BlazorFile.Repositories;

// Interface
public interface IImageUploadRepository
{
Task UploadImageToDb(ImageFile image);
Task&lt;IEnumerable<ImageFile&gt;> GetImages();
}

// Implementation of interface

public class ImageUploadRepository: IImageUploadRepository
{
private readonly IConfiguration _config;
// key defined in the connection string in appsettings.json
const string CONN_KEY = "default";

    public ImageUploadRepository(IConfiguration config)
    {
        _config = config;
    }

    public async Task UploadImageToDb(ImageFile image)
    {
        var connectionString = _config.GetConnectionString(CONN\_KEY);
        using IDbConnection connection = new SqlConnection(connectionString);
        string sql = "insert into ImageFile (ImageName) values (@ImageName)";
        await connection.ExecuteAsync(sql, new { ImageName = image.ImageName });
    }

    public async Task&lt;IEnumerable<ImageFile&gt;> GetImages()
    {
        var connectionString = _config.GetConnectionString(CONN_KEY);
        using IDbConnection connection = new SqlConnection(connectionString);
        string sql = "select * from ImageFile";
        var images = await connection.QueryAsync&lt;ImageFile&gt;(sql);
        return images;
    }

}
```

**Breakdown:**

- Method `UploadImageToDb` will save your data to db.
- Method `GetImages` will retrieve image from database.

Now add these services to DI container. Open **program.cs** file and add the line below

```cs
// program.cs

builder.Services.AddTransient&lt;IImageUploadRepository,ImageUploadRepository&gt;();
```

---

## File Upload Service

Create a directory and name it `**Utilities.**` Inside this create a interface **IFileUploadService** and a class **FileUploadService.**

```cs
// IFileUploadService.cs
using Microsoft.AspNetCore.Components.Forms;

namespace BlazorFile.Utilities
{
public interface IFileUploadService
{
Task<(int, string)\> UploadFileAsync(IBrowserFile file, int maxFileSize, string\[\] allowedExtensions);
}
}
```

Now we will implement this intrerface.

```cs
// FileUploadService.cs

using Microsoft.AspNetCore.Components.Forms;

namespace BlazorFile.Utilities;

public class FileUploadService : IFileUploadService
{
private readonly IWebHostEnvironment \_environment;

    public FileUploadService(IWebHostEnvironment environment, ILogger&lt;FileUploadService&gt; logger)
    {
        _environment = environment;
    }
    public async Task<(int, string)\> UploadFileAsync(IBrowserFile file, int maxFileSize, string\[\] allowedExtensions)
    {
        var uploadDirectory = Path.Combine(_environment.WebRootPath, "Uploads");
        if (!Directory.Exists(uploadDirectory))
        {
            Directory.CreateDirectory(uploadDirectory);
        }

        if (file.Size > maxFileSize)
        {
            return (0, $"File: {file.Name} exceeds the maximum allowed file size.");
        }

        var fileExtension = Path.GetExtension(file.Name);
        if (!allowedExtensions.Contains(fileExtension))
        {
            return (0, $"File: {file.Name}, File type not allowed");
        }

        var fileName = $"{Guid.NewGuid()}{fileExtension}";
        var path = Path.Combine(uploadDirectory, fileName);
        await using var fs = new FileStream(path, FileMode.Create);
        await file.OpenReadStream(maxFileSize).CopyToAsync(fs);
        return (1, fileName);
    }

}
```

Let’s break it down.

- UploadFileAsync takes 3 params **IBrowserFile file, int maxFileSize, string\[\] allowedExtensions** and returns a tuple **(int, string).** I want to return **status code** and **a message**(on error)/filename(on success), that is why Ihave used tuple here.
- Files will be uploaded inside `**wwwroot/Uploads.**` We will check whether this directory exists or not if not then we will create it.

```cs
var uploadDirectory = Path.Combine(\_environment.WebRootPath, "Uploads");
if (!Directory.Exists(uploadDirectory))
{
Directory.CreateDirectory(uploadDirectory);
}
```

- If file exceeds to its max size we will return with with 0 and error message

```cs
if (file.Size > maxFileSize)
{
return (0, $"File: {file.Name} exceeds the maximum allowed file size.");
}
```

- Retrieve the file extension and match it in **allowedExtensions** array.

```cs
var fileExtension = Path.GetExtension(file.Name);
if (!allowedExtensions.Contains(fileExtension))
{
return (0, $"File: {file.Name}, File type not allowed");
}
```

- Create a filename with GUID with file extension, so it will be unique. Open the fileStream and save it to a directory. Return **(1,filename).** Since we need to save this filename in database ,thats why we are returning it.

```cs
var fileName = $"{Guid.NewGuid()}{fileExtension}";
var path = Path.Combine(uploadDirectory, fileName);
await using var fs = new FileStream(path, FileMode.Create);
await file.OpenReadStream(maxFileSize).CopyToAsync(fs);
return (1, fileName);
```

Add this service to DI container so open **program.cs** file.

```cs
builder.Services.AddTransient&lt;IFileUploadService,FileUploadService&gt;();
```

Our program.cs file should like this now.

```cs
// program.cs

using BlazorFile.Repositories;
using BlazorFile.Utilities;
using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Components.Web;

var builder = WebApplication.CreateBuilder(args);
builder.Services.AddRazorPages();
builder.Services.AddServerSideBlazor();
// new line
builder.Services.AddTransient&lt;IFileUploadService,FileUploadService&gt;();
// new line
builder.Services.AddTransient&lt;IImageUploadRepository,ImageUploadRepository&gt;();

var app = builder.Build();

if (!app.Environment.IsDevelopment())
{
// The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
app.UseHsts();
}

app.UseHttpsRedirection();

app.UseStaticFiles();

app.UseRouting();

app.MapBlazorHub();
app.MapFallbackToPage("/_Host");

app.Run();
```

---

## Front end

Open the index.razor file add the necessary imports on the file.

```cs
@page "/"
@using BlazorFile.Models;
@using BlazorFile.Repositories;
@using BlazorFile.Utilities;
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.Extensions.Logging

@inject ILogger&lt;Index&gt; Logger
@inject IFileUploadService fileService
@inject IImageUploadRepository imageUploadRepo

We are injecting **Logger**(basic logger with console logging), **fileService** and **imageUploadRepo**.

// Index.razor
@code
{
bool loading = false;
List&lt;string&gt; messages = new();
List&lt;IBrowserFile&gt; files = new();
int maxFileSize = 1 \* 1024 \* 1024;
ImageFile imageModel = new();
}
```

These are few fields that we need in this component.

```cs
// Index.razor
@code
{
// .....remaining code which is defined above

private async void SelectFiles(InputFileChangeEventArgs e)
{
files = e.GetMultipleFiles(maxFileSize).ToList();
}

    private async Task HandleFormSubmit()
    {
        loading = true;
        messages.Clear();
        var allowedExtenstions = new string[] { ".png", ".jpg", ".jpeg", ".gif" };
        int count = 0;
        foreach (var file in files)
        {
            try
            {
                (int statusCode, string statusMessage) = await fileService.UploadFileAsync(file, maxFileSize, allowedExtenstions);
                if (statusCode == 1)
                {
                    messages.Add($"File : {file.Name} uploaded");
                    var imageData = new ImageFile
                        {
                            ImageName = statusMessage
                        };
                    // saving imagename to database
                    await imageUploadRepo.UploadImageToDb(imageData);
                    count++;
                }
                else
                    messages.Add(statusMessage);

            }
            catch (Exception ex)
            {
                messages.Add($"File : {file.Name} Error : {ex.Message}");
                Logger.LogError(ex.Message);
            }
        }

        loading = false;
        messages.Add($"{count}/{files.Count} uploaded");
    }

}
```

Add corresponding html too.

```cs
// Index.razor
<EditForm Model="@imageModel" OnValidSubmit="@HandleFormSubmit">
Select File(s):<InputFile OnChange="@SelectFiles" multiple />
<br />
<button type="submit">Upload</button>
</EditForm>

@if (loading)
{
<span>Uploading...</span>
}

<ul style="list-style:none">
    @foreach (var message in messages)
    {
        <li>
            @message
        </li>
    }
</ul>
```

- On file’s **OnChange()** event we are calling **SelectFiles()** method. In that method we are assigning all the selected files to a list named **files**.
- On form submit we are calling **HandleFormSubmit()** method.
- There, we will loop over files and inside it we will implement **try/catch** block.
- With the help of try/catch block, we can count the successfull uploads.
- Inside try block we will call **fileService.UploadFileAsync(….)** method to upload file to the **wwwroot/Uploads** directory. If we get `status code ==1` then we will call **imageUploadRepo.UploadImageToDb(…)** to save image related data to database.
- Since we are uploading multiple files, we need to display multiple message. That is why we have taken a list of message. So that we can add multiple messages.

**Display Images:**

On the same component (Index.razor) we will display images. In index.razor , add new field **images** which will contain list of messages.

```cs
// Index.razor
@code
{
bool loading = false;
List&lt;string&gt; messages = new();
List&lt;IBrowserFile&gt; files = new();
int maxFileSize = 1 \* 1024 \* 1024;
ImageFile imageModel = new();
List&lt;ImageFile&gt; images = new(); // new line

// ..... remaining code
}
```

Now create a method to where you can fetch images data from ImageUploadRepository service.

```cs
// Index.razor

@code
{
// ... remaining code

// new code is below
private async Task LoadImages()
{
try
{
images = (await imageUploadRepo.GetImages()).ToList();
}
catch(Exception ex)
{
messages.Add("Could not load images");
}
}
}
```

We will override a method **OnInitializedAsync(),** so that we can load data when component is initialized.

```cs
// Index.razor

@code
{
// ... remaining code

// new code is below
protected override async Task OnInitializedAsync()
{
messages.Clear();
loading = true;
await LoadImages();
loading = false;
}
}
```

Now we need to display it with html and css.

```cs
@if(images.Count>0)
{

 <h2>Images</h2>
 <div style="display:flex;gap:20px;flex-wrap:wrap;">
 @foreach (var image in images)
 {
 <img src="/Uploads/@image.ImageName" alt="image">
 }
 </div>
}
```

👉 Our final Index.razor component will look like this now.

```cs
@page "/"
@using BlazorFile.Models;
@using BlazorFile.Repositories;
@using BlazorFile.Utilities;
@using Microsoft.AspNetCore.Components.Forms
@using Microsoft.Extensions.Logging

@inject ILogger&lt;Index&gt; Logger
@inject IFileUploadService fileService
@inject IImageUploadRepository imageUploadRepo

<EditForm Model="@imageModel" OnValidSubmit="@HandleFormSubmit">
    Select File(s):<InputFile OnChange="@SelectFiles" multiple />
    &lt;br /&gt;
    <button type="submit">Upload&lt;/button&gt;
&lt;/EditForm&gt;

@if (loading)
{
&lt;span&gt;Uploading...&lt;/span&gt;
}

<ul style="list-style:none">
    @foreach (var message in messages)
    {
        &lt;li&gt;
            @message
        &lt;/li&gt;
    }
&lt;/ul&gt;

@if(images.Count>0)
{
&lt;h2&gt;Images&lt;/h2&gt;

<div style="display:flex;gap:20px;flex-wrap:wrap;">
@foreach (var image in images)
{
<img src="/Uploads/@image.ImageName" alt="image">
}
&lt;/div&gt;
}

@code {
bool loading = false;
List<string\> messages = new();
List&lt;IBrowserFile&gt; files = new();
int maxFileSize = 1 \* 1024 \* 1024;
ImageFile imageModel = new();
List&lt;ImageFile&gt; images = new();

    private async void SelectFiles(InputFileChangeEventArgs e)
    {
        files = e.GetMultipleFiles(maxFileSize).ToList();
    }

    private async Task HandleFormSubmit()
    {
        loading = true;
        messages.Clear();
        var allowedExtenstions = new string\[\] { ".png", ".jpg", ".jpeg", ".gif" };
        int count = 0;
        foreach (var file in files)
        {
            try
            {
                (int statusCode, string statusMessage) = await fileService.UploadFileAsync(file, maxFileSize, allowedExtenstions);
                if (statusCode == 1)
                {
                    messages.Add($"File : {file.Name} uploaded");
                    var imageData = new ImageFile
                        {
                            ImageName = statusMessage
                        };
                    // saving imagename to database
                    await imageUploadRepo.UploadImageToDb(imageData);
                    images.Add(imageData);
                    count++;
                }
                else
                    messages.Add(statusMessage);

            }
            catch (Exception ex)
            {
                messages.Add($"File : {file.Name} Error : {ex.Message}");
                Logger.LogError(ex.Message);
            }
        }

        loading = false;
        messages.Add($"{count}/{files.Count} uploaded");
    }


    protected override async Task OnInitializedAsync()
    {
        messages.Clear();
        loading = true;
        await LoadImages();
        loading = false;
    }

    private async Task LoadImages()
    {
        try
        {
            images = (await imageUploadRepo.GetImages()).ToList();
        }
        catch(Exception ex)
        {
            messages.Add("Could not load images");
        }
    }

}
```

Run the code and enjoy. 😎

![blazor_file_output](/images/blazor_file_output.jpg)

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [November 14, 2023](https://medium.com/p/04dc5c7776b9).

[Canonical link](https://medium.com/@ravindradevrani/upload-files-in-blazor-server-04dc5c7776b9)

Exported from [Medium](https://medium.com) on February 19, 2025.
