+++
date = '2025-02-22T20:58:52+05:30'
draft = false
title = 'The Liskov Substitution Principle (LSP)'
tags = ['design-patterns','SOLID']
categories = ['programming']
+++

![What is Liskov substitution principle](/images/1_RdNrcbPpOQ1z5b9crorp2Q.webp)

The **Liskov Substitution Principle** states that a derived type should be completely replaceable for its base type.

In simpler terms, a child class should do at least what the parent class can do. The child class can have additional behaviors, but it must have all the behaviors that the parent class has.

For instance, an **Animal** has behaviors (eat, sleep, makeSound). A **Dog**, which is a subtype of **Animal**, must have all the behaviors (eat, sleep, makeSound).

In simpler terms, if you ask for an animal which eat, sleep and makeSound then you must be okay with having a dog, a cat, or a horse.

So, that is basically the LSP. LSP is all about having well-designed polymorphic classes. Let’s understand what constitutes bad polymorphic design.

Other SOLID principles

- [Single Responsibility Principle](/posts/single-responsibility-principle/)
- [Open Closed Principle](/posts/open-closed-principle/)
- [Interface Segregation Principle](/posts/interface-segregation-principle/)
- [Dependency Inversion Principle](/posts/dependency-inversion-principle/)

### A code that is violating the LSP

```cs
public abstract class Bird
{
    public abstract void Eat();
    public abstract void MakeSound();
    public abstract void Fly();

    public void Sleep() => Console.WriteLine("Sleeping..");
}

public class Sparrow : Bird
{
    public override void Eat() => Console.WriteLine("Sparrow is eating..");

    public override void Fly() => Console.WriteLine("Sparrow is flying..");

    public override void MakeSound() => Console.WriteLine("chirp..");

}

public class Penguin : Bird
{
    public override void Eat() => Console.WriteLine("Penguin is eating..");

    public override void Fly() => throw new NotImplementedException();

    public override void MakeSound() => Console.WriteLine("Penguin's sound");

}

public class BirdTest
{
    public static void Main()
    {
        Bird sparrow = new Sparrow();
        sparrow.Fly();

        Bird penguin = new Penguin();
        penguin.Fly(); // throws exception
    }
}
```

`Bird` is an abstract class that has methods like Eat(), MakeSound(), Sleep(), and Fly(). Sparrow and Penguin inherit from the Bird class. Since a **Sparrow is a Bird**, a sparrow must do what a bird can do (such as eat, make sound, sleep, and fly), and it does.

A **Penguin is a Bird** too, so a penguin must do what a bird can do (such as eat, make sound, sleep, and fly). However, a penguin cannot fly. When you call the Fly() method of the Penguin class, it throws an error. Therefore, a penguin is not completely replaceable for a bird. This code violates the **Liskov Substitution Principle (LSP)**.

## Solution with LSP

### Solution 1

Let’s create the `IBird` interface.

```cs
public interface IBird
{
  void Eat();
  void MakeSound();
  void Sleep();
}
```

We need to have another interface which will have the bird’s behavior with flying capabilities.

```cs
public interface IFlyableBird:IBird
{
  void Fly();
}
```

Since **sparrow** can fly, so it will implement the `IFlyableBird` interface.

```cs
public class Sparrow : IFlyableBird
{
    public void Eat() => Console.WriteLine("Sparrow is eating..");

    public void Fly() => Console.WriteLine("Sparrow is flying..");

    public  void MakeSound() => Console.WriteLine("chirp..");

    public void Sleep() => Console.WriteLine("Sleeping");

}
```

Penguins do not fly, so they will implement the bird interface.

```cs
public class Penguin : IBird
{
    public void Eat() => Console.WriteLine("Penguin is eating..");

    public void MakeSound() => Console.WriteLine("Penguin's sound");

    public void Sleep() => Console.WriteLine("Sleeping");
}
```

`Sleep()` method is common between all the birds. In our refactored code, we need to implement Sleep() method in every bird related class (eg. Penguin,Sparrow). This does not seem to be a problem now. But, what if we have multiple methods where which shares between all the classes. In that case this solution does not seem right to me.

### Solution 2: Reusing the shared methods (Sleep())

First and foremost, we need to create an interface `IBird`.

```cs
public interface IBird
{
  void MakeSound();
  void Eat();
  void Sleep();
}
```

We need to encapsulate out the fying behaviour. So create an interface with the name `IFlyable`

```cs
public interface IFlyableBird : IBird
{
  void Fly();
}
```

Since we want to reuse the some functionality of the bird like Sleep(). We will be needed an abstract class to.

```cs
public abstract class Bird
{
    public abstract void Eat();
    public abstract void MakeSound();

    public void Sleep() => Console.WriteLine("Sleeping..");

}
```

Since **sparrow** can fly the it will inherit the `Bird` class and implement the `IFlyable` interface.

```cs
public class Sparrow : Bird, IFlyableBird
{
    public override void Eat() => Console.WriteLine("Sparrow is eating..");

    public void Fly() => Console.WriteLine("Sparrow is flying..");

    public override void MakeSound() => Console.WriteLine("chirp..");

}
```

Since **penguin** does not fly so it will only inherit the `Bird` class.

```cs
public class Penguin : Bird
{
    public override void Eat() => Console.WriteLine("Penguin is eating..");

    public override void MakeSound() => Console.WriteLine("Penguin's sound");
}
```

Now let’s test this functionality.

```cs
public class BirdTest
{
    public static void Main()
    {
        Console.WriteLine("Sparrow's behaviors\n");
        IFlyableBird sparrow = new Sparrow();
        sparrow.Fly();
        sparrow.MakeSound();
        sparrow.Eat();
        sparrow.Sleep();

        Console.WriteLine("\nPenguine's behaviors");
        Bird penguin = new Penguin();
        penguin.Eat();
        penguin.Sleep();
        penguin.MakeSound();
    }
}
```

## Summary

A subclass should extend but not contradict the behavior of its superclass. This principle ensures that any client code expecting an instance of the superclass can also work seamlessly with instances of any subclass.

Adhering to LSP promotes robust polymorphic designs where subclasses not only extend but also maintain the expected behavior of their superclass, ensuring code flexibility and reliability in polymorphic scenarios.

---

[Canonical link](https://medium.com/@ravindradevrani/the-liskov-substitution-principle-0017d4609774)
