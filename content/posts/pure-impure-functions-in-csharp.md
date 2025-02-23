+++
date = '2025-02-23T11:38:07+05:30'
draft = false
title = 'Understanding The Pure And Impure Functions in C#'
tags = ['csharp']
categories=['programming']
+++

![What is pure function in c#?](/images/1_zSzCvLdQ0Kjand1tBqwqGw.png)

## Pure functions

Pure function is that:

1. **Always returns the same output** given the same inputs.
2. **Does not modify the state of object** or any external state.
3. **Does not have any side effects** such as I/O operations, exceptions or modifying external variables.

- In other words, a pure function takes input, process it and returns the output without modifying anything else.
- Pure functions are easy to test and debug.

## Examples

1. Mathematical calculations

```cs
public int Add(int a, int b)
{
 return a + b;
}
```

2. String manipulation

```cs
public string Concatenate(string a, string b)
{
 return a + b;
}
```

3. Array operations

```cs
public int[] SortArray(int[] array)
{
 return array.OrderBy(x => x).ToArray();
}
```

4. Data transformations

```cs
public string ConvertToString(int value)
{
 return value.ToString();
}
```

5. Validation

```cs
public bool IsValidEmail(string email)
{
 return email.Contains("@");
}
```

## Impure Functions

Impure function is that

1. **Modifies the state** of the object or any external state.
2. **Has side effects**, such as I/O operation, db operations, throwing exceptions, writing to file,db or console etc.
3. **May return different outputs** given the same inputs, due to external factors.

## Examples of impure functions

- I/O operations

```cs
public void SaveFile(string data)
{
 File.WriteAllText("data.txt", data);
}
```

- Database operations

```cs
public void InsertUser(User user)
{
 // database insert operation
}
```

- Web service calls

```cs
public string GetWeatherData(string city)
{
 // web service call
}
```

- Modifying external collections

```cs
public void AddItem(List<string\> list, string item)
{
 list.Add(item);
}

public void ValidateInput(string input)
{
 if (input == null)
 {
 throw new ArgumentNullException();
 }
}
```

- Sending an email

```cs
public void SendWelcomeEmail(User user)
{
 // send email using SMTP or email service
}
```

- Writing to a log file

```cs
public void LogError(Exception ex)
{
 File.AppendAllText("error.log", ex.Message);
}
```

- Printing to console

```cs
public void PrintReceipt(Order order)
{
 Console.WriteLine("Receipt:");
 Console.WriteLine(order.ToString());
}
```

---

[Canonical link](https://medium.com/@ravindradevrani/understanding-the-pure-and-impure-functions-with-c-examples-efcba0bb1736)
