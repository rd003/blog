+++
date = '2025-11-27T15:34:26+05:30'
draft = false
title = 'Lazy Loading and N+1 Query Problem in Entity framework Core'
tags= ["ef-core","dotnet"]
categories = ["programming"]
image = '/images/nplus1.jpg'
+++
<!-- ![n+1 query problem in entit framework core](/images/nplus1.jpg) -->

[💻Source code](https://github.com/rd003/DotnetPracticeDemos/tree/master/LazyLoadingExample) 

## Lazy loading

You load related entities on demand rather loading at once. This approach is usually useful when you want to load related entities on a certain condition (otherwise always use eager loading).

To enable lazy loading, you need to install this package: `Microsoft.EntityFrameworkCore.Proxies`

And do following changes in `Program.cs`

```cs
builder.Services.AddDbContext<AppDbContext>(o=>o.UseLazyLoadingProxies()
.UseSqlite("Data Source = mydb.db"));
```

Look at the example below:

```cs
app.MapGet("/", async (AppDbContext context) => {
    foreach (var genre in await context.Genres.ToListAsync()) 
    {
        foreach (var book in genre.Books)
        {
            Console.WriteLine($"===> genre: {genre.Name}, Book: {book.Title}, Price : {book.Author}");
        }
    }
    return Results.Ok("Ok");
});
```

We are not loading `books` with `genres` at once. Rather we are loading books for each genres. Let's take a look at `logs of console`.

```bash
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (32ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      SELECT "g"."GenreId", "g"."Name"
      FROM "Genres" AS "g"
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (9ms) [Parameters=[@p='?' (DbType = Int32)], CommandType='Text', CommandTimeout='30']
      SELECT "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Books" AS "b"
      WHERE "b"."GenreId" = @p
===> genre: Science Fiction, Book: Echoes of the Stars, Price : Lena Hart
===> genre: Science Fiction, Book: The Quantum Horizon, Price : Miles Kettering
===> genre: Science Fiction, Book: Voyagers of Andromeda, Price : Cynthia Rowe
===> genre: Science Fiction, Book: Neon Future, Price : David Kalmar
===> genre: Science Fiction, Book: Orbit of Silence, Price : R.J. Maddox
===> genre: Science Fiction, Book: Shadows on Europa, Price : Mark Feldman
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[@p='?' (DbType = Int32)], CommandType='Text', CommandTimeout='30']
      SELECT "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Books" AS "b"
      WHERE "b"."GenreId" = @p
===> genre: Fantasy, Book: The Silver Grove, Price : Alana Rivers
===> genre: Fantasy, Book: Crown of Mist, Price : Tobias Wynne
===> genre: Fantasy, Book: Dragonfire Oath, Price : Kara Blayde
===> genre: Fantasy, Book: The Shattered Kingdom, Price : Evan Marlowe
===> genre: Fantasy, Book: Runes of the Ancients, Price : Gwen Halberg
===> genre: Fantasy, Book: A Song for the Phoenix, Price : Michaela Thorn
===> genre: Fantasy, Book: The Last Enchanter, Price : R. L. Bramson
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[@p='?' (DbType = Int32)], CommandType='Text', CommandTimeout='30']
      SELECT "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Books" AS "b"
      WHERE "b"."GenreId" = @p
===> genre: Horror, Book: The Hollow Night, Price : Samuel Pike
===> genre: Horror, Book: Ashwood Asylum, Price : Marjorie Keene
===> genre: Horror, Book: Beneath the Black Lake, Price : Daniel Kress
===> genre: Horror, Book: Creepstone Manor, Price : Olivia Mercer
===> genre: Horror, Book: The Whispering Room, Price : Gareth Lowell
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[@p='?' (DbType = Int32)], CommandType='Text', CommandTimeout='30']
      SELECT "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Books" AS "b"
      WHERE "b"."GenreId" = @p
===> genre: Mystery, Book: The Vanishing Key, Price : Isabelle Crane
===> genre: Mystery, Book: Murder at Redhall Station, Price : Colin Ferris
===> genre: Mystery, Book: Secrets of Willow Lane, Price : Julia Harwood
===> genre: Mystery, Book: The Case of the Glass Dagger, Price : Victor Allard
===> genre: Mystery, Book: Silent Witnesses, Price : Dana Whitford
===> genre: Mystery, Book: Death in the Ivy House, Price : Helen Corwin
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (1ms) [Parameters=[@p='?' (DbType = Int32)], CommandType='Text', CommandTimeout='30']
      SELECT "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Books" AS "b"
      WHERE "b"."GenreId" = @p
===> genre: Historical Fiction, Book: The Emperor's Messenger, Price : Stephen Lorne
===> genre: Historical Fiction, Book: A Winter in Vienna, Price : Clara Voigt
===> genre: Historical Fiction, Book: Swords of the Republic, Price : Marcus Hawthorne
===> genre: Historical Fiction, Book: The Silk Merchant's Daughter, Price : Evelyn Marin
===> genre: Historical Fiction, Book: Under the Iron Banner, Price : Graham Kessler
===> genre: Historical Fiction, Book: The Paris Letters, Price : Marion Devereaux
```

It makes database round trip for each genre's books. 

- It is "the (in)famous" `n+1` query problem. 
- For `1` initial query (`await context.Genres.ToListAsync()`), it makes `n` additional queries.
- If you have `10 genres`. It makes `1` initial query to load all the genres and `10 queries` for each genre. Which makes it to `10+1 = 11` queries.

## How to fix this

Load early with eager loading.

```cs
var genres = await context.Genres.Include(g => g.Books).ToListAsync();
foreach (var genre in genres)
{
    foreach (var book in genre.Books) {
        Console.WriteLine($"===> genre: {genre.Name}, Book: {book.Title}, Price : {book.Author}");
    }
}
```

Console log:

```bash
info: Microsoft.EntityFrameworkCore.Database.Command[20101]
      Executed DbCommand (34ms) [Parameters=[], CommandType='Text', CommandTimeout='30']
      SELECT "g"."GenreId", "g"."Name", "b"."BookId", "b"."Author", "b"."GenreId", "b"."Title"
      FROM "Genres" AS "g"
      LEFT JOIN "Books" AS "b" ON "g"."GenreId" = "b"."GenreId"
      ORDER BY "g"."GenreId"
===> genre: Science Fiction, Book: Echoes of the Stars, Price : Lena Hart
===> genre: Science Fiction, Book: The Quantum Horizon, Price : Miles Kettering
===> genre: Science Fiction, Book: Voyagers of Andromeda, Price : Cynthia Rowe
===> genre: Science Fiction, Book: Neon Future, Price : David Kalmar
===> genre: Science Fiction, Book: Orbit of Silence, Price : R.J. Maddox
===> genre: Science Fiction, Book: Shadows on Europa, Price : Mark Feldman
===> genre: Fantasy, Book: The Silver Grove, Price : Alana Rivers
===> genre: Fantasy, Book: Crown of Mist, Price : Tobias Wynne
===> genre: Fantasy, Book: Dragonfire Oath, Price : Kara Blayde
===> genre: Fantasy, Book: The Shattered Kingdom, Price : Evan Marlowe
===> genre: Fantasy, Book: Runes of the Ancients, Price : Gwen Halberg
===> genre: Fantasy, Book: A Song for the Phoenix, Price : Michaela Thorn
===> genre: Fantasy, Book: The Last Enchanter, Price : R. L. Bramson
===> genre: Horror, Book: The Hollow Night, Price : Samuel Pike
===> genre: Horror, Book: Ashwood Asylum, Price : Marjorie Keene
===> genre: Horror, Book: Beneath the Black Lake, Price : Daniel Kress
===> genre: Horror, Book: Creepstone Manor, Price : Olivia Mercer
===> genre: Horror, Book: The Whispering Room, Price : Gareth Lowell
===> genre: Mystery, Book: The Vanishing Key, Price : Isabelle Crane
===> genre: Mystery, Book: Murder at Redhall Station, Price : Colin Ferris
===> genre: Mystery, Book: Secrets of Willow Lane, Price : Julia Harwood
===> genre: Mystery, Book: The Case of the Glass Dagger, Price : Victor Allard
===> genre: Mystery, Book: Silent Witnesses, Price : Dana Whitford
===> genre: Mystery, Book: Death in the Ivy House, Price : Helen Corwin
===> genre: Historical Fiction, Book: The Emperor's Messenger, Price : Stephen Lorne
===> genre: Historical Fiction, Book: A Winter in Vienna, Price : Clara Voigt
===> genre: Historical Fiction, Book: Swords of the Republic, Price : Marcus Hawthorne
===> genre: Historical Fiction, Book: The Silk Merchant's Daughter, Price : Evelyn Marin
===> genre: Historical Fiction, Book: Under the Iron Banner, Price : Graham Kessler
===> genre: Historical Fiction, Book: The Paris Letters, Price : Marion Devereaux
```

👉 You get all the data in one database query.