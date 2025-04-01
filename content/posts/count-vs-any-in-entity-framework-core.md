+++
date = '2025-04-01T11:03:07+05:30'
draft = false
title = 'EF Core under the hood: Count() vs Any()'
tags = ['dotnet']
categories=['programming']
+++

Let's say you want to execute a code block when `Book` table is not empty. In Entity Framework Core, we can achieve this in two ways (there might be others but I am unaware of them):

Option 1:

```cs
 if(context.Books.Count()>0)
 {
     // do something
 }
```

Option 2:

```cs
 if (context.Books.Any())
 {
     // do something
 }
```

**Note 📢:** I am testing these queries against a table containing 1 million rows.

Both conditions do the job. Let's check out what is going on under the hood and let's find out there equivalent sql queries.

## Equivalent sql query

### 1. context.Books.Count()

```sql
 SELECT COUNT(*)
      FROM [Book] AS [b]
```

### 2. context.Books.Any()

```sql
SELECT CASE
          WHEN EXISTS (
              SELECT 1
              FROM [Book] AS [b]) THEN CAST(1 AS bit)
          ELSE CAST(0 AS bit)
      END
```

## Let's compare both

### Execution plan

![execution plan](/images/count_any_execution_plan.webp)

Actual number of rows read : `1M` with Count() and `1` with Any().

### IO statistics

![io statistics](/images/count_any_io_70.webp)

Logical reads: `23515` with Count() and `3` with Any().

- As you have noticed, there is a noticable difference in `Count()` and `Any()`.
- `Count()` scans the whole table while `Any()` stops as soon as it finds the single matching record, because it is using the `EXISTS` operator.
- If you are checking whether a table holds any records or not `Any()` is a better choice.
