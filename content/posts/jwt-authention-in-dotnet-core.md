+++
date = '2025-05-18T17:11:50+05:30'
draft = false
title = 'Jwt Authention and role base authorization in Dotnet Core'
tags = ["dotnet","authentication"]
categories= ['programming']
+++


![jwt-authentication-in-dotnet](/images/jwt-dotnet-9.webp)

## Create a new web api project

Run these commands in a sequence to create a new project.

```sh
dotnet new sln -o JwtDotnet9

cd JwtDotnet9

dotnet sln add JwtDotnet9/JwtDotnet9.csproj
```

Open the project in vs code.

```sh
code .
```

=> [Source Code](https://github.com/rd003/JwtDotnet9)

=> [Securing The .NET 9 App: Signup, Login, JWT, Refresh Tokens, and Role Based Access with PostgreSQL](https://ravindradevrani.com/posts/dotnet-core-jwt-refresh-token/)



## Install the required nuget packages

```sh
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
```

## Jwt configuration in appsettings

Open `appsettings.json` and add these lines

```json
  "JWT": {
    "ValidAudience": "http://localhost:5163",
    "ValidIssuer": "http://localhost:5163",
    "Secret": "your-32-characters-long-super-strong-jwt-secret-key"
  }
```

Let's understand, what are these:

- **ValidAudience**: It defines who is going to consume this token. In our case, the application running on the `http://localhost:5163` can consume this token. Make sure to change it to according to your audience.
- **ValidIssuer**: Issuer of the token.
- **JwtSecret** : Secret key for the token. We are going to store it in appsettings for the sake of simplicity. But this value should be rotated, that is why, for production we need to put it in a place like `azure key vault`.

## JWT configuration in Program.cs

Open the `Program.cs` and add these lines.

```cs
// Authentication
builder.Services.AddAuthentication(options =>
{
options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
options.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
options.SaveToken = true;
options.RequireHttpsMetadata = false;
options.TokenValidationParameters = new TokenValidationParameters
{
ValidateIssuer = true,
ValidateAudience = true,
ValidAudience = builder.Configuration["JWT:ValidAudience"],
ValidIssuer = builder.Configuration["JWT:ValidIssuer"],
ClockSkew = TimeSpan.Zero,
IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["JWT:secret"]))
};
});

```

If you don't set `ClockSkew = TimeSpan.Zero', then you can not set JWT expiry time to less than 5 minutes. For testing stuff, you need short expiry (around 1 or 2 min).

Make sure to include these lines also

```cs
app.UseAuthentication();
app.UseAuthorization();

```

## Token Service

```cs
// Services/TokenService.cs

using System.Security.Claims;

namespace JwtDotnet9.Services;

public interface ITokenService
{
    string GenerateAccessToken(IEnumerable<Claim> claims);
}

public class TokenService : ITokenService
{
    public string GenerateAccessToken(IEnumerable<Claim> claims)
    {
        throw new NotImplementedException();
    }
}}
```

For the sake of simplicity, I have created the interface and a class in the same file, it is not a recommended practice, make sure to create them separately.

Let's implement the `TokenService` class and inject the `IConfiguration` to it. Through `IConfiguration` we can get things from `appsettings.json`.

```cs
public class TokenService : ITokenService
{
    private readonly IConfiguration _configuration;
    public TokenService(IConfiguration configuration)
    {
        _configuration = configuration;
    }

    public string GenerateAccessToken(IEnumerable<Claim> claims)
    {
        throw new NotImplementedException();
    }
}
```

Let's complete the `GenerateAccessToken()` method.

```cs
    public string GenerateAccessToken(IEnumerable<Claim> claims)
    {
        var tokenHandler = new JwtSecurityTokenHandler();

        // Create a symmetric security key using the secret key from the configuration.
        var authSigningKey = new SymmetricSecurityKey
                        (Encoding.UTF8.GetBytes(_configuration["JWT:Secret"]));

        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Issuer = _configuration["JWT:ValidIssuer"],
            Audience = _configuration["JWT:ValidAudience"],
            Subject = new ClaimsIdentity(claims),
            Expires = DateTime.Now.AddMinutes(15),
            SigningCredentials = new SigningCredentials
                          (authSigningKey, SecurityAlgorithms.HmacSha256)
        };

        var token = tokenHandler.CreateToken(tokenDescriptor);

        return tokenHandler.WriteToken(token);
    }  
```

## Register the token service

```cs
// Program.cs

builder.Services.AddTransient<ITokenService, TokenService>();
```

## Create a login model

```cs
// Models/LoginModel.cs

using System.ComponentModel.DataAnnotations;

namespace JwtDotnet9.Models;

public class LoginModel
{
    [Required]
    public string Username { get; set; } = string.Empty;

    [Required]
    public string Password { get; set; } = string.Empty;

}
```

## Create UserModel

```cs
// Models/User.cs

namespace JwtDotnet9.Models;

public class User
{
    public string Username { get; set; } = string.Empty;
    public string Password { get; set; } = string.Empty;
    public List<string> Roles { get; set; } = [];
}
```

## UserService

Create a user service to manipulate the user related operation. I have created a list of users, because I am not going to use any database in this project. You know why (for the sake of simplicity). For production, please use `Identity` or any similar authentication mechanism to authenticate and store the user.

```cs
// Services/UserService.cs
using JwtDotnet9.Models;

namespace JwtDotnet9.Services;

public interface IUserService
{
    User? GetUser(string username, string password);
}

public class UserService : IUserService
{
    private List<User> _users = new()
    {
        new()
        {
            Username = "admin",
            Password = "admin123",
            Roles = ["Admin"]
        },
        new()
        {
            Username = "user",
            Password = "user123",
            Roles = ["User"]
        }
   };

    public User? GetUser(string username, string password)
    {
        return _users.FirstOrDefault(u => u.Username == username && u.Password == password);
    }
}
```

Make sure to register it in the `Program.cs`

```cs
builder.Services.AddTransient<IUserService, UserService>();
```

## Create AccountController

Create `AccountController` and inject `ITokenService` and `IUserService` to it.

```cs
// Controllers/AccountController.cs
[ApiController]
[Route("/accounts")]
public class AccountController : ControllerBase
{

    private readonly ITokenService _tokenService;
    private readonly IUserService _userService;

    public AccountController(ITokenService tokenService, IUserService userService)
    {
        _tokenService = tokenService;
        _userService = userService;
    }
}
```

Let's implement the `Login()` method

```cs
   [HttpPost("login")]
    public IActionResult Login(LoginModel model)
    {
        try
        {
            var user = _userService.GetUser(model.Username, model.Password);

            if (user == null)
            {
                return Unauthorized("Invalid username or password");
            }

            // creating the necessary claims

            List<Claim> claims = [
                new (ClaimTypes.Name, user.Username),  // claim to store name
            new (JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString())
            // unique identifier for jwt
            ];

            // adding roles to claims

            foreach (var role in user.Roles)
            {
                claims.Add(new Claim(ClaimTypes.Role, role));
            }

            // generating access token
            var token = _tokenService.GenerateAccessToken(claims);

            return Ok(token);
        }
        catch (Exception ex)
        {
            return Unauthorized();
        }
    }
```

### What is Claim?

A `claim` represents a piece of information about a user in the form of key-value pair. Claims are present in the tokens. Example:

```cs
// Built-in Claim Types
new Claim(ClaimTypes.Name, "johndoe") // Username
new Claim(ClaimTypes.Email, "john@example.com") // Email address
new Claim(ClaimTypes.Role, "Admin") // User role
// Cusom claim
new Claim("Department", "IT") // Custom claim

```

## Testing the endpoint

I am using [Rest Client vs code extension by Huachao Mao](https://marketplace.visualstudio.com/items?itemName=humao.rest-client). If you are using Visual Studio 2022, it is already integrated. However, you can use any client of your choice (eg. Postman, Insomnia).

In your application, you have a file with extension `.http`. In my project it is named as `JwtDotnet9.http`. Open that file, which should look like this

```
@JwtDotnet9_HostAddress = http://localhost:5163

GET {{JwtDotnet9_HostAddress}}/weatherforecast/
Accept: application/json

###
```

### Login endpoint test

Add these line below the symbol `###`.

```.http

POST {{JwtDotnet9_HostAddress}}/accounts/login
Content-Type: application/json

{
    "username":"user",
    "password":"user123"
}
```

Above the line `POST {{JwtDotnet9_HostAddress}}/accounts/login`, you must be seeing a link `Send Request`, click on it and you will get a response:

```txt
HTTP/1.1 200 OK
Connection: close
Content-Type: text/plain; charset=utf-8
Date: Sun, 18 May 2025 08:20:10 GMT
Server: Kestrel
Transfer-Encoding: chunked

eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InVzZXIiLCJqdGkiOiIzZTJhZDRmZC04OGY3LTQwMjUtYTkzMi0zN2YxYzkyMTgwYzIiLCJyb2xlIjoiVXNlciIsIm5iZiI6MTc0NzU1NjQxMSwiZXhwIjoxNzQ3NTU3MzExLCJpYXQiOjE3NDc1NTY0MTEsImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTE2MyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTE2MyJ9.DnjVf-vh-xnMlooRofIs7iiLrgAmAz9_ZJGUcIeBDDk
```

You can easily decode the JWT using a website named `jwt.io`. Let's see what is inside our JWT :

```json
{
  "unique_name": "user",
  "jti": "3e2ad4fd-88f7-4025-a932-37f1c92180c2",
  "role": "User",
  "nbf": 1747556411,
  "exp": 1747557311,
  "iat": 1747556411,
  "iss": "http://localhost:5163",
  "aud": "http://localhost:5163"
}
```

## Authenticating the endpoints

We can authentication our endpoints in two way:

### 1. At individual method level

You just need to put `Authorize` attribute over the method.

```cs
[Authorize]
public IEnumerable<WeatherForecast> Get()
{

}
```

### 2. At controller level

Put `Authorize` attribute above controller and all the methods of the Controller will be authorized.

```cs
[Authorize]
[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{

}
```


### Allow anonymous

If you put `[Authorize]` attribute at the controller level, then all the methods of the controller are going to be authorized. If you want to bypass the security for some controller methods then you need to add `AllowAnonymous` attribute above that method.

```cs
    [AllowAnonymous]
    [HttpGet("/some-method")]
    public IActionResult SomeMethod()
    {
        return Ok();
    }
```

## Let's test the authenticated resource

Request:

```txt
GET {{JwtDotnet9_HostAddress}}/weatherforecast/
Accept: application/json
```

Response:

```txt
HTTP/1.1 401 Unauthorized
Content-Length: 0
Connection: close
Date: Sun, 18 May 2025 10:22:33 GMT
Server: Kestrel
WWW-Authenticate: Bearer
```

## How to access the authenticated resource

To access the authenticated resource, first hit the `login` endpoint and copy the `JWT` from the response.

You need to pass JWT in the `Authorization` header. Make sure to prepend `Bearer` in the JWT token.

eg. `Authorization : Bearer your_jwt`

```txt

GET {{JwtDotnet9_HostAddress}}/weatherforecast/
Accept: application/json
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6InVzZXIiLCJqdGkiOiI4ZmUzNDhiYi02MjI2LTRjNGItYWFlOC0wNzIxNzYzZDdlMDgiLCJyb2xlIjoiVXNlciIsIm5iZiI6MTc0NzU2NDQzOSwiZXhwIjoxNzQ3NTY1MzM5LCJpYXQiOjE3NDc1NjQ0MzksImlzcyI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTE2MyIsImF1ZCI6Imh0dHA6Ly9sb2NhbGhvc3Q6NTE2MyJ9.ybr5EkOmXSAGWRgCvW3ZhTzJJ_7WRAzS_YXR7gFuaLM
```

## Role based authorization

What if you want to allow access to specific 'Role' (eg. Admin). Then you just need to add `Roles` value in the `Authorize` attribute.

eg. `[Authorize(Roles = "Admin")]` 

For multiple roles: `[Authorize(Roles = "Admin,Accounts,SomeOtherRole")]`

```cs
[Authorize(Roles = "Admin")]
[ApiController]
[Route("[controller]")]
public class WeatherForecastController : ControllerBase
{

}
```

Now, if you try to access the `/weatherforecast` endpoint with user's `JWT`. Then you will get the `403 forbidden` as a response. Which indicates that you are an authenticated user, but you have no access rights to access this resource. 

```txt
HTTP/1.1 403 Forbidden
Content-Length: 0
Connection: close
Date: Sun, 18 May 2025 10:48:45 GMT
Server: Kestrel
```

To access this resource, you have to login with `admin` credentials and then use that `JWT` to access the protected resources.

