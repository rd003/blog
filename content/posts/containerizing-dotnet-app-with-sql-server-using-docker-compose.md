+++
date = '2025-11-20T13:57:05+05:30'
draft = false
title = 'Containerizing Dotnet App With Sql Server Using Docker Compose'
tags = ['dotnet','docker']
categories = ['programming']
+++

![running dotnet core app in docker with postgres](/images/1_EkIFSmrwAnxQ7EF8BCtQuA.png)

In this tutorial, we are going to containerize the .NET Web API application with docker. I am assuming you are familiar with docker. At least, you should have some understandings of how docker works. However, I have covered all the steps needed to create a docker container for your application, but I am not going to cover the [theoretical concepts](https://en.wikipedia.org/wiki/Docker_%28software%29) of docker.

## Last updated on:

- 20-November-2025

### 🔨Tools needed

- Visual Studio Code (Free)
- .Net 10.0 SDK (Free)
- Docker desktop (Free)

### 🧑‍💻Tech used

- .Net 10.0 Web APIs (controller APIs)
- Ms SQL Server 2025 (within a container)
- Docker compose

**🍵Note:** I am using windows 11 operating system. However, I also have tested it in the Linux mint xia and it is working fine.

### Why to chose docker compose?

General workflow of creating images and container **without docker compose**:

![Without docker compose](/images/1_6-UxPoNDg8CaCrzcmX9KFA.png)

You have to create and run containers separately, which involves typing all the commands manually in the terminal or bash each time.

### With docker compose

![with docker compose](/images/1_a5ctJIb01ezA3dFn-ivMFQ.png)

All the steps to build the images and create the containers are defined in a a single file called `compose.yaml` . You just need to fire a single command to create and run multiple containers.

### Let’s start with pulling the Github repo

To save time, I have already created the .net application and you can pull the [Github repo](https://github.com/rd003/DotnetDockerDemo) to get the application.

```sh
git clone https://github.com/rd003/DotnetDockerDemo.git
```

Open this application in the visual studio code and follow the steps.

### Creating a Dockerfile

First and foremost, create a file named **‘Dockerfile’** in the root directory. Make sure, **Dockerfile** does not have any extension.

![docker file](/images/1_mbkxHtBmAEpcR6C2jB4_Iw.jpg)

Add the following content in the docker file.

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /source

# copy csproj and restore as distinct layers
COPY \*.sln .
COPY DotnetDockerDemo.Api/\*.csproj ./DotnetDockerDemo.Api/
RUN dotnet restore

# copy everything else and build app
COPY DotnetDockerDemo.Api/. ./DotnetDockerDemo.Api/
WORKDIR /source/DotnetDockerDemo.Api
RUN dotnet publish -c release -o /app

# final stage/image
FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS final
WORKDIR /app
COPY --from=build /app ./

ENTRYPOINT ["dotnet", "DotnetDockerDemo.Api.dll"]
```

This `Dockerfile` contains the instruction to create a docker image of our .net application. It is needed to build a .net application image, which will run in a container.

### Creating a compose.yaml file

Next, create a file name `compose.yaml` in the root directory and paste the following content there.

```yaml
services:
  server:
    container_name: people-apis
    build: .
    image: people-api:1.0.0
    ports:
      - 8080:8080
    environment:
      - ASPNETCORE_ENVIRONMENT=Production
      - ASPNETCORE_URLS=http://+:8080
      - ConnectionStrings__default=Server=db,1433;Database=DotnetDockerDemo;User Id=sa;Password=p@55w0rd;TrustServerCertificate=True
    depends_on:
      db:
        condition: service_healthy
  db:
    image: "mcr.microsoft.com/mssql/server:2025-latest"
    container_name: sql_server
    ports:
      - 1433:1433
    environment:
      - ACCEPT_EULA=y
      - MSSQL_SA_PASSWORD=p@55w0rd
    volumes:
      - sql-server-data:/var/opt/mssql
    healthcheck:
      test: [ "CMD", "/opt/mssql-tools18/bin/sqlcmd", "-S", "localhost", "-U", "sa", "-P", "p@55w0rd", "-C", "-Q", "SELECT 1" ]
      interval: 10s
      timeout: 5s
      retries: 10
      start_period: 30s

volumes:
  sql-server-data:
    name: sql-data
```

In this file, we have defined two services.

1. **server:** It builds a docker image of .net application named `people-api:1.0.0`  and create a container for it, which will listen on the port `8080`.
2. **db:** It pulls the `sql server` image from the `docker hub`, create the container for it which will listen in the port `1433`. The image will be pulled only once; if you already have a sql server image with similar tag, it won’t be pull again.

Let's discuss few more things.

- `db` service performs health check. It ensures that the sql server is spun up and running.
- Before running the server, we make sure that sql server is up and running.
- `server` service depends on `db` and wait to finish the `db`. `db` must be in healthy condition. 
- In `server` section, we also haved defined `environments`. In this way, we can override the `appsettings.json`. 
- I also have created a `volume` in sql server section.

```yml
volumes:
  sql-server-data:
  name: sql-data
```

I have create a volume named `sql-server-data` and using this volume as follow

```yml
volumes:
  - sql-server-data: /var/opt/mssql
```

This line mounts `sql-server-data` volume to the path `/var/opt/mssql` . **By creating volumes our data persists outside the container.** If we remove the container or recreate it, our data (database, tables, procedures…everything) will persist.

**Note:** The `dockerfile` and `compose.yaml` file is created at November,20,2025. The content present in **dockerfile** and **compose file** is valid as of now, but may not be valid if you are reading this blog post in distant future.

#### Run docker compose

We need to run the following command

```sh
docker compose up -d
```

`-d` flag indicates that container is running in the `detached mode`. This command will execute the `compose.yaml` file and create the container for the .net application and sql server.

As a result of the command, you should see something like this in your terminal.

![docker running](/images/1_8Wn4flup_4Up_uuL9D9mNg.jpg)

To verify if container is running or not, run the following command:

```sh
docker ps -a
```

As a result, you should see something like this in your terminal.

![docker ps -a](/images/1_di8iOe5GQWulFFmFkyUXNg.jpg)

However, you can also verify it in the docker desktop.

![docker desktop](/images/1_QKWWk-zKboLOGpqSKOS2hQ.jpg)

### Testing the application

To test the application, open a web browser and type the url [http://localhost:8080/weatherforecast](http://localhost:8080/weatherforecast). As a result, you should see the following response in the browser.

![response1](/images/1_qKVhg2cNtjj26USci_lXeg.png)

This indicates that our application is working perfectly.

### Testing the endpoints using sql server

Type the url [http://localhost:8080/api/people/](http://localhost:8080/api/people/) in the browser and as a result you receives the person array.

## Removing composed containers

```bash
docker compose down
```

Then also remove the people api image and related volume for proper cleanup. 

## 💻 Code with Dockerfile and compose.yaml

I have created a separate branch which contains the dockerfile and `compose.yaml` file. To get the source code with these file, you need to checkout the branch container .

**Url:** https://github.com/rd003/DotnetDockerDemo/tree/container

To get this branch along in your cloned project, you need to run `git checkout container`.
---

Originally published by me at [medium.com](https://medium.com/@ravindradevrani/containerize-your-net-application-with-sql-server-using-docker-compose-d04b0c4ff4d1)
