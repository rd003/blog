+++
date = '2025-02-20T17:28:02+05:30'
draft = false
title = 'Catch Exception Globally in Dotnet Core Apis'
tags = ['dotnet']
categories = ["programming"]
+++

![Catch Exception Globally in Dotnet Core Apis](https://cdn-images-1.medium.com/max/800/1*Hj2IaFBmE4fJrBN_MZ0q3Q.png)

There are to ways of catching exception in .net core, one is using try/catch and other one is catching them globally. Although there is nothing wrong with **try/catch** blog, it is an elegant way of exception handling. Although you can also catch exceptions globally, If you want to log errors in one place. There are various approaches to achieve this, but we will create the custom middleware to achieve it.

{{< youtube id="HqYUgPlGbE8" title="global exception handling" autoplay="false" >}}

Let’s get staring. Lets create a class inside the **models** folder and name it **ErrorResponse.cs.**

👉**Models/ErrorResponse.cs**

```cs
public class ErrorResponse
 {
 public int StatusCode { get; set; }
 public string? Message { get; set; }

        public override string ToString()
        {
            return JsonSerializer.Serialize(this);
        }
    }
```

We will use this class to return the error response.

Since, we don’t have inbuilt classes for **NotFoundException** or **BadRequest** exception, so we will create custom exceptions.

👉**Exceptions/NotfoundException.cs**

```cs
namespace SerilogDemo.Exceptions
{
 public class NotFoundException : Exception
 {
 public NotFoundException(string message) : base(message)
 {
 }
 }

    public class BadRequestException : Exception
    {
        public BadRequestException(string message) : base(message)
        {
        }
    }

}

```

Let’s create our custom middleware. But before that, I want to say that, I have used here serilog for logging in this project. You can read [this article](https://medium.com/@ravindradevrani/serilog-in-net-6-and-7-a18cdedf21b8) of mine, to know about serilog.

👉**Middleware/ExceptionMiddleware.cs**

```cs
using SerilogDemo.Exceptions;
using SerilogDemo.Models;
using System.Net;

namespace SerilogDemo.Middlewares
{
 public class ExceptionMiddleware : IMiddleware
 {
 private readonly ILogger<ExceptionMiddleware> \_logger;

        public ExceptionMiddleware(ILogger<ExceptionMiddleware> logger)
        {
            \_logger = logger;
        }

        public async Task InvokeAsync(HttpContext context, RequestDelegate next)
        {
            try
            {
                await next(context);
            }
            catch (Exception ex)
            {

                \_logger.LogError(ex.Message);
                await HandleException(context, ex);
            }
        }

        private static Task HandleException(HttpContext context, Exception ex)
        {
            int statusCode = StatusCodes.Status500InternalServerError;
            switch (ex)
            {
                case NotFoundException \_:
                    statusCode = StatusCodes.Status404NotFound;
                    break;
                case BadRequestException \_:
                    statusCode = StatusCodes.Status400BadRequest;
                    break;
                case DivideByZeroException \_:
                    statusCode = StatusCodes.Status400BadRequest;
                    break;
                // you can define some more exceptions, according to need
            }
            var errorResponse = new ErrorResponse
            {
                StatusCode = statusCode,
                Message = ex.Message
            };
            context.Response.ContentType = "application/json";
            context.Response.StatusCode = statusCode;
            return context.Response.WriteAsync(errorResponse.ToString());
        }
    }

    // Extension method for this middleware

    public static class ExceptionMiddlewareExtension
    {
        public static void CongigureExceptionMiddleware(this IApplicationBuilder app)
        {
            app.UseMiddleware<ExceptionMiddleware>();
        }
    }

}
```

Let’s look at the code below.

```cs
switch (ex)
 {
 case NotFoundException _:
 statusCode = StatusCodes.Status404NotFound;
 break;
 case BadRequestException _:
 statusCode = StatusCodes.Status400BadRequest;
 break;
 case DivideByZeroException _:
 statusCode = StatusCodes.Status400BadRequest;
 break;
 // you can define some more exceptions, according to need
 }

```

Here we are defining multiple cases, so that we can give different types of status code to client beside 500. In this way we have more control over reponse. If you want to catch other type of exception, just define more cases. If those exception does not exist, just create your own.

Now let’s back to the original flow of this code. We have created an exception method with name **CongigureExceptionMiddleware ,** so that we can leave our program.cs file more neat and clean.

Now register your middleware in **program.cs.**

`builder.Services.AddTransient<ExceptionMiddleware>();`

Call **ConfigureExceptionMiddleware** in middleware section of **program.cs**

```cs
app.UseHttpsRedirection();

app.UseAuthorization();
// exception middleware
app.CongigureExceptionMiddleware();

app.MapControllers();

app.Run();
```

Now lets create a controller, **PersonController**.

```cs
public class PersonController : ControllerBase
 {

        \[HttpGet("{id}")\]
        public IActionResult Get(int id)
        {
            if (id == 1)
            {
                int a = 5;
                int c = a / 0;
            }
            else if (id == 2)
            {
                throw new NotFoundException("record does not found");
            }
            else
            {
                throw new BadRequestException("Bad request");
            }

            return Ok();
        }



    }
```

👉Hit this endpoint **(/api/person/1)**

You will get **400** status code and following response.

```json
{
  "StatusCode": 400,
  "Message": "Attempted to divide by zero."
}
```

👉Hit this endpoint **(/api/person/2)**

```json
You will get **404** status code and following response.

{
 "StatusCode": 404,
 "Message": "record does not found"
}
```

👉Hit this endpoint **(/api/person/3)**

You will get **400** status code and following response.

```json
{
  "StatusCode": 400,
  "Message": "Bad request"
}
```

Here we have learn, how we can handle different type of exception with custom middleware.

📎Source code: [https://github.com/rd003/SerilogDemo/tree/GlobalErrorHandling](https://github.com/rd003/SerilogDemo/tree/GlobalErrorHandling)

---

Orignally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [March 19, 2023](https://medium.com/p/a37565a5e66c).

[Canonical link](https://medium.com/@ravindradevrani/catch-exceptions-globally-in-net-core-apis-a37565a5e66c)

Exported from [Medium](https://medium.com) on February 19, 2025.
