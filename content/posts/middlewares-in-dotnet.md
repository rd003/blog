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

## Updated at

- 25-june-2025
- 26-june-2025
- 01-July-2025

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
  Console.WriteLine("This is middleware");
  await next(context);
});
```

**Note:** Middleware do not run until you make any `http` request. 

Let's add an endpoint.

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

// endpoint
app.MapGet("/", () =>
{
    return "Hello";
});

app.Use(async (context, next) =>
{
    Console.WriteLine("This is middleware");
    await next(context);
});

app.Run();
```

If you run the application and call the endpoint `http://localhost:5000`. You will get `Hello` as the response. If you open your console, you will notice these logs.

```bash
This is middleware
```

Before moving to 2nd and 3rd way to create a middleware, let’s explore more about middlewares.

## Exploring more about middlewares

Let’s explore some more things about middlewares what we have discussed in the beginning.

```cs
app.Use(async (context, next) =>
{
    Console.WriteLine("===> Middleware 1 before next() (during req)");
    await next(context);
    Console.WriteLine("===> Middleware 1 after next() (during response)");
});

app.Use(async (context, next) =>
{
    Console.WriteLine("===> Middleware 2 before next() (during req)");
    await next(context);
    Console.WriteLine("===> Middleware 2 after next() (during response)");
});
```

Terminal logs:

```bash
===> Middleware 1 before next() (during req)
===> Middleware 2 before next() (during req)
===> Middleware 2 after next() (during response)
===> Middleware 1 after next() (during response)
```

So what does this show us?

- Code block before `next()` is executed while request.
- Code block after `next()` is executed while response.
- Response flow back in reverse order, as we have discussed in the beginning of the blog post.

#### Modifying request and response

We can modify the request and response in the middleware. In this example, we are adding a custom request header (X-Custom-Req) and a custom response header (X-Custom-Response) and also appending some text in the response.

```cs
app.Use(async (context, next) =>
{
    // adding a request header
    context.Request.Headers.Append("X-Custom-Req", "Custom Req");

    // adding a response header
    context.Response.Headers.Append("X-Custom-Response", "Custom Response");

    // Request Headers
    Console.WriteLine("\nREQUEST HEADERS:");
    foreach (var header in context.Request.Headers.OrderBy(h => h.Key))
    {
        Console.WriteLine($"  {header.Key}: {string.Join(", ", header.Value.ToArray())}");
    }

    context.Response.ContentType = "text/plain";

    await next(context);

    // Response Headers
    Console.WriteLine("\nRESPONSE HEADERS:");
    foreach (var header in context.Response.Headers.OrderBy(h => h.Key))
    {
        Console.WriteLine($"  {header.Key}: {string.Join(", ", header.Value.ToArray())}");
    }
    Console.WriteLine("=" + new string('=', 50));

    await context.Response.WriteAsync("\nAppended in middleware 1...\n");
});

app.Use(async (context, next) =>
{
    await next(context);

    await context.Response.WriteAsync("\nAppended in middleware 2");
});
```

Request endpoint:

```cs
app.MapGet("/greetings", () =>
{
    return "Hello world";
});
```

Response:

```bash
HTTP/1.1 200 OK
Connection: close
Content-Type: text/plain
Date: Wed, 25 Jun 2025 16:51:51 GMT
Server: Kestrel
Transfer-Encoding: chunked
X-Custom-Response: Custom Response

Hello world
Appended in middleware 2
Appended in middleware 1...
```

Logs in terminal:

```bash
REQUEST HEADERS:
  Accept-Encoding: gzip, deflate
  Connection: close
  Host: localhost:5009
  User-Agent: vscode-restclient
  X-Custom-Req: Custom Req

RESPONSE HEADERS:
  Connection: close
  Content-Type: text/plain
  Date: Wed, 25 Jun 2025 13:51:51 GMT
  Server: Kestrel
  Transfer-Encoding: chunked
  X-Custom-Response: Custom Response
===================================================
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

## Branching the middleware pipeline

There might be a situation, when you want to execute separate middleware pipeline on certain paths or on certain scenarios.

### Map

`Map` branches on the basis of request path.

In the example below, if the request starts with `/admin` , certain middlewares will be executed.

```cs
app.Map("/admin", HandleMapAdmin);

app.Run();

void HandleMapAdmin(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        Console.WriteLine("===> Middleware for admin");
        await next(context);
    });

    app.Run(async context =>
    {
        await context.Response.WriteAsync("Response from admin branch");
    });
}
```

If you make a request` http://localhost:5285/`

```bash
~$ curl http://localhost:5285/

===> main pipeline
```

If requests are like `/admin` or `/admin/blah` (it should starts with `/admin`), you will the similar response (`Response from admin branch`).

```bash
~$ curl http://localhost:5285/admin
Response from admin branch


~$ curl http://localhost:5285/admin/blah
Response from admin branch
```

Map can not join the main pipeline.

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Map("/admin", HandleMapAdmin);

app.Run(async context =>
{
    await context.Response.WriteAsync("===> main pipeline");
});

app.Run();

void HandleMapAdmin(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        Console.WriteLine("===> Middleware for admin");
        await next(context);
    });
}
```

Curl req:

```bash
~$ curl http://localhost:5285/admin -v
* Host localhost:5285 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:5285...
* Connected to localhost (::1) port 5285
* using HTTP/1.x
> GET /admin HTTP/1.1
> Host: localhost:5285
> User-Agent: curl/8.12.1
> Accept: */*
>
< HTTP/1.1 404 Not Found
< Content-Length: 0
< Date: Thu, 26 Jun 2025 15:32:53 GMT
< Server: Kestrel
<
* Connection #0 to host localhost left intact
```

If it has joined the main branch it would have gave the response `===> main pipeline` instead of `404 not found` status.

### MapWhen

Branches the request pipeline based on the result of the given predicate.

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapWhen(context => context.Request.Query.ContainsKey("page"),
    Handle);

app.Run(async context =>
{
    await context.Response.WriteAsync("===> main pipeline");
});

app.Run();

void Handle(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        var page = context.Request.Query["page"];
        Console.WriteLine($"===> Page = {page}");
        await next(context);
    });

    app.Run(async context =>
    {
        await context.Response.WriteAsync("Response from branch");
    });
}
```

Request 1:

```bash
~$ curl http://localhost:5285/
===> main pipeline
```

Request 2:

```bash
curl http://localhost:5285/something?page=22
Response from branch
```

It went to the different branch of pipeline when it gets the query parameter page.

**Note:** MapWhen can not rejoin the main pipeline.

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapWhen(context => context.Request.Query.ContainsKey("page"),
    Handle);

app.Run(async context =>
{
    await context.Response.WriteAsync("===> main pipeline");
});

app.Run();

void Handle(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        var page = context.Request.Query["page"];
        Console.WriteLine($"===> Page = {page}");
        await next(context);
    });
}
```

Note that, there is not any terminal middleware in Handle method, request flow must go the next middleware. We are assuming that it will go the next middleware defined in the main pipeline. Would it?? Theoretically yes… So let’s find out.

```bash
~$ curl http://localhost:5285/something?page=22 -v

* Host localhost:5285 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:5285...
* Connected to localhost (::1) port 5285
* using HTTP/1.x
> GET /something?page=22 HTTP/1.1
> Host: localhost:5285
> User-Agent: curl/8.12.1
> Accept: */*
>
< HTTP/1.1 404 Not Found
< Content-Length: 0
< Date: Thu, 26 Jun 2025 15:34:04 GMT
< Server: Kestrel
<
* Connection #0 to host localhost left intact
```

As you can see we are getting `404 not found`, but we should get `200 OK` status code and `===> main pipeline` as a response body.

That’s clearly indicates that, `MapWhen` don’t re-join the main pipeline.

### UseWhen

Let’s replace MapWhen withUseWhen .

```cs
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseWhen(context => context.Request.Query.ContainsKey("page"),
    Handle);

app.Run(async context =>
{
    await context.Response.WriteAsync("===> main pipeline");
});

app.Run();

void Handle(IApplicationBuilder app)
{
    app.Use(async (context, next) =>
    {
        var page = context.Request.Query["page"];
        Console.WriteLine($"===> Page = {page}");
        await next(context);
    });
}
```

Let’s make a curl request

```bash
~$ curl http://localhost:5285/something?page=22
===> main pipeline
```

It clearly indicates that `UseWhen` can re-join the main pipeline unless you have use terminal middleware in the branch pipeline.
---

[💻 Source Code](https://github.com/rd003/DotnetPracticeDemos/tree/master/MiddlewareDemo)
