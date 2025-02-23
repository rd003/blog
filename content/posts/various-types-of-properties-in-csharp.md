+++
date = '2025-02-23T12:48:39+05:30'
draft = false
title = "Let's dive into various types of properties in c#"
tags = ['csharp']
categories=['programming']
+++

![various types of properties in c#](/images/1_6qVs2G138-DyPmnG2z_dyQ.png)

I assume you have some knowledge of C# properties. If not, here’s a quick definition: **A property is a class member that provides a flexible way to read, write, or compute the value of a private field.** Don’t worry if you’re new to properties; we’ll be using them in this blog, and I’ll explain them as we go along.

### 1. Properties with getter and setter

```cs
public class Person
{
 public string Name { get;set; }
 public int Age { get; set;}
}
```

Generally, we define properties like this. The Person class has two properties **Name** and **Age,** each with getters and setters. This enables you to set and read their values.

{{< youtube id="OVw-ympH6ME" title="various types of properties in csharp" autoplay="false" >}}

### Setting the property value

```cs
public class PropertyTestDrive
{
 public static void Main()
 {
 Person person = new Person();
 person.Name = "John";
 person.Age = 10;
 }
}
```

Properties can also have default values, as shown below.

```cs
public string Name { get; set; } = "John";
public int Age { get; set; } = 10;
```

### Initializing properties through object initializer

We can also initialize properties with object initializer.

```cs
Person person = new Person
 {
 Name = "John Doe",
 Age = 20
 };
```

### Reading the propertie’s value

```cs
Console.WriteLine($"Name: {person.Name}, Age: {person.Age}");
```

You can access the the **Name** with `person.Name` and **Age** with `person.Age` .

### 2. The read-only properties

We can also make our properties read-only by removing the setter (set;). This allows you to access the values, but not modify them.

```cs
Person person = new Person();
person.Name = "John"; // ❌ this line will give error
person.Age = 20; // ❌ this line will give error
```

With object initializer.

```cs
Person person = new Person()
{
 Name = "John Doe", // ❌ error
 Age = 20 // ❌ error
};
```

It can not be set even with in a `Person` Class

```cs
public class Person
{
    public string Name { get; }
    public int Age { get;}

    public void SetName(string name)
    {
        Name = name;   //❌ This line will give error because you can not set the readonly property
    }
}
```

### How do I set Name and Age then?

Typically, we set read-only properties with constructor, which will be demonstrated later. Alternatively, you can also assign default values to read-only properties, as shown below.

```cs
public class Person
{
 public string Name { get; } = "John"; // assiging default value 'John'
 public int Age { get; } = 10; // assiging default value '10'
}

public class PropertyTestDrive
{
 public static void Main()
 {
 Person person = new Person();
 Console.WriteLine($"Name: {person.Name}, Age: {person.Age}");
 // Output: Name: John, Age: 10
 }
}
```

Additionally, values can be set through the constructor.

```cs
public class Person
{
    public string Name { get; }
    public int Age { get; }

    // Parameterize constructor to set the values of Name and Age
    public Person (string name,int age)
    {
        Name= name;
        Age= age;
    }
}

public class PropertyTestDrive
{
    public static void Main()
    {
    // Instansiating object by passing name and age to the constructor
    Person person = new Person("John",10);

        Console.WriteLine($"Name: {person.Name}, Age: {person.Age}");
    }
}
```

If a class has only the read-only properties, it becomes immutable. Immutability means that once an object is instantiated, its state can not be changed. In this case, once the `Person` class is instantiated, values of`Name` and `Age` can not be modified.

```cs
 Person person = new Person("John",10);
 person.Name = "John Doe"; // ❌ gives error
 person.Age = 10; // ❌ gives error
```

### 3. Properties with private setter

```cs
public class Person
{
 public string Name { get; private set; }
 public int Age { get; private set; }
}
```

These properties can be set within the same class, but not from outside the class. Let’s illustrate this with an example.

```cs
public class PropertyTestDrive
{
 public static void Main()
 {
 Person person = new Person();
 person.Name = "John Doe"; // ❌ you can not set Name, this will give error
 person.Age = 10; // ❌ you can not set Age, this will give error
 }
}
```

### How to set Name and Age then?

Well, you can assign the default values to the properties, as shown below.

```cs
 public string Name { get; private set; } = "John Doe";
 public int Age { get; private set; } = 10;
```

Constructors are commonly used for setting the values of properties with private setter.

```cs
public class Person
{
    public string Name { get; private set; }
    public int Age { get; private set; }

    // Parameterized constructor for setting the value of Name and Age
    public Person(string name, int age)
    {
        Name = name;
        Age = age;
    }
}

public class PropertyTestDrive
{
 public static void Main()
 {
 Person person = new Person("John",10);
 }
}
```

You can assign the values to properties inside the class. Let’s see how

```cs
public class Person
{
    public string Name { get; private set; }
    public int Age { get; private set; }

    // assinging value to Name
    public void SetName(string name)
    {
        Name = name;
    }

    // assinging value to Age
    public void SetAge(int age)
    {
        Age = age;
    }

}

public class PropertyTestDrive
{
 public static void Main()
 {
    Person person = new Person();
    person.SetName("John");
    person.SetAge(20);
 }
}
```

We have created setter methods to set the properties. However, when using private setters, you can only set the value of a property within the class itself. Notably, you cannot set the value of read-only property(property with getter only) even from within the class.

### 3. Init only properties

```cs
public class Person
{
 public string Name { get; init; }
 public int Age { get; init; }
}
```

Well, we can not set init-only properties as shown below.

```cs
 Person person = new Person();
 person.Name = "John Doe"; // ❌ Gives error
 person.Age = 10; // ❌ Gives error
```

### How to set the Name and Age then?

Typically, the init-only properties are set using object initializer, as demonstrated below.

```cs
Person person = new Person
{
 Name = "John Doe",
 Age = 10
};
```

However, they can also be set through constructor.

```cs
public class Person
{
 public string Name { get; init; }
 public int Age { get; init; }public Person(string name, int age)
 {
 Name = name;
 Age = age;
 }
}

public class PropertyTestDrive
{
 public static void Main()
 {
    Person person = new Person("John", 11);
 }
}
```

Note that, default values can be assigned to properties, as shown in the following example

```cs
 public string Name { get; init; } = "John";
 public int Age { get; init; } = 11;
```

**Note:** If your class have only init-only property that your class becomes immutable.

### 4. Write only properties

We can aslo have the write only properties. However, it is not the common practice and used it with caution. We just have to remove the getter. However, we can not remove the getter of auto-implemented property (`public string Name { set; })`, for that we have to use full implementation of the property.

```cs
private string name;

public string Name
{
 set { name = value; }
}
```

Honestly, I never found a good use case for write-only property.

### Key Takeaways

- **Properties** are a fundamental concept in C# that allow you to encapsulate fields and control access to them.
- **Read-only** properties ensure data integrity and immutability.
- **Private setters** allow you to set properties within the class but not from outside.
- **Init-only** properties can only be set during object initialization and through the constructor.
- **Write-only** properties are rare and should be used with caution.

---

[Canonical link](https://medium.com/@ravindradevrani/lets-dive-into-various-types-of-properties-in-c-1a0f733066a0)
