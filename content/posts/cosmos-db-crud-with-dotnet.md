+++
date = '2025-09-07T21:37:42+05:30'
draft = false
title = 'Cosmos DB For NoSQL - CRUD With Dotnet'
tags= ["dotnet","azure"]
categories = ["programming","cloud"]
+++

![Cosmos DB for NoSQL](/images/cosmos/cosmos_db_for_no_sql.png)

`Azure Cosmos DB for NoSQL` is a fully managed and serverless `NoSQL` and `vector database` for modern app development, including AI applications and agents. With its SLA-backed speed and availability as well as instant dynamic scalability, it is ideal for real-time NoSQL applications that require high performance and distributed computing over massive volumes of NoSQL and vector data. 

**Soruce:** learn.microsoft.com, you can learn more about it from [here](https://learn.microsoft.com/en-us/azure/cosmos-db/nosql/overview)

"OpenAI relies on Cosmos DB to dynamically scale their ChatGPT service – one of the fastest-growing consumer apps ever – enabling high reliability and low maintenance." – Satya Nadella, Microsoft chairman and chief executive officer  [Source: learn.microsoft.com](https://learn.microsoft.com/en-us/azure/cosmos-db/introduction)

Let's do some real work. Most of you are not here to learn the theorotical aspects. Right? Off course.. So.. Create an azure account first, If you haven't created. You can create a trial account with some credit for 30 days. After that let's create an cosmos db resource.

## Lets create cosmos db resource in azure

I am creating this resource for the demo, I am trying to save every penny here. You need to change the options if you are looking for a scalable production database.

First and foremost, log-in to the `Azure portal`. Go to the `Databases` section and select `Azure Cosmos DB`

![cosmos db crud with dotnet core](/images/cosmos/cosmos_1.png) 

In the next step, you will notice a lot of options, we need to select `Azure Cosmos DB for NoSql`.

![cosmos db tutorial](/images/cosmos/cosmos_2.png)  

![cosmos db](/images/cosmos/cosmos_3.1.png)

Note that, you need to select a `resource group` if it is not already created. I have created a resource group named `rg_CosmosDemo`. You can easily cleanup the resource in this way. When you are done playing with cosmos db, just delete the resource group named `rg_CosmosDemo` and it will remove the `CosmosDb` resource along with it.

![cosmos db 3.2](/images/cosmos/cosmos_3.2.png)  

**📢 Note:** I am selecting the option `serverless` for the sake of the demo. It is a very cheap option while you are learning.

![cosmos_3.3](/images/cosmos/cosmos_3.3.png) 

Click on the `Create` button and the cosomos db resource will be created soon, you have to wait a bit.

After that, go to that resource and let's check the security of the resource.

## Securing cosmos db account

Only give public access to yourself (i.e public ip address of your manchine) 

![cosmos_security](/images/cosmos/cosmos_security.png)


Now we will create a database after this.

### Create a database

![cosmos_db](/images/cosmos/cosmos_db.png)  

![cosmos_db.2](/images/cosmos/cosmos_db.2.png)  

### Create a container

Think container as a `table` in the terminology of `sql` - and `collection` in the terminology of` mongo db`.

![cosmos_container](/images/cosmos/cosmos_container.png) 

- **Database id:** database name which we have created earlier.

- **Container id:** name of container

- **Partition key:** It creates a logical partition in our container. Let's say you have a key name `Country` in the `people` container. If we make `Country` as a partition key, then all the records will be logically partitioned by the `Country`. It helps to retrieve data faster, you just have to look up in the specifict partition. Right now we are making a field `id` as a partition key. It will evenly distribute data in each partition. Note that I have provided a value `\id`, which is correct, we need to prepend `\`.

Do not select `Add hierarchical key`. 

After that, just create the container.

### Let's make a query to the container.

![cosmos_query](/images/cosmos/cosmos_query.png) 

---

# CosmosDb CRUD with dotnet

Source code : https://github.com/rd003/DotnetPracticeDemos/tree/master/AzureDemos/CosmosDemo

## Creating a new project

Execute these commands in a sequence (one-by-one)

```sh
# Create a solution
 dotnet new sln -o CosmosDemo

# Change director
 cd CosmosDemo

# Create new blank .net project
 dotnet new web -n CosmosDemo.Api

# add project to solution
 dotnet sln add CosmosDemo.Api/CosmosDemo.Api.csproj

# open project in vs code
 code . 
```

## Nuget packages

```bash
 dotnet add package Microsoft.Azure.Cosmos
```

## Let's find the connection string

![cosmos_constr](/images/cosmos/cosmos_constr.png) 

Copy the `Primary Connection String`'s value.

## appsettings.json

```json
"CosmosDb": {
    "ConnectionString": "",
    "Database": "PersonDb"
  }
```

Do not expose `ConnectionString` string to any one. In dev environment we must put it in a `secrets-manager`, which is stored in our machine, not in a project. In production, you need to put that `ConnectionString` in the `environment variable` of the `AppService` (where your project is deployed).

Let's save our `ConnectionString` in the the `secrets-manager`.

```sh
# Visit to a project directory
cd CosmosDemo.Api

# Initialize
dotnet user-secrets init
```

You will notice a line in `CosmosDemo.Api.csproj`:

```xml
 <UserSecretsId>c2bfad31-ffe4-41a9-88e0-715fba6a41bd</UserSecretsId>
```

Add a secret:

```sh
dotnet user-secrets set "CosmosDb:ConnectionString" "<your-connection-string>"
```

Path of a secret 
 
   - Windows: `%APPDATA%\Microsoft\UserSecrets\<user_secrets_id>\secrets.json`
   - Linux/Mac: `~/.microsoft/usersecrets/<user_secrets_id>/secrets.json`
   
**📢 Note:** Get user_secret_id from  `CosmosDemo.Api.csproj` (<UserSecretsId>c2bfad31-ffe4-41a9-88e0-715fba6a41bd</UserSecretsId>)


## Model

For the sake of demo, I have created `Person` class in the `Program.cs`

```cs
// Program.cs

public class Person
{
    [JsonProperty(PropertyName = "id")]
    public string Id { get; set; } = Guid.NewGuid().ToString();
    public string FirstName { get; set; } = null!;
    public string LastName { get; set; } = null!;
}
```

We need to store `id` in lowercase, so we need to decorate it with `JsonProperty`

## Create a method in Program.cs

Make sure to include these two namespaces.

```cs
using Microsoft.Azure.Cosmos;
using Newtonsoft.Json;
```

Method to get container:

```cs
// Program.cs

static Container GetContainer(IConfiguration config)
{
    string connectionString = config["CosmosDb:ConnectionString"] ?? throw new ConfigurationErrorsException("CosmosDb:ConnectionString");

    var client = new CosmosClient(connectionString);

    string databaseName = config["CosmosDb:Database"] ?? throw new ConfigurationErrorsException("CosmosDb:Database");

    var database = client.GetDatabase(databaseName);

    var contaier = database.GetContainer("people");

    return contaier;
}
```

We need to get a container in every single endpoint, that is why I am creating this method.

## Endpoints

All the endpoints are defined in `Program.cs`. Which is not a best practice, but it is a demo so I am doing it.

### POST

```cs
app.MapPost("/api/people", async (IConfiguration config, Person person) =>
{
    var container = GetContainer(config);

    ItemResponse<Person> response = await container.CreateItemAsync(item: person, partitionKey: new PartitionKey(person.Id));

    Console.WriteLine($"====> RU {response.RequestCharge}");

    return Results.Ok(person);
});
```

**📢 Note:** This line `Console.WriteLine($"====> RU {response.RequestCharge}");` is used for checking the value of `RU`. In this way you can figure out how costly our call is and optimize it if needed.

### PUT 

```cs
app.MapPut("/api/people", async (IConfiguration config, Person person) =>
{
    var container = GetContainer(config);

    ItemResponse<Person> response = await container.ReplaceItemAsync(person, person.Id, partitionKey: new PartitionKey(person.Id));

    Console.WriteLine($"====> RU {response.RequestCharge}");

    return Results.Ok(person);
});
```

### GET ALL 

```cs
app.MapGet("/api/people", async (IConfiguration config) =>
{
    var container = GetContainer(config);
    var iterator = container.GetItemQueryIterator<Person>();
    var people = new List<Person>();

    while (iterator.HasMoreResults)
    {
        var response = await iterator.ReadNextAsync();
        Console.WriteLine($"====> RU {response.RequestCharge}");
        people.AddRange(response);
    }
    return Results.Ok(people);
});
```

### Filter the records 

Let's say we want to retrieve records where `FirstName` is "John".

```cs
app.MapGet("/api/people", async (IConfiguration config, string firstName) =>
{
    var container = GetContainer(config);

    string query = "SELECT * FROM people p WHERE p.FirstName = @firstName";
    var queryDefinition = new QueryDefinition(query)
  .WithParameter("@firstName", firstName);

    var iterator = container.GetItemQueryIterator<Person>(queryDefinition: queryDefinition);
    var people = new List<Person>();

    while (iterator.HasMoreResults)
    {
        var response = await iterator.ReadNextAsync();
        Console.WriteLine($"====> RU {response.RequestCharge}");
        people.AddRange(response);
    }
    return Results.Ok(people);
});
```

### Get by id 

```cs
app.MapGet("/api/people/{id}", async (IConfiguration config, string id) =>
{
    var container = GetContainer(config);

    ItemResponse<Person> response = await container.ReadItemAsync<Person>(id: id, partitionKey: new PartitionKey(id));
    Console.WriteLine($"====> RU {response.RequestCharge}");

    return Results.Ok(response.Resource);
});
```

### Delete

```cs
app.MapDelete("/api/people/{id}", async (IConfiguration config, string id) =>
{
    var container = GetContainer(config);

    ItemResponse<Person> response = await container.DeleteItemAsync<Person>(id: id, partitionKey: new PartitionKey(id));

    Console.WriteLine($"====> RU {response.RequestCharge}");

    return Results.NoContent();
});
```