+++
date = '2025-02-22T21:50:00+05:30'
draft = false
title = 'The Dependency Inversion Principle (DIP)'
tags = ['design-patterns','SOLID']
categories = ['programming']
image = '/images/1_FjEBNQw1jozLAACTbGgs7w.webp'
+++

<!-- ![Dependency Inversion Principle in c#](/images/1_FjEBNQw1jozLAACTbGgs7w.webp) -->

The **Dependency Inversion Principle** states that:

1. **High-level modules** should not depend on **low-level modules**. Both should depend on **abstractions** (e.g., interfaces).
2. **Abstractions** should not depend on **details**. **Details** (concrete implementations) should depend on **abstractions**.

**Source:** [Wikipedia](https://en.wikipedia.org/wiki/Dependency_inversion_principle "https://en.wikipedia.org/wiki/Dependency_inversion_principle")

Other SOLID Principles

- [Single Responsibility Principle](/posts/single-responsibility-principle/)
- [Open Closed Principle](/posts/open-closed-principle/)
- [Liskov Substitution Problem](/posts/liskov-substitution-principle/)
- [Interface Segregation Principle](/posts/interface-segregation-principle/)

## Example without DIP

```cs
public class UserRepository
{
    public string GetUserById(int id)
    {
        // Code to fetch user from the database
        return "User";
    }
}

public class UserService
{
    private readonly UserRepository _userRepository;

    public UserService()
    {
        _userRepository = new UserRepository();
    }
    public string GetUser(int id)
    {
        return _userRepository.GetUserById(id);
    }
}
```

One problem with this code is , the`UserService` is tightly coupled with the `UserRepository`. Another problem is, if you want to use different implementation of `UserReposoitory`, you can not easily do it. For instance you want to swap your `UserRepsoitory` to `UserRepositoryWithDifferentDatabase`.

## With DIP

```cs
public interface IUserRepository
{
    string GetUserById(int id);
}

public class UserRepository:IUserRepository
{
    public string GetUserById(int id)
    {
        // Code to fetch user from the database
        return "User";
    }
}

public class UserService
{
    private readonly IUserRepository _userRepository;

    public UserService(IUserRepository userRepository)
    {
        _userRepository = userRepository;
    }
    public string GetUser(int id)
    {
    return _userRepository.GetUserById(id);
    }
}

public class DIPTest
{
    public static void Main()
    {
        UserService userService = new UserService(new UserRepository());
        Console.WriteLine(userService.GetUser(2));
    }
}
```

Now, `UserService` is depend on abstraction (`IUserRepository`). `UserService` is not responsible for instantiating the `UserRepository`. It is loosely coupled now. If you have another repository (eg. `UserRepositoryWithDifferentDatabase`), which implements the `IUserRepository`, you can pass it's instance instead of `UserRepository`. User service don't care if you pass the instance of `UserRepository` or `UserRepositoryWithDifferentDatabase`, because both implements the same interface.

## What is inversion?

You might be wondering what is **inversion?** What are we inverting here? First we need to understand the traditional approach. Traditionally high level module depends on the low level module. If we consider our example, our dependency direction is **UserService -> UserRepository**, **UserService** is depending on the **UserRepository**.

Using the DIP, **UserService** depends on **IUserRepository**. So we have changed the flow of dependency (**UserService -> IUserRepository)**

> I personally find this name “Dependency Inversion” very confusing, specially the term “Inversion”. But it is what it is. I would encourage you to search more about it.

## References

[https://stackoverflow.com/questions/27978841/what-is-meant-by-inversion-in-dependency-inversion](https://stackoverflow.com/questions/27978841/what-is-meant-by-inversion-in-dependency-inversion)

---

[Canonical link](https://medium.com/@ravindradevrani/the-dependency-inversion-principle-dip-7b505dd9d28e)
