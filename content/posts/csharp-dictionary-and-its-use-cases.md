+++
date = '2025-02-20T17:40:42+05:30'
draft = false
title = 'C# Dictionary and Its Use Cases'
tags = ['csharp']
categories=['programming']
image = '/images/csharp-dictionary-and-its-use-cases.png'
+++

<!-- ![Use cases of c# dictionary](/images/csharp-dictionary-and-its-use-cases.png) -->

## What is dictionary?

Dictionary is a collection, that store the value in the form of key value pair. It allows you to quick access of value using the key. This data structure is widely used in programming because of its fast look-up time, which makes it ideal for applications that require quick data retrieval

👉 You can not add duplicate key in dictionary

**Creating a dictionary:**

```cs
Dictionary<int, string> customerNames = new Dictionary<int, string>();
```

We have created a dictionary with a name **customerNames.** This dictionary holds the **integer key** and **string value.**

**Adding values to dictionary:**

We can assume that, key is a ID of the customer, value is the name of customer.

```cs
customerNames.Add(1, "John Smith");
customerNames.Add(2, "Jane Doe");
customerNames.Add(3, "Bob Johnson");
```

**Finding the Customer with key:**

```cs
int customerId = 2;
 if (customerNames.TryGetValue(customerId, out string customerName))
 {
 Console.WriteLine($"Customer with ID {customerId} is {customerName}");
        }
        else
        {
            Console.WriteLine($"Customer with ID {customerId} not found");
 }
```

**Getting all key and values of dictionary:**

```cs
foreach(KeyValuePair<int,string\> kvp in customerNames)
 {
 Console.WriteLine($"key: {kvp.Key} , value: {kvp.Value}");
 }
```

👉 These are few basic operations of dictionary. I am not going cover them in this article.

## Use cases of dictionary:

1. **Lookup tables:** Dictionaries are commonly used as lookup tables where you can quickly find the value associated with a given key. For example, you could use a dictionary to store the names of countries and their corresponding ISO codes.

```cs
Dictionary<string,string\> countryCodes = new Dictionary<string,string>();
 countryCodes.Add("Mali", "MLI");
 countryCodes.Add("Australia", " AUS");
 countryCodes.Add("Barbados", "BRB");
 countryCodes.Add("Canada", "CAN");

        // Lookup the iso code for a country
        string isoCode = countryCodes\["Barbados"\];
        Console.WriteLine(isoCode);// output: BRB

        // check if a country exists or not
        if(countryCodes.ContainsKey("Canada") )
        {
            Console.WriteLine("Yes it is in dictionary");
        }
```

**2. Counting:** Dictionaries can be used to count occurrences of items in a collection. For example, you could use a dictionary to count the number of times each word appears in a text document.

```cs
string text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. ipsum dolor lorem amet";
 string[] words = Regex.Matches(text, @"\\w+")
 .Cast&lt;Match&gt;()
 .Select(m => m.Value)
 .ToArray();

        Dictionary<string, int\> wordCounts = new Dictionary<string, int>();
        foreach(string word in words)
        {
            string normalizedWord = word.ToLower();
            if(wordCounts.ContainsKey(normalizedWord) )
            {
                wordCounts\[normalizedWord\]++;
            }
            else
            {
                wordCounts\[normalizedWord\] = 1;
            }

        }

        foreach(KeyValuePair<string,int\> kvp in wordCounts)
        {
            Console.WriteLine($"key: {kvp.Key}, value: {kvp.Value}");
        }

```

**3.** **Caching:** Dictionaries are often used for caching frequently accessed data. For example, you could use a dictionary to cache the results of a complex calculation or a database query.

```cs
public class Product
 {
 public int Id { get; set; }
 public string Name { get; set; }
 public int Views { get; set; }
 }

public class ProductRepository
{
 private Dictionary<int, List&lt;Product&gt;> \_productCache;

    public ProductRepository()
    {
        _productCache = new Dictionary<int, List&lt;Product&gt;>();
    }


    public List&lt;Product&gt; GetTop10MostViewedProducts()
    {
        if (_productCache.ContainsKey(-1))
        {
            return _productCache\[-1\].ToList();
        }

        // perform the expensive query to get the most viewed products
        var top10Products = new List&lt;Product&gt;();
        for(int i = 0; i < 10; i++)
        {
            top10Products.Add(new Product { Id = i, Name = $"product-{i}",Views= new Random().Next(0,100) });
        };

        // add the results to the cache with a special key of -1
        _productCache\[-1\] = top10Products;

        return top10Products;
    }

}
```

👉 **Note:** In this example, i have not added, cache eviction strategy or expiration time set for the cache entries, so the cache will continue to grow in size until the application is restarted or the cache is manually cleared. It is generally a good practice to implement some kind of cache eviction strategy to prevent the cache from growing too large and consuming too much memory.  
Although I wont encourage you to use it for caching purpose. Use proper caching management, if you want full control over cache.

**4. Mapping :** Dictionaries can be used to map one set of values to another. For example, you could use a dictionary to map customer IDs to customer names.

```cs
Dictionary<int, string> customerNames = new Dictionary<int, string>();

// Add some customer ID to name mappings
customerNames.Add(1, "John Smith");
customerNames.Add(2, "Jane Doe");
customerNames.Add(3, "Bob Johnson");

// Look up a customer name by their ID
int customerId = 2;
if (customerNames.TryGetValue(customerId, out string customerName))
{
 Console.WriteLine($"Customer with ID {customerId} is {customerName}");
}
else
{
    Console.WriteLine($"Customer with ID {customerId} not found");
}
```

In this example, we are mapping **CustomerName** with **Id.** In this way we can easily find customer, we just need to look for Id. In above example, we are finding the name of customer with id=2;

**5. Settings:** Dictionaries can be used to store application settings that can be accessed by various parts of the application. For example, you could use a dictionary to store user preferences such as font size or theme.

---

If you find this article useful, then consider to clap and share it. You can also follow me on YouTube, I have created lots of content related to .net core and angular.

Orginally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [April 18, 2023](https://medium.com/p/baf65a8e9961).

[Canonical link](https://medium.com/@ravindradevrani/c-dictionary-and-its-use-cases-baf65a8e9961)

Exported from [Medium](https://medium.com) on February 19, 2025.
