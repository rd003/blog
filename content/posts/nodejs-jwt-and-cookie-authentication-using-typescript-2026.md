+++
date = '2026-08-01T16:09:30+05:30'
draft = false
title = 'Nodejs JWT & Cookie Authentication Using Typescript (2026 guide)'
categories= ['programming']
tags = ['nodejs','authentication','typescript']
image = '/images/node-jwt-with-ts-sqlite-prisma.webp'
+++

`REST` Apis are `session less`. You can not maintain the authentication session for the whole application. For that purpose, `JSON web token (JWT)` comes in play. How it works:

- User hits the `login` or `authenticate` endpoint with valid credentials.
- In response, if user is authenticated, user get’s a `access-token (JWT)` , which contains the user’s info like `username` and `role`.
- You need to pass `JWT` in `Authorization` header with every protected endpoint.
- With this, the server knows a valid and authenticated user is accessing the resource.
- `JWT` has a expiry date, it does not live forever.
- Also need to note that, `JWT` is not saved in database.

## What is the refresh token and why we need it?

You are thinking that, if I can do authentication with `JWT`, then why do I bother to create a `refresh token`. Let me break it down

- For security reasons, it is reccomended to set a short expiry time to `JWT`, preferably `15 minutes`. They live for a short period.
- Which means, you have to login in every 15 minutes. Well, it seems a pain.
- Now refresh tokens comes into play.

Now authentication flow will be different.

- User hits the login or authenticate endpoint by passing valid credentials.
- If logged in successfull, two tokens are generated: `refresh-token` and `access-token (JWT)`. `refresh-token` get saved in the database, along with it’s validity and validity of a refresh-token for a longer expiry(30 days or more). Let’s say we have set refresh-token’s expiry to 30 days.
- In response, user gets two tokens: `access-token` and `refresh-token`.
- When `access-token` expires, user have to call refreshToken api endpoint and pass `access-token + refresh token` and in response, the user gets **newly generated** `access` and `refresh token`.
- Which means you don’t need to login for next 30 days.
- After 30 days when `refresh-token` is expired, a user have to login again to get new `refresh-token`.

## Why need a cookie based authention along with JWT?

Within a javascript client, you stores `access-token` and `refresh-token` in `local storage`. Which is not secure and can be compromised. `Http-Only Cookie` based authentication is much secure, it can only be accessed and used by the server. A javascript client can not read its value, which protects it from XSS attacks.

However, we also need to provide tokens in a respose body if the client is mobile application (android or ios app).

So we are considering this app for both web and mobile clients.

## source code

- [Backend only](https://github.com/rd003/NodeReactAuth/tree/main/backend)
- [Fullstack project with react](https://github.com/rd003/NodeReactAuth)

## Tech stack

These are some major libraries used:

- Node js (version ^24)
- Typescript
- express js (for backend)
- Zod (validation)
- Sqlite (database)
- Prisma (ORM)
- jsonwebtoken (for jwt)
- cookie-parse (parsing cookies)
- bcrypt (encryption of password)

## Setting up a new project

Execute these commands in a sequence to create the required directories and files. 

```bash
#1
mkdir -p NodeReactAuth/backend/src

#2
touch NodeReactAuth/backend/src/index

#3
code NodeReactAuth # it will open this project in vs code
```

Open Vs Code's integrated terminal by pressing ctrl and ` (ctrl and backtick symbol together) and execute these commands in a sequence:

```bash
#1
cd backend

#2
npm init -y 

#3
npm install express cors

#4
npm install -D typescript tsup tsx @types/node @types/express @types/cors

#5
npx tsc --init
```

In `npm install -D <package_name>` command, `-D` flags indicates that these are dev dependencies. You can find them in `devDependencies` section in `package.json` file .They are not the part of production deployement, they are not installed in production and they are not shipped with a production build.

Folder structure should look like this.

```txt
NodeReactAuth
├──backend/
   ├── node_modules/
   ├── package.json
   ├── package-lock.json
   ├── src/
   │   └── index.ts
   └── tsconfig.json
```

Update the `tsconfig.json`:

```ts
{
  // Visit https://aka.ms/tsconfig to read more about this file
  "compilerOptions": {
    // File Layout
    "rootDir": "./src",
    "outDir": "./dist",
    // Environment Settings
    // See also https://aka.ms/tsconfig/module
    "module": "preserve",
    "moduleResolution": "bundler",
    "target": "esnext",
    "types": [],
    // For nodejs:
    "lib": [
      "esnext"
    ],
    "types": [
      "node"
    ],
    // and npm install -D @types/node
    // Other Outputs
    "sourceMap": true,
    "declaration": true,
    "declarationMap": true,
    // Stricter Typechecking Options
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    // Style Options
    // "noImplicitReturns": true,
    // "noImplicitOverride": true,
    // "noUnusedLocals": true,
    // "noUnusedParameters": true,
    // "noFallthroughCasesInSwitch": true,
    // "noPropertyAccessFromIndexSignature": true,
    // Recommended Options
    "strict": true,
    //"jsx": "react-jsx",
    "verbatimModuleSyntax": true,
    "isolatedModules": true,
    "noUncheckedSideEffectImports": true,
    "moduleDetection": "force",
    "skipLibCheck": true,
  }
}
```

Update these sections of package.json file.

```js
   "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsup src/index.ts --format esm --out-dir dist",
    "start": "node dist/index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "type": "module",
```

We are going to use `ES Modules` instead of `CommonJs`. So we have use type: module.

Add these lines in `src/index.ts`:

```ts
import express, { type Request, type Response } from "express";
import cors from "cors";

const app = express();
const port = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());

app.get('/', (req: Request, res: Response) => {
    res.send("Hello");
});

```

Our initial project has been set up. You can run it with `npm run dev`. Execute
the endpoint `http://localhost:3000/`, it will respond with text `Hello`.

## More packages

We need to install more packages. Execute commands in a sequence

```bash
#1
npm i bcrypt jsonwebtoken cookie-parser cors helmet dotenv @prisma/client @prisma/adapter-better-sqlite3 zod 

#2
npm i -D tsup prisma @types/better-sqlite3 @types/bcrypt @types/jsonwebtoken @types/cookie-parser
```

## backend/.env

Create a file named `.env` with backend directory and add this line. This file is a development environment file, contains credential must be excluded from git tracking.

```txt
DATABASE_URL="file:./dev.db"
```

## Initialize prisma

```bash
npx prisma init --datasource-provider sqlite
```

## replace prisma/schema.prisma with this:

```ts
generator client {
  provider = "prisma-client"
  output   = "../src/generated/prisma"
}

datasource db {
  provider = "sqlite"
}

model User {
  id                 Int       @id @default(autoincrement()) @map("Id")
  email              String    @unique @map("Email")
  passwordHash       String    @map("PasswordHash")
  role               String    @map("Role")
  refreshToken       String?   @map("RefreshToken")
  refreshTokenExpiry DateTime? @map("RefreshTokenExpiry")

  @@map("Users")
}
```

run

```sh
npx prisma migrate dev --name init
```

It generates tyhe migration files in a location `/prisma/migrations/<new_migration_folder>/<sql_file>`.

```sh
npx prisma generate
```

It uses the last migration file and generates the database.

## create src/lib/prisma.ts

```ts
// src/lib/prisma.ts

import { PrismaClient } from "../generated/prisma/client.js";
import { PrismaBetterSqlite3 } from "@prisma/adapter-better-sqlite3";
const connectionString = `${process.env.DATABASE_URL}`;

const adapter = new PrismaBetterSqlite3({ url: connectionString });
const prisma = new PrismaClient({ adapter });

export { prisma };
```

Make sure to import `import "dotenv/config";` at the top of the `index.ts` file.

## Validators

We need schema validation for signup and login endpoints.

```ts
// src/validators/user.validator.ts

import type { NextFunction, Request, Response } from "express";
import { z, ZodType } from "zod";   // ZodSchema → ZodType

export const userSchema = z.object({
    email: z.email("Please provide a valid email address")
        .min(5, "Email must be at least 5 characters long")
        .max(100, "Email must not exceed 100 characters"),
    password: z.string()
        .min(8, "Password must be at least 8 characters long")
        .max(70, "Password must not exceed 70 characters")
        .regex(
            /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/,
            "Password must contain at least 1 uppercase letter, 1 lowercase letter, 1 number, and 1 special character (@$!%*?&)"
        )
});

export const loginSchema = z.object({
    username: z.email("Please provide a valid email address")
        .min(1, "Username is required")
        .max(100, "Username must not exceed 100 characters"),
    password: z.string()
        .min(1, "Password is required")
        .max(70, "Password must not exceed 70 characters")
});


export const validate = (schema: ZodType) =>
    (req: Request, res: Response, next: NextFunction) => {
        const result = schema.safeParse(req.body);
        if (!result.success) {
            return res.status(400).json({
                statusCode: 400,
                message: "Validation failed",
                errors: result.error.issues.map(issue => issue.message)
            });
        }
        next();
    };
```

## Types src/types/apiResponse.ts 

```ts
// src/types/apiResponse.ts

export interface ApiResponse<T = undefined> {
    statusCode: number;
    message: string;
    data?: T;
    errors?: string[];
}
```

## User Controller

```ts
// src/controllers/userController.ts

import type { Request, Response } from "express";
import bcrypt from "bcrypt";
import { prisma } from '../lib/prisma'
import type { ApiResponse } from "../types/apiResponse";
```

Add Signup, login, logout, refreshAccessToken, getUserInfo methods in userController.ts

## Signup function

```ts
export const signup = async (req: Request, res: Response<ApiResponse>) => {
    try {
        const existingUser = await prisma.user.findUnique({
            where: { email: req.body.email }
        });

        if (existingUser) {
            return res.status(409).json({
                statusCode: 409,
                message: "User already exists"
            });
        }

        const saltRounds = 10;
        const passwordHash = await bcrypt.hash(req.body.password, saltRounds);

        await prisma.user.create({
            data: {
                email: req.body.email,
                passwordHash,
                role: "user"
            }
        });

        res.status(201).json({
            statusCode: 201,
            message: "User is created"
        });
    } catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
};
```

## Login function

First we need to add these values in .env file.

```txt
JWT_SECRET=your-very-secure-secret-key-here
JWT_EXPIRES_IN=15m
REFRESH_TOKEN_EXPIRES_IN=30d

```

### cokie-parser

`cookie-parser` library is need to get the cookies. Make sure you have installed it already. Now we need to to set cookie-parser middleware

```ts
//index.ts

app.use(cookieParser())
```

### time converter utility

We are using the time defined in `.env` file (`JWT_EXPIRES_IN`) as maxAge of cookie. But cookies, `maxAge` value needs to be set in `milliseconds` and our `JWT_EXPIRES_IN` values is `24h`. So we need a converter.

```ts
//src/utils / time.util.ts
export const convertToMilliseconds = (timeString: string) => {
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
```

### Token payload

```ts
// src/types/tokenPaylod.ts

export interface TokenPayload {
    username: string;
    role?: string;
}
```

### Generate access and refresh tokens in pair

Add these lines in `userController.ts`.

```ts
// controllers/userController.ts

import jwt from "jsonwebtoken";


const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
    throw new Error("JWT_SECRET is not set in environment variables");
}

const JWT_EXPIRES_IN = process.env.JWT_EXPIRES_IN || "15m";
const REFRESH_EXPIRY = process.env.REFRESH_TOKEN_EXPIRES_IN || "7d";


const generateAccessAndRefreshTokens = (payload: TokenPayload) => {
    const accessToken = jwt.sign(payload, JWT_SECRET, {
        expiresIn: JWT_EXPIRES_IN
    } as jwt.SignOptions);

    const refreshToken = jwt.sign(
        { username: payload.username },
        JWT_SECRET,
        { expiresIn: REFRESH_EXPIRY } as jwt.SignOptions
    );

    return { accessToken, refreshToken };
};

```

We could generate refresh token with other ways, but in this way we can get `username` from `refreshToken` in refresh endpoint. We have no other way to retrieve username in the refresh endpoint, if we are working with **http cookies only**. We could utilize the `accessToken` and extract `username` from its `payload`, but `accessToken cookie` would have been expire at the time of `refresh` endpoint, so it can not be used in `refresh endpoint`. However, you can access the `accessToken` if it would not be passed through http only cookie, means it has passed throught the body, then we can easily utilize the `accessToken`.

**Login function**

```ts
import { convertToMilliseconds } from "../utils/time.util";
import type { CookieOptions } from "express";

export const login = async (req: Request, res: Response<ApiResponse<{ accessToken: string; refreshToken: string }>>) => {
    try {
        const user = await prisma.user.findUnique({
            where: { email: req.body.username }
        });

        if (user === null) {
            return res.status(401).json({
                statusCode: 401,
                message: "Invalid username or password"
            });
        }

        const isMatch = await bcrypt.compare(req.body.password, user.passwordHash);

        if (!isMatch) {
            return res.status(401).json({
                statusCode: 401,
                message: "Invalid username or password"
            });
        }

        const payload: TokenPayload = {
            username: user.email,
            role: user.role
        };
        const { accessToken, refreshToken } = generateAccessAndRefreshTokens(payload);

        await prisma.user.update({
            where: { id: user.id },
            data: {
                refreshToken,
                refreshTokenExpiry: new Date(Date.now() + convertToMilliseconds(REFRESH_EXPIRY))
            }
        });

        const jwtCookieOptions: CookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(JWT_EXPIRES_IN),
            sameSite: "strict"
        };

        const refreshTokenCookieOptions: CookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(REFRESH_EXPIRY),
            path: "/api/auth/refresh",
            sameSite: "strict"
        };

        res
            .status(200)
            .cookie("accessToken", accessToken, jwtCookieOptions)
            .cookie("refreshToken", refreshToken, refreshTokenCookieOptions)
            .json({
                statusCode: 200,
                message: "Login successful",
                data: { accessToken, refreshToken }
            });
    } catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
};
```

Let’s see what is the meaning of attributes in the cookie options.

- **httpOnly**: `true` means, it can only be accessed and used by the server. A javascript client can not read its value, which protects it from `XSS attacks`.
- **secure:** If `true` then can only be accessed over `https`
- **maxAge:** Expiration time of cookie. After this time cookie is automatically deleted from the browser.
- **sameSite:** strict says it can not be sent with cross site requests.


## Logout function

```ts
// src/controllers/userController.ts

export const logout = async (req: Request, res: Response<ApiResponse>) => {
    try {
        const username = req.user.username;

        await prisma.user.update({
            where: { email: username },
            data: {
                refreshToken: null,
                refreshTokenExpiry: null
            }
        });

        res.status(200)
            .clearCookie("accessToken")
            .clearCookie("refreshToken", { path: "/api/auth/refresh" })
            .json({
                statusCode: 200,
                message: "You are successfully logged out"
            });
    } catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
};
```

## Refresh function

```ts
// src/controllers/userController.ts

export const refreshAccessToken = async (req: Request, res: Response<ApiResponse<{ accessToken: string; refreshToken: string }>>) => {
    try {
        const refreshTokenInReq: string | undefined = req.cookies?.refreshToken || req.body?.refreshToken;

        if (!refreshTokenInReq) {
            return res.status(401).json({
                statusCode: 401,
                message: "refreshToken is not provided"
            });
        }

        let decodedRefreshToken: TokenPayload;
        try {
            decodedRefreshToken = jwt.verify(refreshTokenInReq, JWT_SECRET) as TokenPayload;
        } catch (error) {
            console.log(`=====> ${error}`);
            return res.status(401).json({
                statusCode: 401,
                message: "Invalid refresh token"
            });
        }

        console.log(`decoded refresh token: ${JSON.stringify(decodedRefreshToken)}`);

        const user = await prisma.user.findUnique({
            where: { email: decodedRefreshToken.username }
        });

        if (
            !user ||
            user.refreshToken !== refreshTokenInReq ||
            !user.refreshTokenExpiry ||
            user.refreshTokenExpiry.getTime() < Date.now()
        ) {
            return res.status(400).json({
                statusCode: 400,
                message: "Refresh token is invalid or expired."
            });
        }

        const payload: TokenPayload = {
            username: user.email,
            role: user.role
        };
        const { accessToken, refreshToken } = generateAccessAndRefreshTokens(payload);

        const updatedUser = await prisma.user.update({
            where: { id: user.id },
            data: { refreshToken }
        });

        const jwtCookieOptions: CookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: convertToMilliseconds(JWT_EXPIRES_IN),
            sameSite: "strict"
        };

        const expiryDate = updatedUser.refreshTokenExpiry ?? new Date();
        const currentDate = new Date();
        const remainingTimeMs = expiryDate.getTime() - currentDate.getTime();

        const refreshTokenCookieOptions: CookieOptions = {
            httpOnly: true,
            secure: true,
            maxAge: remainingTimeMs > 0 ? remainingTimeMs : 0,
            path: "/api/auth/refresh",
            sameSite: "strict"
        };

        console.log("====> new refresh token has generated.");

        res
            .status(200)
            .cookie("accessToken", accessToken, jwtCookieOptions)
            .cookie("refreshToken", refreshToken, refreshTokenCookieOptions)
            .json({
                statusCode: 200,
                message: "Token refreshed",
                data: { accessToken, refreshToken }
            });
    } catch (error) {
        console.log(`❌user.controller/refresh => catch=====>${error}`);
        return res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
};
```

## User info function

Get the information of a logged-in user.

```ts
// src/controllers/userController.ts

export const getUserInfo = async (req: Request, res: Response<ApiResponse<{ username: string; role: string }>>) => {
    try {
        const username = req.user.username;

        const user = await prisma.user.findUnique({
            where: { email: username },
            select: {
                email: true,
                role: true
            }
        });

        if (!user) {
            return res.status(404).json({
                statusCode: 404,
                message: "User not found"
            });
        }

        res.status(200).json({
            statusCode: 200,
            message: "User info fetched",
            data: {
                username: user.email,
                role: user.role
            }
        });
    } catch (error) {
        console.log(`❌=====>${error}`);
        res.status(500).json({
            statusCode: 500,
            message: "Internal server error"
        });
    }
};
```

## Authentication middlewares

Let’s say you want to enter in a science museum. You need a `user-pass` for that. When you give your pass to a security personalle, you are allowed to enter to the museum. It is called `authentication`.

You enters the museum, there are certain places, where a normal user like you can not enter, even you have a `user-pass`. But those `user-pass` are not allowed there. You need a `special-pass` to enter there. It is called `authorization`.

**Authentication:** Who you are

**Authorization:** What you can access

For that purpose, we need to create an `authentication middleware`, which will be injected into a route, and responsible for checking `authentication`.

```ts
// src/middleware/authentication.middleware.ts

import type { Request, Response, NextFunction } from "express";
import jwt, { type VerifyErrors, type JwtPayload } from "jsonwebtoken";
import type { ApiResponse } from "../types/apiResponse";
import type { TokenPayload } from "../types/tokenPayload";

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET) {
    throw new Error("JWT_SECRET is not set in environment variables");
}

// here we will define our middlewares


// authentication middleware


// required role middleware
```

### But...create this type first

Create a file `src/types/express.d.ts` and copy the code below:

```ts
// src/types/express.d.ts
import type { TokenPayload } from "./apiResponse.js";

declare global {
    namespace Express {
        interface Request {
            user?: TokenPayload;
        }
    }
}

export { };
```

### Authention middleware

Let's define the authentication middleware which is responsible for authentication.

```ts
// src/middleware/authentication.middleware.ts

export const authenticateToken = (req: Request, res: Response<ApiResponse>, next: NextFunction) => {
    const token = req.cookies?.accessToken || req.header("Authorization")?.replace("Bearer ", "");
    console.log(`======> jwt: ${token}`);

    if (!token) {
        return res.status(401).json({
            statusCode: 401,
            message: "Access token required"
        });
    }

    jwt.verify(token, JWT_SECRET, (err: VerifyErrors | null, decoded: JwtPayload | string | undefined) => {
        if (err) {
            return res.status(403).json({
                statusCode: 403,
                message: "Invalid or expired token"
            });
        }
        console.log(`=====> JWT verified => req.user : ${JSON.stringify(decoded)}`);
        req.user = decoded as TokenPayload;
        next();
    });
};
```

### Create a middleware for checking allowed roles (authorization part)

```ts
// src/middleware/authentication.middleware.ts

// required role middleware
export const requiredRoles = (allowedRoles: string[]) => {
    return (req: Request, res: Response<ApiResponse>, next: NextFunction) => {
        if (!req.user) {
            return res.status(401).json({
                statusCode: 401,
                message: "Authentication required"
            });
        }
        if (!allowedRoles.includes(req.user.role ?? "")) {
            return res.status(403).json({
                statusCode: 403,
                message: "Insufficient permissions"
            });
        }
        next();
    };
};
```

## User routes

Let's define all user routes in a single place (`user.routes.ts`).

```ts
// routes/user.routes.ts

import express from "express";
import { login, signup, logout, getUserInfo, refreshAccessToken } from "../controllers/userController"
import { validate, userSchema, loginSchema } from "../validators/user.validator";
import { authenticateToken } from "../middleware/authentication.middleware";

const router = express.Router();
router.post("/signup", validate(userSchema), signup);
router.post("/login", validate(loginSchema), login);
router.get('/me', authenticateToken, getUserInfo)
router.post('/logout', authenticateToken, logout)
router.post('/refresh', refreshAccessToken)

```

Note: `authenticateToken` is a middleware that checks whether a client is authenticated or not. No one can access the `logout` and `me` endpoint without a valid `accessToken`.

## Register routes in index.ts

```ts
// index.ts

import userRoutes from './routes/user.routes'

app.use('/api/auth', userRoutes);

```

## Make sure credentials is set to true for cookie base authentication

```ts
// index.ts

app.use(cors({
    origin: 'http://localhost:5173',
    credentials: true  // it is essential to set cookies
}));
```

## Greetings endpoints

TL;DR needed for testing `authorization` and `authentication`.

These are the simple APIs just returning the 200 status code along with an object, there is no database interactivity in these APIs. We need these APIs to test `authentication` and `authorization`. However, `authentication` is already been tested with `auth/me` and `auth/logout` endpoints -- only a user with a valid `JWT` can access them. But, we also need to test the `authorization`, where an authenticated user with a certain role (eg. `admin`) can access the endpoint.

We will create two endpoints:

- `GET /greetings` (can be accessed by any authenticated user)
- `DELETE /greetings` (can only be accessed by a user with role: `admin`)

### greetrings controller

```ts
// src/controllers/greetingController.ts

import type { Request, Response } from "express";
import type { ApiResponse } from "../types/apiResponse";

export const getGreeting = (req: Request, res: Response<ApiResponse>) => {
    res.status(200)
        .json({
            statusCode: 200,
            message: 'Hello world'
        });
}

export const deleteGreeting = (req: Request, res: Response<ApiResponse>) => {
    res.status(200)
        .json({
            statusCode: 200,
            message: 'Greeting is deleted!'
        });
}
```

### greeting routes

```ts
// src/routes/greeting.route.ts

import express from "express";
import { getGreeting, deleteGreeting } from "../controllers/greetingController";
import { authenticateToken, requiredRoles } from "../middleware/authentication.middleware";

const router = express.Router();
router.get('/', authenticateToken, getGreeting);
router.delete('/', authenticateToken, requiredRoles(['admin']), deleteGreeting);

export default router;
```

Note: `authenticateToken` is a middlware, which checks wheter a user is authenticated or not. `requiredRoles` restricts endpoint access rights to certain roles (in our example, it is an `admin` role).

### Register routes in index.ts

```ts
// index.ts
import greetingRoutes from './routes/greeting.route';

// rest of the codes

app.use('/api/greetings', greetingRoutes);

// rest of the codes
```

## index.ts (final)

```ts
// index.ts

import "dotenv/config";
import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";
import userRoutes from './routes/user.routes'
import greetingRoutes from './routes/greeting.route';

const app = express();
const port = process.env.PORT || 3000;
app.use(cors({
    origin: 'http://localhost:5173',
    credentials: true  // it is essential to set cookies
}));
app.use(express.json());
app.use(cookieParser())

app.use('/api/auth', userRoutes);
app.use('/api/greetings', greetingRoutes);

app.listen(port, () => {
    console.log(`Application is running at http://localhost:${port}`);
});
```

## Testing auth apis

I am using a VS Code extension - [REST Client by Huachao Mao](https://marketplace.visualstudio.com/items?itemName=humao.rest-client) for testing the APIs. You can you any client like `postman`, `insomnia` or even just a `curl` request. If using the REST Client, then create a file `user.http` in a directory `backend/http-file` (offcource create a directory too). 

backend/http-files/user.http:

```txt
@base_address = http://localhost:3000/api/auth 
@jwt = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5AZXhhbXBsZS5jb20iLCJyb2xlIjoidXNlciIsImlhdCI6MTc4NTU1ODcwMSwiZXhwIjoxNzg1NTU5NjAxfQ.6aCJKw_AqKcRJI24z6T-SL9y_9a6e8-NWAjrEkatgPE

POST {{base_address}}/signup 
Content-Type : application/json

{
    "email": "ravindra@example.com",
    "password": "Ravindra@123"
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
Authorization: Bearer {{jwt}}

### Refresh token
POST {{base_address}}/refresh
Content-Type: application/json

{
    "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5AZXhhbXBsZS5jb20iLCJyb2xlIjoidXNlciIsImlhdCI6MTc4NTU1ODcwMSwiZXhwIjoxNzg1NTU5NjAxfQ.6aCJKw_AqKcRJI24z6T-SL9y_9a6e8-NWAjrEkatgPE",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImpvaG5AZXhhbXBsZS5jb20iLCJpYXQiOjE3ODU1NTg3MDEsImV4cCI6MTc4ODE1MDcwMX0.Hyjh4grGFPyGm_SDPjxpiHuWAvrvfk2HPtKntYvWVcI"
}
```

## Testing greeting apis

backend/http-files/greetings.http:

```txt
@base_address = http://localhost:3000/api/greetings 
@jwt = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluQGV4YW1wbGUuY29tIiwicm9sZSI6ImFkbWluIiwiaWF0IjoxNzg1NTc4NTQwLCJleHAiOjE3ODU1Nzk0NDB9.eENYWFNW-vMJs-ZOFcNFn3fbs8wotdKZoCSuHOS8No0

GET {{base_address}}
Authorization: Bearer {{jwt}}

###
DELETE {{base_address}}
Authorization: Bearer {{jwt}}
```

## Testing in frontend

### Angular

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

### JS fetch API

```ts
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

### AXIOS

```ts
await axios.post('https://your-api.com/login', loginData, {
                withCredentials: true
            });
```