+++
date = '2025-02-24T18:07:04+05:30'
draft = false
title = 'SingleAsync vs SingleOrDefaultAync vs FirstAsync vs FirstOrDefaultAsync vs FindAync'
tags = ['dotnet','csharp']
categories = ['programming']
+++

![SingleAsync() vs SingleOrDefaultAync() vs FirstAsync() vs FirstOrDefaultAsync() vs FindAync() in c#](/images/1_X3XFl2jfkUpXfqbt6CtsQA.png)

I don’t think there is any need of introduction. Let’s jump to the code section. We coders understand with code more. Let’s understand the concept then you don’t need to remember any definition.

This is the recordset against which I am running queries.

| Id  | FirstName | LastName |
| --- | --------- | -------- |
| 1   | John      | Doe      |
| 2   | Ravindra  | Devrani  |
| 3   | Mohan     | Singh    |
| 20  | Mahesh    | Soni     |
| 21  | John      | Snow     |

First and foremost let’s say we need a record with LastName=”Doe”.

```cs
var person = await context.People.SingleAsync(p\=>p.LastName\=="Doe");
```

Works fine since there is only one record with LastName="Doe"

```cs
var person = await context.People.SingleAsync(p\=>p.FirstName\=="Jack");
//System.InvalidOperationException: Sequence contains no elements.
```

Since we don't have any record with FirstName = Jack. we are getting the exception.

Here `SingleOrDefault()` comes handy.

```cs
var person = await context.People.SingleOrDefaultAsync(p\=>p.FirstName\=="Jack");
```

Rather than throwing an exception, `SingleOrDefaultAsync()` assigns default value (which is null for the instance) if no record found. We have two records with first name : "John" ; John Doe and John Snow

```cs
var person = await context.People
 .SingleOrDefaultAsync(p => p.FirstName == "John");

//System.InvalidOperationException: Sequence contains more than one element.
```

In this case `FirstAsync()` will be useful. We get the first record and it will skip other records.

```cs
var person = await context.People.FirstAsync(p => p.FirstName == "John");

// John Doe
```

If we don't have any records with the filter criteria, we will get an exception.

```cs
var person = await context.People.FirstAsync(p => p.FirstName == "Jack");

//System.InvalidOperationException: Sequence contains no elements.
```

`FirstOrDefaultAsync()` will solve this problem.

```cs
var person = await context.People
 .FirstOrDefaultAsync(p => p.FirstName == "Jack");
```

### What about the Find() or FindAsync()

Let's take a look at this example:

```cs
var person = await context.People.SingleAsync(a => a.PersonId == 1);

var person2 = await context.People.SingleAsync(a => a.PersonId == 1);
```

First, it makes a database call for the instance `person` then it makes one more database call for the instance `person2`, even we are trying to get the same record.

Let's try it with `FindAsync()`:

```cs
var person = await context.People.FindAsync(1);

var person2 = await context.People.FindAsync(1);
```

It gives same result as `SingleAsync()`, but here is a catch, for the first line of code, it will make a database call (for instance 'person'). For the instance `person2`, it won't make any database call and retrieve this record from the memory. It will just make one database call.

> `Find()` or `FindAsync()` first checks the EF Core change tracker (in-memory cache) to see if this entity was already loaded. If yes then it loads it from the memory.

**Note:** `Find()` or `FindAsync()` method only works with `primary key`. In the above example, we are trying to get record with `PersonId=1` and `PersonId` is a `primary key`.

---

[Canonical link](https://medium.com/@ravindradevrani/singleasync-vs-singleordefaultaync-vs-firstasync-vs-firstordefaultasync-vs-findaync-e1d150d79e3a)
