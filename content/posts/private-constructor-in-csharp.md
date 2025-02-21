+++
date = '2025-02-21T10:20:08+05:30'
draft = false
title = 'Private Constructor in C#'
tags = ['csharp']
categories = ['programming']
+++

![private constructor in c#](/images/1_pz1zZlr5MwRQYYQd0yCC4g.png)

In C#, a private constructor is a constructor method declared with the `private` access modifier (or without mentioning any modifier). If a class have only a private constructor and does not have any public constructor, then you are not able to create the instance of a class. Example 👇

```cs
public class Student
{
 Student() { } // private constructor
}

public class Program
{
 static void Main()
 {
 Student stu = new(); //Error CS0122 'Student.Student()'
 // is inaccessible due to its protection level

    }

}
```

When you try to create the instance of stu, you will the following error.

`Error CS0122 ‘Student.Student()’ is inaccessible due to its protection level.`

## Why do we even need a private constructor?

Well it have several purposes.

**👉 Singleton Pattern:** One common use case is to implement the singleton pattern, where a class ensures that only one instance of itself can be created and provides a global point of access to that instance. [This article from csharpindepth.com explain all the aspects of singleton.](https://csharpindepth.com/articles/singleton)

**👉Factory Methods:** Private constructors can be used in conjunction with public factory methods to control how instances of a class are created. This allows the class to enforce certain conditions or perform setup tasks before an instance is created.

**👉 Utility Classes:** Similar to static classes, utility classes containing only static methods may have private constructors to prevent instantiation. These classes typically provide helper functions or extension methods that can be used across the application.

```cs
public class Student
{
 Student() { }
 public static void HelperMethod()
 {
 // code goes here
 }

public static void HelperMethodTwo()
 {
 // code goes here
 }
}

public class Program
{
 static void Main()
 {
 Student.HelperMethod();
 Student.HelperMethodTwo();
 }
}
```

## Additional resources

[**Why do we need a private constructor?**](https://stackoverflow.com/questions/2585836/why-do-we-need-a-private-constructor)

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [February 21, 2024](https://medium.com/p/0b17acebdced).

[Canonical link](https://medium.com/@ravindradevrani/private-constructor-and-its-use-cases-in-c-0b17acebdced)

Exported from [Medium](https://medium.com) on February 19, 2025.
