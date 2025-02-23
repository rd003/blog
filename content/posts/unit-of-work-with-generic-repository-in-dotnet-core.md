+++
date = '2025-02-23T17:38:31+05:30'
draft = false
title = 'Unit of Work With Generic Repository in DotNet Core'
tags = ['dotnet']
categories = ['programming']
+++

The **Unit of Work** Pattern is all about coordinated changes to the database. It groups multiple operations, such as inserts, updates, and deletes, into one transaction. This simply means that all the changes are done together as a complete action, or they all don’t happen at all. In case something goes wrong in one of the operations, the whole transaction rolls back and keeps the database consistent by not allowing partial updates. This makes it easy to handle errors and ensures reliable data.

**💻 Source code:** [https://github.com/rd003/DotnetUowDemo](https://github.com/rd003/DotnetUowDemo)

### Tools needed

- .NET 8 SDK (Maybe .net 9 would be released at the time you are reading it, it would also work in .net 9. However older versions like 6 and 7 will also work).
- Visual Studio Code With **C# Dev kit** extension.
- Microsoft SQL Server.

First and foremost, we are going to create a new project. Open the terminal or command prompt and run the following commands one by one.

```sh
dotnet new sln -o DotnetUowDemo
cd DotnetUowDemo
dotnet new webapi -o DotnetUOWDemo.Api --use-controllers
dotnet sln add .\DotnetUOWDemo.Api\
code .
```

The last command `code .` will open this project in the Vs Code editor.

### **Configuring EF core**

#### Required Nuget packages

👉 Install the following nuget packages by running following commands in a sequence.

```sh
dotnet add package Microsoft.EntityFrameworkCore.SqlServer
dotnet add package Microsoft.EntityFrameworkCore.Design
dotnet add package AutoMapper.Extensions.Microsoft.DependencyInjection
```

#### Defining the connection string

Open `appsettings.json` and add the line below

```json
"ConnectionStrings": {
 "default": "server=your_server_name;database=DotnetUOWDemo;integrated security=true; encrypt=false"
 }
```

**⚠️Note:** Make sure to change `server` value according to your sql server instance name.

#### Creating domain models

Create a folder named `Models` and create a class named `Category` inside this folder. Write the following code in the `Category` class.

```cs
using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models;

public class Category
{
    public int Id { get; set; }

    [Required]
    [MaxLength(20)]
    public string Name { get; set; } = string.Empty;

    public ICollection<Product> Products { get; set; } = [];

}
```

👉 Create another class named `Product` in the `Models` folder.

```cs
using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models;

public class Product
{
    public int Id { get; set; }

    [Required]
    [MaxLength(30)]
    public string ProductName { get; set; } = string.Empty;

    public int CategoryId { get; set; }

    public Category Category { get; set; } = null!;

}
```

👉 Create another class named `AppDbContext` and add the following code.

```cs
using Microsoft.EntityFrameworkCore;

namespace DotnetUOWDemo.Api.Models;

public class AppDbContext : DbContext
{
    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options)
    {

    }

    public DbSet<Category> Categories { get; set; }
    public DbSet<Product> Products { get; set; }
}
```

👉**Program.cs**

Add following line in the `Program.cs` file.

```cs
builder.Services.AddDbContext<AppDbContext>(options=>options.UseSqlServer(builder.Configuration.GetConnectionString("default")));
```

#### Migrations

Now we need to run migration commands to persist these entities in the database. Run the following commands in a sequence (one by one). Make sure you have installed the [ef tools](https://learn.microsoft.com/en-us/ef/core/cli/dotnet).

```sh
dotnet ef migrations add init
dotnet ef database update
```

### Generic Repository

Create a folder named `Repositories` and in this folder create an interface named `IRepository`.

```cs
using System.Linq.Expressions;

namespace DotnetUOWDemo.Api.Repositories;

public interface IRepository<T> where T : class
{
 void Add(T entity);
 void Update(T entity);
 void Delete(T entity);
 Task<T?> GetByIdAsync(int id, bool noTracking = false);
 Task<IEnumerable<T>> GetAllAsync(Expression<Func<T, bool\>>? filter = null, Func<IQueryable<T>, IOrderedQueryable<T>>? orderBy = null, string includeProperties = "");
}
```

Create a class named `Repository` in the `Repositories` folder.

```cs
using System.Linq.Expressions;
using DotnetUOWDemo.Api.Models;
using Microsoft.EntityFrameworkCore;

namespace DotnetUOWDemo.Api.Repositories;

public class Repository<T> : IRepository<T> where T : class
{
    private readonly AppDbContext _context;
    private readonly DbSet<T> _dbSet;

    public Repository(AppDbContext context)
    {
        _context = context;
        _dbSet = _context.Set<T>();
    }
    public void Add(T entity) => _dbSet.Add(entity);

    public void Update(T entity) => _dbSet.Update(entity);

    public void Delete(T entity) => _dbSet.Remove(entity);

    public async Task<T?> GetByIdAsync(int id, bool noTracking = false)
    {
        var query = _dbSet.AsQueryable();
        if (noTracking)
        {
            query = query.AsNoTracking();
        }
        return await query.FirstOrDefaultAsync(e => EF.Property<int\>(e, "Id") == id);
    }

    public async Task<IEnumerable<T>> GetAllAsync(Expression<Func<T, bool\>>? filter = null, Func<IQueryable<T>, IOrderedQueryable<T>>? orderBy = null, string includeProperties = "")
    {
        IQueryable<T> query = _dbSet;
        if (filter != null)
        {
            query = query.Where(filter);
        }
        foreach (var includeProperty in includeProperties.Split([','], StringSplitOptions.RemoveEmptyEntries))
        {
            query = query.Include(includeProperty);
        }
        if (orderBy != null)
        {
            return await orderBy(query).ToListAsync();
        }
        else
        {
            return await query.ToListAsync();
        }
    }
}
```

In this class we have created all the generic CRUD methods.

### Defining the unit of work

Create a new folder named `UnitOfWork`. In this folder create an interface named `IUnitOfWork` .

```cs
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.Repositories;

namespace DotnetUOWDemo.Api.UnitOfWork;

public interface IUnitOfWork : IDisposable
{
 IRepository<Category> CategoryRepository { get; }
 Task<int\> SaveChangesAsync();
}
```

Create a class `UnitOfWork` which will implement the `IUnitOfWork` interface.

```cs
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.Repositories;

namespace DotnetUOWDemo.Api.UnitOfWork;

public class UnitOfWork : IUnitOfWork
{
    private readonly AppDbContext _context;
    private IRepository<Category>? _categoryRepository = null;
    private IRepository<Product>? _productRepository = null;

    public UnitOfWork(AppDbContext context)
    {
        _context = context;
    }
    public IRepository<Category> CategoryRepository
    {
        get
        {
            if (_categoryRepository == null)
            {
                _categoryRepository = new Repository<Category>(_context);
            }
            return _categoryRepository;
        }
    }
    public IRepository<Product> ProductRepository
    {
        get
        {
            if (_productRepository == null)
            {
                _productRepository = new Repository<Product>(_context);
            }
            return _productRepository;
        }
    }

    public async Task<int\> SaveChangesAsync()
    {
        return await _context.SaveChangesAsync();
    }

    private bool disposed = false;

    protected virtual void Dispose(bool disposing)
    {
        if (!disposed)
        {
            if (disposing)
            {
                _context.Dispose();
            }
        }
        disposed = true;
    }

    public void Dispose()
    {
        Dispose(true);
        GC.SuppressFinalize(this);
    }

}
```

Now we need to register the **UnitOfWork** in the **Program** class.

```cs
builder.Services.AddScoped<IUnitOfWork, UnitOfWork>();
```

### **Services**

Although we can directly inject the **IUnitOfWork** service in the controller, but that will reduce the testability. We will create a Service, where we will inject the **IUnitOfWork.**

Create a folder named `Services` and create an interface named `ICategoryService` which have all the crud method declarations.

```cs
using System.Linq.Expressions;
using DotnetUOWDemo.Api.Models;

namespace DotnetUOWDemo.Api.Services;

public interface ICategoryService
{
 Task<Category> AddCategoryAsync(Category category);
 Task<Category> UpdateCategoryAsync(Category category);
 Task DeleteCategoryAsync(Category category);
 Task<Category?> GetCategoryByIdAsync(int id);
 Task<IEnumerable<Category>> GetAllCategoriesAsync();
}
```

Now create a class named **CategoryService** in the Service folder.

```cs
using System.Linq.Expressions;
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.UnitOfWork;

namespace DotnetUOWDemo.Api.Services;

public class CategoryService : ICategoryService
{
    private readonly IUnitOfWork _unitOfWork;

    public CategoryService(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Category> AddCategoryAsync(Category category)
    {
        _unitOfWork.CategoryRepository.Add(category);
        await _unitOfWork.SaveChangesAsync();
        return category;
    }

    public async Task<Category> UpdateCategoryAsync(Category category)
    {
        _unitOfWork.CategoryRepository.Update(category);
        await _unitOfWork.SaveChangesAsync();
        return category;
    }

    public async Task DeleteCategoryAsync(Category category)
    {
        _unitOfWork.CategoryRepository.Delete(category);
        await _unitOfWork.SaveChangesAsync();
    }


    public async Task<Category?> GetCategoryByIdAsync(int id)
    {
        return await _unitOfWork.CategoryRepository.GetByIdAsync(id, noTracking: true);
    }

    public Task<IEnumerable<Category>> GetAllCategoriesAsync()
    {
        return _unitOfWork.CategoryRepository.GetAllAsync();
    }

}
```

### DTOs

Create a new folder name `DTOs` inside the `Models` folder. In this folder create three classes named **CategoryCreateDto**, **CategoryDisplayDto**, **CategoryUpdateDto.**Their defintions are below.

```cs
// CategoryCreateDto

using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models.DTOs;

public class CategoryCreateDto
{
 [Required]
 [MaxLength(20)]
 public string Name { get; set; } = string.Empty;
}

// CategoryDisplayDto

namespace DotnetUOWDemo.Api.Models.DTOs;

public class CategoryDisplayDto
{
 public int Id { get; set; }
 public string Name { get; set; } = string.Empty;
}

//CategoryUpdateDto

using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models.DTOs;

public class CategoryUpdateDto
{
    public int Id { get; set; }

    [Required]
    [MaxLength(20)]
    public string Name { get; set; } = string.Empty;
}
```

### Mapper

Now, we need to map each of the class to the `Category` class. So, we are going to use automapper for it. Create a folder named `Profiles`. In this folder, create a class named `MyProfile`.

Register mapper in the **Program.cs**.

```cs
builder.Services.AddAutoMapper(typeof(Program));

using AutoMapper;

public class MyProfile : Profile
{
}
```

We need to inherit the **Profile** class of **Automapper** library. In this class we will define all the mappings.

```cs
using AutoMapper;
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.Models.DTOs;

namespace DotnetUOWDemo.Api.Profiles;

public class MyProfile : Profile
{
 public MyProfile()
 {
 CreateMap<Category, CategoryCreateDto>().ReverseMap();
 CreateMap<Category, CategoryUpdateDto>().ReverseMap();
 CreateMap<Category, CategoryDisplayDto>().ReverseMap();
 }
}
```

### **Category Controller**

Create an Api controller named `CategoriesController`.

```cs
using Microsoft.AspNetCore.Mvc;

namespace DotnetUOWDemo.Api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class CategoriesController : ControllerBase
{
}
```

Inject **CategoryService**, **ILogger** and **IMapper** services to it.

```cs
using AutoMapper;
using DotnetUOWDemo.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DotnetUOWDemo.Api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class CategoriesController : ControllerBase
{
    private readonly ICategoryService _categoryService;
    private readonly ILogger<CategoriesController> _logger;
    private readonly IMapper _mapper;

    public CategoriesController(ICategoryService categoryService, ILogger<CategoriesController> logger, IMapper mapper)
    {
        _categoryService = categoryService;
        _logger = logger;
        _mapper = mapper;
    }

}
```

Now we will create a **post** method.

```cs
    [HttpPost]
    public async Task<IActionResult> AddCategory(CategoryCreateDto categoryToAdd)
    {
        try
        {
            var category = _mapper.Map<Category>(categoryToAdd);
            await _categoryService.AddCategoryAsync(category);
            return CreatedAtAction(nameof(AddCategory), category);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }
```

Now, create the **put** method.

```cs
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateCategory(int id, [FromBody] CategoryUpdateDto categoryToUpdate)
    {
        try
        {
            if (id != categoryToUpdate.Id)
            {
                return BadRequest("Category ID mismatch");
            }
            var existingCategory = await _categoryService.GetCategoryByIdAsync(id);
            if (existingCategory == null)
            {
                return NotFound("Category not found");
            }
            var category = _mapper.Map<Category>(categoryToUpdate);
            await _categoryService.UpdateCategoryAsync(category);
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }
```

Delete method.

```cs
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteCategory(int id)
    {
        try
        {
            var category = await _categoryService.GetCategoryByIdAsync(id);
            if (category == null)
            {
                return NotFound("Category not found");
            }
            await _categoryService.DeleteCategoryAsync(category);
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }
```

Now create a get method, which returns a single record on the basis of id.

```cs
    [HttpGet("{id}")]
    public async Task<IActionResult> GetCategory(int id)
    {
        try
        {
            var category = await _categoryService.GetCategoryByIdAsync(id);
            if (category == null)
            {
                return NotFound("Category not found");
            }
            var categoryToReturn = _mapper.Map<CategoryDisplayDto>(category);
            return Ok(categoryToReturn);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }
```

Now create another get method, which will return all the records.

```cs
    [HttpGet]
    public async Task<IActionResult> GetCategories()
    {
        try
        {
            var categories = await _categoryService.GetAllCategoriesAsync();
            var categoriesToReturn = _mapper.Map<IEnumerable<CategoryDisplayDto>>(categories);
            return Ok(categoriesToReturn);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }
```

It is how unit of work pattern work. In the next section we will create one more **service** named **ProductService.**

---

### Product Service

👉 **Services/IProductService.cs**

```cs
// Services/IProductService
using System.Linq.Expressions;
using DotnetUOWDemo.Api.Models;

namespace DotnetUOWDemo.Api.Services;

public interface IProductService
{
 Task<Product> AddProductAsync(Product product);
 Task<Product> UpdateProductAsync(Product product);
 Task DeleteProductAsync(Product product);
 Task<Product?> GetProductByIdAsync(int id);

    Task<IEnumerable<Product>> GetAllProductsAsync(string sTerm = "");

}
```

👉 **Services/ProductService.cs**

```cs
using System.Linq.Expressions;
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.UnitOfWork;

namespace DotnetUOWDemo.Api.Services;

public class ProductService : IProductService
{
    private readonly IUnitOfWork _unitOfWork;

    public ProductService(IUnitOfWork unitOfWork)
    {
        _unitOfWork = unitOfWork;
    }

    public async Task<Product> AddProductAsync(Product product)
    {
        _unitOfWork.ProductRepository.Add(product);
        await _unitOfWork.SaveChangesAsync();
        return product;
    }

    public async Task<Product> UpdateProductAsync(Product product)
    {
        _unitOfWork.ProductRepository.Update(product);
        await _unitOfWork.SaveChangesAsync();
        return product;
    }

    public async Task DeleteProductAsync(Product product)
    {
        _unitOfWork.ProductRepository.Delete(product);
        await _unitOfWork.SaveChangesAsync();
    }

    public async Task<Product?> GetProductByIdAsync(int id)
    {
        return await _unitOfWork.ProductRepository.GetByIdAsync(id, noTracking: true);
    }

    public Task<IEnumerable<Product>> GetAllProductsAsync(string sTerm = "")
    {
        Expression<Func<Product, bool\>>? filter = null;
        if (!string.IsNullOrWhiteSpace(sTerm))
        {
            sTerm = sTerm.ToLower();
            filter = x => x.ProductName.ToLower().Contains(sTerm);
        }
        return _unitOfWork.ProductRepository.GetAllAsync(filter: filter, orderBy: x => x.OrderBy(x => x.ProductName), includeProperties: "Category");
    }

}
```

In this service, our `GetAll` different. We have used **filtering**, **order by** and **include** (to join two tables: product and category).

### Service registeration in Program.cs

```cs
builder.Services.AddScoped<IProductService, ProductService>();
```

### Product DTOs

Create three classes named **ProductCreateDto,** **ProductUpdateDto,** **ProductDisplayDto** in the DTOs folder.

```cs
// ProductCreateDto

using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models.DTOs;

public class ProductCreateDto
{
 [Required]
 [MaxLength(30)]
 public string ProductName { get; set; } = string.Empty;

    public int CategoryId { get; set; }

}

// ProductUpdateDto

using System.ComponentModel.DataAnnotations;

namespace DotnetUOWDemo.Api.Models.DTOs;

public class ProductUpdateDto
{
    public int Id { get; set; }

    [Required]
    [MaxLength(30)]
    public string ProductName { get; set; } = string.Empty;

    public int CategoryId { get; set; }

}

// ProductDisplayDto

namespace DotnetUOWDemo.Api.Models.DTOs;

public class ProductDisplayDto
{
    public int Id { get; set; }

    public string ProductName { get; set; } = string.Empty;

    public int CategoryId { get; set; }

    public string CategoryName { get; set; } = string.Empty;

}
```

### Mapping Product Dtos

Add these mapping in the **MyProfile.**

```cs
CreateMap<Product, ProductCreateDto>().ReverseMap();
CreateMap<Product, ProductUpdateDto>().ReverseMap();
CreateMap<Product, ProductDisplayDto>().ReverseMap();
```

### Product Controller

```cs
using AutoMapper;
using DotnetUOWDemo.Api.Models;
using DotnetUOWDemo.Api.Models.DTOs;
using DotnetUOWDemo.Api.Services;
using Microsoft.AspNetCore.Mvc;

namespace DotnetUOWDemo.Api.Controllers;

[Route("api/[controller]")]
[ApiController]
public class ProductsController : ControllerBase
{
    private readonly IProductService _productService;
    private readonly ILogger<ProductsController> _logger;
    private readonly IMapper _mapper;

    public ProductsController(IProductService productService, ILogger<ProductsController> logger, IMapper mapper)
    {
        _productService = productService;
        _logger = logger;
        _mapper = mapper;
    }

    [HttpPost]
    public async Task<IActionResult> AddProduct(ProductCreateDto productToAdd)
    {
        try
        {
            var product = _mapper.Map<Product>(productToAdd);
            await _productService.AddProductAsync(product);
            return CreatedAtAction(nameof(AddProduct), product);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateProduct(int id, [FromBody] ProductUpdateDto productToUpdate)
    {
        try
        {
            if (id != productToUpdate.Id)
            {
                return BadRequest("Product ID mismatch");
            }
            var existingProduct = await _productService.GetProductByIdAsync(id);
            if (existingProduct == null)
            {
                return NotFound("Product not found");
            }
            var product = _mapper.Map<Product>(productToUpdate);
            await _productService.UpdateProductAsync(product);
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProduct(int id)
    {
        try
        {
            var product = await _productService.GetProductByIdAsync(id);
            if (product == null)
            {
                return NotFound("Product not found");
            }
            await _productService.DeleteProductAsync(product);
            return NoContent();
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

    [HttpGet("{id}")]
    public async Task<IActionResult> GetProduct(int id)
    {
        try
        {
            var product = await _productService.GetProductByIdAsync(id);
            if (product == null)
            {
                return NotFound("Product not found");
            }
            var productToReturn = _mapper.Map<ProductDisplayDto>(product);
            return Ok(productToReturn);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

    [HttpGet]
    public async Task<IActionResult> GetProducts(string sTerm = "")
    {
        try
        {
            var products = await _productService.GetAllProductsAsync(sTerm);
            var productsToReturn = products.Select(p => new ProductDisplayDto
            {
                Id = p.Id,
                ProductName = p.ProductName,
                CategoryId = p.CategoryId,
                CategoryName = p.Category.Name
            });
            return Ok(productsToReturn);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

}
```

### Summary

However, Unit of work pattern reduce redundancy but it also add some complexity to it. I am not going to give any opinion about it, you can find lots of opinions in the links below.

**💻 Source code:** [https://github.com/rd003/DotnetUowDemo](https://github.com/rd003/DotnetUowDemo)

---

### Useful references and opinions about Unit Of Work

Repository pattern and unit of work is very debatable topic. Lots of people loves it and lots of people hates it also. Now, wo know how unit of work work so these reference might help you. Here are some references you can check out.

[**Is Unit Of Work and Repository Patterns very useful for big projects?**  
I'm starting a new web project using ASP.NET Webforms + EF4. I'm trying to apply a repository pattern with a unit of…](https://stackoverflow.com/questions/7940854/is-unit-of-work-and-repository-patterns-very-useful-for-big-projects "https://stackoverflow.com/questions/7940854/is-unit-of-work-and-repository-patterns-very-useful-for-big-projects")

---

[Canonical link](https://medium.com/@ravindradevrani/unit-of-work-with-generic-repository-in-net-with-ef-core-ab9fff917c70)
