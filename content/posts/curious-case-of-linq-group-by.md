+++
date = '2025-02-24T16:17:33+05:30'
draft = false
title = 'Curious Case of LINQ Group By'
tags = ['csharp','linq']
categories= ['programming']
image = '/images/1_JfMz_6yLa8eisgi58OxNWQ.png'
+++

<!-- ![curious case of linq group by](/images/1_JfMz_6yLa8eisgi58OxNWQ.png) -->

### Schema

- Department (DepartmentId, Name)
- Employee (EmployeeId, Name, DepartmentId)

### Result set I need

Show all departments with total number of employees. Do not skip the departments which have 0 employees. As shown below:

DepartmentIdNameTotalEmployees1Engineering22Marketing13HR0

I have applied various queries and checked their equivalent sql.

### 1. Straightforward but skips the department which has no employees

This query does not meet my requirement. It would be a good choice if I don’t need departments without any employees.

```cs
private static async Task<IResult> GetDepartmentsWithEmployeeCount1(AppDbContext context)
{
 var departments = await context.Employees
     .Include(e => e.Department)
     .GroupBy(e => new { e.DepartmentId, e.Department.Name })
     .Select(g => new DepartmentWithEmployeeCount(
                 g.Key.DepartmentId,
                 g.Key.Name,
                 g.Count())
 ).ToListAsync();
 return TypedResults.Ok(departments);
 }
```

Which results in:

```sql
SELECT [e].[DepartmentId], [d].[Name], COUNT(*)
 FROM [Employees] AS [e]
 INNER JOIN [Departments] AS [d] ON [e].[DepartmentId] = [d].[DepartmentId]
 GROUP BY [e].[DepartmentId], [d].[Name]
```

### 2. Results correctly but using co related queries

```cs
private static async Task<IResult> GetDepartmentsWithEmployeeCount2(AppDbContext context)
 {
 var departmets = await context.Departments
 .Include(d => d.Employees)
 .GroupBy(d => new { d.DepartmentId, d.Name })
 .Select(g =>
 new DepartmentWithEmployeeCount(
 g.Key.DepartmentId,
 g.Key.Name,
 g.SelectMany(d => d.Employees).Count()
 )
 )
 .ToListAsync();
 return TypedResults.Ok(departmets);
 }
```

Which results in:

```sql
-- 2
SELECT [d].[DepartmentId], [d].[Name], (
 SELECT COUNT(*)
 FROM [Departments] AS [d0]
 INNER JOIN [Employees] AS [e] ON [d0].[DepartmentId] = [e].[DepartmentId]
 WHERE [d].[DepartmentId] = [d0].[DepartmentId] AND [d].[Name] = [d0].[Name])
 FROM [Departments] AS [d]
 GROUP BY [d].[DepartmentId], [d].[Name]
```

### 3. Using Group join

```cs
private static async Task<IResult> GetDepartmentsWithEmployeeCount3(AppDbContext context)
 {
 var departments = await context.Departments
 .GroupJoin(
 context.Employees,
 d => d.DepartmentId,
 e => e.DepartmentId,
 (d, employees) => new DepartmentWithEmployeeCount(
 d.DepartmentId,
 d.Name,
 employees.Count()
 )
 )
 .ToListAsync();
 return TypedResults.Ok(departments);
 }
```

Which results in:

```sql
SELECT [d].[DepartmentId], [d].[Name], (
 SELECT COUNT(*)
 FROM [Employees] AS [e]
 WHERE [d].[DepartmentId] = [e].[DepartmentId])
 FROM [Departments] AS [d]
```

### 4th way

```cs
private static async Task<IResult> GetDepartmentsWithEmployeeCount4(AppDbContext context)
 {
 Console.WriteLine("---4---");
 var departments = await context.Departments
 .GroupBy(d => new { d.DepartmentId, d.Name })
 .Select(g => new DepartmentWithEmployeeCount
 (
 g.Key.DepartmentId,
 g.Key.Name,
 context.Employees.Count(e => e.DepartmentId == g.Key.DepartmentId)
 )
 ).ToListAsync();

        return TypedResults.Ok(departments);
    }
```

Which leads to sql query:

```sql
SELECT [d].[DepartmentId], [d].[Name], (
 SELECT COUNT(*)
 FROM [Employees] AS [e]
 WHERE [e].[DepartmentId] = [d].[DepartmentId])
 FROM [Departments] AS [d]
 GROUP BY [d].[DepartmentId], [d].[Name]
```

### 5th

```cs
// 5
 private static async Task<IResult> GetDepartmentsWithEmployeeCount5(AppDbContext context)
 {
 Console.WriteLine("---5---");
 var departments = await context.Departments
 .Select(d => new DepartmentWithEmployeeCount(
 d.DepartmentId,
 d.Name,
 d.Employees.Count()
 ))
 .ToListAsync();

        return TypedResults.Ok(departments);
    }
```

Equivalent sql (which is similar to 3rd, solution with GroupJoin):

```sql
SELECT [d].[DepartmentId], [d].[Name], (
SELECT COUNT(*)
FROM [Employees] AS [e]
WHERE [d].[DepartmentId] = [e].[DepartmentId])
FROM [Departments] AS [d]
```

### 6. Using older linq query

Finally I have executed the older type of linq query and it generated the sql, that I need. I used it a lot in my starting .NET Days. It exactly gave me the result I need.

```cs
private static async Task<IResult> GetDepartmentsWithEmployeeCount6(AppDbContext context)
 {
 Console.WriteLine("---6---");
 var departments = await (from d in context.Departments
 join e in context.Employees
 on d.DepartmentId equals e.DepartmentId
 into empGroup
 from e in empGroup.DefaultIfEmpty()
 group e by new { d.DepartmentId, d.Name } into g
 select new DepartmentWithEmployeeCount( g.Key.DepartmentId,
 g.Key.Name,
 g.Count(e => e != null)
 )
 ).ToListAsync();

        return TypedResults.Ok(departments);
    }
```

This type of LINQ looks complicated and verbose, but do not look mysterious like the previous ones. You can easily predict, what SQL query will be generated.

equivalent sql:

```sql
SELECT [d].[DepartmentId], [d].[Name], COUNT(CASE
 WHEN [e].[EmployeeId] IS NOT NULL THEN 1
 END)
 FROM [Departments] AS [d]
 LEFT JOIN [Employees] AS [e] ON [d].[DepartmentId] = [e].[DepartmentId]
 GROUP BY [d].[DepartmentId], [d].[Name]
```

May be there are more solutions of it and they may be better but I am not aware of them.

### Which queries are better?

I am not good at analyzing which query performs best. Also I do not have large dataset to test with. According to GPTs there ranks are (I confirmed it with multiple AIs):

1. Query 6
2. Query 3 (Using GroupJoin) and Query5 which generate similar sql query.

### Which Queries Are Less Efficient?

- Query 1: Skips departments with 0 employees → Incorrect result.
- Query 2: Uses correlated subqueries, performing redundant work.
- Query 4: Calls `context.Employees.Count(e => e.DepartmentId == g.Key.DepartmentId)` inside the projection, which executes a separate subquery for each department → worst performance

**Sometimes LINQ queries feels like big black box. They looks simple and mysterious at the same time. We need to be careful with them and must check the generated sql query.**

[Canonical link](https://medium.com/@ravindradevrani/curious-case-of-linqs-groupby-75fe8d7fd32d)
