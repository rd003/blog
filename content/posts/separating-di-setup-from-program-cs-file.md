+++
date = '2025-02-22T18:18:10+05:30'
draft = false
title = 'Separating the DI Setup From Program.cs file'
tags = ['dotnet']
categories = ['programming']
+++

![Separating the DI Setup From Program.cs file](/images/1_h_LeJyZLYUaGtal9iEKFOg.png)

Let’s take a look at the **program.cs** file below.

```cs
using InventoryMgt.Api.Middlewares;
using InventoryMgt.Data.Repositories;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();
builder.Services.AddTransient<ICategoryRepository, CategoryRepository>();
builder.Services.AddTransient<IProductRepository, ProductRepository>();
builder.Services.AddTransient<IPurchaseRepository, PurchaseRepository>();
builder.Services.AddTransient<IStockRepository, StockRepository>();
builder.Services.AddTransient<ISaleRepository, SaleRepository>();
builder.Services.AddTransient<ExceptionMiddleware>();
builder.Services.AddCors(options =>
{
 options.AddDefaultPolicy(policy =>
 {
 policy.WithOrigins("*").AllowAnyHeader().AllowAnyMethod().WithExposedHeaders("X-Pagination");
 });
});
var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
 app.UseSwagger();
 app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthorization();
app.ConfigureExceptionMiddleware();
app.MapControllers();

app.Run();
```

It is a regular **program.cs** file. Since we use the dependency injection in our application, we have to register lots of service in our **program.cs** file. For example:

```cs
builder.Services.AddTransient<ICategoryRepository, CategoryRepository>();
```

If we have fewer services in our application, then putting them in a `program.cs` file is fine. However, this is not the case in larger applications. In larger applications, we have many services to register. We even have to add lots of middleware in that file. So it is good practice to create separate files for registering the services and adding the middleware. We are not creating a separate file for the middleware in this article; we will focus on the services only.

👉 Create a new Folder **_Extensions_** in the root folder. Create a new class with name **_ServiceRegistratonExtension.cs_**

```cs
// Extensions/ServiceRegistratonExtension.cs

namespace InventoryMgt.Api.Extensions;
public static class ServiceRegistratonExtension
{

}

👉 Copy all the service-related lines from the `program.cs` file and paste them into this class.

// Extensions/ServiceRegistratonExtension.cs

using InventoryMgt.Api.Middlewares;
using InventoryMgt.Data.Repositories;

namespace InventoryMgt.Api.Extensions;
public static class ServiceRegistratonExtension
{
 public static IServiceCollection RegisterServices(this IServiceCollection services)
 {
 services.AddControllers();
 services.AddEndpointsApiExplorer();
 services.AddSwaggerGen();
 services.AddTransient<ICategoryRepository, CategoryRepository>();
 services.AddTransient<IProductRepository, ProductRepository>();
 services.AddTransient<IPurchaseRepository, PurchaseRepository>();
 services.AddTransient<IStockRepository, StockRepository>();
 services.AddTransient<ISaleRepository, SaleRepository>();
 services.AddTransient<ExceptionMiddleware>();
 services.AddCors(options =>
 {
 options.AddDefaultPolicy(policy =>
 {
 policy.WithOrigins("*").AllowAnyHeader().AllowAnyMethod().WithExposedHeaders("X-Pagination");
 });
 });
 return services;
 }
}
```

👉`RegisterServices(this IServiceCollection services){...}` is an extension method that takes `IServiceCollection` as a parameter and also returns `IServiceCollection`. Inside this method, we will register all the services and return the same data that we receive from the parameters.

⚠️ **Note:** In the `program.cs` file, it was `builder.services.{service_name}`. But in this extension class, it will be `services.{service_name}`.

Now, we need to call this extension method in the `program.cs` file. Remove all the lines that starts with `builder.service` and add the line shown below.

```cs
// program.cs

//....... rest of the code

builder.Services.RegisterServices();

// ... rest of the code
```

**Note:** Make sure to add this namespace in the `program.cs` file

```cs
using InventoryMgt.Api.Extensions;
```

Now, our `program.cs` file looks like this.

```cs
// program.cs

using InventoryMgt.Api.Extensions; // This line must be included
using InventoryMgt.Api.Middlewares;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.RegisterServices(); // <--- updated line
var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
 app.UseSwagger();
 app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors();
app.UseAuthorization();
app.ConfigureExceptionMiddleware();
app.MapControllers();

app.Run();
```

Orignally posted by me : [Canonical link](https://medium.com/@ravindradevrani/separating-the-di-setup-from-program-cs-file-45fd50969e0c)
