+++
date = '2025-09-20T16:56:26+05:30'
draft = true
title = 'Azure App Configuration With Dotnet(C#)'
tags= ["dotnet","azure"]
categories = ["programming","cloud"]
+++

![Azure app configuration in c# dotnet](/images/appconfig/azure_app_configuration_csharp.png)

## Dontet core web api app

- Create a new `dotnet core web api` application
- In `appsettings.js`, add following lines:

```js
"Color": "Color from appsettings",
"Person": {
  "Name": "Name from appsettings"
}
```

- In `program.cs` create an endpoint:

```cs
app.MapGet("/", (IConfiguration config) =>
{
    string color = config.GetSection("Color").Value ?? "No color";
    string name = config.GetSection("Person:Name").Value ?? "No name";
    return Results.Ok(new
    {
        color,
        name,
        message = "Hello.."
    });
});
```

- Run the application and in the browser or postman, visit the root endpoint `eg. https://localhost:7040/` you will notice:

```js
{
  "color": "Color from appsettings",
  "name": "Name from appsettings",
  "message": "Hello.."
}
```

Let's try to load these settings from azure `app configuration`.

## Create a resource `azure app configuration`

![Search app configuration](/images/appconfig/1.png)

![create app configuration](/images/appconfig/2.png)

## Adding config values

There are two ways to create it

👉1. Create manually

![manually create key value](/images/appconfig/1_manual.png)

👉2. By import/export. We are going to use this option. 

In `source file`, click on `browse` and browse the `appsettings.json`, which is located in your project.

![import/export](/images/appconfig/2_import.png)

This step will import everything from `appsettings.json`. Delete the unnecessary configs.

![import/export](/images/appconfig/2_import_delete.png)

Click on three dots '...' of each key-value and edit its values.

![import/export](/images/appconfig/2_import_edit.png)

## Configure app configuration in dotnet app

### Package

Add the following nuget package.

`Microsoft.Azure.AppConfiguration.AspNetCore`

### Connection string

```js
"ConnectionStrings": {
  "AppConfig": "<your-connection-string>"
}
```

Copy this value from here.

![import/export](/images/appconfig/connectionString.png)


### Load cofiguration

Add these lines in `Program.cs`

```cs
string appConfigConnectionString = builder.Configuration.GetConnectionString("AppConfig")
    ?? throw new InvalidOperationException("The connection string 'AppConfiguration' was not found.");

builder.Configuration.AddAzureAppConfiguration(appConfigConnectionString);
```

Now, run the application and in the browser or postman, visit the root endpoint `eg. https://localhost:7040/` you will notice:


```js
{
  "color": "Color from app config",
  "name": "Name from appconfig",
  "message": "Hello.."
}
```

## Loading keys with prefixes

Since this can be a centralized config store, which may be shared with multiple apps. You want to name keys that make sense and you can easily identify them. Eg. `DotnetSample:Person:Name` and `DotnetSample:Color` says that these are the key of `Dotnet Sample app`. To retrieve this you have to change your configuration in `Program.cs`. 

![import/export](/images/appconfig/KeyValueWithPrefix.png)


In this ways you loads the configs that is only relevant to your application.

 ```cs
 builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(appConfigConnectionString)
      .Select("DotnetSample:*");
});
 ```
 
 It will load the config keys that starts with `DotnetSample:`.
 
 Endpoint:
 
 ```cs
 app.MapGet("/", (IConfiguration config) =>
{
    string color = config.GetSection("DotnetSample:Color").Value ?? "No color";
    string name = config.GetSection("DotnetSample:Person:Name").Value ?? "No name";
    return Results.Ok(new
    {
        color,
        name,
        message = "Hello.."
    });
});
 ```
 
You can also modify appsettings.json, if you want to load different config in devenvironment and different config in production. 
 
appsettings: 
 
```cs
 "DotnetSample": {
  "Color": "Color from appsettings",
  "Person": {
    "Name": "Name from appsettings"
  }
}
```

Offcource, you also need to call `builder.Configuration.AddAzureAppConfiguration` only in production. 

```cs
if (builder.Environment.IsProduction())
{
    builder.Configuration.AddAzureAppConfiguration(options =>
    {
        options.Connect(appConfigConnectionString)
          .Select("DotnetSample:*");
    });
}
```
 
 