+++
date = '2025-02-20T10:31:52+05:30'
draft = false
title = 'JWT Authentication and Role Based Authorization in Dotnet Core'
tags = ["dotnet","authentication"]
category = ["programming"]
+++

![JWT Authentication in dotnet core](/images/jwt_role_based_auth.png)

## JWT

According to [jwt.io](https://jwt.io/) JSON Web Tokens are an open, industry standard [**RFC7519**](https://tools.ietf.org/html/rfc7519) method for representing claims securely between two parties.

When we create REST APIs, then we don't want that any one can access
those apis. REST APIs, will only be accessed by the authenticated user.
We authenticate our user with the help of jwt.

**How jwt works?**

First, we give an authentication endpoint to user, where he/she puts
credential, in return we give a jwt token to user which have an expiry
date. To consume any protected resource, user need to pass jwt token on
authorization header.

In this tutorial we will learn how to secure our .net 7 apis with jwt
and how to create secure resources on the basis of role.

Let's create a new project, open visual studio, create a new project of
type Asp.net Core WebApp.

Name of solution is **"Book-Store-Spa-Backend"** and project is
**"BookStore.Api".**

![jwt_rbac_project_create1](/images/jwt_rbac_project_create1.png)

Now, use the configuration below and click on next.

![jwt_rbac_project_create2](/images/jwt_rbac_project_create1.png)

Now we have successfully created a .net core solution with api project,
but we need another project for data layer. So right click on solution
and add .net project type of class library.

![jwt_rbac_project_create3](/images/jwt_rbac_project_create3.png)

![jwt_rbac_project_create4](/images/jwt_rbac_project_create4.png)

Now we have created the desired solution.

**Book-Store-Spa-Backend** is our root folder, inside it we have a
**sln** file and 2 different projects.

(i) BookStore.Api (UI layer)

(ii) BookStore.Data (Data layer)

**⚠️** Now add the reference of **BookStore.Data** in **BookStore.Api ⚠️**

---

Add the following nuget packages in **BookStore.Data**

```cs
Microsoft.EntityFrameworkCore.SqlServer
Microsoft.EntityFrameworkCore.Tools
Microsoft.AspNetCore.Identity.EntityFrameworkCore
```

Add the following packages in **BookStore.Api** project.

```bash
Microsoft.EntityFrameworkCore.Design

Microsoft.AspNetCore.Authentication.JwtBearer
```

Add these line into **appsettings.json** file

```json
  "ConnectionStrings": {
    "conn": "data source=.;initial catalog=BookStoreBackend;integrated security=True;TrustServerCertificate=True"
  },
  "JWT": {
    "ValidAudience": "https://localhost:7062",
    "ValidIssuer": "https://localhost:7062",
    "Secret": "ByYM000OLlMQG6VVVp1OH7Xzyr7gHuw1qvUC5dcGt3SNM"
  },
```

Here,

**"ConnectionStrings"** represents the connection string value to
connect with database.

**ValidAudience** is the valid audience for the app.

**ValidIssuer** is the issuer of token

Note: `https://localhost:7062` is the url of our app that will run
on kestrel server. You can find it in
**_Bookstore.Api/Properties/appsettings.json._**

**_👉 BookStore.Data/Models/ApplicationUser.cs_**

```cs
using System.ComponentModel.DataAnnotations;
using Microsoft.AspNetCore.Identity;

namespace BookStaore.Data.Models;

/// <summary>
        /// ApplicationUser class will inherit the class IdentityUser so that we can add a field Name to User's Identity table in database
/// </summary>
public class ApplicationUser : IdentityUser{

/// <summary>
        /// Gets or sets the name of the user. Maximum length is 30 characters.
/// </summary>
 [MaxLength(30)]
   public string? Name { get; set; }
}
```

Since we can not directly add any new field to identity tables, it will
add a new field "Name" to identity table.

👉**_BookStore.Data/Models/ApplicationDbContext.cs_**

```cs
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace BookStore.Data.Models;
/// <summary>
/// Provides a database context for the BookStore application using Entity Framework Core and Identity Framework.
/// </summary>
public class ApplicationDbContext : IdentityDbContext<ApplicationUser>
{
    /// <summary>
    /// Initializes a new instance of the ApplicationDbContext class with the specified DbContext options.
    /// </summary>
    /// <param name="options">The options to be used by the DbContext.</param>
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) : base(options)
    {
        // The base constructor handles initializing the DbContext with the provided options.
    }
}
```

Add following lines in **Program.cs** file:

```cs
using BookStore.Data.Models;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using System.Text;


builder.Services.AddDbContext<ApplicationDbContext>(options => options.UseSqlServer(builder.Configuration.GetConnectionString("conn")));

// For Identity
builder.Services.AddIdentity<ApplicationUser, IdentityRole>()
                .AddEntityFrameworkStores<ApplicationDbContext>()
                .AddDefaultTokenProviders();
// Adding Authentication
builder.Services.AddAuthentication(options =>
            {
                options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
                options.DefaultScheme = JwtBearerDefaults.AuthenticationScheme;
            })

// Adding Jwt Bearer
            .AddJwtBearer(options =>
            {
                options.SaveToken = true;
                options.RequireHttpsMetadata = false;
                options.TokenValidationParameters = new TokenValidationParameters()
                {
                    ValidateIssuer = true,
                    ValidateAudience = true,
                    ValidAudience = builder.Configuration["JWT:ValidAudience"],
                    ValidIssuer = builder.Configuration["JWT:ValidIssuer"],
                    ClockSkew = TimeSpan.Zero,
                    IssuerSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(builder.Configuration["JWT:Secret"]))
                };
            });

// add app.UseAuthentication() middleware


app.UseHttpsRedirection(); // existing line
app.UseAuthentication(); // 👈👈it is new line
app.UseAuthorization(); // existing line
app.MapControllers();// existing line
```

### **Migrations:**

In order to add identity and our custom tables (although we did not
created any), we need to run following migration commands.

Open **package manager console** and select **default project** from
dropdown to **BookStore.Data** . Migration commands will work on
**BookStore.Data** since our DbContext file is in BookStore.Data
project. Run these two migration commands

```cs
add-migration init
update-database
```

---

**_👉BookStore.Data/Models/UserRoles.cs_**

```cs
namespace BookStore.Data.Models
{
    /// <summary>
    /// A static class that defines the available user roles in the application.
    /// </summary>
    public static class UserRoles
    {
        /// <summary>
        /// The role name for the administrator.
        /// </summary>
        public const string Admin = "Admin";

        /// <summary>
        /// The role name for regular users.
        /// </summary>
        public const string User = "User";
    }
```

**_👉BookStore.Data/Models/RegistrationModel.cs_**

```cs
using System.ComponentModel.DataAnnotations;

namespace BookStore.Data.Models;
public class RegistrationModel
{
    [Required(ErrorMessage = "User Name is required")]
    public string? Username { get; set; }

    [Required(ErrorMessage = "Name is required")]
    public string? Name { get; set; }

    [EmailAddress]
    [Required(ErrorMessage = "Email is required")]
    public string? Email { get; set; }

    [Required(ErrorMessage = "Password is required")]
    public string? Password { get; set; }
}
```

**_👉BookStore.Data/Models/LoginModel.cs_**

```cs
using System.ComponentModel.DataAnnotations;

namespace BookStore.Data.Models;

public class LoginModel
{
      [Required(ErrorMessage = "User Name is required")]
      public string? Username { get; set; }

      [Required(ErrorMessage = "Password is required")]
      public string? Password { get; set; }
}
```

---

Lets create authorization service, where we will implement registration
and login functionality.

👉**_BookStore.Api/Services/IAuthService.cs_**

```cs
public interface IAuthService
    {
        Task<(int, string)> Registeration(RegistrationModel model, string role);
        Task<(int, string)> Login(LoginModel model);
    }
```

👉**_BookStore.Api/Services/AuthService.cs_**

```cs
using BookStore.Data.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using System.Text;

namespace BookStore.Api.Services
{
    public class AuthService : IAuthService
    {
        private readonly UserManager<ApplicationUser> userManager;
        private readonly RoleManager<IdentityRole> roleManager;
        private readonly IConfiguration _configuration;
        public AuthService(UserManager<ApplicationUser> userManager, RoleManager<IdentityRole> roleManager, IConfiguration configuration)
        {
            this.userManager = userManager;
            this.roleManager = roleManager;
            _configuration = configuration;

        }
        public async Task<(int,string)> Registeration(RegistrationModel model,string role)
        {
            var userExists = await userManager.FindByNameAsync(model.Username);
            if (userExists != null)
                return (0, "User already exists");

            ApplicationUser user = new ApplicationUser()
            {
                Email = model.Email,
                SecurityStamp = Guid.NewGuid().ToString(),
                UserName = model.Username,
                Name = model.Name
            };
            var createUserResult = await userManager.CreateAsync(user, model.Password);
            if (!createUserResult.Succeeded)
                return (0,"User creation failed! Please check user details and try again.");

            if (!await roleManager.RoleExistsAsync(role))
                await roleManager.CreateAsync(new IdentityRole(role));

            await userManager.AddToRoleAsync(user, role);

            return (1,"User created successfully!");
        }

        public async Task<(int,string)> Login(LoginModel model)
        {
            var user = await userManager.FindByNameAsync(model.Username);
            if (user == null)
                return (0, "Invalid username");
            if (!await userManager.CheckPasswordAsync(user, model.Password))
                return (0, "Invalid password");

            var userRoles = await userManager.GetRolesAsync(user);
            var authClaims = new List<Claim>
            {
               new Claim(ClaimTypes.Name, user.UserName),
               new Claim(JwtRegisteredClaimNames.Jti, Guid.NewGuid().ToString()),
            };

            foreach (var userRole in userRoles)
            {
              authClaims.Add(new Claim(ClaimTypes.Role, userRole));
            }
            string token = GenerateToken(authClaims);
            return (1, token);
        }


        private string GenerateToken(IEnumerable<Claim> claims)
        {
            var authSigningKey = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["JWT:Secret"]));

            var tokenDescriptor = new SecurityTokenDescriptor
            {
                Issuer = _configuration["JWT:ValidIssuer"],
                Audience = _configuration["JWT:ValidAudience"],
                Expires = DateTime.UtcNow.AddHours(3),
                SigningCredentials = new SigningCredentials(authSigningKey, SecurityAlgorithms.HmacSha256),
                Subject = new ClaimsIdentity(claims)
            };

            var tokenHandler = new JwtSecurityTokenHandler();
            var token = tokenHandler.CreateToken(tokenDescriptor);
            return tokenHandler.WriteToken(token);
        }
    }
}
```

I am using tuple here, so that I can return status-code and message
without createing a class. If you don't like this approach and have
other options , let me know that option.

👉**_Program.cs_**

```cs
// Add services to the container.
builder.Services.AddTransient<IAuthService,AuthService>();
```

👉**_AuthenticationController_**

```cs
    [Route("api/[controller]")]
    [ApiController]
    public class AuthenticationController : ControllerBase
    {
        private readonly IAuthService _authService;
        private readonly ILogger<AuthenticationController> _logger;

        public AuthenticationController(IAuthService authService, ILogger<AuthenticationController> logger)
        {
            _authService = authService;
            _logger = logger;
        }


        [HttpPost]
        [Route("login")]
        public async Task<IActionResult> Login(LoginModel model)
        {
            try
            {
                if (!ModelState.IsValid)
                    return BadRequest("Invalid payload");
                var (status, message) = await _authService.Login(model);
                if (status == 0)
                    return BadRequest(message);
                return Ok(message);
            }
            catch(Exception ex)
            {
                _logger.LogError(ex.Message);
                return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }

        [HttpPost]
        [Route("registeration")]
        public async Task<IActionResult> Register(RegistrationModel model)
        {
            try
            {
            if (!ModelState.IsValid)
                return BadRequest("Invalid payload");
            var (status, message) = await _authService.Registeration(model, UserRoles.User);
            if (status == 0)
            {
                return BadRequest(message);
            }
            return CreatedAtAction(nameof(Register), model);

            }
            catch (Exception ex)
            {
                _logger.LogError(ex.Message);
                return StatusCode(StatusCodes.Status500InternalServerError, ex.Message);
            }
        }
    }
```

Now lets create create some protected resources and see how we can
protect our controller.

👉**_FruitController_**

```cs
[Route("api/fruits")]
    [ApiController]
    [Authorize]
    public class FruitController : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var fruits= await Task.FromResult(new string[] { "apple", "bananana", "kiwi" });
            return Ok(fruits);
        }
    }
```

This controller is authorized now, you can not access its methods
without passing jwt token.

If you want that, few of the controller methods need to be accessed by
everyone,without login. So just put `[AllowAnonymous]` attribute above
that method.

```cs
    [Route("api/fruits")]
    [ApiController]
    [Authorize]
    public class FruitController : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var fruits= await Task.FromResult(new string[] { "apple", "bananana", "kiwi" });
            return Ok(fruits);
        }

        [HttpGet]
        [Route("test")]
        [AllowAnonymous]
        public async Task<IActionResult> Test()
        {
            var fruits = await Task.FromResult(new string[] { "apple", "bananana", "kiwi" });
            return Ok(fruits);
        }


    }
```

Let's create another controller, that can only be accessed by admin. Put
`[Authorize(Roles ="Admin")]` above the controller.

👉**_PersonController_**

```cs
    [Route("api/people")]
    [ApiController]
    [Authorize(Roles ="Admin")]
    public class PersonController : ControllerBase
    {
        [HttpGet]
        public async Task<IActionResult> Get()
        {
            var fruits= await Task.FromResult(new string[] { "Jack", "Joe", "Jill" });
            return Ok(fruits);
        }
    }
```

---

Let's test our api end points, I am not putting any unnecessary
screenshots, sorry if it creates some confusion.

⌨️ **_api/fruits_**

You will get **401** status code in response, it means you are **not
authorized** to access this endpoint.

⌨️ **_api/fruits/test_**

You will get **200** status code and **"hi..."** in response. Because
you have set `[AllowAnonymous]` to this resource.

To access protected route like api/fruits, we need to login first. So
lets create a new user with registration.

👉 `https://localhost:7062/api/authentication/registeration`

pass this payload in body.

```json
{
  "username": "john",
  "email": "john@gmail.com",
  "password": "John@123",
  "name": "John Doe"
}
```

**Response:**

status code 201 created

```json
{
  "username": "john",
  "name": "John Doe",
  "email": "john@gmail.com",
  "password": "John@123"
}
```

Lets login, with login endpoint.

👉
[**_https://localhost:7062/api/authentication/login_**](https://localhost:7062/api/authentication/login)

pass this payload in body.

```json
{
  "username": "john",
  "password": "John@123"
}
```

**Response:**

```json
status code: 200
response:
{
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1bmlxdWVfbmFtZSI6ImpvaG5AZ21haWwuY29tIiwianRpIjoiYmUzMzdhZmItYWFkYy00NzZjLWExNDEtNDQ3ZGU2YWI4MTdlIiwicm9sZSI6IlVzZXIiLCJuYmYiOjE2Nzg5NjQ5MTcsImV4cCI6MTY3ODk3NTcxNywiaWF0IjoxNjc4OTY0OTE3LCJpc3MiOiJodHRwczovL2xvY2FsaG9zdDo3MDYyIiwiYXVkIjoiaHR0cHM6Ly9sb2NhbGhvc3Q6NzA2MiJ9.Bbsg6YxvpnN6jN6bdDKW1tJfTJGhQv_G5m0m3paO3vY
}
```

After successfull login, we get the JWT token in response, so copy that
jwt token, and we will pass it in protected route (api/fruits)

👉[**_https://localhost:7062/api/fruits_**](https://localhost:7062/api/fruits)

### with jwt token

![api_fruits_token](/images/api_fruits_token.png)

Now will get 200 ok status code and array of fruits in response.

---

That's good so far, so lets try to access admin protected resource, with
the same jwt token, just change the url and pass the same jwt token.

👉[**_https://localhost:7062/api/people_**](https://localhost:7062/api/people)

**Response:** 403 forbidden, it means you are authenticated, but you
have no rights to access this resource. So we need to make login request
with admin credentials.

Since we have not registered any admin till now, so lets make a little
change in our registration method.

```cs
// var (status, message) = await _authService.Registeration(model, UserRoles.User);
 var (status, message) = await _authService.Registeration(model, UserRoles.Admin);
```

We are changing the role from User to Admin. After registering admin,
change back to normal , change role back to the user, because we do not
want to make public api for creating admin. Test registration api again

👉 `https://localhost:7062/api/authentication/registeration`

```json
{
  "username": "admin",
  "name": "Ravindra",
  "email": "ravindra@gmail.com",
  "password": "Admin@123"
}
```

👉Now login with these credentials

```json
{
  "username": "admin",
  "password": "Admin@123"
}
```

And pass the retrieved token to **api/people**, you will be able to
access this resource now.

**📝Source code:**
[https://github.com/rd003/dotnet-jwt-medium](https://github.com/rd003/dotnet-jwt-medium)
