+++
date = '2025-02-20T19:49:29+05:30'
draft = false
title = 'Polymorphism in depth with Csharp'
tags = ['oops']
categories=['programming'] 
+++

![polymorphism in csharp](/images/polymorphism.png)

Polymorphism is one of the core concept of object oriented programming. Word **polymorphism = poly (many) + morphism (forms)**. As it’s name suggesting polymorphism means, an entity can have multiple forms.

**Other oops core concepts :**

- [Abstraction in C#](/posts/abstraction-in-csharp/)
- [Encapsulation in C#](/posts/encapsulation-in-csharp/)
- [Inheritance in c#](/posts/inheritance-in-csharp/)

Let’s learn polymorphism through mistakes.

Jim requires an entry system for his pet shop, which exclusively houses various breeds of dogs. This system will manage the entry and records of all dogs entering and exiting the premises.

![pet shop](/images/1_fOe1CgsARNML9WBcdQtDwg.jpg)

Photo by [Nancy Guth](https://www.pexels.com/photo/photography-of-three-dogs-looking-up-850602/) from Pexels

It is easy, right… So lets create the system.

```cs
public class Dog
{
    public string Name { get; }
    public string Breed { get; }
    public string Color { get; }

    public Dog(string name, string breed, string color)
    {
    Name = name;
    Breed= breed;
    Color = color;
    }

    public void Eat()
    {
    Console.WriteLine("Eating");
    }

    public void Sleep()
    {
    Console.WriteLine("Sleeping");
    }

    public void MakeSound()
    {
    Console.WriteLine("Woff!");
    }
}

public class PetShopEntrySystem
{
    private List<Dog> dogs;

    public PetShopEntrySystem()
    {
        dogs = new List<Dog>();
    }

    public void AddDog(Dog dog)
    {
        dogs.Add(dog);
    }

    public IEnumerable<Dog> GetDogs()
    {
        return dogs;
    }
}

public class PetshopEntrySimulator
{
    static void Main()
    {
        Dog dog1 = new Dog("Max", "Golden Retriever", "Golden");
        Dog dog2 = new Dog("Luna", "Sibarian Husky", "Grey/White");
        Dog dog3 = new Dog("Duke", "Labrador Retriever", "Chocolate Brown");

        PetShopEntrySystem entrySystem = new PetShopEntrySystem();
        entrySystem.AddDog(dog1);
        entrySystem.AddDog(dog2);
        entrySystem.AddDog(dog3);

        var dogs = entrySystem.GetDogs();
        DisplayDogs(dogs);
    }

    private static void DisplayDogs(IEnumerable<Dog> dogs)
    {
        foreach (var dog in dogs)
        {
            Console.WriteLine($"Name: {dog.Name}, Breed: {dog.Breed}, Color: {dog.Color}");
        }
    }

}
```

Jim is pleased with his current system, which efficiently tracks all records of the dogs in his pet shop. As his business is expanding, Jim now wants to include cats in his inventory.

![dog and cat](/images/1_7R4wsAgrVLA72HLKsfEdjg.jpg)

Photo by [Nadia Vasil’eva](https://www.pexels.com/photo/person-holding-a-brown-dog-and-a-cat-6821106/) from pexels

To accommodate this, we need to create a **Cat** class and integrate it into the existing entry system, similar to the process used for dogs.

```cs
public class Cat
{
    public string Name { get; }
    public string Breed { get; }
    public string Color { get; }

    public Cat(string name, string breed, string color)
    {
        Name = name;
        Breed = breed;
        Color = color;
    }

    public void Eat()
    {
        Console.WriteLine("Eating");
    }

    public void Sleep()
    {
        Console.WriteLine("Sleeping");
    }

    public void MakeSound()
    {
        Console.WriteLine("Meau...!");
    }

}

// refactored pet shop entry system

public class PetShopEntrySystem
{
    private List<Dog> dogs;
    private List<Cat> cats;

    public PetShopEntrySystem()
    {
        dogs = new List<Dog>();
        cats = new List<Cat>();
    }

    public void AddDog(Dog dog)
    {
        dogs.Add(dog);
    }

    public void AddCat(Cat cat)
    {
        cats.Add(cat);
    }

    public IEnumerable<Dog> GetDogs()
    {
        return dogs;
    }

    public IEnumerable<Cat> GetCats()
    {
        return cats;
    }

}

// Pet shop entry simulator for testing the application

public class PetshopEntrySimulator
{
   static void Main()
   {
        // existing code for dog entries

        // enterting cat's data
        Cat cat1 = new Cat("Whiskers", "Persian", "White");
        Cat cat2 = new Cat("Mittens", "Maine Coon", "Grey/Tabby");
        Cat cat3 = new Cat("Ginger", "British Shorthair", "Orange/Ginger");

        PetShopEntrySystem entrySystem = new PetShopEntrySystem();
        entrySystem.AddCat(cat1);
        entrySystem.AddCat(cat2);
        entrySystem.AddCat(cat3);

        var cats = entrySystem.GetCats();
        DisplayCats(cats);
    }

    // existing DisplayDogsMethod

    private static void DisplayCats(IEnumerable<Cat> cats)
    {
        foreach (var cat in cats)
        {
            Console.WriteLine($"Name: {cat.Name}, Breed: {cat.Breed}, Color: {cat.Color}");
        }
    }

}
```

Certainly! To streamline the entry system for Jim’s pet shop and make it scalable for additional pet types, we can create a common `Animal` class to encapsulate all shared attributes and methods. Here's how we can refactor the system:

```cs
public class Animal
{
    public string Name { get; }
    public string Breed { get; }
    public string Color { get; }

    public Animal(string name, string breed, string color)
    {
        Name = name;
        Breed = breed;
        Color = color;
    }
    public virtual void Eat()
    {
        Console.WriteLine("Eating");
    }

    public void Sleep()
    {
        Console.WriteLine("Sleeping");
    }

    public virtual void MakeSound()
    {
        Console.WriteLine("making sound");
    }

}
```

Since cats and dogs may have different eating habits and make different sounds, we make these methods virtual in the `Animal` class so that they can be overridden in their respective classes. The `Sleep` method will remain the same for all classes.

Let’s refactor the `Dog` , `Cat` and `PetShopEntrySystem` classes.

```cs
public class Cat : Animal
{
  public Cat(string name, string breed, string color)
  : base(name, breed, color)
  {

  }

  public override void Eat()
  {
     Console.WriteLine("Cat is eating");
  }

  public override void MakeSound()
  {
     Console.WriteLine("Meau...!");
  }
}


public class Dog : Animal
{
  public Dog(string name, string breed, string color)
  : base(name, breed, color)
  {
  }

  public override void Eat()
  {
     Console.WriteLine("Dog is Eating");
  }

  public override void MakeSound()
  {
     Console.WriteLine("Woff! woof");
  }
}

public class PetShopEntrySystem
{
   private readonly List<Animal> animals;

   public PetShopEntrySystem()
   {
      animals = new List<Animal>();
   }

   public void AddAnimal(Animal animal)
   {
      animals.Add(animal);
   }

   public IEnumerable<Animal> GetAnimals()
   {
       return animals;
   }

}
```

We now maintain a single list of animals, and provide a single method for adding an animal and retrieving all animals. Let’s test the system.

```cs
public class PetshopEntrySimulator
{
  static void Main()
  {
        Animal cat1 = new Cat("Whiskers", "Persian", "White");
        Animal cat2 = new Cat("Mittens", "Maine Coon", "Grey/Tabby");
        Animal cat3 = new Cat("Ginger", "British Shorthair", "Orange/Ginger");
        cat1.Eat();
        cat1.Sleep();
        cat1.MakeSound();

        Dog dog1 = new Dog("Max", "Golden Retriever", "Golden");
        Dog dog2 = new Dog("Luna", "Sibarian Husky", "Grey/White");
        Dog dog3 = new Dog("Duke", "Labrador Retriever", "Chocolate Brown");

        PetShopEntrySystem entrySystem = new PetShopEntrySystem();

        // adding cats
        entrySystem.AddAnimal(cat1);
        entrySystem.AddAnimal(cat2);
        entrySystem.AddAnimal(cat3);

        // adding dogs
        entrySystem.AddAnimal(dog1);
        entrySystem.AddAnimal(dog2);
        entrySystem.AddAnimal(dog3);

        var animals = entrySystem.GetAnimals();
        DisplayAnimals(animals);
    }

    private static void DisplayAnimals(IEnumerable<Animal> animals)
    {
        foreach (var animal in animals)
        {
            Console.WriteLine($"Name: {animal.Name}, Breed: {animal.Breed}, Color: {animal.Color}");
        }
    }

}
```

We now have a single method for adding and displaying animals. You can add any number of animal types without changing the code in the `Animal` and `PetShop` classes. Our system is very flexible now.

However, instantiating the `Animal` class directly, like `Animal animal = new Animal();`, doesn't make sense. What kind of animal is it? What is its behavior? These questions can't be answered just by looking at this instantiation. Therefore, it makes sense to convert the `Animal` class into an abstract class.

```cs
public abstract class Animal
{
   //remaining code
}
```

We override the `MakeSound()` and `Eat()` methods in every concrete class. There is no benefit in having concrete implementations of `MakeSound()` and `Eat()` methods in the `Animal` class. Therefore, let's make these methods abstract.

```cs
public abstract class Animal
{
    public string Name { get; }
    public string Breed { get; }
    public string Color { get; }

    public Animal(string name, string breed, string color)
    {
        Name = name;
        Breed = breed;
        Color = color;
    }

    public void Sleep()
    {
        Console.WriteLine("Sleeping");
    }

    public abstract void Eat();
    public abstract void MakeSound();

}
```

We can relate this to the definition “an object can take many forms.”

A `Dog` is an `Animal`, a `Cat` is an `Animal`, and a `Cow` is an `Animal` too. An `Animal` can take many forms (Dog, Cat, Cow, and many more). We can easily replace one animal type with another at runtime, providing flexibility.

```cs
Dog dog = new Dog(); // This is not polymorphism

Animal dog = new Dog(); // This is polymorphism
```

Let’s understand it in simpler terms.

![some image](/images/1_evWYiuwo-wgw3uoa3f_czQ.png)

---

### Polymorphism through interfaces

**⚠️Note:** Polymorphism can also be achieved through interfaces. Simply replace the base class with an interface.

For example:

```cs
public interface INotification
{
    void Send();
}

public class EmailNotification : INotification
{
    public void Send()
    {
       // Email sending logic
    }
}

public class SmsNotification : INotification
{
    public void Send()
    {
       // SMS sending logic
    }
}
```

Here, `INotification` is a base type, and `SmsNotification` and `EmailNotification` are the derived types.

**Why did we use inheritance before?**

Because we wanted to reuse the functionality like `Name`, `Breed`, and `Sleep()` of the `Animal` class. Be careful when choosing between an interface and an abstract class as a base type. This concept is also known as **subtype polymorphism** and is an example of **runtime polymorphism**.

**Why is it called runtime polymorphism?**

When you call a method (like `MakeSound`) on an `Animal` reference, the computer needs to figure out which specific method to use. Is it the dog’s bark or the cat’s meow? This decision is made while the program is running, not when the code is being written or compiled. That’s why it’s called “runtime” polymorphism.

### Method Overloading (Compile-time Polymorphism)

**It is debatable** whether to call method overloading polymorphism. Some consider it compile-time polymorphism, while others do not. I thought it should be included in this discussion.

Method overloading occurs when two or more methods in the same class have the same name but different parameters. The compiler determines which method to invoke based on the method signature. It is called compile time polymorphism because at the compile time, compiler knows which method it is calling.

```cs
class Calculator
{
    public int Add(int a, int b)
    {
        return a + b;
    }

    public int Add(int a, int b,int c)
    {
        return a + b + c;
    }

    public double Add(double a, double b)
    {
        return a + b;
    }

}
```

In this example, the `Add` method is overloaded to handle both integer and double parameters. Calculator class have two Add methods but with different number of arguments.

### TLDR

Polymorphism, a core concept in object-oriented programming, allows an entity to take multiple forms. In a pet shop system, this is demonstrated by creating a base `Animal` class and derived `Dog` and `Cat` classes, allowing for flexible handling of different animals. The `Animal` class's `Eat()` and `MakeSound()` methods are made abstract to be overridden in derived classes. Polymorphism can also be achieved through interfaces, providing further flexibility. Additionally, method overloading, though debatable as a form of polymorphism, allows multiple methods with the same name but different parameters in a single class.

---

Original post by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [February 5, 2024](https://medium.com/p/ea312521d050). [Canonical link](https://medium.com/@ravindradevrani/polymorphism-in-c-ea312521d050)

Exported from [Medium](https://medium.com) on February 19, 2025.
