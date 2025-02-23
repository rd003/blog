+++
date = '2025-02-22T21:35:42+05:30'
draft = false
title = 'The Interface Segregation Principle (ISP)'
tags = ['design-patterns','SOLID']
category = ['programming']
+++

![what is Interface Segregation Principle?](/images/ISP.jpg)

📢 Clients should not be forced to depend on interfaces they do not use.

In simpler terms, this principle suggests that an interface should not include methods that implementing classes don’t need. It Encourages us to create smaller interfaces over the big fat interface.

Other SOLID principles

- [Single Responsibility Principle](/posts/single-responsibility-principle/)
- [Open Closed Principle](/posts/open-closed-principle/)
- [Liskov Substitution Problem](/posts/liskov-substitution-principle/)
- [Dependency Inversion Principle](/posts/dependency-inversion-principle/)

## Violating example

Imagine you have an interface for workers in a company:

```cs
public interface IWorker
{
  void Work();
  void Eat();
  void Sleep();
}

public class Robot : IWorker
{
    public void Work()
    {
        Console.WriteLine("Robot is working.");
    }

    public void Eat()
    {
        // Robots don't eat, so this method is unnecessary for this class
        throw new NotImplementedException();
    }

    public void Sleep()
    {
        // Robots don't sleep, so this method is unnecessary for this class
        throw new NotImplementedException();
    }

}

public class HumanWorker : IWorker
{
    public void Work() => Console.WriteLine("Human is working.");

    public void Eat() => Console.WriteLine("Human is eating.");

    public void Sleep() => Console.WriteLine("Human is sleeping.");

}
```

In this example, `IWorker` interface forces the `Robot` class to implement methods (`Eat` and `Sleep`). But robot does not need to have these functionalities. It is violating the ISP because **Robot** is forced to use **Eat()** and **Sleep()** methods.

## Corrected Example

Now, let’s refactor this design to adhere to the Interface Segregation Principle:

```cs
public interface IWorkable
{
    void Work();
}

public interface IFeedable
{
    void Eat();
}

public interface ISleepable
{
    void Sleep();
}

public class Robot : IWorkable
{
    public void Work() => Console.WriteLine("Robot is working.");
}

public class HumanWorker : IWorkable, IFeedable, ISleepable
{
    public void Work() => Console.WriteLine("Human is working.");

    public void Eat() => Console.WriteLine("Human is eating.");

    public void Sleep() => Console.WriteLine("Human is sleeping.");
}
```

In the refactored example, we have split the `IWorker` interface into three smaller interfaces: `IWorkable`, `IFeedable`, and `ISleepable`. Each class is free to choose the interface it needs. Now, the `Robot` class have to implement `IWorkable` interface only. While the `HumanWorker` class implements all three interfaces.

By splitting interfaces into more specific ones, we adhere to the **Interface Segregation Principle**, making the code more modular, easier to maintain, and less prone to errors.

---

[Canonical link](https://medium.com/@ravindradevrani/the-interface-segregation-principle-isp-eae6ae0dcdae)
