+++
date = '2025-02-23T15:55:14+05:30'
draft = false
title = 'Containerizing Dotnet App With PostgreSql Using Docker Compose'
tags = ['dotnet','docker']
categories = ['programming']
+++

![Containerizing A .NET App With Postgres Using Docker Compose](/images/1_L8Rtngz25d4SLhLZR7liaA.png)

In this tutorial, we are going to **containerize the .NET Web API application with docker and postgres**. I am assuming you are familiar with docker. At least, you should have some understandings of how docker works. However, I have covered all the steps needed to create a docker container for your application, but I am not going to cover the [theoretical concepts](https://en.wikipedia.org/wiki/Docker_%28software%29) of docker.

### 🔨Tools needed

- Visual Studio Code (Free)
- .Net 8.0 SDK (Free)
- Docker desktop (Free)

### 🧑‍💻Tech used

- .Net 8.0 Web APIs (controller APIs)
- Postgres (within a container)
- Docker compose

**🍵Note:** I am using windows 11 operating system.

### Why to chose docker compose?

General workflow of creating images and container **without docker compose**:

![without docker](/images/1_EtvCLfmbqtDaMG1qviQ9Rw.png)

You have to create and run containers separately, which involves typing all the commands manually in the terminal or bash each time.

### With docker compose

![using docker image](/images/1_c2bk8tqIsRXfjx9NiPEtuA.png)

All the steps to build the images and create the containers are defined in a a single file called `compose.yml` . You just need to fire a single command to create and run multiple containers.

### Let’s start with pulling the Github repo

To save time, I have already created an application. You can pull the source code from my Github repo. Execute these commands one by one

```cs
git clone https://github.com/rd003/DotnetApiPostgres.git

code DotnetApiPostgres
```

At this point, your application must have opened in the visual studio code.

### Creating a Dockerfile

First and foremost, create a file named **‘Dockerfile’** in the root directory. Make sure, **Dockerfile** does not have any extension.

![dockerfile](/images/1_jmPUFggtbIG3WyKITNx67Q.jpg)

A **dockerfile** in the root directory

Add the following content in the docker file.

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /source

# copy csproj and restore as distinct layers
COPY *.sln .
COPY DotnetApiPostgres.Api/*.csproj ./DotnetApiPostgres.Api/
RUN dotnet restore

# copy everything else and build app
COPY DotnetApiPostgres.Api/. ./DotnetApiPostgres.Api/
WORKDIR /source/DotnetApiPostgres.Api
RUN dotnet publish -c release -o /app

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app ./

ENTRYPOINT ["dotnet", "DotnetApiPostgres.Api.dll"]
```

This **Dockerfile** contains the instruction to create a docker image of our .net application. It is needed to build a .net application image, which will run in a container.

### Creating a compose.yml file

Next, create a file name `compose.yml` in the root directory and paste the following content there.

```yml
services:
 web_api:
 container_name: perons_api_app
 build: .
 ports:
  - 8080:8080
 depends_on:
  - "db"
 db:
 image: postgres
 container_name: postgres_db
 ports:
  - 5432:5432
 environment:
 POSTGRES_PASSWORD: Ravindra@123
 volumes:
  - postgres_data:/var/lib/postgresql/data

volumes:
 postgres_data:
```

In this file, we have defined two services.

- First, it will build a docker image of .net application and create a container for it, which will listen on the port 8080
- Second, it will pull the postgres image from the docker hub, create the container for it which will listen in the port 5432. The image will be pulled only once; if you already have a postgres image, it won’t be pull again.

In the service named `web_api` , I have defined a a property or key named `depends_on` with the value `db` . It means `web_api` service is depends on the service `db` . `**web_api**` will wait until `db` is up and running before starting. However, it is not necessary, because our project is not depending on the db on the startup, so use can remove this key.

You may have noticed, I have defined a `volume` with name `postgres_data` in `Volumes` section. I have linked this volume with my db service and bind the path `/var/lib/postgresql/data` to it. By doing so, our database has become persistent. If we delete the postgeress container, our database and all of its data still persists.

**Note:** The `dockerfile` and `compose.yaml` file is created at August,2024. The content present in **dockerfile** and **compose file** is valid as of now, but may not be valid if you are reading this blog post in distant future.

### Move Connectionstring

Since container runs the published version of .net applcation, so you need to define connection string in the **appsettings.json**. In this application, the connection string is defined in the **appsettings.development.json.** Remove the connection string from the **appsettings.development.json** and add the connection string to the **appsettings.json**. Connection string should look like as follows.

```cs
"ConnectionStrings": {
 "default": "Host=192.168.x.x;Port=5432;Database=PersonDb;Username=postgres;Password=Ravindra@123"
 }
```

You may have noticed, I have defined **‘Host ’** as **‘192.168.x.x’.** Here’s what it means:

- **192.168.x.x** represents the IP address of your host machine (the machine you are currently using).

To proceed, follow these steps:

- Open the **terminal** and run the command `ipconfig`
- Copy the **IPv4** address, which would be something like **192.168.x.x**
- Replace the `Host=192.168.x.x` with `Host=your_ip_address`

#### Run docker compose

We need to run the following command

docker compose up -d

`-d` flag indicates that container is running in the detached mode. This command will execute the `compose.yml` file and create the container for the .net application and postgres.

As a result of the command, you should see something like this in your terminal.

![docker comose up -d](/images/1_OwzIi18MQT0EQlI9gBSGEQ.jpg)

To verify if container is running or not, run the following command:

```sh
docker ps -a
```

As a result, you should see something like this in your terminal.

![running in container](/images/1_1Lmffd5GUG0GAaFIfeSOkA.jpg)

### Create database

To proceed further, we need to create database in the postgres db. Follow the steps one by one.

```sh
cd DotnetApiPostgres.Api

dotnet ef database update
```

`dotnet ef database update` command will generate the database in the postgres db.

### Testing the application

Our application is running at `http://localhost:8080`

To test the application open the postman and test the **POST** endpoint as shown below.

**URL**: `http://localhost:8080/api/people`

**Method**: POST

**Body**:

{  
 "name": "John Doe"  
}

![testing in postman](/images/1_kvDIybk7dsJ4I3fdZBTLUA.jpg)

In this way, by using the docker compose, we can easily containerize our applications and run multiple containers with a single command.

### 💻 Code with Dockerfile and compose.yaml

I have created a separate branch which contains the **dockerfile** and **compose.yml** file. To get the source code with these file, you need to checkout the branch `container` .

**Url:** [https://github.com/rd003/DotnetApiPostgres/tree/container](https://github.com/rd003/DotnetApiPostgres/tree/container)

---

[Canonical link](https://medium.com/@ravindradevrani/containerizing-a-net-app-with-postgres-using-docker-compose-a35167b419e7)
