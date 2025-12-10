+++
date = '2025-05-17T17:32:06+05:30'
draft = false
title = 'C#: Byte and Its Use Cases'
tags = ['csharp']
categories= ['programming']
image = '/images/byte-in-csharp.webp'
+++

<!-- ![c# byte](/images/byte-in-csharp.webp) -->

- `byte` is a value type in c#
- `byte` is an unsigned integer which stores value from 0 to 255, which means it can not store negetive numbers.
- Size of `byte` is 8-bit (1 byte)
- CTS equivalent of byte is `System.Byte`
- It's default value is 0
- It is great for memory optimization when dealing with small numbers.

Examples:

```cs
byte a = 10;

Console.WriteLine(a);

```

## Use cases

1. Working with ASCII value

```cs
 byte asciiValue = (byte)'R'; // 82
 byte asciiValue2 = (byte)'r'; // 114
```

2. Encoding text into bytes

```cs
 using System.Text;

 string message = "Ravindra";
 byte[] encoded = Encoding.UTF8.GetBytes(message);

 Console.WriteLine($"{string.Join(",",encoded)}");

 // op: 82,97,118,105,110,100,114,97
```

Note: Each character is encoded using UTF-8. For standard letters, the byte values match their ASCII codes.. (R: 82, a:97, v:118 ...)

3. Read bytes from file

```cs
 byte[] fileData = File.ReadAllBytes("/home/ravindra/Pictures/Learn.png");
 Console.WriteLine($"Read {fileData.Length} bytes from file"); 
 // o/p: Read 61427 bytes from file
```

Let's go little further and read first 10 bytes from the file.

```cs
byte[] fileData = File.ReadAllBytes("/home/ravindra/Pictures/Learn.png");

for (int i = 0; i < Math.Min(10, fileData.Length); i++)
{
  Console.WriteLine($"byte {i}: byte: {fileData[i]}, hex: {fileData[i]:X2}");
}
```

4. Working with file streams

Filestream allows you to read from and write to files at a low level — byte-by-byte. 

```cs
string filePath = "file.txt";

// Write to a file
using (FileStream fs = new FileStream(filePath, FileMode.Create))
{
  byte[] data = Encoding.UTF8.GetBytes("Hello there!!");
  fs.Write(data, 0, data.Length);
}

// reading from file

using (FileStream fs = new FileStream(filePath, FileMode.Open))
{
  byte[] buffer = new byte[fs.Length];
  fs.Read(buffer, 0, buffer.Length);
  string result = Encoding.UTF8.GetString(buffer);
  Console.WriteLine(result);
}
```

5. It is quite useful when you don't want to use unnecessarily extra memory.


## When not to use byte?

- When you need negetive numbers then use `sbyte`
- When numbers exceed 255 characters