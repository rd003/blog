+++
date = '2025-02-23T11:07:40+05:30'
draft = false
title = 'Facade Pattern With C#'
tags = ['design-patterns']
categories = ['programming']
image = 'https://cdn-images-1.medium.com/max/800/1*bz4k8n2SUByW5GfAmVJsVw.png'
+++

<!-- ![Facade Design Pattern (with c# example)](https://cdn-images-1.medium.com/max/800/1*bz4k8n2SUByW5GfAmVJsVw.png) -->

The **Facade pattern** is a **structural design pattern** that provides a simplified interface to a complex system of classes or interfaces.

Let’s understand it with example. Imagine a **home automation system**.

![home automation system](/images/1_JllHeIOXl6B2flbICm7jdg.png)

Let’s implement it programmatically.

```cs
public class FacadePatternTestDrive
{
    public static void Main(string[] args)
    {
        ILights lights = new Lights();
        IAirConditioner airConditioner = new AirConditioner();
        ISecuritySystem securitySystem = new SecuritySystem();

        // When leaving home
        lights.TurnOff();
        airConditioner.TurnOff();
        securitySystem.Arm();
        Console.WriteLine("You have left home.");

        // When entering home
        lights.TurnOn();
        airConditioner.TurnOn();
        securitySystem.Disarm();
        Console.WriteLine("Welcome home!");
    }

}
```

**Note:** AirConditioner, SecuritySystem and Lights class is not present in the above example for the sake of simplicity. We will write those classes when we implement the facade pattern.

## Subsystems

AirConditioner, SecuritySystem and Light classes are the subsystem of the application.

## Problem

The main flaw with this design is, client have to manually follow all the steps on leaving and entering the house. Client have to deal with the complexity. Right now our home automation system is very simple (for the sake of simplicity), it have three subsystems only. What if we have lots of subsystems and client have to follow lots of complex steps on entering and leaving the home.

## Solution

All the complexities should be encapsulated out of the client system and moved to a facade class.

Let’s define our subsystems first.

```cs
// Subsystem 1: Lights
public interface ILights
{
 void TurnOff();
 void TurnOn();
}

public class Lights : ILights
{
    public void TurnOn() => Console.WriteLine("Lights are ON");

    public void TurnOff() => Console.WriteLine("Lights are OFF");

}

// Subsystem 2: AirConditioner
public interface IAirConditioner
{
 void TurnOff();
 void TurnOn();
}

public class AirConditioner : IAirConditioner
{
    public void TurnOn() => Console.WriteLine("Air Conditioner is ON");

    public void TurnOff() => Console.WriteLine("Air Conditioner is OFF");
}

// Subsystem 3: SecuritySystem
public interface ISecuritySystem
{
 void Arm();
 void Disarm();
}

public class SecuritySystem : ISecuritySystem
{
    public void Arm() => Console.WriteLine("Security System is ARMED");

    public void Disarm() => Console.WriteLine("Security System is DISARMED");
}
```

We have defined **AirConditioner**, **SecuritySystem** and **Lights** subsystems. Home automation system have to interact with each subsystem on leaving and entering to the house.

Let’s define our `HomeAutomationFacade` class.

```cs
public class HomeAutomationFacade
{
    private readonly ILights _lights;
    private readonly IAirConditioner _airConditioner;
    private readonly ISecuritySystem _securitySystem;

    public HomeAutomationFacade(ILights lights, IAirConditioner airConditioner, ISecuritySystem securitySystem)
    {
        _lights = lights;
        _airConditioner = airConditioner;
        _securitySystem = securitySystem;
    }

    public void LeaveHome()
    {
        _lights.TurnOff();
        _airConditioner.TurnOff();
        _securitySystem.Arm();
        Console.WriteLine("You have left home.");
    }

    public void EnterHome()
    {
        _lights.TurnOn();
        _airConditioner.TurnOn();
        _securitySystem.Disarm();
        Console.WriteLine("Welcome home!");
    }

}
```

The `HomeAutomationFacade` class ties together the various subsystems, providing a simple interface with two methods: `LeaveHome()` and `EnterHome()`. When you leave home, the facade turns off the lights and air conditioner and arms the security system. When you enter home, it turns on the lights and air conditioner and disarms the security system.

Let’s define the client of the application.

```cs
public class FacadePatternTestDrive
{
    public static void Main(string[] args)
    {
        ILights lights = new Lights();
        IAirConditioner airConditioner = new AirConditioner();
        ISecuritySystem securitySystem = new SecuritySystem();

        HomeAutomationFacade facade = new HomeAutomationFacade(lights, airConditioner, securitySystem);

        // When leaving home
        facade.LeaveHome();

        // When entering home
        facade.EnterHome();
    }

}
```

### Output

```sh
Lights are OFF
Air Conditioner is OFF
Security System is ARMED
You have left home.
Lights are ON
Air Conditioner is ON
Security System is DISARMED
Welcome home!
```

Now, client have very simple interface for using the home automation system. It just have to use the `HomeAutomationFacade` class. On leaving the home we have to call the `LeaveHome` method and on entering the home client have to call the `EnterHome` method.

## When to Use the Facade Pattern

The Facade Pattern is particularly useful when:

- You want to provide a simple interface to a complex subsystem.
- You want to decouple the client from the complex subsystems.

## Conclusion

The **Facade Design Pattern** is a powerful tool for simplifying complex systems by providing a single, unified interface to multiple subsystems. By using a facade, you can reduce the complexity of client code and make your system more maintainable.

---

[Canonical link](https://medium.com/@ravindradevrani/facade-design-pattern-with-c-example-6b2dfe3ec03d)
