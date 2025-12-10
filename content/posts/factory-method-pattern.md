+++
date = '2025-02-23T10:19:59+05:30'
draft = false
title = 'Factory Method Pattern with c#'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_5oURcquFv1Ch9ct5rf-yFw.png'
+++

<!-- ![factory method pattern in c#](/images/1_5oURcquFv1Ch9ct5rf-yFw.png) -->

The **Factory Method Pattern** is a creational design pattern that provides an interface for creating objects in a superclass but allows subclasses to alter the type of objects that will be created.

This pattern is useful when a class cannot anticipate the class of objects it needs to create or when subclasses want to specify the objects to be created.

## A Notification System

Imagine we need to develop a notification system that can send different types of notifications such as Email, SMS, and Push Notifications. Each type of notification has a distinct implementation but shares a common interface. Instead of creating each notification type directly in our main logic, we can use the **Factory Method Pattern** to encapsulate the instantiation process, making our code more modular and extensible.

### Product

First we defines a common interface for all types of notifications. Each notification must implement the `Send` method.

```cs
public interface INotification
{
 void Send(string message);
}
```

### Concrete Products

This defines the implementation of the product interface (i.e `INotification`) and each implementations have it’s own `Send` method.

```cs
// Concrete Product 1
public class EmailNotification : INotification
{
 public void Send(string message)
 {
 Console.WriteLine($"Email sent..\\n msg: {message}");
 }
}

// Concrete Product 2
public class SmsNotification : INotification
{
 public void Send(string message)
 {
 Console.WriteLine($"Sms sent..\\n msg: {message}");
 }
}

// Concrete Product 3
public class PushNotification : INotification
{
 public void Send(string message)
 {
 Console.WriteLine($"Push notification sent..\\n msg: {message}");
 }
}
```

We have **three** implementations of **INotification : EmailNotification, SmsNotification and PushNotification** and each one have it’s own implementation of the `Send` method.

### Creator or Abstract Creator

It is responsible for declaring the factory method which creates and returns the instance of the product. Let’s create the creator class.

```cs
public abstract class NotificationCreator
{
 protected abstract INotification CreateNotification(); // factory method

    public void Notify(string message)
    {
        INotification notification = CreateNotification();
        notification.Send(message);
    }

}
```

- `NotificationCreator` is an abstract class that declares the factory method `CreateNotification`, which must be implemented by its subclasses. This method is responsible for creating and returning an instance of a class that implements the `INotification` interface.
- The `NotificationCreator` class also includes a `Notify` method that uses the factory method to obtain a notification object and then sends a message using that object. It does not need to know the specifics of the actual object; it only requires that the object conforms to the `INotification` interface. The specific implementation (such as `SmsNotification`, `EmailNotification`, or `PushNotification`) is determined by the subclass.

### Concrete Creators

Concrete creators override the factory method to return an instance of a specific product.

```cs
// concrete creator
public class EmailNotificationCreator : NotificationCreator
{
 protected override INotification CreateNotification()
 {
 return new EmailNotification();
 }
}

// concrete creator
public class SmsNotificationCreator : NotificationCreator
{
 protected override INotification CreateNotification()
 {
 return new SmsNotification();
 }
}

// concrete creator
public class PushNotificationCreator : NotificationCreator
{
 protected override INotification CreateNotification()
 {
 return new PushNotification();
 }
}
```

These classes are inherited from the `NotificationCreator` and overrides the `CreateNotification` method to return an instance of the specific notification type.

### Let’s test the system

```cs
public class NotificationTest
{
    public static void Main()
    {
        NotificationCreator creator;

        creator = new EmailNotificationCreator();
        creator.Notify("Hello");

        creator = new SmsNotificationCreator();
        creator.Notify("Hello again");

        Console.ReadLine();
    }
}
```

## **When to use?**

- When the exact type of object needs to be determined at a runtime.
- When a class can not anticipate the class of objects it needs to create.

## Benefits of Using the Factory Method Pattern

1. **Flexibility**: You can easily add new types of notifications without changing existing code. For example, adding a new `WhatsAppNotification` would only require creating a new class and a corresponding creator.
2. **Separation of Concerns**: The `NotificationCreator` class handles the creation of notifications, while the concrete notification classes handle the specifics of sending notifications. This separation makes the code easier to manage and understand.
3. **Single Responsibility Principle**: Each class has a single responsibility. The creator classes are responsible for creating notifications, and the notification classes are responsible for sending notifications.

## Conclusion

The **Factory Method Pattern** is a powerful design pattern that promotes flexibility and maintainability in your code. By encapsulating the instantiation logic in separate classes, you make your code more modular and easier to extend. In our example, we used this pattern to create a **notification system** that can send different types of notifications seamlessly.

---

[Canonical link](https://medium.com/@ravindradevrani/understand-the-factory-method-pattern-with-c-a20c8f3003b6)
