+++
date = '2025-02-20T18:39:45+05:30'
draft = false
title = 'Fluent Validation in Dotnet Core'
tags = ['dotnet']
categories=['programming']
+++

![fluent validation in asp.net core](/images/1_c2gndRKm-6SwqxruBvENFQ.png)

## Fluent validation

Fluent validation is a third party library for validating your models in .NET . It is totally free.

📢 📝 Last Updated: 21-August-2024

## Why fluent validation?

If you already have used data annotation for validation, then you must be aware of validation in .NET. So you might be thinking why do we need fluent validation.

Fluent validation helps you to separate validation logic from your models. That makes you code clean. If you have complex validation logic, then you want to define it separately rather than making your model unreadable.

If you have small scale project and does not have complex validation logic, then using data annotation makes more sense.

You can use the hybrid validation, it is totally up to you and what suits you best. None of them is good or bad. It depends on your requirements.

## 💻Source Code

👉Branch : [**Fluent-Validation**](https://github.com/rd003/net9demo/tree/Fluent-Validation)

## Create a project or use existing one

We will create a .net core project with template .Net Core Web Api. If you have existing project (for practicing) , then it is good. Don’t waste your precious time on creating a new one.

![fluent_validation_project_type](/images/fluent_validation_project_type.jpg)

## Folder structure

![folder structure](/images/1_qWt0GSNpAdUpmTeK8_6VQA.jpg)

## Model

```cs
// Models/Person.cs
public class Person
{
 public int Id { get; set; }
 public string ? Name { get; set; }
 public string? Email { get; set; }
 public int Age { get; set; }
}
```

## Easiest way (Data annotation)

Data annotation is the easiest way to validate your models..Nothing is wrong with it. It is fast and well suited for small projects. You must be familiar it with. Below is the example of it.

```cs
// Models/Person.cs
public class Person
{
 public int Id { get; set; }
 [Required]
 [MaxLength(50)]
 public string ? Name { get; set; }
 [Required]
 [MaxLength(50)]
 public string? Email { get; set; }
 public int Age { get; set; }
}
```

## Fluent Validation

Fluent validation is a third party library which is free. So you need to install it first.

👉 `install-package FluentValidation.DependencyInjectionExtensions`

👉 Remove all the data annotation from Person.cs (If you are using)

```cs
// Models/Person.cs

public class Person
{
 public int Id { get; set; }
 public string ? Name { get; set; }
 public string? Email { get; set; }
 public int Age { get; set; }
}
```

## Validator

We will create a separate class **PersonValidator** inside **Validators** directory. There we will define all the validation logic.

👉 Validators/PersonValidator.cs

```cs
//Validators/PersonValidator.cs

using FluentValidation;
using net9demo.Models;

namespace net9demo.Validators;

public class PersonValidator: AbstractValidator<Person>
{
 public PersonValidator()
 {
 RuleFor(person=>person.Name).NotNull().MaximumLength(50);
 RuleFor(person=>person.Email).NotNull().MaximumLength(50);
 }
}
```

These rules are self explanatory

👉First & Second rule, **Name** and **Email** can not be null (but they can be empty string), empty and their maximum length should be 50 characters.

## Program.cs

You need some configuration in Program.cs to make validation work.

```cs
builder.Services.AddScoped<IValidator<Person\>, PersonValidator>();
```

## Adding validation errors to ModelState

Create a folder named “Extensions”, inside this folder create a class named “Extensions”.

```cs
public static void AddToModelState(this ValidationResult result, ModelStateDictionary modelState)
{
 foreach (var error in result.Errors)
 {
 modelState.AddModelError(error.PropertyName, error.ErrorMessage);
 }
}
```

`AddToModelState` method will add all errors to the ModelState.

## Person Controller

To use the validator, we have to inject the `IValidator<Person>` into `PersonController` and check the validation manually. If validation fails, we will return `UnprocessableEntity()`,which returns `422 Unprocessable Entity` status code along with validation errors.

```cs
using FluentValidation;
using Microsoft.AspNetCore.Mvc;
using net9demo.Models;
using net9demo.Repositories;
namespace net9demo.Controllers;

[Route("api/people")]
[ApiController]
public class PersonController : ControllerBase
{
 private readonly IValidator<Person> _validator;
 private readonly IPersonRepository personRepository;
 private readonly ILogger<PersonController> logger;

    public PersonController(IValidator<Person> validator, IPersonRepository personRepository, ILogger<PersonController> logger)
    {
        _validator = validator;
        this.personRepository = personRepository;
        this.logger = logger;
    }


    [HttpPost]
    public async Task<IActionResult> AddPerson(Person person )
    {
        // checking validation
        var personValidator = await _validator.ValidateAsync(person);
        if (!personValidator.IsValid)
        {
            personValidator.AddToModelState(ModelState);
            return UnprocessableEntity(ModelState);
        }

        try
        {
            return CreatedAtAction(nameof(AddPerson),person);
        }
        catch (Exception ex)
        {
            logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
        }
    }

}
```

## Test with swagger ui

![req](/images/1_aKs2sp-X1W_tQTjLXyXzXA.jpg)

request

![res](/images/1_xD_u3-WwGsK67ciRuvYTSA.jpg)

response

## **Email validator**

```cs
RuleFor(person=>person.Email).NotNull().MaximumLength(50).EmailAddress();
```

## **Regular Expression and custom message**

```cs
RuleFor(person => person.Password)
.NotEmpty()
.NotNull()
.MaximumLength(20)
.Matches("^(?=.*\\d).*$")
.WithMessage("Password must contain numeric value");
```

## Final ‘PersonValidator’ class

```cs
using FluentValidation;
using net9demo.Models;

namespace net9demo.Validators;

public class PersonValidator: AbstractValidator<Person>
{
    public PersonValidator()
    {
      RuleFor(person=>person.Name).NotEmpty().NotNull().MaximumLength(50);
      RuleFor(person=>person.Email).NotEmpty().NotNull().MaximumLength(50).EmailAddress();
      RuleFor(person => person.Age).NotNull();
      RuleFor(person => person.Password).NotEmpty().NotNull().MaximumLength(20).Matches("^(?=.*\\d).*$").WithMessage("Password must contain numeric value");
    }
}
```

## **Adding Category Validator**

Let’s create a new validator class named `CategoryValidator` inside the `Validators` folder.

```cs
public class CategoryValidator:AbstractValidator<Category>
{
 public CategoryValidator()
 {
 RuleFor(c => c.Name).NotEmpty().NotNull().MinimumLength(2).MaximumLength(20);
 }
}
```

Register it in the **Program.cs**

```cs
builder.Services.AddScoped<IValidator<Category\>, CategoryValidator\>();
```

## Register all the validator at once (test them also)

If we have n validators, we have to register then n-times. But we can register them all at one. Just add the following line in **Program.cs :**

```cs
// either comment these two lines or remove them.
//builder.Services.AddScoped<IValidator<Person>, PersonValidator>();
//builder.Services.AddScoped<IValidator<Category>, CategoryValidator>();

builder.Services.AddValidatorsFromAssemblyContaining<PersonValidator>();
```

`builder.Services.AddValidatorsFromAssemblyContaining<PersonValidator>()`

It will register all the validators in the same assembly in which `PersonValidator` is defined.

👉For more detail please visit official docs of [fluent validation](https://fluentvalidation.net/).

---

Original post by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [December 15, 2023](https://medium.com/p/c748da274204).

[Canonical link](https://medium.com/@ravindradevrani/fluent-validation-in-net-core-8-0-c748da274204)

Exported from [Medium](https://medium.com) on February 19, 2025.
