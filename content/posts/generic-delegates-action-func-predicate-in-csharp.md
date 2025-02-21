+++
date = '2025-02-21T09:54:50+05:30'
draft = false
title = 'Generic Delegates (Action, Func & Predicates) in Csharp'
+++

![Generic delegate c#, action func predicate in c#](/images/1_Fd96UK0xih85jyUlAiBDAg.png)

In C#, [**delegates**](/posts/delegates-anonymous-method-and-lambda-expression/) are used to refer to methods with a specific signature. `Generic delegates` extend this concept by allowing you to create delegates that can work with any method signature, rather than being tied to a specific signature.

Here’s a basic example of a generic delegate:

```cs
delegate T MyGenericDelegate<T>(T arg);
```

You can use this generic delegate as follows.

```cs
MyGenericDelegate<int> handler1 = CustomSquare;
int square=handler1(4);
Console.WriteLine(square); //16

MyGenericDelegate<string\> handler2 = CustomToUpper;
Console.WriteLine(CustomToUpper("helLo")); //HELLO
```

## In-built Generic delegates

C# comes with inbuilt generic delegates like `Action`, `Func` and `Predicate`.

### Action delegate

Action is an in-built delegate that takes 0to n arguments and does not return anything (void type).

```cs
static void Main()
{
     // 0 argument
     Action Greeting = () =>
     {
         Console.WriteLine("Hello");
     };

     // 1 argument
     Action<string\> messageInUpper = (message) =>
     {
         Console.WriteLine(message.ToUpper());
     };
     messageInUpper("hello world..."); //HELLO WORLD...

     // 2 arguments
     Action<int, int\> sum = (a, b) =>
     {
         Console.WriteLine($"sum of {a} and {b} = {a + b}");
     };
     sum(11,2);  //sum of 11 and 2 = 13

}
```

### Func delegate

`Func` takes 0 to n arguments and always returns a value. The main difference between `Action` and `Func` is, `Func` always returns the value.

```cs
static void Main()
{
     // take 0 args and return 4
     Func<int> simple = () =>4;

     // takes two integer args return their sum
     Func<int,int,int> sum = (x,y)=> x + y;

     // takes two integer args return their differece
     Func<int,int,int> subtract = (x,y)=> x - y;

     Console.WriteLine(simple()); //4
     Console.WriteLine(sum(3,2)); //5
     Console.WriteLine(subtract(3,2)); //1
}
```

### Predicate delegate

Predicate delegate takes only 1 arguments and returns a boolean value.

```cs
static void Main()
{
// return true if passed argument is greater than 4
Predicate<int\> simple = (n) => n>4;

    Console.WriteLine(simple(4)); //false

}
```

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [February 11, 2024](https://medium.com/p/100c5251e554).

[Canonical link](https://medium.com/@ravindradevrani/generic-delegates-action-unc-predicate-in-c-100c5251e554)

Exported from [Medium](https://medium.com) on February 19, 2025.
