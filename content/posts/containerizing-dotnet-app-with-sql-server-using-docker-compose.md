+++
date = '2025-02-23T13:57:05+05:30'
draft = true
title = 'Containerizing Dotnet App With Sql Server Using Docker Compose'
tags = ['dotnet','docker']
categories = ['programming']
+++

![running dotnet core app in docker with postgres](/images/1_EkIFSmrwAnxQ7EF8BCtQuA.png)

In this tutorial, we are going to containerize the .NET Web API application with docker. I am assuming you are familiar with docker. At least, you should have some understandings of how docker works. However, I have covered all the steps needed to create a docker container for your application, but I am not going to cover the [theoretical concepts](https://en.wikipedia.org/wiki/Docker_%28software%29) of docker.

### 🔨Tools needed

- Visual Studio Code (Free)
- .Net 8.0 SDK (Free)
- Docker desktop (Free)

### 🧑‍💻Tech used

- .Net 8.0 Web APIs (controller APIs)
- Ms SQL Server (within a container)
- Docker compose

**🍵Note:** I am using windows 11 operating system.

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
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
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
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
COPY --from=build /app ./

ENTRYPOINT ["dotnet", "DotnetDockerDemo.Api.dll"]
```

This **Dockerfile** contains the instruction to create a docker image of our .net application. It is needed to build a .net application image, which will run in a container.

### Creating a compose.yaml file

Next, create a file name `compose.yaml` in the root directory and paste the following content there.

```yaml
services:
 server:
 container_name: people-apis
 build: .
 ports:
  - 8080:8080
 depends_on:
  - "sql"
 sql:
 image: "mcr.microsoft.com/mssql/server:2022-latest"
 container_name: sql_server
 ports:
  - 1433:1433
 environment:
  - ACCEPT_EULA=y
  - MSSQL_SA_PASSWORD=myStrong(!)Password
 volumes:
  - sql-server-data:/var/opt/mssql

volumes:
 sql-server-data:
 name: sql-data
```

In this file, we have defined two services.

- First, it will build a docker image of .net application and create a container for it, which will listen on the port 8080
- Second, it will pull the sql server image from the docker hub, create the container for it which will listen in the port 1433. The image will be pulled only once; if you already have a sql server image, it won’t be pull again.

I have created volume in sql server section.

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

**Note:** The `dockerfile` and `compose.yaml` file is created at August,2024. The content present in **dockerfile** and **compose file** is valid as of now, but may not be valid if you are reading this blog post in distant future.

#### Open the appsettings.json

```json
"ConnectionStrings": {
 "default": "Server=192.168.x.x,1433;Database=DotnetDockerDemo;User Id=sa;Password=myStrong(!)Password;encrypt=false"
 }
```

You may have noticed, I have defined **‘server ’** as **‘192.168.x.x,1433’.** Here’s what it means:

- **192.168.x.x** represents the IP address of your host machine (the machine you are currently using)
- **1433** is the **port of sql server** which is running in a container. We have defined this port in the`compose.yaml` file.

To proceed, follow these steps:

- Open the **terminal** and run the command `ipconfig`
- Copy the **IPv4** address, which would be something like **192.168.x.x**
- Replace the `Server=192.168.x.x,1433` with `Server=your_ip_address,1433`

#### Run docker compose

We need to run the following command

```sh
docker compose up -d
```

`-d` flag indicates that container is running in the detached mode. This command will execute the `compose.yaml` file and create the container for the .net application and sql server.

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

To test the application, open a web browser and type the url `[http://localhost:8080/weatherforecast](http://localhost:8080/weatherforecast)`. As a result, you should see the following response in the browser.

![response1](https://cdn-images-1.medium.com/max/800/1*qKVhg2cNtjj26USci_lXeg.png)

This indicates that our application is working perfectly.

### Testing the endpoints using sql server

Type the url `[http://localhost:8080/api/people/](http://localhost:8080/api/people/)` in the browser and as a result you might receive the person array or **an error** (as I am currently getting).

Internal server error: An exception has been raised that is likely  
due to a transient failure. Consider enabling transient error resiliency  
by adding 'EnableRetryOnFailure' to the 'UseSqlServer' call.

If you encounter this error, which means we are trying to access a database that does not exist yet. I have defined a database initializer functionality in the `Program.cs` file, which creates the database and adds some data to the `Person` table when the application runs for the first time. Ideally, this should have worked automatically when we served the URL `http://localhost:8080` for the first time. However, it did not happen in my case, possibly due to a permission-related issue in Docker. I couldn’t find the actual reason. If you face the same problem, you can follow these steps:

1\. Open the integrated terminal of visual studio code.

2\. Change the directory location to **DotnetDockerDemo.Api**

cd DotnetDockerDemo.Api

3\. Run the following command.

dotnet run

As a result, you will see something like this in the terminal.

![](https://cdn-images-1.medium.com/max/800/1*-rmky9CEjrN91w0K9VL-JA.jpeg)

My application is running at `[http://localhost:5241](http://localhost:5241/api/people)` , and yours might be too, but confirm it first.

3\. Enter the url `[http://localhost:5241/api/people](http://localhost:5241/api/people)` in the browser and you will see an array of person as a response.

#### What was actually happened, when we ran the application locally?

As I have mentioned earlier, I have defined a **database initializer** functionality in the`Program.cs` file, which will create a database and add some data to the **Person** table when we ran the application for the first time.

### What next ?

Now, our application is ready to serve. Open the web browser and enter the url `[http://localhost:8080/api/people](http://localhost:8080/api/people/)` . As a resuld, you should see the follwoing response.

![response 3](https://cdn-images-1.medium.com/max/800/1*bGmP05GR4SecF12R1ttX-w.png)

response of the endpoint `[http://localhost:8080/api/people](http://localhost:8080/api/people/)`

By using docker compose, we have easily containerized our dotnet application with SQL Server.

### 💻 Code with Dockerfile and compose.yaml

I have created a separate branch which contains the **dockerfile** and **compose.yaml** file. To get the source code with these file, you need to checkout the branch `container` .

**Url:** [https://github.com/rd003/DotnetDockerDemo/tree/container](https://github.com/rd003/DotnetDockerDemo/tree/container)

---

Please consider to clap and share if this post helped you.

### Connect with me

👉 [YouTube](https://youtube.com/@ravindradevrani)  
👉 [Twitter](https://twitter.com/ravi_devrani)  
👉 [GitHub](https://github.com/rd003)

[**Become a supporter**](https://www.buymeacoffee.com/ravindradevrani) **🍵**

By [Ravindra Devrani](https://medium.com/@ravindradevrani) on [August 19, 2024](https://medium.com/p/d04b0c4ff4d1).

[Canonical link](https://medium.com/@ravindradevrani/containerize-your-net-application-with-sql-server-using-docker-compose-d04b0c4ff4d1)

Exported from [Medium](https://medium.com) on February 19, 2025.
