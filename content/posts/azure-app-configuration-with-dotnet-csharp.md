+++
date = '2025-09-20T16:56:26+05:30'
draft = false
title = 'Azure App Configuration With Dotnet(C#)'
tags= ["dotnet","azure"]
categories = ["programming","cloud"]
image = '/images/appconfig/azure_app_configuration_csharp.png'
+++

<!-- ![Azure app configuration in c# dotnet](/images/appconfig/azure_app_configuration_csharp.png) -->

- Azure `App Configuration` is a fully managed service, which provides you a way to store the configurations in a centralized store. You can store configurations of multiple apps in a single place.
- It is really helpful for cloud native application (eg. Microservices), which runs on multiple virtual machines and use multiple external services.
- It allows us to store Key-value pairs, manage feature flags, and organize configurations using labels and namespaces.
- The main benefit is, it supports [dynamic refreshing](https://learn.microsoft.com/en-us/azure/azure-app-configuration/enable-dynamic-configuration-aspnet-core). Which means, you can change config values without restarting the app.
- You can also add reference of azure key vault secret here.

Let's see these things in action.

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

## Configure the app configuration in a dotnet app

### Nuget Packages

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
    ?? throw new InvalidOperationException("The connection string 'AppConfig' was not found.");

builder.Configuration.AddAzureAppConfiguration(appConfigConnectionString);
```

Now, run the application and in the browser or postman, visit the root endpoint `eg. https://localhost:7040/` and you will notice:


```js
{
  "color": "Color from app config",
  "name": "Name from appconfig",
  "message": "Hello.."
}
```

These values are loaded from `App Configuration`.

## Loading keys with prefixes

Since this can be a centralized config store, which may be shared with multiple apps. You want to name keys that make sense and you can easily identify them. Eg. `DotnetSample:Person:Name` and `DotnetSample:Color` says that these are the key of `Dotnet Sample app`. 

![import/export](/images/appconfig/KeyValueWithPrefix.png)

To retrieve this you have to change your configuration in `Program.cs`. 

 ```cs
 builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(appConfigConnectionString)
      .Select("DotnetSample:*");
});
 ```
 
In this ways you loads the configs that is only relevant to your application.

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
 
You can also modify appsettings.json, if you want to load different config in dev environment and different config in production environment. 
 
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
 
## More resources

- [Quickstart: Create an ASP.NET Core app with Azure App Configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/quickstart-aspnet-core-app?tabs=entra-id)
- [Dynamic configuration](https://learn.microsoft.com/en-us/azure/azure-app-configuration/enable-dynamic-configuration-aspnet-core)