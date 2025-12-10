+++
date = '2025-02-26T07:29:14+05:30'
draft = false
title = 'Dotnet Service Lifetime : AddTransient(), AddScoped(), AddSingleton()'
tags = ['dotnet']
categories = ['programming']
image = '/images/transient.png'
+++

<!-- ![AddTransient() AddScoped() AddSingleton() in dotnet core](/images/transient.png) -->

## Example Setup

I am using a `MinimalApi` application. Create a new one if you need.

```bash
dotnet new webapi -n DITest
```

Open it in a IDE or editor of your choice.

```cs
public interface IMyService
{
    Guid InstanceId { get; }
}

public class MyService : IMyService
{
    public Guid InstanceId { get; }

    public MyService()
    {
        InstanceId = Guid.NewGuid();
        // We are logging in the constructor, so that we get notified whenever the instance is created
        Console.WriteLine($"==> Service created with InstanceId: {InstanceId}");
    }
}
```

`IMyService` have a read-only property named `InstanceId` of type `Guid`, which is set from the constructor.
We are logging inside the constructor, so that we can get notified whenever the new instance is created.

## Creating a middleware

We are creating a middleware, where we request for the instance of the serive and log the instance id to the console.

```cs
app.Use(async (context, next) =>
{
    var scopedService = context.RequestServices.GetRequiredService<IMyService>();
    Console.WriteLine($"Middleware - InstanceId: {scopedService.InstanceId}");
    await next(context);
});
```

## Create an endpoint

```cs
app.MapGet("/test", (IMyService service1,IServiceProvider serviceProvider) =>
{
    var service2 = serviceProvider.GetRequiredService<IMyService>();
    Console.WriteLine($"At endpoint-  InstanceId1:{service1.InstanceId}");
    Console.WriteLine($"At endpoint-  InstanceId2:{service2.InstanceId}");

    return Results.Ok(new
    {
        InstanceId1 = service1.InstanceId,
        InstanceId2= service2.InstanceId
    });
});
```

## 📢 At how many places we are requesting for the instance of IMyService?

At 3 places.

- Once at middleware
- Twice at `/test` endpoint

## AddTransient

Let's register our service as transient.

```cs
builder.Services.AddTransient<IMyService, MyService>();
```

Let's run the application and hit the endpoint `{baseUrl}/test`.

Open the console and you will notice these logs:

```bash
==> Service created with InstanceId: 486bc64a-b0d4-4216-9b36-3ca97b7fa5cd
Middleware - InstanceId: 486bc64a-b0d4-4216-9b36-3ca97b7fa5cd
==> Service created with InstanceId: 93021022-6d9f-4243-867b-454d09825dcf
==> Service created with InstanceId: 8ea09c7f-955c-44c3-b684-4cc14ac873ca
At endpoint-  InstanceId1:93021022-6d9f-4243-867b-454d09825dcf
At endpoint-  InstanceId2:8ea09c7f-955c-44c3-b684-4cc14ac873ca
```

Each time we are requesting for the service, we are getting a new instance. Exactly 3 instances in one http request : 1 for the middleware and 2 for the endpoints.

## AddScoped

```cs
builder.Services.AddScoped<IMyService, MyService>();
```

Let's run the application and hit the endpoint `{baseUrl}/test`.

```bash
==> Service created with InstanceId: 58f6af3f-cdd7-44be-bb11-65653d958848
Middleware - InstanceId: 58f6af3f-cdd7-44be-bb11-65653d958848
At endpoint-  InstanceId1:58f6af3f-cdd7-44be-bb11-65653d958848
At endpoint-  InstanceId2:58f6af3f-cdd7-44be-bb11-65653d958848
```

Let's hit the endpoint `{baseUrl}/test` one more time.

```bash
## this log is from the previous request
==> Service created with InstanceId: 58f6af3f-cdd7-44be-bb11-65653d958848
Middleware - InstanceId: 58f6af3f-cdd7-44be-bb11-65653d958848
At endpoint-  InstanceId1:58f6af3f-cdd7-44be-bb11-65653d958848
At endpoint-  InstanceId2:58f6af3f-cdd7-44be-bb11-65653d958848

## this log is from the current request
==> Service created with InstanceId: 1d53377b-2ac0-4388-84bf-8adaf0bf9db1
Middleware - InstanceId: 1d53377b-2ac0-4388-84bf-8adaf0bf9db1
At endpoint-  InstanceId1:1d53377b-2ac0-4388-84bf-8adaf0bf9db1
At endpoint-  InstanceId2:1d53377b-2ac0-4388-84bf-8adaf0bf9db1
```

As you have noticed, the instance of `IMyService` is created once per http request and reused.

📢 When using entity framework core, `AddDbContext` registers `DbContext` type with scoped lifetime by default.

## AddSingleton

```cs
builder.Services.AddSingleton<IMyService, MyService>();
```

Let's run the application and hit the endpoint `{baseUrl}/test`.

```bash
==> Service created with InstanceId: 7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
Middleware - InstanceId: 7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId1:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId2:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
```

Let's hit the endpoint `{baseUrl}/test` one more time.

```bash
## req 1
==> Service created with InstanceId: 7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
Middleware - InstanceId: 7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId1:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId2:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
## req 1
Middleware - InstanceId: 7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId1:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
At endpoint-  InstanceId2:7d80f0bb-110c-4bc4-ac72-4f6f0f7ee2fd
```

As you have noticed, instance of the `IMyService` is created once and shared with subsequent requests.

## Summary

- **AddTransient**: Instance is created each time when the service is requested.

- **AddScoped** : Instance is created once per scope (or http request) and shared across the scope. In the case of web apis, scope is equivalent to http request.

- **AddSingleton** : Instance is created once per application lifetime and shared across the application lifetime.
