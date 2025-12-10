+++
date = '2025-02-23T10:29:26+05:30'
draft = false
title = 'Abstract Factory Pattern With C#'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_W32QuVMnpP6_DEGtHsk75Q.png'
+++

<!-- ![Abstract factory pattern (with c# example)](/images/1_W32QuVMnpP6_DEGtHsk75Q.png) -->

The **Abstract Factory pattern** is a creational design pattern that **provides an interface for creating families of related or dependent objects without specifying their concrete classes**. It allows a client to create objects from a variety of related classes without needing to know the specifics of their implementations.

## GUI Factory Example

Let’s say, we need to create GUI components for different themes in our application. Each theme includes a consistent set of components such as buttons and checkboxes. We want to ensure that the creation of these components is consistent and interchangeable.

### Products or abstract products

First define the products that our factory is going to create.

```cs
// Abstract Product A
public interface IButton
{
 void Render();
}

// Abstract Product B
public interface ICheckbox
{
 void Render();
}
```

Each **family** will consist of **two** products **button** and **checkbox** (i.e `IButton` and `ICheckBox`).

### Concrete Products

The products are just abstractions so we need to implement them. These implementations are called concrete products.

- **IButton** have two implementations **DarkButton** and **LightButton**
- **ICheckBox** have two implementations **DarkCheckBox** and **LightCheckBox**

```cs
// Concrete Product A1
public class LightButton : IButton
{
 public void Render()
 {
 Console.WriteLine("Rendering a light button");
 }
}

// Concrete Product A2
public class DarkButton : IButton
{
 public void Render()
 {
 Console.WriteLine("Rendering a dark button");
 }
}

// Concrete Product B1
public class LightCheckbox : ICheckbox
{
 public void Render()
 {
 Console.WriteLine("Rendering a light checkbox");
 }
}

// Concrete Product B2
public class DarkCheckbox : ICheckbox
{
 public void Render()
 {
 Console.WriteLine("Rendering a dark checkbox");
 }
}
```

### Abstract Factory

It declare methods, which are responsible for creating the products.

```cs
public abstract class GUIFactory
{
 public abstract IButton CreateButton();
 public abstract ICheckbox CreateCheckbox();
}
```

**GUIFactory** declare two methods:

- **CreateButton** of return type **IButton**
- and **CreateCheckBox** of return type **ICheckBox**.

### Concrete Factories

Concrete factory implements the abstract factory. Let’s implement the **LightThemeFactory** and **DarkThemeFactory.**

```cs
// Concrete Factory 1
public class LightThemeFactory : GUIFactory
{
    public override IButton CreateButton()
    {
    return new LightButton();
    }

    public override ICheckbox CreateCheckbox()
    {
        return new LightCheckbox();
    }

}

// Concrete Factory 2
public class DarkThemeFactory : GUIFactory
{
    public override IButton CreateButton()
    {
    return new DarkButton();
    }

    public override ICheckbox CreateCheckbox()
    {
        return new DarkCheckbox();
    }

}
```

- The **LightThemeFactory** creates and returns the instances of **LightButton** and **LightCheckBox**.
- The **DarkThemeFactory** creates and returns the instances of **DarkButton** and **DarkCheckBox**.

### Client

The client uses the abstract factory to create and interact with the products.

```cs
public class Application
{
    private readonly IButton _button;
    private readonly ICheckbox _checkbox;

    public Application(GUIFactory guiFactory)
    {
        _button = guiFactory.CreateButton();
        _checkbox = guiFactory.CreateCheckbox();
    }

    public void Render()
    {
        _button.Render();
        _checkbox.Render();
    }

}
```

### Let’s test this

```cs
public class GuiFactoryTest
{
    public static void Main()
    {
        // Light theme client
        GUIFactory lightFactory = new LightThemeFactory();
        Application lightApp = new Application(lightFactory);
        lightApp.Render();

        // Dark theme client
        GUIFactory darkFactory = new DarkThemeFactory();
        Application darkApp = new Application(darkFactory);
        darkApp.Render();

        Console.ReadLine();
    }

}
```

### Families of objects

- **Button** and **CheckBox** makes one family.
- **Abstract factory** is responsible for creating the family of objects.
- The **LightThemeFactory** is responsible for creating the family of objects **(LightButton+LightCheckBox).**
- The **DarkThemeFactory** is responsible for creating the different family of objects **(DarkButton+DarkCheckbox).**

## When to use?

When your system needs to create multiple families of related or dependent objects, the Abstract Factory pattern ensures that these objects are created together. This helps maintain consistency across related objects.

## Advantages

- **Encapsulation**: Encapsulates the creation logic for a set of related products.
- **Consistency**: Ensures that related products are created together and are compatible.
- **Flexibility**: Makes it easy to introduce new product families without altering the client code.
- **Decoupling**: Decouples the client code from the concrete classes, reducing dependency and enhancing flexibility.

## Disadvantages

- **Complexity**: Introduces additional complexity with multiple interfaces and factory classes.
- **Overhead**: May add unnecessary overhead if the number of product families or the complexity of object creation is low.

## Key Difference with Factory Method Pattern

**1. Scope:**

- **Factory Method:** Focuses on a single product.
- **Abstract Factory:** Focuses on a family of products.

**2. Responsibility:**

- **Factory Method:** Relies on subclasses to define the actual product creation.
- **Abstract Factory:** Provides an interface for creating related products, and concrete factories implement this interface.

## Conclusion

The **Abstract Factory pattern** is useful when you need to create **families of related objects**. It ensures that the creation process is consistent and that the client code is decoupled from the concrete classes. This pattern is particularly useful when you anticipate adding new product families in the future or when you need to enforce the use of related products together.

---

[Canonical link](https://medium.com/@ravindradevrani/abstract-factory-pattern-with-c-example-e2293bb3d611)
