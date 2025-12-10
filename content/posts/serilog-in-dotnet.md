+++
date = '2025-02-19T15:40:41+05:30'
title = 'Serilog in .NET'
tags= ["dotnet"]
categories = ["programming"]
canonical_url = "https://medium.com/@ravindradevrani/serilog-in-net-6-and-7-a18cdedf21b8"
image = '/images/serlilog_feature_image.webp'
+++

<!-- ![serilog-in-dotnet](/images/serlilog_feature_image.webp) -->

In your development journey you have faced so many runtime exceptions. You have handled that with try catch block. But in the runtime you never know where that error has happened and you have to
trace that whole section with putting breakpoints. Sometime you have thought that I wish.. I would get notified whenever that exception occur. Then the logging frameworks comes in the play.

Although .net core comes with its own logging mechanism but it have very limited options for logging. With 3rd party logging framework or 3rd party logging library you have multiple options, like you can log into files, console, database and so on.

## Serilog

Serilog is a logging library for .net which give us various options for logging like file, console or database. In this tutorial we will learn to log into console and file.

If you also want to see a video version of it you can check it out,
thats is short and precise.

{{< youtube id="YGv_3-nKWcw" title="Your Video Title" autoplay="false" >}}

Now lets get started ⌨️

Let use the power of dotnet cli, open your terminal/cmd and type the following command where **webapi** is a project type and **SerilogDemo** is the name of project.

![cli_command](/images/cli_command.webp)

I am using **_visual studio 2022_** in this tutorial, so go to the location where you have created this project, in my case it is _documents/projects/ytprojects._ Now open the folder "SerilogDemo". You
will have following files there

![project_structure](/images/project_structure.jpg)

Double Click on **SerilogDemo.csproj.user** file , it will open our
project on visual studio. It will look like this

![project](/images/project.jpg)

Now for logging we need some libraries, for that goto tools\>nuget package manager \> package manager console

![PMC](/images/PMC)

```bash
install-package serilog.aspnetcore
install-package Serilog.Sinks.File
install-package Serilog.Sinks.Console
```

- _Serilog.AspNetCore_ package installs the serilog library
- _Serilog.Sinks.File_ helps to log data into file
- _Serilog.Sinks.Console_ helps us to log data into Console

Now , replace the **appsettings.json** file's content with the content
below

```json
{
  "Serilog": {
    "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [{ "Name": "Console" }]
  },
  "AllowedHosts": "*"
}
```

Open **program.cs** file and write these line in the top of it 👇👇

```cs
using Serilog;
var configuration = new ConfigurationBuilder()
                      .AddJsonFile("appsettings.json")
                      .Build();
Log.Logger = new LoggerConfiguration()
    .ReadFrom.Configuration(configuration)
   .CreateLogger();

Log.Logger.Information("Logging is working fine");
```

Now you need to add one more line

```cs
builder.Host.UseSerilog();
```

You have successfully integrated basic console logging. You can check
the console window.👇👇👇

![console_logging_fine](/images/console_logging_fine)

Now we will create a controller and try to log error there. So create a new controller **PersonController.** Write these lines in the controller

```cs
namespace SerilogDemo.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class PersonController : ControllerBase
    {
        private readonly ILogger<PersonController> _logger;

        public PersonController(ILogger<PersonController> logger)
        {
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Get()
        {
            try
            {
                int a = 5;
                int c = a / 0;
                return Ok();
            }
            catch (Exception ex)
            {
                _logger.LogError(ex.Message);
                return StatusCode(500);
            }
        }
    }
}
```

Run the project and execute this api endpoint **api/person.** If you check the console window you will see these messages.

![devide_by_zero](/images/devide_by_zero)

Now we are only able to see the log message and timestamp, but we are
not able to see in which file , which method we are getting these log
messages. For that we need some more configuration. So modify "WriteTo"
key of **appsettings.json**

```json
//"WriteTo": [
     // {
       // "Name": "Console"
     // }

 "WriteTo": [
        {
          "Name": "Console"
        },
       {
          "Name": "MSSqlServer",
          "Args": {
            "connectionString": "data source=.;initial catalog=InventoryDb;integrated security=true",
            "sinkOptionsSection": {
              "tableName": "Logs",
              "schemaName": "dbo",
              "autoCreateSqlTable": true
            },
            "restrictedToMinimumLevel": "Warning"
          }
        }
      ],
```

Now we can see more information in logging like 👇👇👇

![Console_Log](/images/Console_Log)

If you need to log more information like machine name, environment, thread id ,for that we need to install enrichers. Install following packages.

```sh
Install-Package Serilog.Enrichers.Thread
Install-Package Serilog.Enrichers.Environment
Install-Package Serilog.Enrichers.Process
```

Add following lines in logger configuaration at **appsettings.json**.

```json
"Enrich": [ "WithThreadId", "WithProcessId", "WithEnvironmentName", "WithMachineName" ]
```

Now **appsetting.json** file would look like 👇👇

```json
{
  "Serilog": {
    "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact"
        }
      }
    ],
    "Enrich": [
      "WithThreadId",
      "WithProcessId",
      "WithEnvironmentName",
      "WithMachineName"
    ] // these are new lines"
  },
  "AllowedHosts": "*"
}
```

Now your logs will look like 👇👇👇👇

![logs](/images/logs)

Now we need to do one last thing. We also need file logging system in this application. So we need to add few lines in **appsettings.json** file. Add these lines there inside "WriteTo" key

```json
{
  "Name": "File",
  "Args": {
    "path": "/Logs/log.txt",
    "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact"
  }
}
```

Your final **appsettings.json** file would look like this 👇👇👇👇

```json
{
  "Serilog": {
    "Using": ["Serilog.Sinks.Console", "Serilog.Sinks.File"],
    "MinimumLevel": {
      "Default": "Information",
      "Override": {
        "Microsoft": "Warning",
        "System": "Warning"
      }
    },
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact"
        }
      },
      {
        "Name": "File",
        "Args": {
          "path": "/Logs/log.txt",
          "formatter": "Serilog.Formatting.Compact.CompactJsonFormatter, Serilog.Formatting.Compact"
        }
      }
    ],
    "Enrich": [
      "WithThreadId",
      "WithProcessId",
      "WithEnvironmentName",
      "WithMachineName"
    ] // these are new lines"
  },
  "AllowedHosts": "*"
}
```

Now it will create a **_Logs_** folder and create a **_log.txt_** file inside it. Now your log will be logged into **_console_** and **_log.tx_**t file.

📎💻Source code:
[https://github.com/rd003/SerilogDemo](https://github.com/rd003/SerilogDemo)

[Canonical
link](https://medium.com/@ravindradevrani/serilog-in-net-6-and-7-a18cdedf21b8)
