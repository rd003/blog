+++
date = '2025-02-23T10:57:26+05:30'
draft = false
title = 'Decorator Pattern With C#'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_2qpDUZpD1bTPd1-TkfbrUA.png'
+++

<!-- ![decorator patter with c#](/images/1_2qpDUZpD1bTPd1-TkfbrUA.png) -->

The Decorator pattern is a structural pattern that enables you to wrap an object with additional behaviors or responsibilities without changing its external interface. It’s like adding layers of decorations to a gift — you can add or remove decorations without altering the gift itself.

**Example:**

Let’s say, we have a book whose base price is 500 INR. Some buyers need a hard cover book which costs some extra money, some need a signed copy which also add some additional cost, some needs the both hard cover and a signed copy which adds more cost. May be in future we want to remove the option of hard cover book or may be we want to add some extra features to it. How do we make our system more flexible, that is the big question.

Well, decorator pattern can save the day.

**How?**

- Create an Book object
- If you need a hard cover book then create the **HardCoverDecorator** object and wrap it around the Book object. Simple explanation, `**Book + HardCoverDecorator = HardCoveredBook**`
- If you need the both hard cover and a signed copy, then create the **HardCoverDecorator** object, wrap it around the book object. At last create the **SignedCopyDecorator** object and wrap it around **HardCover** object. Simple explanation `**Book + HardCoverDecorator + SignedCopyDecorator = HardCoveredSignedCopyBook**`

#### Create the Component Interface

```cs
public interface IBook
{
 string GetDescription();
 double GetPrice();
}
```

#### Create the concrete component

```cs
public class Book : IBook
{
    public string Title { get; }
    public string Author { get; }

    public Book(string title,string author)
    {
        Title = title;
        Author = author;
    }

    public string GetDescription()
    {
        return $"Book: {Title} by {Author}";
    }

    public double GetPrice()
    {
        return 500; // base price
    }

}
```

#### Abstract decorator class

```cs
public abstract class BookDecorator : IBook
{
    protected IBook book;
    public BookDecorator(IBook book)
    {
    this.book = book;
    }

    public abstract string GetDescription();

    public abstract double GetPrice();
}
```

#### Concrete Decorators

```cs
// Concrete decorator
public class SignedCopyDecorator : BookDecorator
{
    public SignedCopyDecorator(IBook book):base(book)
    {

    }

    public override string GetDescription()
    {
        return $"{book.GetDescription()}, Signed Copy";
    }

    public override double GetPrice()
    {
        return book.GetPrice() + 100; // Add signed copy cost
    }

}
```

#### Testing the system

```cs
public class BookTestDrive
{
    public static void Main()
    {
        IBook book = new Book("C# in Depth", "Jon Skeet");
        Console.WriteLine(book.GetDescription() + ": " + book.GetPrice());

        // book with hard cover
        book = new HardcoverDecorator(book);
        Console.WriteLine(book.GetDescription() + ": " + book.GetPrice());

        // book with hard cover and signed copy
        book = new SignedCopyDecorator(book);
        Console.WriteLine(book.GetDescription() + ": " + book.GetPrice());

    }

}
```

#### Output of the test

```bash
Book: C# in Depth by Jon Skeet: 500
Book: C# in Depth by Jon Skeet, Hardcover: 700
Book: C# in Depth by Jon Skeet, Hardcover, Signed Copy: 800
```

The Decorator pattern provides a flexible and reusable way to extend the behavior of an object without changing its implementation. By following these steps and understanding how to decorate objects, you can write more maintainable and scalable code. Happy decorating!

[Canonical link](https://medium.com/@ravindradevrani/understanding-the-decorator-pattern-c-18adbcb1d800)
