+++
date = '2025-02-23T08:19:49+05:30'
draft = false
title = 'Composition:  What, Why And When?'
tags = ['oops']
categories=['programming']
image = '/images/1_YArOSlj41qOCfuCBcvZ_5w.png'
+++

<!-- ![what is composition?](/images/1_YArOSlj41qOCfuCBcvZ_5w.png) -->

**Composition** is when your class is composed of one or more objects from other classes. A simple example is a `Car` composed of `Engine` and `Wheel` objects. **Inheritance** defines an **"is-a"** relationship, while **composition** defines a **"has-a"** relationship.

For example, `Dog` **is-a** `Animal`, and `Circle` **is-a** _Shape_. It defines inheritance.

This makes sense because you want to reuse all the features of `Animal` (eat, sleep, walk, makeNoise) in the `Dog` class. `Cow` is-a Animal too, so `Cow` can also inherit the `Animal` class. Since **cows** and **dogs** make different noises and eat different things, we have to redefine or override the `makeNoise()` and `eat()` methods in the `Dog` and `Cow` classes. The point is when we want to reuse the functionality of a class and also want subtype polymorphism (`Dog` and `Cow` are subtypes of `Animal`), then we must use **inheritance**.

A `Car` needs an **engine** and **wheels**. Does it make sense to say a `Car` **is-an** `Engine`? I guess not. A `Car` **has-an** `Engine`, and a `Car` **has-a** `Wheel`. It makes complete sense. Here, we just want to reuse the functionality of the `Engine` and `Wheel` classes, not the subtype polymorphism. So, we need **composition**, not **inheritance**. We can take another real-life example: a `House` **has-a** `Room` (not `House` **is-a** `Room`).

**Note:** In composition, if the main class is destroyed, then the objects it is composed of will be destroyed too. Composed objects cannot live outside the main object.

In our example, if the `Car` object is destroyed, then the `Wheels` and `Engine` will be destroyed too because we are instantiating these classes inside the `Car` class.

UML-ish representation of the example

![uml diagram of composition](/images/1_8rpnyEPf6cJJDZpxHanSpg.jpg)

Here is a practical example written in Java but also applicable in C#.

Engine class

```java
public class Engine {
 private String type;
 public Engine(String type) {
 this.type = type;
 }
 public String getType() {
 return type;
 }
}
```

Wheel class

```java
public class Wheel {
 private int size;
 public Wheel(int size) {
 this.size = size;
 }
 public int getSize() {
 return size;
 }
}
```

Car class

```java
 public class Car {
    private Engine engine;
    private Wheel[] wheels;

    public Car(String engineType,int wheelSize) {
        this.engine = new Engine(engineType);
        this.wheels = new Wheel[4];

        for (int i = 0; i < wheels.length; i++) {
            this.wheels[i]= new Wheel(wheelSize);
        }
    }
    public Engine getEngine() {
        return engine;
    }

    public Wheel[] getWheels() {
        return wheels;
    }
    public void displayDetails() {
        System.out.println("Car Engine Type: " + engine.getType());
        System.out.println("Wheel Size: " + wheels[0].getSize());
    }
}
```

Car Test Drive

```java
public class CarTestDrive {
 public static void main(String[] args) {
    Car car = new Car("v8", 17);
    car.displayDetails();
 }
}
```

`Engine` and `Wheel` objects are instantiated inside the `Car` class. If we destroy the car object, wheels and engine will be destroyed too. Wheel and Engine can not exist without the car object.

### Advantages of composition

#### **Flexibility and code reusability**

The `Engine` and `Wheel` classes can be reused in other contexts, not just within the `Car` class. For example, they could be used in a `Truck` or `Motorcycle` class.

Also, you can easily plug-in a new feature in your car. You just have to create a new class and use it’s object in the class car.

#### Loose Coupling

Changes to the `Engine` or `Wheel` class are less likely to affect the Car class, as they are loosely coupled through well-defined interfaces.

#### Encapsulation

The internal details of `Engine` and `Wheel` are hidden from the `Car` class. The `Car` class only interacts with these objects through their public methods.

#### Improved Modularity

Each component (Engine, Wheel, Car) can be developed and tested independently, enhancing modularity.

### Summary

Composition is when an object is composed of one or more objects. Use **composition** if you want to reuse the functionality of a class and do not want subtype polymorphism. If you need to reuse the functionality of a class and you also want to use subtype polymorphism then consider the **inheritance.**

[**Understanding Aggregation: How It Differs from Composition**  
Aggregation is when an object is made up of one or more objects, but those objects can live outside the main object. It…](/posts/aggregation-in-oops)

[Canonical link](https://medium.com/@ravindradevrani/composition-what-why-and-when-aa43cebb3494)
