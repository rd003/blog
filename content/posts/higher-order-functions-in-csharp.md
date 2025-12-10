+++
date = '2025-02-23T13:07:13+05:30'
draft = false
title = 'Higher Order Functions in C#'
tags = ['csharp']
categories=['programming']
image = 'https://cdn-images-1.medium.com/max/800/1*y637ZiP8h1B5XyLgbFm-GQ.png'
+++

<!-- <!-- ![Higher-order functions in c#](https://cdn-images-1.medium.com/max/800/1*y637ZiP8h1B5XyLgbFm-GQ.png) --> -->

**Higher-order functions (HOF)** are functions that can take a function as an argument or return a function or both. In C#, higher-order functions are achieved using delegates, lambda expressions and expression trees.

## Example 1: Using a Delegate

```cs
// Declare a delegate that takes an int and returns an int
public delegate int IntOperation(int x);

public class Program
{
    // Higher-order function that takes a delegate as an argument
    public static int PerformOperation(int value, IntOperation operation)
    {
    return operation(value);
    }

    public static void Main()
    {
        // Create a delegate instance that points to the Square method
        IntOperation square = x => x \* x;

        // Pass the delegate to the higher-order function
        int result = PerformOperation(5, square);
        Console.WriteLine(result); // Output: 25
    }

}
```

## Example 2 : Using lambda expression

```cs
// Higher-order function that takes a lambda expression as an argument
public static int PerformOperation(int value, Func<int, int\> operation)
{
 return operation(value);
}

// main method

// Define a lambda expression that squares a number
Func<int, int> square = x => x * x;

// Pass the lambda expression to the higher-order function
int result = PerformOperation(5, square);
```

## Example 3: Function as a Return Value

```cs
public class Program
{
    // Higher-order function that returns a function
    public static Func<int, int\> GetOperation(bool isSquare)
    {
        if (isSquare)
        {
            return x => x \* x;
        }
        else
        {
            return x => x + x;
        }
    }

    public static void Main()
    {
        // Get a function that squares a number
        Func<int, int> operation = GetOperation(true);

        // Use the returned function
        int result = operation(5);
        Console.WriteLine(result); // Output: 25
    }
}
```

In c#, higher order functions are everywhere. If one have used LINQ, must have used HO functions. Collection’s Where() is the good example.

```cs
List<int> numbers = [1, 2, 3, 4, 5];
var even = numbers.Where(n => n > 3);
```

`Where()` takes `Func<int, bool> predicate)` as a parameter. It can be written as:

```cs
List<int\> numbers = [1, 2, 3, 4, 5];
Func<int, bool\> isGreaterThanThree = n => n > 3;
var greaterThanThree = numbers.Where(isGreaterThanThree);
```

Or can be replaced with anonymous function or delegate. The point is, `Where` is taking function as a parameter

## Common higher-order functions in c\#

Select, Where, OrderBy, OrderByDescending, Aggregate, Any, ForEach, GroupBy, Count, Sum, Average, Min, Max are some of the higher-order functions. These functions are commonly used with LINQ (Language Integrated Query) to manipulate collections in a functional style, allowing for concise and expressive code.

---

[Canonical link](https://medium.com/@ravindradevrani/higher-order-functions-in-c-f8c52b04c7fe)
