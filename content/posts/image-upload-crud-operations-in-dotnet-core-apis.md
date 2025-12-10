+++
date = '2025-02-22T18:28:32+05:30'
draft = false
title = 'Image Upload CRUD Operations in .NET Core WebAPIs'
tags = ['dotnet']
categories=['programming']
image = '/images/1_raTlXZDRoXEYN5Calq8q0Q.png'
+++

<!-- ![how to upload images in .net core web api](/images/1_raTlXZDRoXEYN5Calq8q0Q.png) -->

Upload images in .net core apis

In this article, we will learn how to upload/update/delete/read images in .net core APIs. I hate to give long and unnecessary intros, So let’s come to the point’s.

💻 You can get the code from this [github repo](https://github.com/rd003/ImageManipulation_APIs_DotNetCore).

## What is the logic behind it? 🤔

When you upload the image (or any file), we will generate the unique image name with it’s extension (eg. uniquename.png). Save the image name in the database and save the file with the same name inside the project. In production apps, you can not simply upload files to the server, you have to give permission to that folder. Or you can use other file storage service, where you will save your files.

## Why don’t I prefer to save image in database? 🤔

You can definitely save the image in the database in the binary format, base-64 string format. But it will increase the size of your database. Which can increase your bills and lead some performance issue.

## Project Structure

![project structure](/images/1_NMahFsCf04hXNJpWGVhhZQ.jpg)

I am assuming that, you know how to create a solution file, with multiple projects.

**Solution name:** `ImageManipulation`

**Project 1:** `ImageManipulation.API` (.net core web api)

**Project 2:** `ImageManipulation.Data` (Class Library)

**⚠️Note:** Don’t forget to add the reference of **ImageManipulation.Data** in the **ImageManipulation.API** project.

## Models

Create a class named `Product`

```cs
// ImageManipulation.Data/Models/Prodcut.cs
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace ImageManipulation.Data.Models;

[Table("Product")]
public class Product
{
 public int Id { get; set; }

    [Required]
    [MaxLength(30)]
    public string? ProductName { get; set; }

    [Required]
    [MaxLength(50)]
    public string? ProductImage { get; set; }

}
```

Add another class `ApplicationDbContext`

```cs
// ImageManipulation.Data/Models/ApplicationDbContext.cs

using Microsoft.EntityFrameworkCore;

namespace ImageManipulation.Data.Models;

public class ApplicationDbContext: DbContext
{
 public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options):base(options)
 {

 }

    public DbSet<Product> Products { get; set; }
}
```

## Nuget Packages

👉 **In ImageManipulation.API**

- _Microsoft.EntityFrameworkCore.Tools_

👉 **In ImageManipulation.Data**

- _Microsoft.EntityFrameworkCore.SqlServer_
- _Microsoft.Extensions.Configuration.Abstractions_

## appsettings.json file

Add connection string in `appsettings.json` file

```json
"ConnectionStrings": {
 "default": "server=your_sql_server_instance_name;database=ImageManipulation;integrated security=true; encrypt=false"
},
```

## Program.cs file

Update the program.cs file, with following code

```cs
builder.Services.AddDbContext<ApplicationDbContext\>(options =>
 options.UseSqlServer(builder.Configuration.GetConnectionString("default"))
);
```

## Migrations

Open package manage console `(Tools->Nuget Package Manager->Package Manager Console)` and run these command in a successive manner.

```sh
add-migration initialCreate
update-database
```

At this stage, we have successfully created our database.

---

## DTOs

```cs
// ImageManipulation.Data/Models/DTO/ProductDTO.cs

using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Http;
// NOTE: for using above namespace include this line in csproj
// of this class library :
//<FrameworkReference Include="Microsoft.AspNetCore.App" />

namespace ImageManipulation.Data.Models.DTO;
public class ProductDTO
{
 [Required]
 [MaxLength(30)]
 public string? ProductName { get; set; }

    [Required]
    public IFormFile? ImageFile { get; set; }

}

public class ProductUpdateDTO
{

    [Required]
    public int Id { get; set; }

    [Required]
    [MaxLength(30)]
    public string? ProductName { get; set; }

    [Required]
    [MaxLength(50)]
    public string? ProductImage { get; set; }

    public IFormFile? ImageFile { get; set; }

}
```

👉 `IFormFile` comes under the `Microsoft.AspNetCore.Http` namespace and this namespace does not included in project by default. You have to add it manually. So open the `ImageManipulation.Data.csproj` file or double click on `ImageManipulation.Data` project, which is shown in solution explorer. Add follwing line in the file inside the `ItemGroup` tag.

`<FrameworkReference Include=”Microsoft.AspNetCore.App” />`

```xml
// ImageManipulation.Data.csproj

//..... existing lines

<ItemGroup>
 // ...... previous lines

 // new line 👇
 <FrameworkReference Include="Microsoft.AspNetCore.App" />
</ItemGroup>

// ..... ..... existing lines
```

## ProductRepository

```cs
// ImageManipulation.Data/Repositorie/ProductRepository.cs

using ImageManipulation.Data.Models;
using Microsoft.EntityFrameworkCore;

namespace ImageManipulation.Data.Repositories;

public interface IProductRepository
{
    Task<Product> AddProductAsync(Product product);
    Task<Product> UpdateProductAsync(Product product);
    Task<IEnumerable<Product>> GetProductsAsync();
    Task<Product?> FindProductByIdAsync(int id);
    Task DeleteProductAsync(Product product);
}

public class ProductRepository(ApplicationDbContext context) : IProductRepository
{
    public async Task<Product> AddProductAsync(Product product)
    {
        context.Products.Add(product);
        await context.SaveChangesAsync();
        return product; // returning created product, it will automatically fetch \`Id\`
    }

    public async Task<Product> UpdateProductAsync(Product product)
    {
        context.Products.Update(product);
        await context.SaveChangesAsync();
        return product;
    }

    public async Task DeleteProductAsync(Product product)
    {
        context.Products.Remove(product);
        await context.SaveChangesAsync();
    }

    public async Task<Product?> FindProductByIdAsync(int id)
    {
        var product = await context.Products.FindAsync(id);
        return product;
    }

    public async Task<IEnumerable<Product>> GetProductsAsync()
    {
        return await context.Products.ToListAsync();
    }

}
```

## FileService

```cs
// ImageManipulation.Data/Repositorie/.cs

using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;

namespace ImageManipulation.Data.Services;

public interface IFileService
{
    Task<string\> SaveFileAsync(IFormFile imageFile, string[] allowedFileExtensions);
    void DeleteFile(string fileNameWithExtension);
}

public class FileService(IWebHostEnvironment environment) : IFileService
{

    public async Task<string\> SaveFileAsync(IFormFile imageFile, string[] allowedFileExtensions)
    {
        if (imageFile == null)
        {
            throw new ArgumentNullException(nameof(imageFile));
        }

        var contentPath = environment.ContentRootPath;
        var path = Path.Combine(contentPath, "Uploads");
        // path = "c://projects/ImageManipulation.Ap/uploads" ,not exactly, but something like that

        if (!Directory.Exists(path))
        {
            Directory.CreateDirectory(path);
        }

        // Check the allowed extenstions
        var ext = Path.GetExtension(imageFile.FileName);
        if (!allowedFileExtensions.Contains(ext))
        {
            throw new ArgumentException($"Only {string.Join(",", allowedFileExtensions)} are allowed.");
        }

        // generate a unique filename
        var fileName = $"{Guid.NewGuid().ToString()}{ext}";
        var fileNameWithPath = Path.Combine(path, fileName);
        using var stream = new FileStream(fileNameWithPath, FileMode.Create);
        await imageFile.CopyToAsync(stream);
        return fileName;
    }


    public void DeleteFile(string fileNameWithExtension)
    {
        if (string.IsNullOrEmpty(fileNameWithExtension))
        {
            throw new ArgumentNullException(nameof(fileNameWithExtension));
        }
        var contentPath = environment.ContentRootPath;
        var path = Path.Combine(contentPath, $"Uploads", fileNameWithExtension);

        if (!File.Exists(path))
        {
            throw new FileNotFoundException($"Invalid file path");
        }
        File.Delete(path);
    }

}
```

The code demonstrated above for uploading files is simple, according to logic, which I have explained in the starting, If you haven’t read it, please read it first. File will be saved in `Uploads` folder, in the root directory.

## Program.cs

Add these lines.

```cs
// .... previous lines
builder.Services.AddTransient<ApplicationDbContext\>();
builder.Services.AddTransient<IProductRepository, ProductRepository\>();
builder.Services.AddTransient<IFileService, FileService\>();
builder.Services.AddCors(options =>
{
 options.AddDefaultPolicy(
 policy =>
 {
 policy.WithOrigins("\*").AllowAnyMethod().AllowAnyHeader(); ;
 });
});
// .... other lines

// mapping Uploads folder to Resources folder
app.UseStaticFiles(new StaticFileOptions
{
 FileProvider = new PhysicalFileProvider(
 Path.Combine(builder.Environment.ContentRootPath, "Uploads")),
 RequestPath = "/Resources"
});

app.UseCors(); // for enabling cross origin requests

// .... other lines
```

Actual file path is `basePath/uploads/imageName.extension`

Our files will be saved in `Uploads` folder, but will not expose this name to the client. But, we have mapped `Uploads` to `Resources`. So file path for client will be `basePath/resources/imageName.extension`

## Controllers

```cs
//ImageManipulation.API/Controllers/ProductController.cs

using ImageManipulation.Data.Models;
using ImageManipulation.Data.Models.DTO;
using ImageManipulation.Data.Repositories;
using ImageManipulation.Data.Services;
using Microsoft.AspNetCore.Mvc;

namespace ImageManipulation.API.Controllers;

[Route("api/products")]
[ApiController]
public class ProductController(IFileService fileService, IProductRepository productRepo, ILogger<ProductController> logger) : ControllerBase
{
            [HttpPost]
            public async Task<IActionResult> CreateProduct([FromForm] ProductDTO productToAdd)
            {
            try
            {
            if (productToAdd.ImageFile?.Length > 1 \* 1024 \* 1024)
            {
            return StatusCode(StatusCodes.Status400BadRequest, "File size should not exceed 1 MB");
            }
            string[] allowedFileExtentions = [".jpg", ".jpeg", ".png"];
            string createdImageName = await fileService.SaveFileAsync(productToAdd.ImageFile, allowedFileExtentions);

            // mapping \`ProductDTO\` to \`Product\` manually. You can use automapper.
            var product = new Product
            {
                ProductName = productToAdd.ProductName,
                ProductImage = createdImageName
            };
            var createdProduct = await productRepo.AddProductAsync(product);
            return CreatedAtAction(nameof(CreateProduct), createdProduct);
        }
        catch (Exception ex)
        {
            logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }


    // api/products/1
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateProduct(int id, [FromForm] ProductUpdateDTO productToUpdate)
    {
        try
        {
            if (id != productToUpdate.Id)
            {
                return StatusCode(StatusCodes.Status400BadRequest, $"id in url and form body does not match.");
            }

            var existingProduct = await productRepo.FindProductByIdAsync(id);
            if (existingProduct == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, $"Product with id: {id} does not found");
            }
            string oldImage = existingProduct.ProductImage;
            if (productToUpdate.ImageFile != null)
            {
                if (productToUpdate.ImageFile?.Length > 1 \* 1024 \* 1024)
                {
                    return StatusCode(StatusCodes.Status400BadRequest, "File size should not exceed 1 MB");
                }
                string[] allowedFileExtentions = [".jpg", ".jpeg", ".png"];
                string createdImageName = await fileService.SaveFileAsync(productToUpdate.ImageFile, allowedFileExtentions);
                productToUpdate.ProductImage = createdImageName;
            }

            // mapping \`ProductDTO\` to \`Product\` manually. You can use automapper.
            existingProduct.Id = productToUpdate.Id;
            existingProduct.ProductName = productToUpdate.ProductName;
            existingProduct.ProductImage = productToUpdate.ProductImage;

            var updatedProduct = await productRepo.UpdateProductAsync(existingProduct);

            // if image is updated, then we have to delete old image from directory
            if (productToUpdate.ImageFile != null)
                fileService.DeleteFile(oldImage);

            return Ok(updatedProduct);
        }
        catch (Exception ex)
        {
            logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }


    // api/products/1
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        try
        {
            var existingProduct = await productRepo.FindProductByIdAsync(id);
            if (existingProduct == null)
            {
                return StatusCode(StatusCodes.Status404NotFound, $"Product with id: {id} does not found");
            }

            await productRepo.DeleteProductAsync(existingProduct);
            // After deleting product from database,remove file from directory.
            fileService.DeleteFile(existingProduct.ProductImage);
            return NoContent();  // return 204
        }
        catch (Exception ex)
        {
            logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

    // api/products/1
    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        var product = await productRepo.FindProductByIdAsync(id);
        if (product == null)
        {
            return StatusCode(StatusCodes.Status404NotFound, $"Product with id: {id} does not found");
        }
        return Ok(product);
    }


    // api/products
    [HttpGet]
    public async Task<IActionResult> GetProducts()
    {
        var products = await productRepo.GetProductsAsync();
        return Ok(products);
    }

}
```

**⚠️ Note:** When you are using `post` and `put` APIs, then please make sure to pass your data from the `Form`. Since we posting the file too, our content type must be `multipart/form-data`.

## Test the Post API with swagger

![post api swagger](/images/1_aa-CIyPUC4TXkoUJd-YLcg.jpg)

---

[Canonical link](https://medium.com/@ravindradevrani/image-upload-crud-operations-in-net-core-apis-7407f111d2f4)
