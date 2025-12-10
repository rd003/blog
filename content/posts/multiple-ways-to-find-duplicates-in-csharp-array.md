+++
date = '2025-02-20T17:49:19+05:30'
draft = false
title = 'Multiple Ways to Find Duplicates in Csharp Array'
tags = ['csharp']
categories=['programming']
image = '/images/csharp-duplicates.png'
+++

<!-- ![find duplicates in c# array](/images/csharp-duplicates.png) -->

In C#, we can use various approaches to find duplicate elements in array. Each have pros and cons. We will use 3 approaches in this article.

1. **Using a HashSet**
2. **Using a Dictionary**
3. **Using LINQ**

Lets take this array as an example, from this array we will extract **distinct numbers** and **duplicate numbers.**

```cs
int[] numbers = { 4,7, 2, 3, 4, 5, 3, 6, 7, 8,1, 8 };
```

We will use this array in all three approaches. So let’s understand one by one.

## Using HashSet

`HashSet` is a data structure, that holds the unique items. Using `HashSet` , we can easily find the duplicates in array.

This approach involves iterating over the input array and adding each element to a HashSet. If an element is already present in the HashSet, it is considered a duplicate. This approach has an average time complexity of O(n) and is particularly useful if the input array is large and the order of the elements does not matter. But it can have few problems, which we will discuss later.

```cs
public class Program
{
 static void Main()
 {
 int[] numbers = { 4, 7, 2, 3, 4, 5, 3, 6, 7, 8, 1, 8 };
 HashSet<int> distinctNumbers = new();
 HashSet<int> duplicateNumbers = new();

        foreach (int number in numbers)
        {
            if (!distinctNumbers.Add(number))
                duplicateNumbers.Add(number);
        }

        Console.WriteLine("original array");
        PrintArray(numbers);

        Console.WriteLine("distinct Numbers");
        PrintArray(distinctNumbers.ToArray());

        Console.WriteLine("duplicate Numbers");
        PrintArray(duplicateNumbers.ToArray());

        Console.ReadLine();
    }

    static void PrintArray(int[] numArray)
    {
        foreach (int num in numArray)
        {
            Console.Write($"{num} ");
        }
        Console.WriteLine();
    }

}
```

Let’s break it. We are extracting distinct and duplicate numbers from the array

```cs
int[] numbers = { 4, 7, 2, 3, 4, 5, 3, 6, 7, 8, 1, 8 };
```

We have created two `HashSet` **distinctNumbers** and **duplicateNumbers**.

```cs
HashSet<int> distinctNumbers = new();
HashSet<int> duplicateNumbers = new();
```

We will iterate over the **numbers** array, try to add a **number** in **distinctNumbers**. If it is added successfully then it is a unique number, otherwise we will add it in a **duplicateNumbers**.

```cs
foreach (int number in numbers)
 {
 if (!distinctNumbers.Add(number))
 duplicateNumbers.Add(number);
 }
```

**Output:**

```txt
original array
4 7 2 3 4 5 3 6 7 8 1 8
distinct Numbers
4 7 2 3 5 6 8 1
duplicate Numbers
4 3 7 8
```

**⚠️Downsides:** These are the few downsides for using HashSet.

1. **Memory usage:** The `**HashSet`\*\* approach requires additional memory to store the unique and duplicate elements separately. In worst-case scenario, where all the elements are unique, you will end up with a hash set that’s the same size as the original array.
2. **Ordering:** The \`HashSet\` approach does not preserve the order of the original array, so if order matters in your application, you will need to find a different approach.
3. **Performance:** The performance of the `**HashSet`** approach can degrade if the input array is very large, as the `**Add`** method has a time complexity of **O(1)** on average, but in the worst case, it could be **O(n)\*\* if there are many hash collisions.
4. **Data type limitations:**

- When you use the `HashSet` approach to find duplicates and unique elements in an array, the elements in the array need to be of a certain type. Specifically, they need to be either a value type (like `int`, `float`, or `bool`) or a reference type (like `string`, `object`, or a custom class that you define).
- However, if you have an array of a custom object type that you’ve created, like a `Person` class that has properties for name, age, and address, you may run into a problem. The reason is that the `HashSet` class doesn't know how to compare two `Person` objects to see if they're equal or not.
- To solve this problem, you need to teach the `HashSet` class how to compare `Person` objects. You can do this by implementing the `IEquatable<T>` interface on your `Person` class. This interface provides a way to define how two objects of the same type should be compared for equality.
- If you don’t implement the `IEquatable<T>` interface (or another interface called `IEqualityComparer<T>`), the `HashSet` class will use the default comparison behavior, which is to check if the objects are the same reference in memory. This means that two `Person` objects that have the same name, age, and address but are different objects in memory will not be considered equal by the `HashSet` class.
- So, to summarize, if you’re using the `HashSet` approach to find duplicates and unique elements in an array, make sure that the elements in the array are of a type that can be compared for equality by the `HashSet` class. If you're using a custom object type, you'll need to implement the `IEquatable<T>` interface (or another equivalent interface) to define how two objects of that type should be compared for equality

## Using Dictionary

This approach is similar to using a `HashSet`, but instead of storing only the unique values, we store each element of the input array in a `Dictionary` as a **key** and the number of times it appears in the array as the **value**. This approach has a time complexity of O(n) and is useful if we need to keep track of the count of each duplicate value.

```cs
int[] numbers = { 4, 7, 2, 3, 4, 5, 3, 6, 7, 8, 1, 8, 8 };
 Dictionary<int, int> counts = new Dictionary<int, int>();
 foreach (int num in numbers)
 {
 if (counts.ContainsKey(num))
 counts[num]++;
 else
 counts[num] = 1;
 }

        int[] distinctNumbers = counts.Select(kv => kv.Key).ToArray();

        int[] duplicateNumbers = counts.Where(a => a.Value > 1)
                        .Select(kv => kv.Key).ToArray();

        Console.WriteLine("original array");
        PrintArray(numbers);

        Console.WriteLine("distinct Numbers");
        PrintArray(distinctNumbers);

        Console.WriteLine("duplicate Numbers");
        PrintArray(duplicateNumbers);

        Console.ReadLine();
```

**👉Note:** **PrintArray()** method is defined in the previous example, so I am not going to reimplement in this example and next example.

Let’s break it. We are extracting distinct and duplicate numbers from the array

```cs
int[] numbers = { 4, 7, 2, 3, 4, 5, 3, 6, 7, 8, 1, 8 };
```

We have created a dictionary with name **counts **, a **number** in a array will be **key** and number of occurences will be stored as a value.

```cs
Dictionary<int, int> counts = new Dictionary<int, int>();
```

We will iterate over the **numbers** array and we will check if this **number** is already exists as a key or not. If a number is not present as a key in dictionary, it means it is the first occurrence , we will assign 1 to this key. Otherwise we will increment it’s value by 1.

```cs
foreach (int num in numbers)
{
if (counts.ContainsKey(num))
counts\[num\]++;
else
counts\[num\] = 1;
}
```

Since all the keys will always be unique, we can store those in the **distinctNumbers** array.

If **key’s value is greater that 1**, it means it is a duplicate, we can select those values from dictionary and store in the **duplicateNumbers** array.

```cs
int[] distinctNumbers = counts.Select(kv => kv.Key).ToArray();

int[] duplicateNumbers = counts.Where(a => a.Value > 1)
.Select(kv => kv.Key).ToArray();
```

**Output:**

**⚠️Downsides :** These are the few downsides for using dictionary.

1. **Extra memory usage:** The dictionary will use extra memory to store the key-value pairs, which can be a problem if you’re working with very large arrays.
2. **Slower performance:** Creating a dictionary involves some overhead, such as allocating memory and performing hash calculations. For small arrays, this may not be noticeable, but for larger arrays it can slow down your program.
3. **Unpredictable order:** When you extract distinct and duplicate elements using a dictionary, the order of the elements may not be preserved. This may not matter for some applications, but for others it can be important.
4. **Limited to one key and value type:** Dictionaries in C# are limited to using a specific key and value type. If you need to extract elements of a different type or structure, you may need to use a different approach.

## Using LINQ

The `LINQ`library provides a concise and expressive way to extract unique and duplicate values from an array. For example, we can use the **Distinct()** method to extract unique values and the **GroupBy()** method to group the duplicates. It have a time complexity of O(n).

```cs
int[] numbers = { 4, 7, 2, 3, 4, 5, 3, 6, 7, 8, 1, 8, 8 };
int[] distinctNumbers = numbers.Distinct().ToArray();
int[] duplicateNumbers = numbers
.GroupBy(x => x)
.Where(g => g.Count() > 1)
.Select(g => g.Key)
.ToArray();

        Console.WriteLine("original array");
        PrintArray(numbers);

        Console.WriteLine("distinct Numbers");
        PrintArray(distinctNumbers);

        Console.WriteLine("duplicate Numbers");
        PrintArray(duplicateNumbers);

        Console.ReadLine();

```

We do not need to break it much. With **Distinct()**, we can get the distinct numbers and using **GroupBy()**, we can get duplicate numbers.

```cs
int[] distinctNumbers = numbers.Distinct().ToArray();
int[] duplicateNumbers = numbers
.GroupBy(x => x)
.Where(g => g.Count() > 1)
.Select(g => g.Key)
.ToArray();
```

**Oututput:**

```txt
original array
4 7 2 3 4 5 3 6 7 8 1 8 8
distinct Numbers
4 7 2 3 5 6 8 1
duplicate Numbers
4 7 3 8
```

**⚠️ Downsides:** These are the few downsides for using LINQ.

1. **Performance:** LINQ operations can be slower than direct loops or specialized data structures, especially for large datasets. If performance is critical, it may be better to use a more specialized approach.
2. **Memory usage:** LINQ operations often create new objects or collections, which can increase memory usage. This can be a concern if memory usage is a limiting factor in the application.
3. **Maintenance:** LINQ expressions can sometimes be difficult to read or understand, which can make it harder to maintain or modify the code in the future. Additionally, using LINQ may require a developer to have a solid understanding of the LINQ syntax and behavior.

All the approaches have its benefits and downsides, choose carefully according to your need.

## 🤷‍♂️TL;DR

**HashSet** is the most efficient and recommended approach for large arrays, as it has a faster lookup time and doesn’t modify the original array. However, if preserving the original array is important, making a copy of the array is required.

**Dictionary** is a good alternative, but it’s less efficient than **HashSet** and requires more memory.

**LINQ** can also be used, but it’s slower than **HashSet** and **Dictionary** and can impact performance for large arrays.

---

Orinally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [April 21, 2023](https://medium.com/p/b570142ce506).

[Canonical link](https://medium.com/@ravindradevrani/multiple-ways-to-find-duplicates-in-c-array-with-pros-and-cons-b570142ce506)

Exported from [Medium](https://medium.com) on February 19, 2025.
