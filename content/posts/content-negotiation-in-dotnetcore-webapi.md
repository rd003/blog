+++
date = '2025-11-22T16:23:29+05:30'
draft = false
title = 'Content Negotiation in Dotnet Core Webapi'
tags = ['dotnet']
categories = ['programming']
image = '/images/content-negotiation.jpg'
+++
<!-- ![content negotiation in dotnet web apis](/images/content-negotiation.jpg) -->

As defined in [rfc2616](https://datatracker.ietf.org/doc/html/rfc2616#section-12) - **"Content nagotiation is the process of selecting the best representation for a given response when there are multiple representations available."**

Clients passes the header `Accept` with values like `application/json`,`application/xml` etc and tells this format is acceptable. Then server gives the response according to that.

In simpler terms, if your API supports xml, json and csv media type, then let clients decide which kind of media type they need as a response.

By default dotnet core supports these media types:

- application/json
- text/json
- text/plain

Let's understand it with example.

```cs
[HttpGet]
public IActionResult GetPeople()
{
    List<Person> people = [
        new(){FirstName="Ravindra", LastName="Devrani" },
        new(){FirstName="John", LastName="Doe" },
        new(){FirstName="Satyendra", LastName="Negi" }
        ];
    return Ok(people);
}
```

Lets make a `cUrl` request to test this endpoint:

```bash
 curl -H "Accept: application/xml" http://localhost:5170/api/people

[{"firstName":"Ravindra","lastName":"Devrani"},{"firstName":"John","lastName":"Doe"},{"firstName":"Satyendra","lastName":"Negi"}]
```
As you may have noticed I have passed `Accept: application/xml` as a header. Which means, I have asked for `application/xml`but I am getting the json format. So, it means, it won't happen automatically. We have to configure it manually.

## Enabling the xml response

To enable xml response, we need to add these lines.

```cs
// Program.cs
builder.Services.AddControllers(op =>
{
    op.RespectBrowserAcceptHeader = true;
}).AddXmlSerializerFormatters();
```

Let's make a curl request now:

```bash
curl -H "Accept: application/xml" http://localhost:5170/api/people

<ArrayOfPerson xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><Person><FirstName>Ravindra</FirstName><LastName>Devrani</LastName></Person><Person><FirstName>John</FirstName><LastName>Doe</LastName></Person><Person><FirstName>Satyendra</FirstName><LastName>Negi</LastName></Person></ArrayOfPerson>
```

Right now it only supports `application/json`,`text/json`, `application/xml`, `text/xml` or xml and json formats in general. If you ask for other than this it returns the default format which is `application/json`

```sh
 curl -H "Accept: text/csv" http://localhost:5170/api/people
[{"firstName":"Ravindra","lastName":"Devrani"},{"firstName":"John","lastName":"Doe"},{"firstName":"Satyendra","lastName":"Negi"}]
```

In the example above, we are asking for `text/csv`. It returns the json data.

However, we can return `406 Not Acceptable` status code, if it does not support that media type.

```cs
builder.Services.AddControllers(op =>
{
    op.RespectBrowserAcceptHeader = true;
    op.ReturnHttpNotAcceptable = true; // 👈 Add this line
}).AddXmlSerializerFormatters();
```

Let's test this:

```sh
curl -H "Accept: text/csv" http://localhost:5170/api/people -v
* Host localhost:5170 was resolved.
* IPv6: ::1
* IPv4: 127.0.0.1
*   Trying [::1]:5170...
* Connected to localhost (::1) port 5170
* using HTTP/1.x
> GET /api/people HTTP/1.1
> Host: localhost:5170
> User-Agent: curl/8.14.1
> Accept: text/csv
>
< HTTP/1.1 406 Not Acceptable ## 👈 Notice this line
< Content-Length: 0
< Date: Sat, 22 Nov 2025 10:33:24 GMT
< Server: Kestrel
<
* Connection #0 to host localhost left intact
```

## Custom formatter

We can also define the custom output formatter. Create a new class named `CsvOutputFormatter`, which inherits from `TextOutputFormatter` base class.

```cs
// CsvOutputFormatter.cs
public class CsvOutputFormatter : TextOutputFormatter
{
    public CsvOutputFormatter()
    {
        SupportedMediaTypes.Add(MediaTypeHeaderValue.Parse("text/csv"));
        SupportedEncodings.Add(Encoding.UTF8);
        SupportedEncodings.Add(Encoding.Unicode);
    }

    public override async Task WriteResponseBodyAsync(OutputFormatterWriteContext context, Encoding selectedEncoding)
    {
        var response = context.HttpContext.Response;
        var buffer = new StringBuilder();
        if (context.Object is IEnumerable<object> items)
        {
            var firstItem = items.FirstOrDefault();
            if (firstItem != null)
            {
                var properties = firstItem.GetType().GetProperties();
                buffer.AppendLine(string.Join(",", properties.Select(p => p.Name)));

                foreach (var item in items)
                {
                    var values = properties.Select(p => p.GetValue(item)?.ToString() ?? string.Empty);
                    buffer.AppendLine(string.Join(",", values));
                }
            }
        }
        await response.WriteAsync(buffer.ToString(), selectedEncoding);
    }
}
```

In Program.cs

```cs
// Program.cs
builder.Services.AddControllers(op =>
{
    op.RespectBrowserAcceptHeader = true;
    op.ReturnHttpNotAcceptable = true;
    op.OutputFormatters.Add(new CsvOutputFormatter()); // 👈 Add this line
}).AddXmlSerializerFormatters();
```

Let's test this:

```sh
curl -H "Accept: text/csv" http://localhost:5170/api/people
FirstName,LastName
Ravindra,Devrani
John,Doe
Satyendra,Negi
```