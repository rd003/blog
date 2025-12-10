+++
date = '2025-02-23T11:30:44+05:30'
draft = false
title = 'Command Pattern With C#'
tags = ['design-patterns']
categories = ['programming']
image = '/images/1_JoPgJdYKXe1o05IS23X0zA.png'
+++

<!-- ![Command Pattern](/images/1_JoPgJdYKXe1o05IS23X0zA.png) -->

**The Command Pattern** is a behavioral design pattern that turns a request into a stand-alone object containing all the information about the request. This conversion allows you to parameterize methods with different requests, queue requests, and support undoable operations.

In simpler terms, the Command Pattern encapsulates a request as an object, thereby allowing users to decouple the sender (invoker) from the object that performs the action (receiver).

## Key Concepts

1. **Command:** An object that encapsulates a request or action.

2. **Receiver:** The object that performs the actual work when the command is executed.

3. **Invoker:** The object that receives the command and triggers its execution.

4. **Client:** The object that creates the command and passes it to the invoker.

## Problem Statement

Let’s say we have a `BankAccount` class with methods for depositing and withdrawing money. We want to create a system that allows us to execute these transactions and also undo them if needed.

## Solution

We’ll implement the Command pattern by creating the following components:

- `ICommand` (command interface)
- `BankAccount` (receiver)
- `DepositCommand` and `WithdrawCommand` (concrete commands)
- `BankAccountManager` (invoker)

### Command interface

```cs
public interface ICommand
{
 void Execute();
 void Undo();
}
```

### Concrete commands

```cs
public class DepositCommand : ICommand
{
    private readonly BankAccount _account;
    private decimal _amount;

    public DepositCommand(BankAccount account, decimal amount)
    {
        _account = account;
        _amount = amount;
    }

    public void Execute()
    {
        _account.Deposit(_amount);
    }

    public void Undo()
    {
        _account.Withdraw(_amount);
    }

}

public class WithdrawCommand : ICommand
{
    private readonly BankAccount _account;
    private decimal _amount;

    public WithdrawCommand(BankAccount account, decimal amount)
    {
        _account = account;
        _amount = amount;
    }

    public void Execute()
    {
        _account.Withdraw(_amount);
    }

    public void Undo()
    {
        _account.Deposit(_amount);
    }

}
```

### Receiver

```cs
public class BankAccount
{
    public decimal Balance { get; set; }

    public void Deposit(decimal amount)
    {
        Balance += amount;
        Console.WriteLine($"Deposited {amount}. New balance: {Balance}");
    }

    public void Withdraw(decimal amount)
    {
        Balance -= amount;
        Console.WriteLine($"Withdrawn {amount}. New balance: {Balance}");
    }

}
```

### Invoker

```cs
public class BankAccountManager
{
    private ICommand _command;

    public void SetCommand(ICommand command)
    {
        _command = command;
    }

    public void ExecuteTransaction()
    {
        _command.Execute();
    }

    public void UndoTransaction()
    {
        Console.WriteLine("Undoing last transaction.");
        _command.Undo();
    }
}
```

### Client Coded

```cs
public class Program
{
    public static void Main()
    {
        BankAccount bankAccount = new();

        DepositCommand depositCommand = new(bankAccount, 200);
        WithdrawCommand withdrawCommand = new(bankAccount, 100);

        BankAccountManager accountManager = new();

        accountManager.SetCommand(depositCommand);
        accountManager.ExecuteTransaction();

        accountManager.SetCommand(withdrawCommand);
        accountManager.ExecuteTransaction();

        accountManager.UndoTransaction();
    }
}
```

### Output

```sh
Deposited 200. New balance: 200
Withdrawn 100. New balance: 100
Undoing last transaction.
Deposited 100. New balance: 200
```

## Key benefits

- **Decoupling:** The command pattern decouples the requester of an action from the provider of that action.
- **Extensibility:** New commands can be added without changing existing code.
- **Flexibility:** Commands can be queued, logged, or rolled back.

## Common applications

- Undo/Redo functionality
- Remote control systems
- Menu systems

In this blog post, we’ve seen how to implement the **Command pattern** in C# using a real-world example. The Command pattern allows us to encapsulate requests as objects, making it easy to parameterize and queue requests. By using this pattern, we can create a system that allows us to execute transactions and also undo them if needed.

---

[Canonical link](https://medium.com/@ravindradevrani/understanding-the-command-design-pattern-c-212b50fabd87)
