+++
date = '2025-02-24T13:28:51+05:30'
draft = false
title = 'Creating and Installing Dotnet CLI Tool'
tags = ["dotnet",]
category = ["programming"]
+++

In this tutorial we are going to learn:

- How to create a cli tool?
- How to create a nuget package?
- How to install it in our machine.

CLI tools are very useful, they are very easy to use. We are already using it in our every day.

```sh
dotnet new console -o CliToolDemo
```

It is the example of dotnet cli tool, simple way to create a .net console application. You can also create your own cli tools. We are going to use a package created by Microsoft named `System.CommandLine` , which is a pre-released version as of I am writing this blog post. It is a pre-released version for so long, I wonder what are the plans about this package. You can also use a library named [Cocona](https://github.com/mayuki/Cocona) to create cli tools, which is pretty simple and widely popular. But I am going to stick with `System.CommandLine` . You should definitely checkout the cocona.

### Tools and Tech Used

- .Net 9 SDK
- Visual Studio Code with `C# Dev Kit` extension

### Create a new project

Open the command prompt/terminal/powershell or whatever you prefer to use and run the following command.

```sh
dotnet new console -o CliToolDemo
```

At this point, our console application type project has been created. After this command, follow the command given below.

```sh
cd CliToolDemo
```

Now we need to install a nuget package.

```sh
dotnet add package System.CommandLine --prerelease
```

As of 24 feb 2024, the package `System.CommandLine` is in pre-release version. Follow the next command, that will open the project in the vs code.

```sh
code .
```

### Creating a simple CLI tool

Open the **Program.cs** file and replace the code with the code demonstrated below.

using System.CommandLine;

```cs
var nameOption = new Option<string>("--name", description: "Your name");
var ageOption = new Option<string>("--age", description: "Your age");

var rootCommand = new RootCommand("My Simple cli tool")
{
 nameOption,
 ageOption
};

rootCommand.SetHandler((name, age) =>
{
 Console.WriteLine($"Hello {name}, you are {age} years old!");
}, nameOption, ageOption); // how to set second argument
return await rootCommand.InvokeAsync(args);
```

Let’s break it down.

```cs
var nameOption = new Option<string>("--name", description: "Your name");
var ageOption = new Option<string>("--age", description: "Your age");
```

The `nameOption` and `ageOption` will be set through the cli. We basically need to pass the arguments `--name` and `--age` from the cli.

```cs
var rootCommand = new RootCommand("My Simple cli tool")
{
 nameOption,
 ageOption
};
```

We are setting the options in this line.

```cs
rootCommand.SetHandler((name, age) =>
{
 Console.WriteLine($"Hello {name}, you are {age} years old!");
}, nameOption, ageOption); // how to set second argument
```

When root command is invoked , the message will be printed in the console. It is the place where we handle the logic part. Our logic is pretty simple, we are taking two arguments **name** and **age** from the console and printing them in the console in a specific format.

### Running the application

```sh
dotnet run -- --name John --age 20
```

### Making it a nuget package

Open the `**.csproj**` file and add these inside the `PropertyGroup`, at the very end.

```xml
<PackAsTool>true</PackAsTool>
<ToolCommandName>mycli</ToolCommandName>
<PackageOutputPath>./nupkg</PackageOutputPath>
```

- `ToolCommandName` determines the name of the tool. When you use the tool you need to use the name `mycli` .
- `PackageOutputPath` deterimes the path , where nuget package file is created. It will be created at the folder named `nupkg`

How it looks like after the change.

```xml
<PropertyGroup>
    <OutputType>Exe</OutputType>
    <TargetFramework>net9.0</TargetFramework>
    <ImplicitUsings>enable</ImplicitUsings>
    <Nullable>enable</Nullable>

    <!-- Add these lines for global tool support -->
    <PackAsTool>true</PackAsTool>
    <ToolCommandName>mycli</ToolCommandName>
    <PackageOutputPath>./nupkg</PackageOutputPath>
</PropertyGroup>
```

Now we need to create a nuget package with the following command.

```sh
dotnet pack
```

Once this command is finished, a nuget package named `CliToolDemo.1.0.0.nupkg` will be created in the folder named `nupkg`

### Installing the cli tool globally

```sh
dotnet tool install --global --add-source ./nupkg CliToolDemo
```

### Using the tool

You can use this tool from any location, because it is installed globally.

```sh
mycli --name john --age 20
```

### Uninstalling the tool

```sh
dotnet tool uninstall -g CliToolDemo
```

### References

- [Tutorial: Create a .NET tool using the .NET CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools-how-to-create)
- [Tutorial: Install and use a .NET global tool using the .NET CLI](https://learn.microsoft.com/en-us/dotnet/core/tools/global-tools-how-to-use)
- [Tutorial: Get started with System.CommandLine](https://learn.microsoft.com/en-us/dotnet/standard/commandline/get-started-tutorial)

---

[Canonical link](https://medium.com/@ravindradevrani/creating-and-installing-a-cli-tool-with-net-ba06295b2a5e)
