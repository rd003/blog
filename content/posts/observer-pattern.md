+++
date = '2025-02-23T10:44:51+05:30'
draft = false
title = 'Observer Pattern'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_RRtdvbSlzrYKi9k4Sw1E8w.png'
+++

<!-- ![Observer pattern in c#](/images/1_RRtdvbSlzrYKi9k4Sw1E8w.png) -->

The **Observer pattern** is a **behavioral design pattern** that defines a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically.

In a simple words, it is like a publisher and subscriber pattern. When publisher publishes something, all it’s subscriber gets notified.

One Example could be, when we subscribe someone’s mailing list we get notified whenever the publisher publishes something.

## Key terms

- **Subject or Observable :** It is a publisher object
- **Observer:** An object that subscribes the subject

## Let’s understand it with an example

Imagine a **simple clock system** where multiple displays (digital and analog) need to show the current time. When the time changes, all displays should update accordingly.

We have a central system (the Clock) that provides the current time. Whenever the time of central system is updated, the time of digital and analog display will be updated too.

Now we can relate the key terms of observer pattern with this example.

**Subject or Observable: Clock** would be the subject here. It have the current time. Any changes to the current time would be immediately notified to the observers.

**Observers: Digital clock and analog clock** are the the observers, which displays the time provided by the clock.

Let’s implement the example

### Subject

```cs
public class Clock
{
 private List<IClockObserver> observers = new List<IClockObserver>();
 private DateTime currentTime;

    public void SetTime(DateTime time)
    {
        currentTime = time;
        NotifyObservers();
    }

    public void RegisterObserver(IClockObserver observer)
    {
        observers.Add(observer);
    }

    public void UnregisterObserver(IClockObserver observer)
    {
        observers.Remove(observer);
    }

    public void NotifyObservers()
    {
        foreach (IClockObserver observer in observers)
        {
            observer.Update(currentTime);
        }
    }

}
```

Clock is the subject. It have the **currentTime** as the state. It has the responsibility of **registering** and **unregistering** the observer. It also have the **NotifyObservers** method, which notifies the observers about the change in state.

Whenever the current time is changed, the **NotifyObservers** method will be called immediately.

### Observer

```cs
public interface IClockObserver
{
 void Update(DateTime time);
}
```

**IClockObserver** is the observer interface which have the **Update** method which basically updates the current time.

When the Subject(**Clock)** updates the state **(currentTime)** , it calls the observer’s **Update** method and pass the latest state **(currentTime)** to it.

### Concrete observers

We have two concrete observers, the **DigitalClock** and the **AnalogClock**, which implements the observer **IClockObserver.**

```cs
public class DigitalClock : IClockObserver
{
 public void Update(DateTime time)
 {
 Console.WriteLine($"Digital Clock : {time.ToString("hh:mm:ss tt")}");
 }
}

public class AnalogClock : IClockObserver
{
 public void Update(DateTime time)
 {
 Console.WriteLine($"Analog Clock : {time.ToString("hh:mm:ss tt")}");
 }
}
```

Change in the **subject(Clock)** would be immediate notified to the **obsrevers(DigitalClock,AnalogClock).**

### Usage

```cs
public class ClockTest
{
    public static void Main()
    {
        Clock clock \= new Clock();

        DigitalClock digitalClock \= new DigitalClock();
        clock.RegisterObserver(digitalClock);

        AnalogClock analogClock \= new AnalogClock();
        clock.RegisterObserver(analogClock);

        clock.SetTime(DateTime.Now);
        clock.SetTime(DateTime.Now.AddSeconds(12));

        // unregistering the digital clock.
        clock.UnregisterObserver(digitalClock);
        clock.SetTime(DateTime.Now.AddSeconds(15));

        Console.ReadLine();
    }
}
```

Only the registered observers gets the state of the subject. When we unregister any observes, it no longer recieve the updates from the subject.

## Benefits

- **Decoupling:** The clock and displays are decoupled, making it easy to add or remove displays without affecting the clock.
- **Extensibility:** New displays can be added without modifying the clock’s code.
- **Flexibility:** Displays can be registered and unregistered at runtime.

## Conclusion

The Observer pattern is a powerful tool for managing one-to-many dependencies between objects. In this simple clock example, we’ve seen how it can be used to decouple the clock from its displays, making the system more flexible and extensible

[Canonical link](https://medium.com/@ravindradevrani/observer-pattern-with-c-example-f723c5204447)
