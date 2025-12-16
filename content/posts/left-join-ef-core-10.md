+++
date = '2025-12-16T9:40:05+05:30'
draft = false
title = 'LeftJoin and RightJoin in  Ef Core 10'
tags = ['dotnet','ef-core']
categories = ['programming']
image = '/images/left-join-ef-10.webp'
+++

Previously there was no simple solution for left or right join. We had to use `DefaultIfEmpty` or `GroupJoin` and `SelectMany`.

With `DefaultIfEmpty()`:

```cs
var customerOrders = await (
    from c in ctx.Customers
    join o in ctx.Orders on c.CustomerId equals o.CustomerId into orders
    from o in orders.DefaultIfEmpty()
    select new {
        c.CustomerId,
        c.CustomerName,
        OrderId = o == null ? 0 : o.OrderId
    }
).ToListAsync();
```

I have used the way described above in most of my career. It was really hard to remember that syntax and I always struggled with that. 

There is also `GroupJoin` and `SelectMany`:

```cs
var customerOrders = await ctx.Customers
    .GroupJoin(
        ctx.Orders,
        c => c.CustomerId,
        o => o.CustomerId,
        (c, orders) => new { Customer = c, Orders = orders }
    )
    .SelectMany(
        x => x.Orders.DefaultIfEmpty(),
        (x, o) => new {
            x.Customer.CustomerId,
            x.Customer.CustomerName,
            OrderId = o == null ? 0 : o.OrderId
        }
    )
    .ToListAsync();
```

Microsoft has introduced `LeftJoin` and `RightJoin` with `EF Core 10`. Which feels more intuitive syntax.

```cs
 var customerOrders = await ctx.Customers.LeftJoin(
      ctx.Orders,
      c=>c.CustomerId,
      o=>o.CustomerId,
      (c, o) => new {
          c.CustomerId,
          c.CustomerName,
          OrderId= o == null ? 0: o.OrderId,
      }
     ).ToListAsync();
```

Which will be translated as:

```bash
SELECT "c"."CustomerId", "c"."CustomerName", CASE
    WHEN "o"."OrderId" IS NULL THEN 0
    ELSE "o"."OrderId"
END AS "OrderId"
FROM "Customers" AS "c"
LEFT JOIN "Orders" AS "o" ON "c"."CustomerId" = "o"."CustomerId"
```
Note that, you can also use `RightJoin()`.