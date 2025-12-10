+++
date = '2025-02-24T16:09:29+05:30'
draft = false
title = 'LINQ: SelectMany()'
tags = ['csharp','linq']
categories= ['programming']
image = '/images/1__maTUD1moRoBBMI2xmBV-Q.png'
+++

<!-- ![select many operator in linq](/images/1__maTUD1moRoBBMI2xmBV-Q.png) -->

NOTE: You can find the source code [here](https://github.com/rd003/DotnetPracticeDemos/tree/master/SelectManyDemo/SelectManyDemo "https://github.com/rd003/DotnetPracticeDemos/tree/master/SelectManyDemo/SelectManyDemo").

### Schema Overview

```cs
// Department
public class Department
{
    public int DepartmentId { get; set; }
    public string Name { get; set; } = string.Empty;

    public ICollection<Employee> Employees { get; set; } = [];
}

// Employee

public class Employee
{
    public int EmployeeId { get; set; }
    public string Name { get; set; } = string.Empty;

    public int DepartmentId { get; set; }

    public Department Department { get; set; } = null!;

    public ICollection<EmployeeSkill> EmployeeSkills { get; set; } = [];
}

// Skills

public class Skill
{
    public int SkillId { get; set; }
    public string Name { get; set; } = string.Empty;

    public ICollection<EmployeeSkill> EmployeeSkills { get; set; } = [];
}

// EmployeeSkills (Junction table)

public class EmployeeSkill
{
    public int EmployeeId { get; set; }
    public int SkillId { get; set; }

    public Employee Employee { get; set; } = null!;
    public Skill Skill { get; set; } = null!;
}
```

In simpler terms:

- We have `Departments` entity
- We have `Skills` entity
- We have `Employees` entity
- An `Employee` must have one Department (can only have one department also)
- An `Employee` can have multiple `Skills` thats why we have a junction table named `EmployeeSkills`

### Employee data

I am also giving the employee data which would make easier to understand the further process. You can compare this data with the response of the other endpoints.

```json
[
  {
    "employeeId": 3,
    "name": "Bob Wilson",
    "departmentName": "Marketing",
    "skills": ["Digital Marketing"]
  },
  {
    "employeeId": 2,
    "name": "Jane Doe",
    "departmentName": "Engineering",
    "skills": ["Python", "C#"]
  },
  {
    "employeeId": 1,
    "name": "John Smith",
    "departmentName": "Engineering",
    "skills": ["SQL", "C#"]
  }
]
```

### Find all the employees from a particular department

```cs
app.MapGet("/api/departments/{departmentId}/employees", async (int departmentId, AppDbContext context) =>
{
 var employees = await context.Departments
 .Where(d => d.DepartmentId == departmentId)
 .SelectMany(d => d.Employees)
 .Select(e => e.Name)
 .ToListAsync();
 return Results.Ok(employees);
});
```

If we run this api :

```txt
GET {{base_address}}/api/departments/1/employees
Accept: application/json
```

The response will be:

```json
["Jane Doe", "John Smith"]
```

### Find all the skills of a particullar employee

```cs
app.MapGet("api/employees/{employeeId}/skills", async (int employeeId, AppDbContext context) =>
{
 var skills = await context.Employees
 .Where(e => e.EmployeeId == employeeId)
 .SelectMany(e => e.EmployeeSkills)
 .Select(e => e.Skill.Name)
 .ToListAsync();
 return Results.Ok(skills);
});
```

If we run this api:

```txt
GET {{base_address}}/api/employees/1/skills
Accept: application/json
```

The output would be:

```json
["SQL", "C#"]
```

> **SelectMany()** method flattens the nested collections into a single sequence.

---

[Canonical link](https://medium.com/@ravindradevrani/understanding-linqs-selectmany-method-b5528b62d7c7)
