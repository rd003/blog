+++
date = '2025-02-20T16:20:16+05:30'
draft = false
title = 'Output Caching With Dotnet 7'
tags = ["dotnet","caching"]
category = ["programming"]
image = '/images/output-caching-dotnet7.png'
+++

<!-- ![Output Caching middleware has introduced in .net 7 , that is used to apply caching in your application. It can be used in any .net core application like Minimal API, Web API with controllers, MVC, and Razor Page. But I am using controller APIs in this project.](/images/output-caching-dotnet7.png) -->

### What is Caching?

Caching is a process of temporarily storing frequently accessed data or
resources in a faster and closer location to the user or application,
with the goal of reducing the time and resources needed to retrieve that
data from its original source. By keeping a copy of the data nearby,
caching enables quicker access and improves the overall performance and
responsiveness of applications.

👉Lets make it simple. If you understand what caching then skip the part
below.

Imagine you have a favorite book that you read often. Instead of putting
it back on the shelf after every use, you might keep it on your bedside
table for easy access. This way, when you want to read it again, you
don't need to go all the way to the bookshelf, saving you time and
effort. The bedside table acts as a "cache" for the book.

(It is just an example, I am not encouraging you to be make your room
unorganized. 😁)

In computer terms, caching works in a similar way. When you visit a
website or use an app, certain data (like images or frequently accessed
information) gets stored in a cache on your device. The next time you
visit the same website or use the app, instead of fetching everything
from the internet again, it quickly retrieves the stored data from the
cache, making the loading process faster and more efficient.

If you prefer Video tutorial, then you can check this one on the similar
topic.

{{< youtube id="nF6aFq4Gn8Y" title="Output caching in .net 7" autoplay="false" >}}

### Output Caching:

Output Caching **middleware** has introduced in **.net 7** , that is
used to enable caching in your application. It can be used in any .net
core application like Minimal API, Web API with controllers, MVC, and
Razor Page. I am using controller APIs in this project.

💻 Here is the [source
code](https://github.com/rd003/CachingAspNetCore/tree/output-cache-medium) of this article.

Add following lines in your **program.cs** file. It needs only 2 Steps
to enable output caching in .net core.

**Step 1:** Add `AddOutputCache()`{.markup--code .markup--p-code}
service.

```cs
builder.Services.AddOutputCache();
```

**Step 2:** Add`UseOutputCache()`{.markup--code .markup--p-code}
middleware.

```cs
app.UseOutputCache();
```

⚠️ **Note:**

👉 Apps that use CORS middleware, `UseOutputCache` must be used after `UseCors`

👉 In Razor Pages apps and MVC apps, `UseOutputCache` must be called after `UseRouting`.

### Add Caching Behaviour: {#7046 .graf .graf--h3 .graf-after--p name="7046"}

Add `[OutputCache]` attribute about any
controller method and that method will be cached. By default it will be
cached for 1 minute ( not 100% sure).

```cs
    [HttpGet]
    [OutputCache]
    public async Task<IActionResult> GetBooks(string? lang,string ? title)
    {
        // ........................
        //......................

    }
```

You can check this endpoint by simply adding a breakpoint in this
method. Make two consecutive requests and It won't hit twice.

**Adding Policies:**

You can add different policies for your application. For example , in
some endpoints you want to use cache for 60 seconds and in some
endpoints you want to enable cache for 30s or 10s. Then you can create
different policies for that.

Replace the **builder.Services.AddOutputCache()** with code below.

```cs
builder.Services.AddOutputCache(options=>{
  options.AddBasePolicy(builder => builder.Expire(TimeSpan.FromSeconds(60)));
  options.AddPolicy("ExpireIn30s",builder=>builder.Expire(TimeSpan.FromSeconds(30)));
});
```

`AddBasePolicy()` allows us to set default behavior or caching. Although we can create as much policy we
want with method `AddPolicy()`. For example if you want to create shorter life cache can can create a new
policy with name `ExpiresIn30s` and set
its expiry to 30 seconds (as shown above).
It was just one example, you can configure this policy with lots of
things, like vary by `query/header/value` or create a policy for `no-cache`.

**Controller:** Set **\*PolicyName="\*\***ExpiresIn15s\***_"_** property of
attribute **OutputCache**.

```cs
    [HttpGet]
    [OutputCache(PolicyName ="ExpiresIn15s")]
    public async Task<IActionResult> GetBooks(string? lang,string ? title)
    {
     ............
    }
```

👉By default output caching follows these rules:

✅ It caches **200** r**esponses only**.

✅ It caches **Head or Get requests only**.

❌ It does not cache the **responses that set cookies**.

❌ It does not cache the **responses to the authenticated requests**.

Source: [Microsoft
Docs](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output?view=aspnetcore-7.0#default-output-caching-policy).

👉We can override default policy but it is not the part of this article.

## No cache

If you don't want to enable cache in a certain method then

- [You can simply add a new policy for no cache like below:]

```cs
options.AddPolicy("NoCache", builder => builder.NoCache());
```

and use it like this

```cs
[OutputCache(PolicyName ="NoCache")]
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
   ......
}
```

- Or you can use it like this, if you are using controller
  methods.

```cs
[OutputCache(NoStore = true)]
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
   ......
}
```

---

## Cache Keys

By default whole URL is the key of the cache. But you can can explicitly
control the cache key.

### 👉Vary By Query

Suppose we have and endpoint that return unique response on the basis of
**"lang"**.

```cs
    [HttpGet]
    [OutputCache(VaryByQueryKeys = new[]{"lang"})]
    public async Task<IActionResult> GetBooks(string? lang,string ? title)
    {
    }
```

Let execute these endpoints:

1. [/api/books]
2. [/api/books?lang=french]
3. [/api/books?lang=english]
4. [/api/book/title=adventure]

First 3 endpoints will return the unique values and cache those data.
While the 4th endpoint will return data from the cache created by
endpoint 1.

Because **Each URL is treated as cache key along with its parameters**
and we have used **_vary by lang_** feature of **output cache**. So
endpoint with parameter **_lang_** will be treated as different and if
you pass parameters other than **_lang_** (eg. **_title_** in our case),
then it will be treated the same as the main endpoint (endpoint without
any paramter).

🙋‍♂️ In a nutshell \`**api/books\` == \`api/books?title=abc\`** and
\`**api/bookss?lang=yourLanguage\`** is unique.

We can also vary the cache on the basis of:

👉 **Vary By Header**

👉 **Vary By Value**

But we are not going to explain it here.

---

## Cache Revalidation

Till now what was happening

- [You have asked server, hey give me the list of Books , in return
  server returns you the list of 10 books.]{#93a3}
- [2nd time, you have requested for books, you got the list of 10
  books, but this time from the cache. But you have got all the 10
  books.]{#5b6e}
- [Same will happen for the 3rd/4th and ....nth time till the cache is
  valid, you will always get 10 books from the cache.]{#e1bc}
- [Now you have seen the problem. What if it is 100 or 1000 books. Off
  course, you are not fetching it from the database, but you are still
  fetching it from the server. It will increase the bandwidth.]{#a558}

Isn't it would be nice, instead of returning 10 books every time, server
will indicate you with some kind of message, like
`'hey! nothing is modified’`{.markup--code .markup--p-code}. Now you can
rely on the the last response (that you have saved locally), until you
got the new response (new response will be received when resource is
modified).

Lets back to the technicality. When we apply cache revalidation, server
returns `304 not modified status code`{.markup--code .markup--p-code}
instead of returning full body response. It indicates that response is
same as the previous one and you can rely on previous response.

There are several ways to achieve this but we are going to use **ETag**
for this. If the client sends an **`If-None-Match`{.markup--code
.markup--p-code}** header with the **etag** value of an earlier
response, and the cache entry is not modified, the server returns
**`304 not modified stauts code`{.markup--code .markup--p-code}**instead
of the **full response.**

```cs
    [HttpGet]
    [OutputCache(VaryByQueryKeys = new[] { "lang" })]
    public async Task<IActionResult> GetBooks(string? lang, string? title)
    {
        try
        {
            var books = await _bookRepos.GetBooks(lang, title);
            _logger.LogInformation("Retrieved books");
            // 👉 adding etag to response header
            Response.Headers.ETag = $"\"{Guid.NewGuid():n}\"";
            return Ok(books);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError, "Something went wrong");
        }

    }
```

In the above code, we have added this line.

```cs
Response.Headers.ETag = $"\"{Guid.NewGuid():n}\"";
```

We are setting **etag header** to **guid**. So when user hit this
endpoint he/she will will receive this value in the response header.

![output-caching-etag](/images/output-caching-etag.jpg)

We have to pass this **etag** value to the **If-None-Match** header in
the request.

![output-caching-dotnet-if-none-match](/images/output-caching-dotnet-if-none-match.jpg)

Now you can see that, until our cache is valid, we would get
`304 not modified`{.markup--code .markup--p-code} **status code** in the
response, not the whole body. Once your cache is invalidated, the server
will issue the response body along with new `etag`

---

## Cache Eviction

**Lets Talk with problem first:**

Lets starts it with 3 steps.

1. Hit the endpoint `api/books (get)` and it will return data and cache it in server.
   Lets suppose we have got 10 items in return.
2. Hit the endpoint `/api/books (post)` and post some data to it. Lets suppose we have
   entered 11th record in the database. Code for this method is
   below:

```cs
    //api/books
    [HttpPost]
    public async Task<IActionResult> AddBook(Book book)
    {
        try
        {
            var createdBook = await _bookRepos.AddBook(book);
            _logger.LogInformation("Books have saved");
            return CreatedAtAction(nameof(AddBook), createdBook);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError);
        }
    }
```

3.Hit the endpoint `api/books (get)` again. We are retrieving 10 items only( because we are getting result from the cached entries) while we have 11 items in the database.

Lets take an another example.

```cs

// api/books/100
[OutputCache]
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
      ....
}
```

👉 Lets suppose we have hit the endpoint
`/api/books/100 (get)`. It will return
book with id 100 and this data is saved into cache. Next time you will
get the cached entry.

👉 Suppose, we have updated the the book record with id=100.

👉 If we hit the endpoint `/api/books/100 (get)` again, and if cache is still valid, you will get the
the older data not the the updated one.

Now I hope you Got the problem 😯. Yeah right?

![that_was_a_problem_right](/images/that_was_a_problem_right.gif)

[pic: Gify.com](https://giphy.com/clips/truerealtv-rap-game-the-WOobHq01T5h1h0qymR)

We need some kind of solution, whenever we add, update or delete an
entry the associated cache data should be deleted. You have added new
book or deleted one, then cached books for endpoint
`api/booksIget)` should be deleted. Next
time user hit the endpoint `api/books(get)`, it will return the newer entries.

Same should goes for the endpoint `api/books/{id}`(get)`.

When user updates the book, the cached entries related to enpoints `api/books/{id}` (get) and `api/books`(get) should be deleted.

👉 Main point is user always needs to get latest data, cache should be
destroyed automatically whenever we add/update/delete the data that is
related to cached data.

👉That is why we need some kind of cache eviction policy.

### What is the solution 🤷‍♂️

**Answer:** Cache eviction 😁

Let's take a general idea behind it.

👉 Whenever we add, update or delete the book. We need to delete cache
entries for these two endpoints below

- `GET api/books`
- `GET api/books/{id}`

👉 We will create a `tag` and put the
endpoints `GET api/books` and
`GET api/books/{id}` under the tag `tag-book`. Take a look on diagram below.

![output-caching-tag](/images/output-caching-tag.png)

If we delete the cache (evict the cache) for `tag-book`{.markup--code
.markup--p-code} , all the related cache entries will be deleted at
once.

Let's see how to do it practically. First and foremost we will create
the tag. There are various ways to do it. Let's focus on this one first.
So we need to modify the base policy as below.

```cs
options.AddBasePolicy(builder =>
  {
    builder
      .With(r => r.HttpContext.Request.Path.StartsWithSegments("/api/books"))
      .Tag("tag-book")
      .Expire(TimeSpan.FromMinutes(2));
  });
```

All the endpoints starts with `api/books` will be considered under the tag
`tag-book`.

Okey, that's fair enough. Now how to delete cache entries for this tag.
For this we need to modify `AddBook`
method . Pass the parameter of type `IOutputCacheStore` to the
method and add the line below:

```cs
await cache.EvictByTagAsync("tag-book", default);
```

It does not make full sense. So here is the full implementation.

```cs
    [HttpPost]
    public async Task<IActionResult> AddBook(Book book, IOutputCacheStore cache)
    {
        try
        {
            var createdBook = await _bookRepos.AddBook(book);
            _logger.LogInformation("Books have saved");
            // evicting the cache related to 'tag-book'
            await cache.EvictByTagAsync("tag-book", default);
            return CreatedAtAction(nameof(AddBook), createdBook);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex.Message);
            return StatusCode(StatusCodes.Status500InternalServerError);
        }
    }
```

👉 The general idea is , whenever we hit the `AddBooks()`{.markup--code
.markup--p-code} method, we are going to evict the the cache associated
with tag `tag-book`{.markup--code .markup--p-code}.

👉 You need to follow the same approach for `put`{.markup--code
.markup--p-code}and `delete`{.markup--code .markup--p-code} methods.

We have successfully achieved cache eviction. If you are not intended to
touch the **base policy** for achieving the cache eviction, then you
need to create another policy for it.

```cs
options.AddPolicy("evict",builder =>
  {
    builder.Expire(TimeSpan.FromSeconds(90))
           .Tag("tag-book");
  });
```

In the controller method, add this policy as shown below.

```cs
[OutputCache(PolicyName ="evict")]
[HttpGet("{id}")]
public async Task<IActionResult> GetById(int id)
{
  //......
}


[HttpGet]
[OutputCache(PolicyName ="evict",VaryByQueryKeys = new[] { "lang" })]
public async Task<IActionResult> GetBooks(string? lang, string? title)
{
  //.....
}
```

It is how we achieve cache eviction.

---

## Resource locking 🔐

By default , resource locking is enabled to avoid the risk of **cache
stampede** and **thundering herd.** Lets see these two terms.

**Cache stampede:** Cache stampede, also known as cache invalidation
storm, occurs when a cached value for a particular resource expires, and
multiple requests are simultaneously triggered to regenerate or
recalculate the value. This can happen when a cached item's time-to-live
(TTL) expires, or it gets evicted from the cache.

**Thundering herd:** Thundering herd is a similar problem that arises
when multiple processes or threads are waiting for a particular event or
resource to become available. When the resource becomes available, all
waiting processes or threads are awakened simultaneously, resulting in
an overwhelming and redundant influx of requests.

To disable locking, we need to call `SetLocking(false)` method, when creating a policy.

```cs
 options.AddPolicy("NoLock", builder => builder.SetLocking(false));
```

---

## Cache storage

**IOutputCacheStore** is used for storage. By default it's used with
**MemoryCache**. We don't recommend **IDistributedCache** for use with
output caching. `IDistributedCache`
doesn\'t have atomic features, which are required for tagging. We
recommend that you create custom **IOutputCacheStore** implementations
by using direct dependencies on the underlying storage mechanism, such
as Redis. source [microsoft
docs](https://learn.microsoft.com/en-us/aspnet/core/performance/caching/output?view=aspnetcore-7.0#cache-storage)

### 💻Source code

Here is the [source
code](https://github.com/rd003/CachingAspNetCore/tree/output-cache-medium)

---

Orignally written by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [July 29, 2023](https://medium.com/p/75b8ce147e57).

[Canonical
link](https://medium.com/@ravindradevrani/output-caching-in-net-7-75b8ce147e57)

Exported from [Medium](https://medium.com) on February 19, 2025.
