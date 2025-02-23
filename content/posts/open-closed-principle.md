+++
date = '2025-02-22T19:24:26+05:30'
draft = false
title = 'Open Closed Principle (OCP)'
tags = ['design-patterns','SOLID']
categories = ['programming']
+++

![open closed principle in c#](/images/1_WDgbogkM-XrxUPlXfOX2Zg.webp)

The **Open-Closed Principle** is one of the five **SOLID** principles. It states that a class should be open for extension but closed for modification. In other words, you should be able to add new functionality without changing existing code.

Once you have written your class, it should not be modified in the future. However, this doesn’t mean you cannot modify your class during early development stages. It means that once your application or software is in production and you want to introduce the new functionality, you should extend that class rather than modifying it.

### How do I add new functionality if I can not modify the class

Create a new class by extending (inheriting) the existing class and introduce the new functionality there. Although it can be achieved with composition and delegation.

### Other SOLID principles

- [Single Responsibility Principle](/posts/single-responsibility-principle/)
- [Liskov Substitution Problem](/posts/liskov-substitution-principle/)
- [Interface Segregation Principle](/posts/interface-segregation-principle/)
- [Dependency Inversion Principle](/posts/dependency-inversion-principle/)

### Example that violates OCP

Let’s consider an application that draws shapes (e.g. circles, rectangles). Our goal is to design this application.

Write the `Circle` and `Rectangle` classes to draw their respective shapes.

```cs
public class Circle
{
    public void Draw()
    {
        Console.WriteLine("Drawing a circle");
    }
}

public class Rectangle
{
    public void Draw()
    {
        Console.WriteLine("Drawing a rectangle");
    }
}
```

We need some constants for various shape type. Enum can solve the problem.

```cs
public enum ShapeType
{
    Circle,
    Rectangle,
    Square
}
```

Create a class where we can draw a shape.

```cs
public class Shape
{
    public void Draw(ShapeType shapeType)
    {
        switch (shapeType)
        {
            case ShapeType.Circle:
                DrawCircle();
                break;

            case ShapeType.Square:
                DrawSquare();
                break;

            case ShapeType.Rectangle:
                DrawRectangle();
                break;

            default:
                Console.WriteLine("Invalid shape type");
                break;
        }
    }

    private void DrawCircle()
    {
        Console.WriteLine("Drawing Circle");
    }

    private void DrawSquare()
    {
        Console.WriteLine("Drawing Square");
    }

    private void DrawRectangle()
    {
        Console.WriteLine("Drawing Rectangle");
    }
}
```

Let’s create an actual interface, where we can test this application.

```cs
public class ShapeTest
{
  public static void Main()
  {
      Shape shape = new Shape();

      // Draw a circle
      shape.Draw(ShapeType.Circle);
  }
}
```

This application seems okay. To draw a shape, we just need a `Shape` object. We call the `Draw()` method of the shape object, pass the shape type, and it will do the job. The `Shape` object seems pretty straightforward. It has a draw method that takes the shape type and prints that shape.

### If it is doing it’s job perfectly, what is the problem then?

Let’s say we want to draw a new shape called `Triangle`. Ok, that is pretty straightforward.

- Introduce the new shape type in the `ShapeType` enum.

```cs
public enum ShapeType
{
    Circle,
    Rectangle,
    Square,
    Triangle
}
```

- Modify the `Draw()` method in the `Shape` class. Introduce a new case in the `Draw()` method.

```cs
public class Shape
{
    public void Draw(ShapeType shapeType)
    {
        switch (shapeType)
        {
            // other cases

            // introducing new case for triangle

            case ShapeType.Triangle:
                DrawTriangle();
                break;

            // default case
        }
    }

    // other Draw methods

    private void DrawTriangle()
    {
        Console.WriteLine("Drawing Triangle");
    }
}
```

Wow, you see, we have added new functionality without encountering too many problems.

Okay, let’s add a few more shapes to our system. I assume you now understand the problem.

Every time we introduce a new shape, we have to modify the `Draw()` method. What if it introduces a bug in the `Draw()` method? All the classes that depend on `Shape` will break if the `Draw()` method has a bug. Additionally, you’ll need to test the shape class again.

### So what is the solution?

Well, there are solutions like inheritance/polymorphism, strategy pattern, visitor pattern and etc.. etc. Let’s solve it inheritance.

#### Redesign our application to follow OCP (using inheritance/polymorphism)

Let’s create an interface `Shape` class which contains a `Draw()` method's.

```cs
public interface IShape
{
    void Draw();
}
```

We can also use the **abstract class** instead of **interface**.

```cs
public abstract class Shape
{
    public abstract void Draw();
}
```

#### Why am I using the Interface instead of Abstract Class?

Because we do not have any method that we want to reuse in the derived class, there is no need for an abstract class. You can use it if you want, and it won’t make any difference in functionality. However, it does not make sense to me to use an abstract class, so I am sticking with an interface.

Let’s create the Circle, Rectangle, and Triangle classes that implement the `IShape` interface.

```cs
public class Circle : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a circle");
    }
}

public class Rectangle : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a rectangle");
    }
}

public class Triangle : IShape
{
    public void Draw()
    {
        Console.WriteLine("Drawing a triangle");
    }
}
```

Let’s refactor our ShapeTest class.

```cs
public class ShapeTest
{
    public static void Main()
    {
        // Drawing a circle
        IShape circle \= new Circle();
        circle.Draw();

        //Drawing a rectangle
        IShape rectangle \= new Rectangle();
        rectangle.Draw();

        // Drawing a triangle
        IShape triangle \= new Triangle();
        triangle.Draw();
    }

}
```

Or you can improve it a bit.

```cs
public class ShapeTest
{
    public static void Main()
    {
        // Drawing a circle
        DrawShape(new Circle());

        //Drawing a rectangle
        DrawShape(new Rectangle());

        // Drawing a triangle
        DrawShape(new Triangle());
    }

    private static void DrawShape(IShape shape)
    {
        shape.Draw();
    }

}
```

Now our application is very flexible. It is open for extension. You can add any number of shape without touching the existing code.

#### Solution with strategy pattern

Create the interface `ShapeDrawStrategy` which have `Draw()` method and it's implementations `CircleDrawStrategy` and `RectangleDrawStrategy`.

```cs
public interface IShapeDrawStrategy
{
    void Draw();
}

public class CircleDrawStrategy : IShapeDrawStrategy
{
    public void Draw()
    {
        Console.WriteLine("Drawing a circle");
    }
}

public class RectangleDrawStrategy : IShapeDrawStrategy
{
    public void Draw()
    {
        Console.WriteLine("Drawing a rectangle");
    }
}
```

Create the `Shape` abstract class and it's derived concrete classes.

```cs
public abstract class Shape
{
    protected IShapeDrawStrategy shapeDrawStrategy;

    public void Draw()
    {
        shapeDrawStrategy.Draw();
    }

}

public class Rectangle : Shape
{
    public Rectangle()
    {
        shapeDrawStrategy = new RectangleDrawStrategy();
    }
}

public class Circle : Shape
{
    public Circle()
    {
        shapeDrawStrategy = new CircleDrawStrategy();
    }
}
```

Create a class `ShapeTestDrive` to test the application.

```cs
public class ShapeTestDrive
{
    public static void Main()
    {
        // drawing a circle
        Shape circle \= new Circle();
        circle.Draw();

        // drawing a rectangle
        Shape rectangle \= new Rectangle();
        rectangle.Draw();
    }
}
```

It is another way to achieve the same result. There is no one-size-fits-all solution. In our case, the first solution is more suitable and straightforward for the simple functionality of drawing a shape. However, if our class were more complex and had multiple methods, the strategy pattern would be a more appropriate solution. I recommend learning more about the strategy pattern. A book I can recommend is “**Head First Design Patterns** **by Eric Freeman, Elisabeth Robson, Bert Bates, Kathy Sierra**”.

### Summary

In my opinion, it does not mean, one should never change the code. What it means to me, we should try to design our classes in a flexible way so that one could introduced new behavior easily and reuse the code. Software always changes, new features/requirements always comes. Any principle is not the god’s saying. You have to choose it according to your need and what fit’s best in your situation. If you want to read other peoples discussion on OCP, you can check them out below.

### References

1. [What is the meaning and reasoning behind the Open/Closed Principle?](https://stackoverflow.com/questions/59016/what-is-the-meaning-and-reasoning-behind-the-open-closed-principle "https://stackoverflow.com/questions/59016/what-is-the-meaning-and-reasoning-behind-the-open-closed-principle")
2. [Clarify the Open/Closed Principle](https://softwareengineering.stackexchange.com/questions/19627/clarify-the-open-closed-principle "https://softwareengineering.stackexchange.com/questions/19627/clarify-the-open-closed-principle")
3. [Why Are So Many Of The Framework Classes Sealed: Microsoft blog](https://learn.microsoft.com/en-in/archive/blogs/ericlippert/why-are-so-many-of-the-framework-classes-sealed "https://learn.microsoft.com/en-in/archive/blogs/ericlippert/why-are-so-many-of-the-framework-classes-sealed")

---

[Canonical link](https://medium.com/@ravindradevrani/ssolid-principles-2-open-close-principle-ocp-e4c3eb2dbdd3)
