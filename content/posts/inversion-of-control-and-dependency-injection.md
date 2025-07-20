+++
date = '2025-07-20T16:10:34+05:30'
draft = false
title = 'Inversion of Control - Dependency Injection - Dependency Inversion Principle'
tags = ['oops']
categories= ['programming']
+++

![inversion of control, dependency injection and dependency inversion principle](/images/ioc.webp)

- **Direct or traditional approach:** Object creates its own dependencies.

- **Inverted approach (inversion of control):** Dependencies are created outside the object. This responsibility is given to someone else.

**Example 1 (Direct approach):**

We have a service named `EmailService` which is an implementation of `INotificationService`.

```cs
public interface INotificationService
{
    void SendNotification();
}

public class EmailService : INotificationService
{
    public void SendNotification()
    {
        // code to send notification 
    }
}
```

OrderService need to use the `INotificationService`. 

```cs
public class OrderService
{
    private readonly INotificationService _notificationService;

    public OrderService()
    {
        _notificationService = new EmailService();
    }
}
```

`OrderService` is responsible for creating the instance of `INotificationService`. It is tightly coupled with both `INotificationService` and `EmailService`. It is not that much flexible either, if you want to swap the instance of `EmailService` with `SmsService` you can't do it easily (if it is being used in multiple places).

**Example2: Inversion of control**

```cs
public class OrderService
{
    private readonly INotificationService _notificationService;

    public OrderService(INotificationService notificationService)
    {
        _notificationService = notificationService;
    }
}
```

In this example, `OrderService` is not creating the instance of `INotificationService`, It is being created by the `IOC container`. `OrderService` need and instance of the `INotificationService` implemention (i.e `EmailService`), it asks `IOC container`, hey give me the instance of `EmailService` and it gets what it asked. It is called `inversion of control`. `INotificationService` is injected through the construction injection (a form of dependency injection).

Now our code is:

- Flexible, we can swap `EmailService` with `SmsService`
- Testable
- Loosely coupled
 
`Dependency Injection` is the implementation of inversion of control. We achieve inversion of control through it. It is the most popular implementation of IOC. However it is not the only one, there are other implentations too like template method pattern, service locator pattern, observer pattern etc.

## Dependency inversion principle

It is one of the SOLID principle given by `Uncle Bob`. It says any high level dependencies (eg. `OrderService`) should not directly depend on a low level module (eg. `EmailService`). Implementations (`OrderService` and `EmailService`) should depend on abstractions (`INotificationService`). 

Note that, dependency inject comes with its own challanges. Consider if you really need to use it.