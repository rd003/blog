+++
date = '2025-03-14T19:16:37+05:30'
draft = true
title = 'Keyset Pagination In Entity Framework Core'
tags = ['dotnet']
categories = ['programming']
+++

First we need to know about the traditional offset based pagination and the problems it introduces.

### Offset pagination

In the code below we are using the offset pagination.

```cs
[HttpGet("offset")]
public async Task<IActionResult> GetBooks(int limit=10, int page=1)
{
    var books = await _context.Books
        .AsNoTracking()
        .OrderBy(a => a.Id)
        .Skip(limit * (page - 1))
        .Take(limit)
        .ToListAsync();
    return Ok(books);
}
```

Which translates to the following sql:

```sql
SELECT
   [b].[Id],
   [b].[Author],
   [b].[Country],
   [b].[ImageLink],
   [b].[Language],
   [b].[Link],
   [b].[Pages],
   [b].[Price],
   [b].[Title],
   [b].[Year]
FROM [Book] AS [b]
ORDER BY [b].[Id]
OFFSET @__p_0 ROWS
FETCH NEXT @__p_1 ROWS ONLY
```

Let's execute this endpoint.

![offset_pagination_page_1](/images/offset_pagination_page_1.jpg)

I have executed the same endpoint 3 to 4 times and it took approximately 10ms.

It great! right.

Let's go to the 1,000th page.

![offsetpage2](/images/offsetpage2.jpg)

Now it is taking 22 ms.

Let's go to the extreme and jump to the 1,000,00th page.

![offset_pagination](/images/offset_pagination.jpg)

At first, it took 618 ms. When I hit the endpoint multiple times, it is taking approximately 317 ms.

**As you have noticed, the response time is increased with page number.**

#### Why?

- For page=1, it skips 0 rows and takes 10 rows.
- For page=2, it skips 10 rows and takes next 10 rows. For skiping, it has to read 10 rows.
- For page=3, it skips 20 rows and takes next 10 rows. For skiping, it has to read 20 rows.

So whenever the page size increases, it has to read more rows.

#### It has one more problem

The problem arises when someone updates records cuncurrently.

Let's say we are taking 10 rows at a time.

- Page 1 have records (1,2,3,4,5,6,7,8,9,10)
- Page 2 have records (11,12,13,14,15,16,17,18,19,20)

You are on page 1. Someone has deleted the 10th record while you are moving to the page 2.
At this time, 11th record will shift to the page 1.

- Page 1 have records (1,2,3,4,5,6,7,8,9,11)
- Page 2 have records (12,13,14,15,16,17,18,19,20,21)

When you reach to the page 2, will find records from 12 to 21. The 11th records won't show you. So you have completely missed the 11th record.

### KeySet Pagination

Keyset pagition solves the problem we have seen earlier. It is also known as `seek based pagination`. Because we directly jump to the certain page.

```cs
[HttpGet("keyset")]
public async Task<IActionResult> GetBooksWithKeyset(int limit = 10, int lastId = 0)
{
    var books = await _context.Books
        .AsNoTracking()
        .OrderBy(b => b.Id)
        .Where(b=>b.Id>lastId)
        .Take(limit)
        .ToListAsync();
    return Ok(books);
}
```

Which translates to following sql:

```sql
SELECT
  TOP(@__p_1)
  [b].[Id],
  [b].[Author],
  [b].[Country],
  [b].[ImageLink],
  [b].[Language],
  [b].[Link],
  [b].[Pages],
  [b].[Price],
  [b].[Title],
  [b].[Year]
FROM [Book] AS [b]
WHERE [b].[Id] > @__lastId_0
ORDER BY [b].[Id]
```

![keyset_pagination](/images/keyset_pagination.jpg)

It is taking 11ms. It takes approximately same amount of time for the first 10 records and for the last 10 records.

**The only downside of this approach is, you can not jump into the particular page, you have to use the next-previous approach.**

### Summary

Always be careful when using pagination. If you don't need the ability to jump to a specific page, consider using keyset pagination instead. Even if you think you need page-jumping functionality, reconsider whether it is truly necessary for your application.
