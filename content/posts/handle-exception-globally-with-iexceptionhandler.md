+++
date = '2025-02-23T18:16:31+05:30'
draft = false
title = 'Handle Exceptions Globally in .NET Core With IExceptionHandler And IProblemDetailService'
tags = ['dotnet']
categories = ['programming']
+++

![Handle exceptions globally in .net](/images/1_vTmRaWCG2u3tyUqkbhl_KA.png)

**Problem details** is a standard way to communicate error details in **HttpResponse,** defined in [rfc 7807](https://datatracker.ietf.org/doc/html/rfc7807). Standard **ProblemDetails** Properties:

- `Type`: URI identifying problem type
- `Title`: Short error description
- `Status`: HTTP status code
- `Detail`: Specific error explanation
- `Instance`: URI identifying specific error occurrence

Problem details is automatically integrated with .net core APIs. When we return the **BadRequest** we generally get response with problem details.

```cs
// controller method
return BadRequest();

// response

{
 "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
 "title": "Bad Request",
 "status": 400,
 "traceId": "00-2d4948694b0f223f7f5dff215b42481b-0288bb95d7604783-00"
}
```

The same thing happens when we return the **NotFoundException.**

```cs
// controller method
return NotFound();
```

```json
// response
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.5",
  "title": "Not Found",
  "status": 404,
  "traceId": "00-665f3aa493eea5f307292a5862fca17e-790e01fa0f9386df-00"
}
```

In the same way we get the validation error message.

```json
{
  "type": "https://tools.ietf.org/html/rfc9110#section-15.5.1",
  "title": "One or more validation errors occurred.",
  "status": 400,
  "errors": {
    "Name": ["The Name field is required."]
  },
  "traceId": "00-75969d38c366a25c50297e96ec3bc265-231440661829261c-00"
}
```

Let’s see if we want to pass some message along with the **NotFound()**.

```cs
// controller method
return NotFound("Person not found");

// response : Person not found
```

In the response, we just get the 404 status code, and string as a content, that we have passed in the **NotFound()** method. Now we are not getting response in the problem details format.

We can use the **Problem()** method to solve this problem, where we can customize the problem details.

```cs
// request
return Problem(
type: "Not found exception",
title: "An error is occured",
detail: "User does not found",
statusCode: 404);
```

response

```json
{
  "type": "Not found exception",
  "title": "An error is occured",
  "status": 404,
  "detail": "User does not found",
  "traceId": "00-1999d07fdaddf513f0cc4ea9244a4cd2-beb18ed447ecdb65-00"
}
```

You can add more details into the problem detail response. For that you need to add this configuration in the **Program** class.

```cs
// Program.cs

builder.Services.AddProblemDetails(options =>
{
 options.CustomizeProblemDetails = context =>
 {
    context.ProblemDetails.Instance = $"{context.HttpContext.Request.Method} {context.HttpContext.Request.Path}";
    context.ProblemDetails.Extensions.TryAdd("requestId", context.HttpContext.TraceIdentifier);

    var activity = context.HttpContext.Features.Get<IHttpActivityFeature>()?.Activity;
    context.ProblemDetails.Extensions.TryAdd("traceId", activity.Id);
    };
});
```

Now our response will look like this.

```json
{
  "type": "Not found exception",
  "title": "An error is occured",
  "status": 400,
  "detail": "User does not found",
  "instance": "GET /api/greetings",
  "traceId": "00-0b258efbf453b2ab17ae347f28200faf-9f2c4c1177edb3ae-00",
  "requestId": "0HN8AV48Q51I4:00000001"
}
```

---

### Handling the Exceptions globally

We can catch all the exceptions in the single place with the help of exception handler middleware.

We need the custom exception class to handle the bad request and the not found exceptions. Create the classes named **BadRequestException** and **NotFoundException**.

```cs
// BadRequestException.cs
public class BadRequestException : Exception
{
 public BadRequestException(string message):base(message)
 {
 }
}

// NotFoundException.cs
public class NotFoundException : Exception
{
    public NotFoundException(string message) : base(message)
    {
    }
}
```

Create a new class named **CustomExceptionHandler.**

```cs
public class CustomExceptionHandler: IExceptionHandler
{
    public async ValueTask<bool> TryHandleAsync(HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
    {
    }
}
```

IExceptionHandler implements the **TryHandleAsync()** method where we handle all the exceptions.

We will catch and log the exceptions in this class. So we need to inject **ILogger** in the class. We alson need to inject the **IProblemDetailsService,** so that we can return response in the problem details format**.**

```cs
public class CustomExceptionHandler: IExceptionHandler
{
    private readonly IProblemDetailsService _problemDetailService;
    private readonly ILogger<CustomExceptionHandler> _logger;

    public CustomExceptionHandler(IProblemDetailsService problemDetailService, ILogger<CustomExceptionHandler> logger)
    {
        _problemDetailService = problemDetailService;
        _logger = logger;
    }

    public async ValueTask<bool> TryHandleAsync(HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
    {
    }

}
```

Now we will write some code in the **TryHandleAsync** method.

```cs
public async ValueTask<bool> TryHandleAsync(HttpContext httpContext, Exception exception, CancellationToken cancellationToken)
{
    _logger.LogError(exception.Message);

    // determining status code on the basis of exception
    var (statusCode,problemDetails) = GetProblemDetailsAndStatusCode(exception);

    httpContext.Response.StatusCode = statusCode;

    return await _problemDetailService.TryWriteAsync(new ProblemDetailsContext {
     HttpContext= httpContext,
     ProblemDetails=problemDetails,
     Exception=exception
    });

}

private (int, ProblemDetails) GetProblemDetailsAndStatusCode(Exception exception)
{
    return exception switch
    {
        BadRequestException =>
        (
            StatusCodes.Status400BadRequest,
            new ProblemDetails
            {
                Status = StatusCodes.Status400BadRequest,
                Title = "Bad request",
                Detail = exception.Message,
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.1"
            }),
        NotFoundException => (
            StatusCodes.Status404NotFound,
            new ProblemDetails
            {
                Status = StatusCodes.Status404NotFound,
                Title = "Resource not found",
                Detail = exception.Message,
                Type = "https://tools.ietf.org/html/rfc7231#section-6.5.4"
            }
        ),
        _ => (
            StatusCodes.Status500InternalServerError,
            new ProblemDetails
            {
                Status = StatusCodes.Status500InternalServerError,
                Title = "Server error",
                Detail = exception.Message,
                Type = "https://tools.ietf.org/html/rfc7231#section-6.6.1"
            }
       ),
    }
}
```

Now, we need to register the exception handler middleware.

```cs
// Program.cs

builder.Services.AddExceptionHandler<CustomExceptionHandler>();

app.UseExceptionHandler();
```

The final **Program** class looks like this.

```cs
using Microsoft.AspNetCore.Http.Features;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

//  new line
builder.Services.AddProblemDetails(options =>
{
 options.CustomizeProblemDetails = context =>
 {
 context.ProblemDetails.Instance = $"{context.HttpContext.Request.Method} {context.HttpContext.Request.Path}";
 context.ProblemDetails.Extensions.TryAdd("requestId", context.HttpContext.TraceIdentifier);
 var activity = context.HttpContext.Features.Get<IHttpActivityFeature>()?.Activity;
 context.ProblemDetails.Extensions.TryAdd("traceId", activity.Id);
 };
});

// **** new line ***
builder.Services.AddExceptionHandler<CustomExceptionHandler>();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
 app.MapOpenApi();
}

// **** new line ***
app.UseExceptionHandler();

app.UseHttpsRedirection();

app.UseAuthorization();
app.MapControllers();
app.Run();
```

Let’s throw the custom exception and check the response.

```cs
// controller method
throw new NotFoundException("User does not found");
```

response

```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.4",
  "title": "Resource not found",
  "status": 404,
  "detail": "User does not found",
  "instance": "GET /api/greetings",
  "traceId": "00-f4d3214afd423ad8d13d934062b283d7-f773987abae78043-00",
  "requestId": "0HN8BHUP5M9SI:00000001"
}
```

---

[Canonical link](https://medium.com/@ravindradevrani/handle-exceptions-globally-in-net-with-iexceptionhandler-and-iproblemdetailservice-6d38882a4109)
