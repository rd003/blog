+++
date = '2025-02-25T10:10:41+05:30'
title = 'LINQ: Zip() operator'
tags= ["csharp","linq"]
categories = ["programming"]
draft= false
image = '/images/zip.png'
+++

<!-- ![zip() operator in](/images/zip.png) -->

> There is also a [video version](https://youtu.be/p1SXSMe0wk8?si=8p2ZptMcPrI_fodS) of this tutorial.

Let's understand it with example.

```cs
int[] nums1 = [1, 2, 3, 4];
int[] nums2 = [3, 4, 5, 6];

IEnumerable<int>? product = nums1.Zip(nums2, (n1, n2) => n1 * n2);

Console.WriteLine(string.Join(", ", product));  // 3, 8, 15, 24
```

Let's break it down:

`IEnumerable<int>? product = nums1.Zip(nums2, (n1, n2) => n1 * n2);`

It takes `nums1[i]` and `nums2[i]`, evaluates it (nums1[0]\*nums2[0]) and returns it. Here `i` is the index of the array. For example.

```txt
products = [
    1*3=3,
    2*4=8,
    3*5=15,
    4*6=24
];
```

Let's take another example.

```cs
string[] students = ["John", "Mike", "Tim"];
int[] testScores = [70, 80, 90];

var studentGrades = students.Zip(testScores, (student, score) =>
                                             new StudetGrade(
                                                student,
                                                score,
                                                score >= 90 ? "A" : "B")
                                             );

foreach (var sg in studentGrades)
{
    Console.WriteLine(sg.ToString());
}

// Model for displaying student grades
public record StudetGrade(string Student, int Score, string Grade);
```

Output:

```bash
StudetGrade { Student = John, Score = 70, Grade = B }
StudetGrade { Student = Mike, Score = 80, Grade = B }
StudetGrade { Student = Tim, Score = 90, Grade = A }
```

## Caveats

It stops at the Shortest Sequence.

```cs
string[] letters = ["A", "B", "C", "D"];

int[] nums = [1, 2, 3];

var sequence = letters.Zip(nums, (l, n) => $"{l}-{n}");

Console.WriteLine(string.Join(", ", sequence));  // A-1, B-2, C-3
```

It has excluded "D", because shortest sequence(nums) has 3 items only, so it will evaluate only 3 items.

The example below follows the same principles.

```cs
string[] letters = ["A", "B", "C"];

int[] nums = [1, 2, 3, 4];

var sequence = letters.Zip(nums, (l, n) => $"{l}-{n}");

Console.WriteLine(string.Join(", ", sequence));  // A-1, B-2, C-3
```

## Using more that two enumerables/arrays

You can aslo use more than two enumerables or arrays as shown below.

```cs
var list1 = new List<int> { 1, 2, 3 };
var list2 = new List<char> { 'A', 'B', 'C' };
var list3 = new List<string> { "One", "Two", "Three" };

var zipped = list1.Zip(list2, (num, letter) => new { num, letter })
                  .Zip(list3, (pair, word) => new { pair.num, pair.letter, word });

foreach (var item in zipped)
{
    Console.WriteLine($"{item.num}-{item.letter}-{item.word}");
}

/* output

1-A-One
2-B-Two
3-C-Three

*/
```

**Zip() merge two sequences (enumerables) into a single sequence of pairs.**
