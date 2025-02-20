+++
date = '2025-02-20T17:58:49+05:30'
draft = false
title = 'Easiest Way to Handle Csv Files in Csharp'
tags = ['csharp','dotnet']
categories= ['programming']
+++

![how to read and write to csv files in c#](/images/csv_dotnet.png)

In this tutorial we will se how to read and write data to **csv** file. It is pretty much easy if you have some external library for that. We are definitely going to use a library and that will be **CsvHelper**.

You can also check the video version of this tutorial.

First and foremost, create a **c# console application** in .net core. After that we need to install a nuget package, which is`**CsvHelper**`

![csv_helper_nuget](/images/csv_helper_nuget.jpg)

In `Program.cs` file, remove the boiler plate code and add this one.

```cs
namespace CsvReaderDemo

public class Program
{
 static void Main() {

    }

}
```

Now we will create a class **Person** in the same file.

```cs
class Person
{
 public string Name { get; set; }
 public int Age { get; set; }
 public string Country { get; set; }
}
```

Inside the class **Program**, we will create a static method **WriteToCsv**

```cs
static void WriteToCsv(string filePath)
 {

        try
        {
            if (!File.Exists(filePath))
            {
                using (File.Create(filePath)) { }
            }


            List&lt;Person&gt; people = new List&lt;Person&gt;
        {
          new Person { Name = "Jane", Age = 25, Country = "UK" },
          new Person { Name = "Any", Age = 30, Country = "Canada" },
          new Person { Name = "Mike", Age = 35, Country = "USA" }
        };


            var configPersons = new CsvConfiguration(CultureInfo.InvariantCulture)
            {
                HasHeaderRecord = false
            };

            using (StreamWriter streamWriter = new StreamWriter(filePath,true))
            using (CsvWriter csvWriter = new CsvWriter(streamWriter, configPersons))
            {
                csvWriter.WriteRecords(people);
            }

            Console.WriteLine("Data written to CSV successfully.");
        }

        catch(Exception ex)
        {
            throw;
        }

    }
```

Lets breakdown it.

👉 This method takes a parameter **filePath** of **string** type.

👉 First we will check if this file exists or not, if it does not exist we need to create that file.

```cs
if (!File.Exists(filePath))
 {
 using (File.Create(filePath)) { }
 }
```

👉 `using` keyword tells us that we do not need to worry about disposal of theobject.

```cs
var configPersons = new CsvConfiguration(CultureInfo.InvariantCulture)
 {
 HasHeaderRecord = false
 };
```

👉Here we are gonna write some configuration for csv helper,   
To this object we are passing a value, **CultureInfo.InvariantCulture**, it means we are not culture dependent right now.

```cs
HasHeaderRecord = false
```

👉 HasHeaderRecord tells whether we need a header or not in a file. So lets set it to false.

```cs
using (StreamWriter streamWriter = new StreamWriter(filePath,true))
```

👉 We are creating instance of **StreamWriter,** it is taking two arguments first one in **filePath**, and second argument indicates whether or not you want to append data to a file or not. We are setting it to **true.**

```cs
using (CsvWriter csvWriter = new CsvWriter(streamWriter, configPersons))
 {
 csvWriter.WriteRecords(people);
 }
```

👉 Her we are creating the instance of **CsvWriter,** it will take two parameters first one is **streamWriter** and another one is **config** options.  
Lets write people to file.  
👉 Make sure to use these name spaces in the top.

```cs
using CsvHelper.Configuration;
using CsvHelper;
using System.Globalization;
```

Let go to the **main** method , call **WriteToCsv** method and pass the **filePath**.

```cs
static void Main()
 {
 string directoryPath = @"C:\\Users\\RD\\Documents\\Projects";
 string fileName = "data.csv";
 string filePath = Path.Combine(directoryPath, fileName);
 WriteToCsv(filePath);
 }
```

Now lets see how to read data from this file. We will create a method **ReadFromCsv** and it will take one argument **filePath** of string type.

```cs
static void ReadFromCsv(string filePath)
 {
 try
 {
 if (File.Exists(filePath))
 {

                var config = new CsvConfiguration(CultureInfo.InvariantCulture)
                {
                    HasHeaderRecord = false
                };
                using (StreamReader streamReader = new StreamReader(filePath))
                using (CsvReader csvReader = new CsvReader(streamReader, config))
                {

                    // Read records from the CSV file
                    IEnumerable&lt;Person&gt; records = csvReader.GetRecords&lt;Person&gt;();

                    // Process each record
                    foreach (Person person in records)
                    {
                        Console.WriteLine($"Name: {person.Name}, Age: {person.Age}, Country: {person.Country}");
                    }
                }
            }
        }
        catch (Exception ex)
        {
            throw;
        }
    }
```

Let’s break it down.

```cs
var config = new CsvConfiguration(CultureInfo.InvariantCulture)
 {
 HasHeaderRecord = false
 };
```

👉 It is the config option for csv reader.

**CultureInfo.InvariantCulture** says that we are not dependent on any culture.

**HasHeaderRecord=false** says that we are not looking for any header to read.

Lets call this method in Main method.

```cs
static void Main()
 {
 string directoryPath = @"C:\\Users\\RD\\Documents\\Projects";
 string fileName = "data.csv";
 string filePath = Path.Combine(directoryPath, fileName);

        // WriteToCsv(filePath);
        ReadFromCsv(filePath);
        Console.ReadKey();

    }
```

So now we can see that, how easy is to read and write to csv file and all thanks to the csv helper library.

📎Source code: [https://github.com/rd003/CsvReaderDemo](https://github.com/rd003/CsvReaderDemo)

---

Originally posted by [Ravindra Devrani](https://medium.com/@ravindradevrani) on [May 20, 2023](https://medium.com/p/6cad58d341fa).

[Canonical link](https://medium.com/@ravindradevrani/easiest-way-to-handle-csv-files-in-c-6cad58d341fa)

Exported from [Medium](https://medium.com) on February 19, 2025.
