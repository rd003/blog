+++
date = '2025-07-29T18:24:07+05:30'
draft = false
title = 'Asynchronous Programming in C# - Comparing it with multithreading'
categories = ['programming']
tags = ['csharp']
+++

![async and await in c#](/images/async-csharp.webp)

`Asynchronous task` is a **non-blocking** task. Main thread goes back to the **thread pool** (and free to do other tasks) when it reaches to await -- and new thread is assigned when wait is complete.

It is different from the multithreading. In multithreding, task is divided between multiple threads. Cores of your CPU are utilized.

## Analogy

Let's say you have some chores like:
 
 1. Boiling eggs 🫕 (or sweet potatoes🍠🍠 if you dont eat eggs 🥚🥚)
 2. Clean 🧹🪣 the house

There are multiple ways to achieve this:

1. Boil the eggs 🥚 and wait until it finishes, then clean 🧹🪣 the house. It is called `synchronous task`.
2. You put eggs 🥚 in boiling water and set the timer ⏰. Meanwhile you finishes other works like clean a house🧹🪣. When timer ⏰ indicates, you close the lit  of boiling pan 🫕. Then again you finishes the remaining task. It is called `asynchronous task`. You are not bound to wait for the task to finish.
3. You has asked someone to boil the eggs🫕 and you are taking care of cleaning 🧹🪣  the house. You are two people 👥 now. It is called `multithreading`, you have more workers to finish the task. 


## Synchronous task

```cs
namespace ConsoleApp;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine($"Main thread : {Thread.CurrentThread.ManagedThreadId}");
        BoilEggs();
        CleanHouse();
        Console.WriteLine($"All task completed by ThreadId: {Thread.CurrentThread.ManagedThreadId}");
    }

    public static void BoilEggs()
    {
        Console.WriteLine("Eggs are boiling...");
        Thread.Sleep(2000);
        Console.WriteLine($"Egg boiled by thread : {Thread.CurrentThread.ManagedThreadId}");
    }

    public static void CleanHouse()
    {
        Console.WriteLine("Cleaning in process..");
        Thread.Sleep(1500);
        Console.WriteLine($"House cleaned by thread : {Thread.CurrentThread.ManagedThreadId}");
    }
}
```

Output:

```bash
Main thread : 1
Eggs are boiling...
Egg boiled by thread : 1
Cleaning in process..
House cleaned by thread : 1
All task complete by ThreadId: 1
```


## Asynchronous Task

```cs
namespace ConsoleApp;

public class Program
{
    public static async Task Main(string[] args)
    {
        Console.WriteLine($"Main thread : {Thread.CurrentThread.ManagedThreadId}");
        await BoilEggs();
        await CleanHouse();
        await SomeOtherChore();
        Console.WriteLine($"All task completed by ThreadId: {Thread.CurrentThread.ManagedThreadId}");
    }

    public static async Task BoilEggs()
    {
        Console.WriteLine("Eggs are boiling...");
        await Task.Delay(2000);
        Console.WriteLine($"Egg boiled by thread : {Thread.CurrentThread.ManagedThreadId}");
    }

    public static async Task CleanHouse()
    {
        Console.WriteLine("Cleaning in process..");
        await Task.Delay(1500);
        Console.WriteLine($"House cleaned by thread : {Thread.CurrentThread.ManagedThreadId}");
    }

    public static async Task SomeOtherChore()
    {
        Console.WriteLine("SomeOther chore in process..");
        await Task.Delay(500);
        Console.WriteLine($"SomeOther chore is completed by thread : {Thread.CurrentThread.ManagedThreadId}");
    }
}
```

Output:

```bash
Main thread : 1
Eggs are boiling...
Egg boiled by thread : 5
Cleaning in process..
House cleaned by thread : 5
SomeOther chore in process..
SomeOther chore is completed by thread : 5
All task completed by ThreadId: 5
```

You can also wait all task at once.

```cs
 Console.WriteLine($"Main thread : {Thread.CurrentThread.ManagedThreadId}");
 Task boilEggTask = BoilEggs();
 Task cleanHouseTask = CleanHouse();
 Task otherChoreTask = SomeOtherChore();
 await Task.WhenAll(boilEggTask, cleanHouseTask, otherChoreTask);
 Console.WriteLine($"All task completed by ThreadId: {Thread.CurrentThread.ManagedThreadId}");
```

output:

```bash
Main thread : 1
Eggs are boiling...
Cleaning in process..
SomeOther chore in process..
SomeOther chore is completed by thread : 5
House cleaned by thread : 5
Egg boiled by thread : 5
All task completed by ThreadId: 5
```

## Multithreading

```cs
using System.Diagnostics.CodeAnalysis;

namespace ConsoleApp;

public class Program
{
    public static void Main(string[] args)
    {
        Console.WriteLine($"Main thread : {Thread.CurrentThread.ManagedThreadId}");
        Thread t1 = new Thread(BoilEggs);
        Thread t2 = new Thread(CleanHouse);
        Thread t3 = new Thread(SomeOtherChore);
        t1.Start();
        t2.Start();
        t3.Start();

        t1.Join();
        t2.Join();
        t3.Join();
    }

    public static void BoilEggs()
    {
        Console.WriteLine("Eggs are boiling...");
        Thread.Sleep(2000);
        Console.WriteLine($"Egg boiled by thread : {Thread.CurrentThread.ManagedThreadId}");
    }

    public static void CleanHouse()
    {
        Console.WriteLine("Cleaning in process..");
        Thread.Sleep(1500);
        Console.WriteLine($"House cleaned by thread : {Thread.CurrentThread.ManagedThreadId}");
    }

    public static void SomeOtherChore()
    {
        Console.WriteLine("SomeOther chore in process..");
        Thread.Sleep(500);
        Console.WriteLine($"SomeOther chore is completed by thread : {Thread.CurrentThread.ManagedThreadId}");
    }
}
```

output:

```bash
Main thread : 1
Eggs are boiling...
Cleaning in process..
SomeOther chore in process..
SomeOther chore is completed by thread : 6
House cleaned by thread : 5
Egg boiled by thread : 4
```

## Real life use case of async

```cs
 string url = "https://jsonplaceholder.typicode.com/users";
 HttpClient client = new();
 var data = await client.GetStringAsync(url);
 Console.WriteLine(data);
```

## When to choose each?

`Async` is useful in `IO bound tasks` like network calls, database calls or manipulating files.

`Multithreading` is useful in` CPU bound tasks` like image/video processing, encryption/hashing or processing the large data.
