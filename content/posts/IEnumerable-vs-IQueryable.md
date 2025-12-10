+++
date = '2025-05-13T11:45:17+05:30'
draft = false
title = 'IEnumerable Vs IQueryable In C#'
tags= ["dotnet","csharp"]
categories = ["programming"]
image = '/images/ienumerable-vs-queryable.webp'
+++

<!-- ![IEnumerable-vs-IQuerable](/images/ienumerable-vs-queryable.webp) -->

There has been a discussion around town about the difference between an `IEnumerable` and an `IQueryable`, especially in c# interviews. I won't be diving into the fact that `IEnumerable` is part of the `System.Collections` namespace and `IQueryable` belongs to `System.Linq` namespace (or did I???). Rather, I’ll focus on the practical usage of both—how they work, and when to use each.

## IQueryable

```cs
 public IActionResult GetPeople()
 {
  // It will retrieve 2 records from database 
  IQueryable<Person> people = _context.People.Take(2); 
  //  Note: At the above line, no data will be retrieved from the database

  return Ok(people); // Data will be retrieved here
 }
```

### Corresponding sql

Note that, I am using `Sqlite`, the above code is translated to this query:

```sql
 SELECT "p"."Id", "p"."FirstName", "p"."LastName"
      FROM "People" AS "p"
      LIMIT @__p_0
```

As we can see, our query is retrieving 2 records from the database.

`IQueryable` follows the `deferred approach`. To understand this, let's take a look at the  example below:

```cs
public IActionResult GetPeople()
{
    IQueryable<Person> people = _context.People.Take(2);
    return Ok();
}
```

In the above code, **no data will be retrieved from the database**. Yes, that is absolutely right, there won't be any database call. Because it has just created a query expression but has not executed it.

### It won't be executed until you ___

1. Use the `ToList()`

```cs
public IActionResult GetPeople()
{
    var people = _context.People.Take(2).ToList(); // Query will be executed immediately
    return Ok();
}
```

2. Loop over it

```cs
IQueryable<Person> people = _context.People.Take(2);

foreach(var person in people) // Query will be executed at this line
{
    Console.WriteLine($"{person.FirstName} {person.LastName}");
}
```

3. Return it to the client

```cs
public IActionResult GetPeople()
{
    IQueryable<Person> people = _context.People.Take(2);
    return Ok(people);
}
```

As we can see, data won't be retrieved until it is used. It is called deferred execution.

### Real world use case of `IQueryable`

`IQueryable` is very useful when we are building queries. Eg. you are applying filter, sorting and pagination :

```cs
IQueryable<Product> query = _context.Products;

// Optional category filter
if (!string.IsNullOrWhiteSpace(category))
{
    query = query.Where(p => p.Category == category);
}

// other stuff like sorting and pagination
   
// we are building a query through each step and it will be executed all at once in the end.
  
return query;
```

You can check the full example [here](https://github.com/rd003/WebApiFSP/blob/master/WepApiFSP.Data/Repositories/BookRepository.cs).

## IEnumerable

```cs
 var people = _context.People.ToList().Take(2); // query will be executed immediately
```

When you call `.ToList()`, you are executing the query immediately and all the data will be loaded into memory. Then it will take 2 records from the memory (not from the database). 

### Corresponding sql

```sql
 SELECT "p"."Id", "p"."FirstName", "p"."LastName"
      FROM "People" AS "p"
```

As you can see, it is loading all the data from the database, putting it in memory, then it is taking 2 records from the memory.


## Key points

- `IEnumerable` is used to work with `in-memory collections`. It's best suited for small collections or scenarios where data is already loaded into memory.

- `IQueryable` is used to build and execute database queries (or other remote data sources). It allows query translation (e.g., to SQL) and defers execution until the query is enumerated.