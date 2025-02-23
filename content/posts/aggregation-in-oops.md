+++
date = '2025-02-23T08:37:49+05:30'
draft = false
title = 'Understanding Aggregation: How It Differs from Composition'
tags = ['oops']
categoris=['programming']
+++

![Aggregation in oops. Aggregation vs Composition.](/images/1_NYnlRXKiuSdrYvLcRGGchQ.png)

**Aggregation** is when an object is made up of one or more objects, but those objects can live outside the main object. It defines the **has-a** relationship.

**Note**: In the aggregation, if main object is destroyed, its aggregated objects may still live.

**Example #1:** A `Library` is an aggregation of `Books`. Books can live without the library.

**Example #2:** A `Department` is an aggregation of `Employees`. If department closes, the Employees can exist on their own.

### Let’s Understand it with example

![Aggregation in oops](/images/1_Vcqyr_HtaJL6c4HnVrPJSQ.jpg)

Aggregation

The Book class

```java
public class Book {
    private String title;
    private String author;

    public Book(String title, String author) {
        this.title = title;
        this.author = author;
    }

    public String getTitle() {
        return title;
    }

    public String getAuthor() {
        return author;
    }
}
```

The Library class

```java
import java.util.ArrayList;
import java.util.List;

public class Library {
    private List<Book> books;

    public Library() {
        books = new ArrayList<>();
    }

    public List<Book> getBooks() {
        return books;
    }

    public void addBook(Book book) {
        books.add(book);
    }

}
```

The LibraryTestDrive class.

```java
public class LibraryTestDrive {
    public static void main(String[] args) {
        Book book1 = new Book("1984", "George Orwell");
        Book book2 = new Book("To Kill a Mockingbird", "Harper Lee");

        Library library = new Library();
        library.addBook(book1);
        library.addBook(book2);

        for (Book book : library.getBooks()) {
            System.out.println(book.getTitle() + " by " + book.getAuthor());
        }
    }
}
```

In this example, the **book** is instantiated outside the `Library` class, and then that book is passed as a parameter to the **addBook()** method. Even if the library object is destroyed, the book object will continue to exist.

### Composition also defines the has-a relation. How is it different then?

**Composition** also defines the **has-a** relationship but it is slightly different. In composition, if a main class destroyes then the objects it is composed of will be destroyed too. Composed objects can not live outside the main object.

**Example #1:** A `Car` is composed of an `Engine` and `Wheels`. If the car Destroyed, the engine and wheels are destroyed as well.

**Example #2** A `House` is composed of `Rooms`. If the house is destroyed, the rooms are destroyed too.

More detailed blog post on composition 👇

[**Composition : What , why and when 🤔**
Composition is when your class is composed of one or more objects from other classes. A simple example is a Car…](/posts/composition-what-why-and-when/)

Let’s look at the example below.

![composition in oops](/images/1_8rpnyEPf6cJJDZpxHanSpg.jpg)

composition

Java implementation of class diagram.

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

public class CarTestDrive {
    public static void main(String[] args) {

        Car car = new Car("v8", 17);
        car.displayDetails();
    }
}
```

If the `car` object is destroyed, there will be no existence of the `engine` and `wheels` because the `wheels` and `engine` are instantiated within the `Car` class.

### Summary

**Aggregation** defines a “has-a” relationship where the composed objects can exist independently of the main object. **Composition** also defines a “has-a” relationship but with a strong dependency, where the composed objects cannot exist without the main object. When you want to reuse the functionality of any class and do not need subtype polymorphism then consider either composition or aggregation.

---

[Canonical link](https://medium.com/@ravindradevrani/understanding-aggregation-how-it-differs-from-composition-1a75df81e0a3)
