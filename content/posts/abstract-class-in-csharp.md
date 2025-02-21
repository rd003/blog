+++
date = '2025-02-21T09:20:13+05:30'
draft = false
title = 'Abstract Class in Csharp'
tags = ['csharp']
categories= ['programming']
+++

In c#, Abstract class is a class that can not be instantiated on its own

![abstract class in c#](/images/1_7nIXLfpui9Rj0eXs8Wk2-A.png)

- In c#, `Abstract class` is a class that can not be instantiated on its own
- It is typically used as a `base class` for other class.
- `Abstract class` provides a way to achieve [`abstraction`](https://medium.com/@ravindradevrani/abstraction-in-c-c3d4c832942a), because there you can just declare the methods (abstract methods) and implement them later.
- It can contain both `abstract methods` (methods without implementation details) and `non-abstract methods` (method with implementation details).
- Similar goal can be achieved with `interface`, but in abstract class you can also define non-abstract method. These methods are needed when you need to share some common functionality.

```cs
public abstract class Shape
{
 // it is the basic syntax of abstract class
}
```

Example:

```cs
abstract class Shape
{
 public abstract void Draw(); // Abstract method without implementation

    public void Display()  //non abstract method
    {
        Console.WriteLine("Displaying shape...");
    }

}

// concrete class
class Circle : Shape
{
 public override void Draw()
 {
 Console.WriteLine("Drawing a circle");
 }
}

// concrete class
class Square : Shape
{
 public override void Draw()
 {
 Console.WriteLine("Drawing a square");
 }
}

class Program
{
 static void Main()
 {
 Shape circle = new Circle();
 circle.Draw(); // Drawing a circle
 circle.Display(); //Displaying shape...

        Shape square = new Square();
        square.Draw();  // Drawing a square
        square.Display(); //Displaying shape...

    }

}
```

- `Shape` is an `abstract class`, which contains an `abstract method` `Draw()` and `non-abstract` method `Display()`.
- We are defining high level overview of any shape. Whatever shape we will have, it must have a feature `Draw`. Since we don’t know the details of the shape yet (it may be circle, pentagon, rectangle) , we can not define it it advance. `Circle/Rectangle/Pentagon` will have it’s own `draw` method. That’s why `Draw()` method is marked as `abstract-method`. It’s implementation will be defined later.
- Now we have two class `Circle` and `Square.` Each class will inherit the `Shape` class and override the `Draw()` method.

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [February 8, 2024](https://medium.com/p/2dc51b1a7249).

[Canonical link](https://medium.com/@ravindradevrani/abstract-class-in-c-2dc51b1a7249)

Exported from [Medium](https://medium.com) on February 19, 2025.
