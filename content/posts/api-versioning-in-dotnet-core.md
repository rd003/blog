+++
date = '2025-02-19T22:07:03+05:30'
draft = false
title = 'Api Versioning in Dotnet Core'
tags= ["dotnet"]
categories = ["programming"]
+++

![Api versioning in .net core](/images/api_versioning_in_dotnet_core.jpg)

[Photo by Jan Loyde Cabrera at medium.com](https://unsplash.com/@thekidph?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

When you are going to do some breaking changes in your apis, it is better to create a new version for that, so that user don't freaked out. They still can use the older APIs and get ready for new
changes. There are various way to create a versions of your APIs like

1. Query string
2. URL
3. HTTP header

> If you prefer video version then you can checkout this video with same content.

{{< youtube id="YGv_3-nWo8Y991cH0" title="api versioning in .net core" autoplay="false" >}}

We are going to look into the 2nd option, Versioning with URL.

Create a new project with .net cli

```bash
dotnet new webapi -o ApiVersionDemo
code ApiVersionDemo
```

Now install this package:

```bash
Microsoft.AspNetCore.Mvc.Versioning
```

Open the **program.cs** file and add these line.

```cs
 builder.Services.AddApiVersioning(options =>
    {
        options.DefaultApiVersion = new ApiVersion(1, 0);
        options.AssumeDefaultVersionWhenUnspecified = true;
        options.ReportApiVersions = true;
    });
```

Now lets break it a bit.

**_DefaultApiVersion,_** sets the default version, if not passed.

**_AssumeDefaultVersionWhenUnspecified,_** specifies that whether or not
to assume a default api version, if version not specified. I

By setting **_ReportApiVersions=true,_** this option enables sending the
**api-supported-versions** and **api-deprecated-versions** HTTP header
in responses.

Lets create our first Controller with name **UsersController** and write
this code there.

```cs
using Microsoft.AspNetCore.Mvc;

namespace ApiVersioningDemo.Controllers
{
    [ApiVersion("1.0")]
    [Route("api/v{version:apiVersion}/users")]
    [ApiController]
    public class UsersController : ControllerBase
    {
        List<string> users= new List<string>{"A1","A7","A5","A4","A5","B1","B2","B5","B6","B57","B21"};

        [HttpGet]
        public IActionResult Get(){
            return Ok(users);
        }
    }
}
```

Attribute ApiVersion("1.0") tells that it is a version 1 api endpoint.
Now lets, test these api and in response header you will get
**_api-supported-version_** information. Your endpoint will be
**_"/api/v32/users"._** I am using **ThunderClient** extension of vs
code, to test web apis, you can use other options like **postman** or
**insomnia**.

![api_v1](/images/api_v1.png)

Now, lets create second version to of this API. Create a new controller
**UsersV2Controller.**

```cs
using Microsoft.AspNetCore.Mvc;

namespace ApiVersioningDemo.Controllers
{
    [ApiVersion("2.0")]
    [Route("api/v{version:apiVersion}/users")]
    [ApiController]
    public class UsersV2Controller : ControllerBase
    {
        List<string> users= new List<string>{"A1","A7","A5","A4","A5","B1","B2","B5","B6","B57","B21"};

        [HttpGet]
        public IActionResult Get(){
            users= users.Where(user=>user.ToLower().StartsWith("b")).ToList();
            return Ok(users);
        }
    }
}
```

This controller's get method will return the list of string, which
starts with "b". Lets check its response header. Your endpoint will be
**_"/api/v2/users"._**

![api_v2](/images/api_v2.png)

Now, it is a good choice to deprecate the older version, so that
consumer can prepare for newer version. In version 1 controller ,
replace the ApiVersion attribute with this code.

```cs
[ApiVersion("1.0",Deprecated =true)]
```

Your controller will look like this now.

```cs
    [ApiVersion("1.0",Deprecated =true)]
    [Route("api/v{version:apiVersion}/users")]
    [ApiController]
    public class UsersController : ControllerBase
    {
      // other stuff will be the same
    }
```

You can check the response header now.

![api_v1_deprecated](/images/api_v1_deprecated.png)

[Canonical
link](https://medium.com/@ravindradevrani/api-versioning-in-net-core-net-7-2eab5142f5a0)
