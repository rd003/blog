+++
date = '2025-05-27T12:49:04+05:30'
draft = false
title = 'Dotnet: All you need to know about middlewares'
categories= ['programming']
tags = ['dotnet']
+++

![Middlewares in .net core](/images/middleware-thumnail.webp)

- In dotnet, a `Middleware` is a piece of code that runs in the request pipeline. 
- Middlewares are put together in a sequence, and their order matters. 
- When a request is made, it goes through each of the middleware. 
- Response flow back in reverse order through the middleware. 
- Each middleware has capability to modify the request or short circuits the pipeline.
- Each middleware can change the response before it's sent to the client.

![middleware pipeline in .net core](/images/middleware-in-dotnet.webp)

## Built-in middlewares

Here are some of the built-in middlewares.

- **UseHttpsRedirection():** Redirects http requests to https.
- **UseHsts():** Add http strict Transport security headers.
- **UseCors():** Enable cross origin request
- UseAuthorization(), UseAuthentication(), UseRouting(), MapControllers(), MapEndpoints().
- Etc etc..

## Configuring middleware

They are configured in the `Program.cs` using the `WebApplicationBuilder`.

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// Order matters!
app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

[💻 Source Code](https://github.com/rd003/DotnetPracticeDemos/tree/master/MiddlewareDemo)

---

## Creating a custom middleware

There are three ways to create the custom middlewares:

### 1. Inline middleware

```cs
app.Use(async (context, next) =>
{
    Console.WriteLine("Before next middleware");

    await next();

    Console.WriteLine("After next middleware");
});
```

**Note:** Middleware do not run until you make any http request. 

Let's add an endpoint.

```cs
var builder = WebApplication.CreateBuilder(args);

var app = builder.Build();

// endpoint
app.Map("/", () =>
{
    return "Hello";
});

app.Use(async (context, next) =>
{
    Console.WriteLine("Before next middleware");
    // do something before next middleware

    await next();

    // do something after the next middleware
    Console.WriteLine("After next middleware");
});
```

If you run the application and call the endpoint `http://localhost:5000`. You will get `Hello` as the response. If you open your console, you will notice these logs.

```bash
Before next middleware
After next middleware
```

### 2. Conventional middlewares

```cs
namespace MiddleWareDemo;

public class RequestLoggingMiddleWare
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleWare> _logger;

    public RequestLoggingMiddleWare(RequestDelegate next, ILogger<RequestLoggingMiddleWare> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context)
    {
        _logger.LogInformation($"Request {context.Request.Method} {context.Request.Path}");

        await _next(context);

        _logger.LogInformation($"Response: {context.Response.StatusCode}");
    }

}
```

In `Program.cs`

```cs
app.UseMiddleware<RequestLoggingMiddleWare>();
```

#### Key points to consider about conventional middleware

- It is registered as [singleton](https://ravindradevrani.com/posts/dotnet-service-lifetime/), when application runs for the first time.
- You can inject [transient](https://ravindradevrani.com/posts/dotnet-service-lifetime/) services to the middleware constructor, but **can not inject the [scoped](https://ravindradevrani.com/posts/dotnet-service-lifetime/) services** in it. e.g:

```cs {hl_lines=[2,10,12,17]}
// Program.cs
builder.Services.AddScoped<ISomeService, SomeService>();  // Scoped service

// Middleware

public class RequestLoggingMiddleWare
{
    private readonly RequestDelegate _next;
    private readonly ILogger<RequestLoggingMiddleWare> _logger;
    private readonly ISomeService _someService;

    public RequestLoggingMiddleWare(RequestDelegate next, ILogger<RequestLoggingMiddleWare> logger, ISomeService someService)
    {
        _next = next;
        _logger = logger;
        _logger.LogInformation("=====> Conventional middleware instantiated");
        _someService = someService;
    }

    // rest of the code
}
```
This application will throw an error  `System.InvalidOperationException: Cannot resolve scoped service 'MiddleWareDemo.ISomeService' from root provider.`


### 3. Factory-Based middlewares

- For this we need to implement `IMiddleware` interface. 
- It has only one method `InvokeAsync()` (as of .NET 9.0).
- Major benefit for me is, it is a strongly typed middleware. I don't need to remember the name of method (i.e InvokeAsync), that leads to less error prone code.
- It is `activated per http request` which allows us to inject scoped services in the middleware.

Example:

```cs
public class FactoryBasedMiddleware : IMiddleware
{
    private readonly ILogger<FactoryBasedMiddleware> _logger;
    public FactoryBasedMiddleware(ILogger<FactoryBasedMiddleware> logger)
    {
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext context, RequestDelegate next)
    {
        _logger.LogInformation("Before request");

        await next(context);

        _logger.LogInformation("After request");
    }
}
```

In `Program.cs`

```cs
builder.Services.AddTransient<FactoryBasedMiddleware>();

app.UseMiddleware<FactoryBasedMiddleware>();
```

📢 Note that, unlike the conventional middleware, you need to register it as a `transient` or `scoped` lifetime.

#### Key points to consider about factory based middlewares

- The factory-based middleware is registered as [scoped or transient](https://ravindradevrani.com/posts/dotnet-service-lifetime/) service (unlike conventional middleware, which registered as [singleton](https://ravindradevrani.com/posts/dotnet-service-lifetime/)).

- Which means factory-based middleware will be activated per http request.

- You can inject transient and scoped services to it (Unlike conventional middleware, which do not allow scoped service injection)

---

## Terminal middleware

All of the above middlewares are non-terminal middlewares. They are chained together. They pass context to the next middleware in the sequence.

Terminal middleware is the final middleware of the pipeline. It is responsible for sending response back to client.

```cs
var app = builder.Build();

app.Map("/", () =>
{
    return "Hello";
});

app.Run(async context =>
{
    await context.Response.WriteAsync("Hello from terminal middleware!");
    // This ends the pipeline
});

app.Run();
```

If we run `localhost:5000`, the page will display `Hello from terminal middleware!`. It will override the response `Hello`.

---

[💻 Source Code](https://github.com/rd003/DotnetPracticeDemos/tree/master/MiddlewareDemo)
