+++
date = '2025-02-21T09:31:26+05:30'
draft = false
title = 'Delegates, Anonymous Method and Lambda Expression'
tags = ['csharp']
categories= ['programming']
+++

![Delegates, anonymous method and lambda expression in c#](/images/1_IjMrDe_CyuhXr3ZpddcOOg.png)

- Delegates in C# are essentially type-safe function pointers.
- They allow you to treat methods as objects, enabling you to pass methods as parameters, store them in variables, and invoke them dynamically.
- Delegates are particularly useful for implementing callback mechanisms and event handling in C#.

delegate void MyDelegate(string message);

You can point this delegate to any method with similar signature.

```cs
namespace BasicsOfCSharp;

// Declare a delegate type
delegate void MyDelegate(string message);

class Program
{
 // Method that matches the delegate signature
 static void DisplayMessage(string message)
 {
 Console.WriteLine("Message: " + message);
 }
 static void Main()
 {
        // Instantiate the delegate.
        MyDelegate handler = DisplayMessage;

        // calling the handler
        handler("Hello..");

    }

}
```

**👉Multicast Delegate:**

You can invoke multiple multiple method with a single handler, it is called `multicast delegate.`

```cs
namespace BasicsOfCSharp;

// Declare a delegate type
delegate void MyDelegate(string message);
class Program
{
// Method that matches the delegate signature
static void DisplayMessage(string message)
{
Console.WriteLine("Message: " + message);
}

    static void Greet (string name)
    {
        Console.WriteLine("Hello : " + name);

    }
    static void Main()
    {
        // Instantiate the delegate.
        MyDelegate handler = DisplayMessage;
        handler += Greet;

        // calling the handler
        handler("John");

        // output
        // Message: John
        // Hello : John

    }

}
```

**👉Removing a method from delegate:**

```cs
static void Main()
{
// Instantiate the delegate.
MyDelegate handler = DisplayMessage;
handler += Greet;

     // calling the handler
     handler("John");

     Console.WriteLine("Removing a method");
     handler -= DisplayMessage;
     handler("John Doe");

     /*
       Message: John
       Hello : John
       Removing a method
       Hello : John Doe
    */

}
```

### Passing delegate as a parameter

```cs
namespace BasicsOfCSharp;

// Define a delegate type for arithmetic operations
delegate int ArithmeticOperation(int x, int y);

class Calculator
{
public int PerformOperation(int x, int y, ArithmeticOperation operation)
{
return operation(x, y);
}
}

class Program
{
    static int Add(int x, int y)
    {
    return x + y;
    }

    static int Subtract(int x, int y)
    {
        return x - y;
    }

    static void Main()
    {
        Calculator calc = new();
        // Pass the Add method as a delegate parameter
        int result1 = calc.PerformOperation(5, 3, Add);
        Console.WriteLine(result1);
        // Pass the Substract method as a  delegate parameter
        int result2 = calc.PerformOperation(5,3,Subtract);
        Console.WriteLine(result2);
    }

}
```

In this example:

- We define a delegate type `ArithmeticOperation` that represents methods taking two `int` parameters and returning an `int`.
- We define a `Calculator` class with a method `PerformOperation` that takes two integers and a delegate representing an arithmetic operation.
- We define `Add` and `Subtract` methods that match the delegate signature.
- In the `Main` method, we create an instance of the `Calculator` class and pass the `Add` and `Subtract` methods as delegate parameters to perform addition and subtraction operations, respectively.

---

### Anonymous methods

Let’s look at this example.

```cs
namespace BasicsOfCSharp;

// Declare a delegate type
delegate void MyDelegate(string message);

class Program
{
// Method that matches the delegate signature
static void DisplayMessage(string message)
{
Console.WriteLine("Message: " + message);
}
static void Main()
{
        // Instantiate the delegate.
        MyDelegate handler = DisplayMessage;

        // calling the handler
        handler("Hello..");

    }

}
```

In this example, delegate `MyDelegate` is pointing to method `DisplayMessage` . We can achieve the same, without creating the actual method. We need to use **anonymous method** for that.

```cs
namespace BasicsOfCSharp;

// Declare a delegate type
delegate void MyDelegate(string message);

class Program
{
static void Main()
{
// Instantiate the delegate with anonymous method
MyDelegate handler = delegate(string message)
{
Console.WriteLine("Message: " + message);
};

        // calling the handler
        handler("Hello..");
    }

}
```

### Lambda expression

Anonymous method can be replace with lambda expression.

```cs
namespace BasicsOfCSharp;

// Declare a delegate type
delegate void MyDelegate(string message);

class Program
{
    static void Main()
    {
        // Instantiate the delegate with lambda expression
        MyDelegate handler = (string message)=>
        {
             Console.WriteLine("Message: " + message);
        };

        // calling the handler
        handler("Hello..");
    }

}
```

---

[Generic Delegates (Action, Func, Predicate)In C#](/posts/generic-delegates-action-func-predicate-in-csharp/)

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [February 10, 2024](https://medium.com/p/f6d72a77160d).

[Canonical link](https://medium.com/@ravindradevrani/delegates-anonymous-method-and-lambda-expression-in-c-f6d72a77160d)

Exported from [Medium](https://medium.com) on February 19, 2025.
