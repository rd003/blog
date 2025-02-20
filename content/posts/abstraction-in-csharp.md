+++
date = '2025-02-20T19:09:36+05:30'
draft = false
title = 'Abstraction in Csharp'
tags = ['oops']
categories=['programming'] 
+++

![abstraction in oops c#](/images/1_6CWERFGOQbJWr-R6wNi2oA.png)

**Abstraction** allows you to focus on the relevant details of an object while ignoring unnecessary complexities.  
This is achieved by defining a simplified representation of an object that **hides the implementation details and exposes only the necessary features**.  
In practical terms, **abstraction is implemented through abstract classes and interfaces in languages like C#**.

**📺Other OOPs related articles :**

- [Encapsulation in C#](https://ravindradevrani.medium.com/encapsulation-in-c-cd6d61aa2c3d)
- [Inheritance in C#](https://ravindradevrani.medium.com/inheritance-in-c-08327a9efee5)
- [Polymorphism in C#](https://medium.com/@ravindradevrani/polymorphism-in-c-ea312521d050)

Let’s implement abstraction by using **interface**. In the real world projects, we use interfaces more often.

```cs
public interface ICar
{
 int Speed { get; set; }

    void Accelerate();

    void Brake();

    void Refuel();

}
```

👉In this case, `ICar` is an `interface` with some features. A class, that implements this interface, will follow this blueprint. That class must have a property name `Speed` and the methods like `Accelerate(),Brake()` and `Refuel()`. These are the necessary details for any type of car, it does not matter if it is a sedan, SUV or a sports car. Every Car will have these features.

👉 So we are declaring the **necessary features** like `Speed`, `Accelarate()`,`Break()` and `Refule()` and **hiding unnecessary complexities** like `implementation details` of these features.

Abstraction is like looking at these things from a high level without worrying about specific details. For example, you don’t care about how the `Brake()` feature will work. You are saying that, hey there will be a `Break()` feature in the Car. How does `Break()` work? We don’t care. It will be taken care later. Which will be shown in this example.

We are creating a class `Sedan`, which is implementing `ICar` interface. In this class, we are defining the `Accelarate(),Brake() and Refuel()` feature according to the sedan cars.

```cs
public class Sedan : ICar
{
 public int Speed { get; set; }

    public void Accelerate()
    {
        // Implementation for accelerating a sedan
    }

    public void Brake()
    {
        // Implementation for braking a sedan
    }

    public void Refuel()
    {
        // Implementation for refueling a sedan
    }

}
```

👉 Similarly, create other **classes** like `SUV`, `SportsCar` etc.

👉 That was all about abstraction you might have few doubts in mind, like why need to create an interface, then implement it in a class. We can directly create a class with all the needed features. If you have that doubt then move to the next section, otherwise you can skip it here.

---

## Why would I take extra steps to create the interface?

Now, you might be wondering that, why do we create an interface and implement it in a class. We can avoid the extra step of creating the interface and define all the methods in the class. As shown in the example below.

```cs
public class Sedan
{
 public int Speed { get; set; }

    public void Accelerate()
    {
        // Implementation for accelerating a sedan
    }

    public void Brake()
    {
        // Implementation for braking a sedan
    }

    public void Refuel()
    {
        // Implementation for refueling a sedan
    }

}
```

Here we are not using any interface and still achieving the same result. Let’s see what are the benefits.

**1. Abstraction:** It helps to look things from high level without worrying about specific details. For example , what are features you need in a car. Just the higher level overview and no need to worry about actual functionality.

**2. Code Consistency:** Using interfaces promotes consistency in your code. If you have multiple classes implementing the same interface, you can use them interchangeably, leading to a more cohesive and predictable codebase.

**3. Ease of Extension:** If you need to add new types of cars in the future, you can easily create additional classes that implement the existing ICar interface. This extension doesn’t require changes to existing code that uses the interface.

**4. Testing and Mocking:** Interfaces make it easier to write unit tests and use mocking frameworks. When you do unit testing, will find the benefits of using interfaces.

**5. Enforces Contract:** It forces you to use all the features of an interface.

**6. Makes your system loosely coupled.**

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [January 30, 2024](https://medium.com/p/c3d4c832942a).

[Canonical link](https://medium.com/@ravindradevrani/abstraction-in-c-c3d4c832942a)

Exported from [Medium](https://medium.com) on February 19, 2025.
