+++
date = '2025-02-19T22:55:02+05:30'
draft = false
title = 'Create Sln File With Multiple Projects'
tags= ["dotnet"]
categories = ["programming"]
+++

![Create Sln File With Multiple Projects](/images/create_sln_with_multiple_files.png)

In this article we will learn how to create a .net core
project with a Solution (sln file) that contains multiple projects. I
know most you guys use visual studio for c# related stuff, but it would
be benificial for person who likes to switch with vs code ocassionally,
like me or who use linux and forced to use .net cli. Although if you are
a new developer and have windows operating system, I will recommend
visual studio, because it is the best possible IDE for c# development.

Our project structure will be like this.

![book_store_multiple_project_structure](/images/book_store_multiple_project_structure.png)

Book-Store-Spa-Backend is our root folder, inside it we have a **sln**
file and 3 different projects.

1. BookStore.Api (UI layer)

2. BookStore.Data (Data layer)

3. BookStore.Test (Unit Testing project)

Create a **sln** file named inside a folder **Book-Store-Spa-Backend**,
it is also our solution name.

```sh
dotnet new sln -o Book-Store-Spa-Backend
```

This command will create a folder name **'Book-Store-Spa-Backend'**,
inside that folder it will create a **sln** file with same name. We need
to create more project , in order to achieve that we need to move into
**'Book-Store-Spa-Backend'**, so in your terminal write this command.

```sh
cd Book-store-spa-backend
```

Now we are inside **"Book-store-spa-backend"** directory.

Create new a web api project. It will be our UI layer.

```sh
dotnet new webapi -o BookStore.Api
```

Let's create another project (class library), it will be our
**DataAccess** layer, where we will write our database logic.

```sh
dotnet new classlib -o BookStore.Data
```

Let's create another project (xunit project for unit testing).

```sh
dotnet new xunit -o BookStore.Test
```

Now we need to create a add these 3 projects in our solution. Write the
following command.

```sh
dotnet sln Book-Store-Spa-Backend.sln add .\BookStore.Api\ .\BookStore.Data\ .\BookStore.Test\ add .\BookStore.Api\ .\BookStore.Data\ .\BookStore.Test\
```

I know you are thinking 😖how to remember these file names .

![hand_hurt](/images/hand_hurt.png)

> Lets make it simple just type **dotnet sln
> Book-Store-Spa-Backend.sln** after that press tab button, it will
> autocomplete the name of project, if it is not the right one then
> press it again, until you find the right one. and its done.

![done](/images/done.png)

Type " cd.. " in terminal. Because we need to exit from this directory,

```sh
cd..
```

Now following command will open our project in vs code.

```sh
code  Book-Store-Spa-Backend
```

![final structure](/images/final_structure.png)

Let's make it feel more like visual studio, this step is completely
optional. Install the following vs code extension.

Last thing we need to do here, we need to add reference of
`BookStore.Data` to `BookStore.Api project`.

```sh
dotnet add .\BookStore.Api\BookStore.Api.csproj
reference
.\BookStore.Data\BookStore.Data.csprojMvcBlogDemoData\MvcBlogDemoData.csproj
```

And add reference of BookStore.Data and BookStore.Api to BookStore.Test

```sh
dotnet add .\BookStore.Test\BookStore.Test.csproj reference .\BookStore.Data\BookStore.Data.csproj
dotnet add .\BookStore.Test\BookStore.Test.csproj reference .\BookStore.API\BookStore.Api.csproj
```

[Canonical
link](https://medium.com/@ravindradevrani/create-sln-file-with-multiple-projects-in-net-core-cli-d5fd59072623)
