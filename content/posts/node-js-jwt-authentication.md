+++
date = '2025-07-04T00:00:00+05:30'
draft = false
title = 'Node Js: Jwt Authentication and refresh token'
categories= ['programming']
tags = ['nodejs','authentication']
+++

![jwt auth in node js](/images/jwt.webp)

Please visit this [post](/posts/node-js-crud-with-sql-server/) first, where I have made this project from scratch and wrote CRUD APIs.


## Source code 

- Backend and specific only to this tutorial: https://github.com/rd003/ng-node-fullstack/pull/new/jwt-refresh
- Complete project with angular : https://github.com/rd003/ng-node-fullstack

## JSON web token (JWT) and why it is needed

REST Apis are session less. You can not maintain the authentication session for the whole application. For that purpose, `JSON web token (JWT)` comes in play. How it works

- User hit the `login or authenticate` endpoint with valid credentials. 
- In response, if user is authenticated, user get's a  `access-token (JWT)` , which contains the user's info like username, role.
- You need to pass JWT in authorization header with every protected endpoint.
- In this a server knows a valid and authenticated use is accessing the resource.
- JWT has a expiry date, it does not live forever.
- Note that, JWT is not saved in database

### What is the refresh token and why we need it?

You are thinking that, if I can do authentication with JWT, then why do I bother to create a refresh token. Let me break it down

- For security reasons, it is reccomended to set a short expiry time to JWT, preferably 15 minutes. They live for a short period.
- Which means, you have to login in every 15 minutes. Well, it seems a pain.
- Now refresh tokens comes in a play.

Now authentication flow will be different

1. User hits the `login or authenticate` endpoint by passing valid credentials.
2. If logged in successfull, two tokens are generated: `refresh-token` and `access-token (JWT)`. `refresh-token` get saved in the database, along with it's validity and validity of `refresh-token` is long (30 days or more). Let's say we have set refresh-token's expiry to 30 days.
3. In response, user gets two tokens: `access-token` and `refresh-token`.
4. When `access-token` expires, user have to call `refreshToken` api endpoint and pass `access-token + refresh+ token` and in response, the user gets newly generated access and refresh token. 
5. Which means you don't need to login for next 30 days.
6. After 30 days when `refresh-token` is expired, a user have to `login` again to get new `refresh-token`.


Soure code : https://github.com/rd003/ng-node-fullstack/tree/jwt/backend

## user model

```js
const { allow } = require('joi');
const { DataTypes } = require('sequelize');

function userModel(sequelize) {
    const attributes = {
        Id: {
            type: DataTypes.INTEGER,
            allowNull: false,
            autoIncrement: true,
            primaryKey: true
        },
        Email: {
            type: DataTypes.STRING(100),
            allowNull: false
        },
        PasswordHash: {
            type: DataTypes.STRING(200),
            allowNull: false
        },
        Role: {
            type: DataTypes.STRING(20),
            allowNull: false
        },
        RefreshToken: {
            type: DataTypes.STRING(400),
            allowNull: true
        },
        RefreshTokenExpiry:{
            type: DataTypes.DATE,
            allow:true
        }
    };

    const options = {
        freezeTableName: true,
        timestamps: false,
        indexes: [
            {
                unique: true,
                fields: ['Email'],
                name: 'UIX_Email'
            }
        ]
    };

    return sequelize.define("Users", attributes, options);
}

module.exports = userModel;
```

## config/database.js

```js
db.Users = userModel(sequelize); 
```
## Validate User (/middlewares/user.validator.js)

```js
const Joi = require('joi');

const userSchema = Joi.object({
    email: Joi.string()
        .email({ minDomainSegments: 2, tlds: { allow: ['com', 'net', 'org', 'edu', 'gov', 'mil', 'int', 'co', 'io', 'me', 'info', 'biz'] } })
        .min(5)
        .max(100)
        .required()
        .messages({
            'string.email': 'Please provide a valid email address',
            'string.min': 'Email must be at least 5 characters long',
            'string.max': 'Email must not exceed 100 characters',
            'any.required': 'Email is required'
        }),
    password: Joi.string()
        .min(8)
        .max(70)
        .pattern(new RegExp('^(?=.*[a-z])(?=.*[A-Z])(?=.*\\d)(?=.*[@$!%*?&])[A-Za-z\\d@$!%*?&]'))
        .required()
        .messages({
            'string.min': 'Password must be at least 8 characters long',
            'string.max': 'Password must not exceed 70 characters',
            'string.pattern.base': 'Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (@$!%*?&)',
            'any.required': 'Password is required'
        })
});

const loginSchema = Joi.object({
    username: Joi.string()
        .min(1)
        .max(100)
        .required(),
    password: Joi.string()
        .min(1)
        .max(70)
        .required()
});



const validateUser = (req, res, next) => {
    const { error } = userSchema.validate(req.body);

    if (error) {
        res.status(400)
            .json({
                statusCode: 400,
                message: "Validation failed",
                errors: error.details.map(detail => detail.message)
            });
    }
    next();
}

const validateLogin = (req, res, next) => {
    const { error } = loginSchema.validate(req.body);

    if (error) {
        res.status(400)
            .json({
                statusCode: 400,
                message: "Validation failed",
                errors: error.details.map(detail => detail.message)
            });
    }
    next();
}
module.exports = {
    validateUser,
    validateLogin
}
```

## Required libraries

First, we need to install these packages.

```js
 npm i bcrypt jsonwebtoken cookie-parser
```

- `bcrypt` for hashing the password
- `jsonwebtoken` for creating and verifying jwt
- `cookie-parser` for retrieving and parsing the cookie

## Controllers 

```js
//controllers/user.controller.js

const { Users } = require('../config/database');
const bcrypt = require('bcrypt');
const { convertToMilliseconds } = require('../utils/time.util');
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key'; // Use a strong secret in production
const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || '15m';
const REFRESH_EXPIRY = process.env.REFRESH_TOKEN_EXPIRES_IN || '7d';


// functions


// at the end of the file

module.exports = {
    signup,
    login,
    logout,
    refreshAccessToken,
    getUserInfo
};

```

Now we will define these functions.

### signup

```js
 const signup = async (req, res) => {
    try {
        // whether user exists
        const user = await Users.findOne({
            where: { email: req.body.email }
        });
        if (user) {
            return res.status(409).json({
                statusCode: 409,
                message: "User already exists"
            });
        }

        // create new user
        const saltRounds = 10;
        const passwordHash = await bcrypt.hash(req.body.password, saltRounds);

        await Users.create({
            Email: req.body.email,
            PasswordHash: passwordHash,
            Role: "user"
        });

        res.status(201).send({
            statusCode: 201,
            message: "User is created"
        });
    }
    catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
}
```

### login

First we need to add these values in `.env` file.

```env
JWT_SECRET=your-very-secure-secret-key-here
JWT_EXPIRES_IN=15m 
REFRESH_TOKEN_EXPIRES_IN=30d
```

### cokie-parser

`cookie-parser` library is need to get the cookies. Make sure you have installed it already. Now we need to to set `cookie-parser` middleware

```js
//app.js

app.use(cookieParser())
```

### time converter utility

We are using the time defined in `.env` file (`JWT_EXPIRES_IN`) as `maxAge` of cookie. But cookies, `maxAge` value needs to be set in milliseconds and our `JWT_EXPIRES_IN` values is `24h`. So we need a converter.

```js
/src/utils/time.util.js

const convertToMilliseconds = (timeString) => {
    if (!timeString) return 24 * 60 * 60 * 1000; // Default to 24 hours

    const timeValue = parseInt(timeString);
    const timeUnit = timeString.slice(-1).toLowerCase();

    switch (timeUnit) {
        case 's': // seconds
            return timeValue * 1000;
        case 'm': // minutes
            return timeValue * 60 * 1000;
        case 'h': // hours
            return timeValue * 60 * 60 * 1000;
        case 'd': // days
            return timeValue * 24 * 60 * 60 * 1000;
        default:
            // If no unit specified, assume seconds
            return timeValue * 1000;
    }
};

module.exports = {
    convertToMilliseconds
};
```

### generate access and refresh tokens in pair

```js
const generateAccessAndRefreshTokens = (payload) => {
    const accessToken = jwt.sign(payload, JWT_SECRET, {
        expiresIn: JWT_EXPIRES_IN
    });

    const refreshToken = jwt.sign({
        username: payload.username
    }, JWT_SECRET, {
        expiresIn: REFRESH_EXPIRY
    });

    return { accessToken, refreshToken };
}
```

I could generate refresh token with other ways, but in this way we can get `username` from refreshToken in `refresh` endpoint. We have no other way to retrieve `username` in the refresh endpoint, if we are working with http cookies only. We could utilize the `accessToken` and extract `username` from its payload, but accessToken cookie would have been exprise at the time of `refresh` endpoint, so it can not be used in `refresh` endpoint. However, you can access the `accessToken` if it would not be passed through `http only cookie`, means it has passed throught the body, then we can easily utilize the accessToken.

### login function

```js
const login = async (req, res) => {
    try {
        const user = await Users.findOne({ where: { email: req.body.username } });
        if (user === null) {
            return res.status(401).json({
                statusCode: 401,
                message: 'Invalid username or password'
            });
        }

        const isMatch = await bcrypt.compare(req.body.password, user.PasswordHash);

        if (!isMatch) {
            return res.status(401).json({
                statusCode: 401,
                message: 'Invalid username or password'
            });
        }

        // generate access and refresh tokens
        const payload = {
            username: user.Email,
            role: user.Role
        };
        const { accessToken, refreshToken } = generateAccessAndRefreshTokens(payload);

        // save refresh token to db
        user.RefreshToken = refreshToken;
        user.RefreshTokenExpiry = new Date(Date.now() + convertToMilliseconds(REFRESH_EXPIRY));
        user.save();

        // set token in cookie
        const jwtCookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(JWT_EXPIRES_IN),
            sameSite: 'strict'
        }

        const refreshTokenCookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(REFRESH_EXPIRY),
            path: '/api/auth/refresh', // Only sent to refresh endpoint
            sameSite: 'strict'
        }

        // since these api can be access by mobile app too, where cookies don't work, so we need to send tokens as a response too.
        res
            .status(200)
            .cookie("accessToken", accessToken, jwtCookieOptions)
            .cookie("refreshToken", refreshToken, refreshTokenCookieOptions)
            .json({
                "accessToken": accessToken,
                "refreshToken": refreshToken
            })
    }
    catch (error) {
        console.log(`❌=====>${error}`);
        return res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
}
```

Let's see what is the meaning of attributes in the cookie options.

- `httpOnly`: `true` means, it can only be accessed and used by the server. A javascript client can not read its value, which protects it from XSS attacks.
- `secure`: If `true` then can only be accessed over `https`
- `maxAge`: Expiration time of cookie. After this time cookie is automatically deleted from the browser.
- `sameSite`: `strict` says it can not be sent with cross site requests.


### logout

```js
const logout = async (req, res) => {
    try {
        // removing refresh token from db

        // First we need to get username/email, which can be obtained from req.user, which has been set in authentication middleware. Since it is an authenticated route, so we can access req.user

        const username = req.user.username;

        const user = await Users.findOne({
            where: {
                Email: username
            }
        });

        user.RefreshToken = null;
        user.RefreshTokenExpiry = null;
        user.save();

        res.status(200)
            .clearCookie("accessToken")
            .clearCookie("refreshToken", { path: '/api/auth/refresh' })
            .json({
                "statusCode": 200,
                "message": "You are successfully logged out"
            });
    } catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
}
```

### refresh token

```js
const refreshAccessToken = async (req, res) => {
    try {
        const refreshTokenInReq = req.cookies?.refreshToken || req.body?.refreshToken;

        if (!refreshTokenInReq) {
            //console.log("===> Step 4: No refresh token, returning 401");
            return res.status(401).json({
                statusCode: 401,
                message: 'refreshToken is not provided'
            });
        }
        // return immediately if token is invalid
        let decodedRefreshToken;
        try {
            decodedRefreshToken = jwt.verify(refreshTokenInReq, JWT_SECRET);
        } catch (error) {
            console.log(`=====> ${error}`);
            return res.status(401).json({
                statusCode: 401,
                message: 'Invalid refresh token'
            });
        }

        console.log(`decoded refresh token: ${JSON.stringify(decodedRefreshToken)}`);
        const user = await Users.findOne({
            where: {
                Email: decodedRefreshToken.username
            }
        });

        // Check if refresh token is valid, not compromised and not expired
        if (!user || user.RefreshToken !== refreshTokenInReq || user.RefreshTokenExpiry < Date.now()) {
            return res.status(400).json({
                statusCode: 400,
                message: 'Refresh token is invalid or expired.'
            });
        }

        // generate new access and refresh token
        const payload = {
            username: user.Email,
            role: user.Role
        };

        const { accessToken, refreshToken } = generateAccessAndRefreshTokens(payload);

        // Rotating the refresh token. In this way attacker have less time window to attack
        user.RefreshToken = refreshToken;
        user.save();

        // set tokens in cookie and also return them in response
        const jwtCookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(JWT_EXPIRES_IN),
            sameSite: 'strict'
        }

        // refresh token options

        // If we fetch maxAge from .env file on every refresh, our refreshToken cookie will never be expired.
        // We need to calculate the maxAge on the basis of refreshTokenExpiry in db
        const expiryDate = new Date(user.RefreshTokenExpiry);
        const currentDate = new Date();
        const remainingTimeMs = expiryDate - currentDate;

        const refreshTokenCookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: remainingTimeMs > 0 ? remainingTimeMs : 0,
            path: '/api/auth/refresh', // Only sent to refresh endpoint
            sameSite: 'strict'
        }

        console.log("====> new  refresh token has generated.");
        res
            .status(200)
            .cookie("accessToken", accessToken, jwtCookieOptions)
            .cookie("refreshToken", refreshToken, refreshTokenCookieOptions)
            .json({
                "accessToken": accessToken,
                "refreshToken": refreshToken
            });
    } catch (error) {
        console.log(`❌user.controller/refresh => catch=====>${error}`);
        return res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
}
```

### Get user info

```js
const getUserInfo = async (req, res) => {
    try {
        const username = req.user.username;
        const user = await Users.findOne({
            attributes: [['Email', 'username'], ['Role', 'role']],
            where: {
                Email: username
            }
        });

        // It is unlikely to happen
        if (!user) {
            return res.status(404).json({
                statusCode: 404,
                message: "User not found"
            });
        }

        res.status(200).json(user);
    }
    catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
}
```

## Authentication middlewares

How do we know, a user which is accessing the endpoint is authenticated user or not. It is called `authentication`. What if you don't want to give every access to a user, eg. only `admin` can `delete` a resource, it is called `authorization` In short, you need to protect your routes. 

- **Layman terminology:** Let's say you want to enter in a `science museum`. You need a `user-pass` for that. When you give your `pass` to a security personalle, you are allowed to enter to the `museum`. You enters the museum, there are certain places, where a `normal user` like you can not enter, even you have a `user-pass`. But those `user-pass` are not allowed there. You need a `special-pass` to enter there. It is called `authorization`.

- Authentication: Who you are
- Authorization: What you can access


For that purpose, we need to create authentication middleware, which will be injected into a route, and responsible for checking authentication.

```js
// /middleware/authentication.middleware.js

const jwt = require('jsonwebtoken');
const JWT_SECRET = process.env.JWT_SECRET;

// here we will define our middlewares


// authentication middleware


// required role middleware

// end of the file
module.exports = {
    authenticateToken,
    requiredRoles
}
```

### authentication middleware

It is responsible, for checking the authentication.

```js
const authenticateToken = (req, res, next) => {
    const token = req.cookies?.accessToken || req.header("Authorization")?.replace("Bearer ", "");
    console.log(`======> jwt: ${token}`);

    if (!token) {
        return res.status(401).json({
            statusCode: 401,
            message: 'Access token required'
        });
    }

    jwt.verify(token, JWT_SECRET, (err, user) => {
        if (err) {
            return res.status(403).json({
                statusCode: 403,
                message: 'Invalid or expired token'
            });
        }
        console.log(`=====> JWT verified =>  req.user : ${JSON.stringify(user)} `);
        req.user = user;
    })
    next();
}
```

### middleware for checking allowed roles

```js
// Middleware to check specific roles
const requiredRoles = (allowedRoles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res.status(401).json({
                statusCode: 401,
                message: 'Authentication required'
            });
        }

        if (!allowedRoles.includes(req.user.role)) {
            return res.status(403).json({
                statusCode: 403,
                message: 'Insufficient permissions'
            });
        }

        next();
    }
}
```

## User routes

```js
// /routes/user.route.js
 
const express = require("express");
const { signup, login, logout, refreshAccessToken, getUserInfo } = require("../controllers/user.controller");
const { validateUser, validateLogin } = require("../middleware/user.validator");
const { authenticateToken } = require("../middleware/authentication.middleware");

router = express.Router();

router.post('/signup', validateUser, signup);
router.post('/login', validateLogin, login);
router.get('/me', authenticateToken, getUserInfo)
router.post('/logout', authenticateToken, logout)
router.post('/refresh', refreshAccessToken)

module.exports = router;
```

Note: `authenticateToken` is a middleware that checks whether a client is authenticated or not. In short no one can access the `logout` endpoint without a valid `accessToken`. 

## route/index.js

```js
const userRoutes = require('./user.routes');
router.use('/api/auth', userRoutes);
```

## Make sure your cors has set credentials to true 

```js
// app.js
app.use(cors({
    origin: 'http://localhost:4200',
    credentials: true  // it is essential to set cookies
}));
```

## Protect the person endpoints

```js
// /routes/personRoutes.js

const express = require('express');
const router = express.Router();
const { validatePerson, validatePersonUpdate } = require('../middleware/validation');
const { getAllPeople, getPersonById, createPerson, updatePerson, deletePerson } = require('../controllers/personController');
const { authenticateToken, requiredRoles } = require('../middleware/authentication.middleware');

router.get('/', authenticateToken, getAllPeople);
router.get('/:id', authenticateToken, getPersonById);
router.post('/', authenticateToken, validatePerson, createPerson);
router.put('/:id', authenticateToken, validatePersonUpdate, updatePerson);
router.delete('/:id', authenticateToken, requiredRoles(['admin']), deletePerson);

module.exports = router;
```

Note: `authenticateToken` is a middlware, which checks wheter a user is authenticated or not. `requiredRoles` restricts endpoint access rights to certain `roles`.

## Testing auth apis 

user.http:

```txt
@base_address = http://localhost:3000/api/auth 

POST {{base_address}}/signup 
Content-Type : application/json

{
    "email": "john@example.com",
    "password": "John@123"
}

###
POST {{base_address}}/login 
Content-Type : application/json

{
    "username": "john@example.com",
    "password": "John@123"
}

###
GET {{base_address}}/me
Authorization: Bearer {{jwt}}

###
POST {{base_address}}/logout
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5AZXhhbXBsZS5jb20iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NDk3MDc4MTgsImV4cCI6MTc0OTcwNzg3OH0.e7RFzaMuGSBg1dPt2rLR7dRo29N1CgtyvahavYJOevA

### Refresh token
POST {{base_address}}/refresh
Content-Type: application/json

{
  "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5AZXhhbXBsZS5jb20iLCJyb2xlIjoiYWRtaW4iLCJpYXQiOjE3NDk3MDc2NjQsImV4cCI6MTc0OTcwNzcyNH0.2D7bn3y4gm3_tGCrBrW4yharyMBfa91Tz6W4SZiVGYk",
  "refreshToken": "1067ad48435b25efa16314ab110c4c6830d7b4edefdbff23674a522d0ff7c837169c5b356f1d1ebf2ba0471ae97bd499e246ebbf38a6a2cca4066dad409c8183"
} 


```


## Front end

### Angular

In angular you have to pass `{withCredential:true}` to set and send the cookies.

```ts
login(loginData: LoginModel) {
  return this.http.post<TokenModel>(
    this.apiUrl + "/login",
    loginData,
    {
      withCredentials: true
    }
  );
}
```

Note that, you have do the same, in every http request which intent to send or recieve the cookie. It is better to create an interceptor for it.


```ts
// http.interceptor.ts

import { HttpInterceptorFn } from '@angular/common/http';

export const httpInterceptor: HttpInterceptorFn = (req, next) => {
  const newReq = req.clone({
    withCredentials: true
  });
  return next(newReq);
};

// app.config.ts
provideHttpClient(
      withInterceptors([httpInterceptor])
    )
```

### In react (fetch api)

```js
fetch('https://your-api.com/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  credentials: 'include', // 👈 Important to include cookies
  body: JSON.stringify({
    username: 'user',
    password: 'pass'
  })
})
.then(res => res.json())
.then(data => console.log(data))
.catch(err => console.error(err));
```