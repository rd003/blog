+++
date = '2026-08-05T11:20:10+05:30'
draft = false
title = 'Authenticating a react and node js app'
tags= ["reactjs","typescript","authentication"]
categories = ["programming"]
image = '/images/react-js-auth.webp'
+++

To work with backend (which is created in node js, sqlite and prisma) you need to follow [this post](/posts/nodejs-jwt-and-cookie-authentication-using-typescript-2026).

💻 [Source code of frontend app](https://github.com/rd003/NodeReactAuth)

💻 [Source code of this fullstack app](https://github.com/rd003/NodeReactAuth/tree/main/frontend)

To create a react app you need to execute this command in terminal:

```sh
npm create vite@latest
```

It asks few things:

- Project name: `frontend`

**Note:** Choose a meaninful name. Since it is part of my fullstack app, one directory is `backend`, so another one is going to be named `frontend`.

- Select a framework: `React`
- Select a variant: `Typescript`
- Which linter to use: `Oxlint` (you can also choose `EsLint`)
- Start with npm and start now? `yes`.

Now, the `npm packages` will be installed and if completed then project should be running at `http://localhost:5173`. You can visit the
route in browser and check the default app created by `vite`. After that, close the app and open it in `VS Code` with `Code frontent` command.

You can run the app from vs code's integrated terminal any time. You just need to press `ctrl` and ` (backtick) buttons together, which opens the terminal.
Then you can fire `npm run dev` command.

Anyway, let's clean up these files: `src/index.css`, `src/App.css` and replace the content of `src/App.tsx` with:

```ts
function App() {
  return (
    <>

    </>
  )
}

export default App
```

At this moment, we have cleared the boilerplate. Now let's create few directories. I am using bash terminal, I would reccommend gitbash to
windows users to follow along or use their alternative powershell command.

Right now one should be inside `frontend` directory in a integrated terminal.

```sh
# 
cd src

# create folders
mkdir -p api auth routes pages components/common types shared

## go back to frontend
cd ..
```

create an environment file too at the root:

```sh
touch .env
```

We will be creating other directories and files as they needed. I will give you the name of a file with path (eg. src/pages/Login.tsx), you need to create that file
by yourself.

## Install required npm packages

```sh
npm i axios tailwindcss@latest @tailwindcss/vite@latest daisyui@latest
```

`axios` is needed for making api calls, rest of the packages are needed for `tailwind css` and `daisy ui`.

## Configure daisy ui

Update `vite.config.ts`

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
})
```

Add these lines in index.css:

```css
@import "tailwindcss";
@plugin "daisyui";
```

## Let's create few pages

Home:

```ts
// src/pages/Home.tsx

export default function Home() {
    return (<>
        <p>Home...</p>
    </>)
}
```

Not Found:

```ts
// src/pages/NotFound.tsx

export default function NotFound() {
    return (<>
        <p>404 Not Found...</p>
    </>)
}
```

Signup:

```ts
// src/pages/SignUp.tsx

export default function SignUp() {
    return (<>
        <p>SignUp...</p>
    </>)
}
```

Login:

```ts
// src/pages/Login.tsx

export default function Login() {
    return (<>
        <p>Login...</p>
    </>)
}
```

Greetings:

```ts
// src/pages/Greetings.tsx

export default function Greetings() {
    return (<>
        <p>Greetings...</p>
    </>)
}
```

## Designing a navbar with react router

First, we need to install react router.

```sh
npm i -D react-router-dom
```

It is being installed as a dev dependency and won't be installed in production server.

Update `main.ts`:

```ts
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

Navbar:

```ts
// src/components/common/Navbar.tsx

import { NavLink, type NavLinkRenderProps } from "react-router-dom";

export function Navbar() {
    const getLinkClass = ({ isActive }: NavLinkRenderProps) => isActive ? "menu-active" : "";
    // error
    return (
        <div className="navbar bg-base-100 shadow-sm px-4">
            <div className="flex-1">
                <NavLink to="/" className="btn btn-ghost text-xl">
                    AuthDemo
                </NavLink>
            </div>
            <div className="flex-none">
                <ul className="menu menu-horizontal px-1 gap-1">
                    <li>
                        <NavLink className={getLinkClass} to="/">Home</NavLink>
                    </li>
                    <li>
                        <NavLink className={getLinkClass} to="/greetings">Greetings</NavLink>
                    </li>
                    <li>
                        <NavLink className={getLinkClass} to="/login">Login</NavLink>
                    </li>
                    <li>
                        <NavLink className={getLinkClass} to="/signup">Signup</NavLink>
                    </li>
                    <li>
                        <button type="button">Logout</button>
                    </li>
                </ul>
            </div>
        </div>
    );
}
```

Update `App.tsx`

```ts
// App.tsx

import { Route, Routes } from "react-router-dom"
import { Navbar } from "./components/common/Navbar"
import Home from "./pages/Home"
import Greetings from "./pages/Greetings"
import Login from "./pages/LoginPage"
import SignUp from "./pages/SignupPage"
import NotFound from "./pages/NotFound"

function App() {
  return (
    <div>
      <Navbar />
      <div className="p-2">
        <Routes>
          <Route index element={<Home />} />
          <Route path="/greetings" element={<Greetings />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div >
  )
}

export default App
```

## Declaring required types

```ts
// src/types/user.ts
export type Role = 'user' | 'admin';

export interface User {
    username: string;
    role: Role;
}
```

api.ts

```ts
// src/types/api.ts

export interface ApiResponse<T = undefined> {
    statusCode: number;
    message: string;
    data?: T;
}

export interface ApiErrorResponse {
    statusCode: number;
    message: string;
}
```

## environment file (.env)

```txt
VITE_API_BASE_URL=http://localhost:3000/api
```

## Defining services

Base for axios requests:

```ts
// src/api/client.ts

import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:3000/api";;

export const apiClient = axios.create({
    baseURL,
    withCredentials: true,
});
```

Auth api serveice:

```ts
// src/api/auth.ts

import { apiClient } from "./client";
import type { ApiResponse } from "../types/api";
import type { User } from "../types/user";

export function signup(email: string, password: string) {
    return apiClient.post<ApiResponse>("/auth/signup", { email, password });
}

export function login(username: string, password: string) {
    return apiClient.post<ApiResponse>("/auth/login", { username, password });
}

export function logout() {
    return apiClient.post<ApiResponse>("/auth/logout");
}

export function getMe() {
    return apiClient.get<ApiResponse<{ username: string; role: User["role"] }>>("/auth/me");
}

export function refresh() {
    return apiClient.post<ApiResponse>("/auth/refresh");
}
```

Greetings api service:

```ts
// src/api/greetings.ts

import { apiClient } from "./client";
import type { ApiResponse } from "../types/api";

export function getGreetings<T = unknown>() {
    return apiClient.get<ApiResponse<T>>("/greetings")
}

export function deleteGreeting() {
    return apiClient.delete<ApiResponse>("/greetings")
}
```

## Writing context api for authentication state management

Let's add some refresh token logic in `api/client.ts`. Replace the content of a file with this:

```ts
// src/api/client.ts

import axios, { AxiosError, type InternalAxiosRequestConfig } from "axios";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:3000/api";;

export const apiClient = axios.create({
    baseURL,
    withCredentials: true,
});

type AuthFailureListener = () => void;
let authFailureListeners: AuthFailureListener[] = [];

// Extend axios config so we can mark a request as "already retried once"
declare module "axios" {
    interface InternalAxiosRequestConfig {
        _retry?: boolean;
    }
}

export function onAuthFailure(listener: AuthFailureListener) {
    authFailureListeners.push(listener);
    return () => {
        authFailureListeners = authFailureListeners.filter((l) => l !== listener);
    };
}

function notifyAuthFailure() {
    authFailureListeners.forEach((listener) => listener());
}

// --- Refresh queue: prevents multiple concurrent 401s from firing
// multiple parallel /refresh calls ---
let isRefreshing = false;
let refreshSubscribers: Array<() => void> = [];

const subscribeTokenRefresh = (cb: () => void) => {
    refreshSubscribers.push(cb);
};

const onRefreshed = () => {
    refreshSubscribers.forEach((cb) => cb());
    refreshSubscribers = [];
};

apiClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError) => {
        const originalRequest = error.config as InternalAxiosRequestConfig | undefined;

        if (!originalRequest) {
            return Promise.reject(error);
        }

        const isAuthEndpoint =
            originalRequest.url?.includes("/auth/login") ||
            originalRequest.url?.includes("/auth/refresh");

        // Only attempt refresh on 401s, once per request, and never for
        // login/refresh itself (avoids infinite loop)
        if (error.response?.status === 401 && !originalRequest._retry && !isAuthEndpoint) {
            originalRequest._retry = true;

            if (isRefreshing) {
                // Queue this request until the in-flight refresh resolves
                return new Promise((resolve) => {
                    subscribeTokenRefresh(() => resolve(apiClient(originalRequest)));
                });
            }

            isRefreshing = true;

            try {
                await apiClient.post("/auth/refresh");
                isRefreshing = false;
                onRefreshed();
                return apiClient(originalRequest);
            } catch (refreshError) {
                isRefreshing = false;
                refreshSubscribers = [];
                notifyAuthFailure(); // tell AuthProvider the session is dead
                return Promise.reject(refreshError);
            }
        }

        return Promise.reject(error);
    }
);
```

Aslo, in `api/auth.ts` add this re-export so AuthProvider doesn't need to import client.ts directly

```ts
// src/api/auth.ts

// import statements and rest of the code is not shown here
// for the sake of brevity 

export { onAuthFailure } from "./client";

// rest of the code
```

### AuthContext

```ts
// src/auth/AuthContext.ts

import { createContext, useContext } from "react";
import type { User } from "../types/user";

export type AuthStatus = "idle" | "loading" | "authenticated" | "unauthenticated";

export interface AuthContextValue {
    user: User | null;
    status: AuthStatus;
    error: string | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => Promise<void>;
    refreshUser: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function useAuth(): AuthContextValue {
    const ctx = useContext(AuthContext);
    if (!ctx) {
        throw new Error("useAuth must be used within an AuthProvider");
    }
    return ctx;
}
```

### AuthProvider

```ts
// src/auth/AuthProvider.tsx

import { useCallback, useEffect, useState, type ReactNode } from "react";
import { AxiosError } from "axios";
import { AuthContext, type AuthStatus } from "./AuthContext";
import * as authApi from "../api/auth";
import type { User } from "../types/user";
import type { ApiErrorResponse } from "../types/api";
import { onAuthFailure } from "../api/auth"; // re-export needed, see note below

function extractErrorMessage(err: unknown): string {
    if (err instanceof AxiosError) {
        const data = err.response?.data as ApiErrorResponse | undefined;
        return data?.message ?? "Something went wrong. Please try again.";
    }
    return "Something went wrong. Please try again.";
}

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [status, setStatus] = useState<AuthStatus>("idle");
    const [error, setError] = useState<string | null>(null);

    // Single source of truth for "who is logged in" — called on mount
    // and again right after login (since /login doesn't return user info).
    const refreshUser = useCallback(async () => {
        setStatus("loading");
        try {
            const res = await authApi.getMe();
            const data = res.data.data;
            if (!data) {
                throw new Error("Malformed /me response");
            }
            setUser({ username: data.username, role: data.role });
            setStatus("authenticated");
            setError(null);
        } catch {
            setUser(null);
            setStatus("unauthenticated");
        }
    }, []);

    // Bootstrap: run once on app mount to determine initial session state.
    useEffect(() => {
        refreshUser();
    }, [refreshUser]);

    useEffect(() => {
        const unsubscribe = onAuthFailure(() => {
            setUser(null);
            setStatus("unauthenticated");
        });
        return unsubscribe;
    }, []);

    const login = useCallback(
        async (username: string, password: string) => {
            setError(null);
            try {
                await authApi.login(username, password);
                await refreshUser(); // populate user/role since /login body doesn't include it
            } catch (err) {
                setStatus("unauthenticated");
                setError(extractErrorMessage(err));
                throw err; // let LoginPage react too (e.g. keep form filled)
            }
        },
        [refreshUser]
    );

    const logout = useCallback(async () => {
        try {
            await authApi.logout();
        } catch {
            // Ignore failure — clear client state regardless, since the goal
            // is getting the user to a logged-out UI state either way.
        } finally {
            setUser(null);
            setStatus("unauthenticated");
            setError(null);
        }
    }, []);

    return (
        <AuthContext.Provider value={{ user, status, error, login, logout, refreshUser }}>
            {children}
        </AuthContext.Provider>
    );
}
```

Update `main.tsx`

```ts
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from './auth/AuthProvider.tsx'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </AuthProvider>
  </StrictMode>,
)
```

## Signup

```tsx
// src/pages/SignUp.tsx
import { useState, type SubmitEvent } from "react";
import { Link, useNavigate } from "react-router-dom"
import * as authApi from "../api/auth"
import { AxiosError } from "axios";
import type { ApiErrorResponse } from "../types/api";

export default function SignUp() {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const [submitting, setSubmitting] = useState(false);

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        if (email.trim() === '' || password.trim() === '') {
            setError("Email or password can not be blank");
            return;
        }
        setError(null);
        setSubmitting(true);
        try {
            await authApi.signup(email, password);
            navigate('/login');
        } catch (err) {
            const data = err instanceof AxiosError ?
                (err.response?.data as ApiErrorResponse | undefined)
                : undefined;
            setError(data?.message ?? "Signup failed. Please try again.");
        } finally {
            setSubmitting(false);
        }
    }
    return (<>
        <div className="flex justify-center items-center min-h-[80vh]">
            <div className="card w-full max-w-sm bg-base-100 shadow-md">
                <div className="card-body">
                    <h2 className="card-title">Sign up</h2>
                </div>
                {error &&
                    <div role="alert" className="alert alert-error text-sm mb-2">
                        <span>{error}</span>
                    </div>
                }

                <form className="flex flex-col gap-3" onSubmit={handleSubmit}>
                    <label className="form-control">
                        <span className="label-text">Email</span>
                        <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} className="input input-bordered w-full" />
                    </label>

                    <label className="form-control">
                        <span className="label-text">Password</span>
                        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="input input-bordered w-full" />
                    </label>

                    <button type="submit" className="btn btn-primary mt-2" disabled={submitting}>{submitting ? "Creating account..." : "Sign up"}</button>
                </form>

                <p className="text-sm mt-2">
                    Already have an account? <Link to="/login" className="link">Log in</Link>
                </p>

            </div>
        </div>
    </>)
}
```

## Login

```tsx
// src/pages/Login.tsx
import { useState, type SubmitEvent } from "react";

import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export default function Login() {

    const { login, error } = useAuth();
    const navigate = useNavigate();
    const location = useLocation();

    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [submitting, setSubmitting] = useState(false);
    const [validationError, setValidationError] = useState<string | null>('');
    const from = (location.state as { from?: string } | null)?.from ?? "/";

    async function handleSubmit(e: SubmitEvent) {
        e.preventDefault();
        setSubmitting(false);
        if (username.trim() === '' || password.trim() === '') {
            setValidationError("username or password can not be blank");
            return; // it is a work around, use react-hook-form in production grade app
        }
        try {
            await login(username, password);
            navigate(from, { replace: true });
        } catch {
            // error is already set in context by AuthProvider; nothing else to do here
        } finally {
            setSubmitting(false);
        }
    }
    return (<div className="flex justify-center items-center min-h-[80vh]">
        <div className="card w-full max-w-sm bg-base-100 shadow-md">
            <div className="card-body">
                <h2 className="card-title">Login</h2>
            </div>
            {error &&
                <div role="alert" className="alert alert-error text-sm mb-2">
                    <span>{error}</span>
                </div>}

            {validationError && <div role="alert" className="alert alert-error text-sm mb-2">
                <span>{validationError}</span>
            </div>}

            <form onSubmit={handleSubmit} className="flex flex-col gap-3">
                <label className="form-control">
                    <span className="label-text">Username</span>
                    <input type="username" value={username} onChange={(e) => setUsername(e.target.value)} className="input input-bordered w-full" />
                </label>

                <label className="form-control">
                    <span className="label-text">Password</span>
                    <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} className="input input-bordered w-full" />
                </label>

                <button type="submit" className="btn btn-primary mt-2" disabled={submitting}>
                    {submitting ? "Authenticating..." : "Login"}
                </button>
            </form>

            <p className="text-sm mt-2">
                Already have an account? <Link to="/signup" className="link">SignUp</Link>
            </p>

        </div>
    </div>)
}
```

## Logout

Update `Navbar.tsx`:

```tsx
// src/components/common/Navbar.tsx

import { NavLink, useNavigate, type NavLinkRenderProps } from "react-router-dom";
import { useAuth } from "../../auth/AuthContext";

export function Navbar() {
    const getLinkClass = ({ isActive }: NavLinkRenderProps) => isActive ? "menu-active" : "";
    const { logout, user, status } = useAuth();
    const navigate = useNavigate();

    async function signout() {
        await logout();
        navigate('/login', { replace: true })
    }

    return (
        <div className="navbar bg-base-100 shadow-sm px-4">
            <div className="flex-1">
                <NavLink to="/" className="btn btn-ghost text-xl">
                    AuthDemo
                </NavLink>
            </div>
            <div className="flex-none">
                <ul className="menu menu-horizontal px-1 gap-1">
                    <li>
                        <NavLink className={getLinkClass} to="/">Home</NavLink>
                    </li>


                    {status === 'authenticated' ?
                        <>
                            <li>
                                <NavLink className={getLinkClass} to="/greetings">Greetings</NavLink>
                            </li>
                            <li>
                                <button type="button" onClick={signout}>Logout({user?.username})</button>
                            </li>
                        </>
                        : <li>
                            <NavLink className={getLinkClass} to="/login">Login</NavLink>
                        </li>
                    }
                </ul>
            </div>
        </div>
    );
}
```

## Greetings page

You need to be authenticated to access the greetings and one should have logged in with admin account to delete the greeting. Actually, there
there is not any array of greetings to show and to delete, these are just dummy apis, returns the data with `statusCode` and `message`.

Note: There is not an option to signup with admin. You have to do it from the backend. Change the hardcoded role from `user` to `admin` in `adminController`-> signup method, then
signup.

```tsx
// src/pages/Greetings.tsx

import { useEffect, useState } from "react";
import * as greetingsApi from "../api/greetings";
import { useAuth } from "../auth/AuthContext";

export default function Greetings() {
    const [error, setError] = useState<string | null>(null);
    const [greeting, setGreeting] = useState('');
    const [loading, setLoading] = useState(true);
    const { user } = useAuth();

    const fetchApis = async () => {
        try {
            const res = await greetingsApi.getGreetings();
            setGreeting(res.data.message);
        } catch (err) {
            console.log(err);
            setError('Something went wrong while fetching greetings');
        } finally {
            setLoading(false);
        }

    }
    useEffect(() => {
        fetchApis();
    }, []);

    async function deleteGreeting() {
        setLoading(true);
        try {
            await greetingsApi.deleteGreeting();
            alert("Greeting is deleted");
        } catch (error) {
            console.log(error);
            setError("Something went wrong while deleting..");
        } finally {
            setLoading(false);
        }
    }
    return (<>
        <h2 className="text-xl">Greetings</h2>

        {error && <p className="text-red-600">{error}</p>}

        {loading && <p>Loading...</p>}

        {greeting && <p>{greeting}</p>}

        {
            user?.role === 'admin' ?
                <button className="btn btn-error" onClick={deleteGreeting}>Delete greeting</button>
                : null
        }

    </>)
}
```

## Protecting the route

To protect the route we need to to create a component `ProtectedRoute.tsx` and to protect the admin route, we need to create `AdminRoute.tsx`.
Right now we don't have any admin route, you can utilise this if you create one.

ProtectedRoute.tsx

```tsx
// src/routes/ProtectedRoute.tsx

import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function ProtectedRoute({ children }: { children: ReactNode }) {
    const { status } = useAuth();
    const location = useLocation();

    if (status === "idle" || status === "loading") {
        return <div className="flex justify-center p-10">Loading...</div>;
    }

    if (status === "unauthenticated") {
        return <Navigate to="/login" state={{ from: location.pathname }} replace />;
    }

    return <>{children}</>;
}
```

AdminRoute.tsx

```tsx
// src/routes/AdminRoute.tsx

import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../auth/AuthContext";

export function AdminRoute({ children }: { children: ReactNode }) {
    const { status, user } = useAuth();
    const location = useLocation();

    if (status === "idle" || status === "loading") {
        return <div className="flex justify-center p-10">Loading...</div>;
    }

    if (status === "unauthenticated") {
        return <Navigate to="/login" state={{ from: location.pathname }} replace />;
    }

    if (user?.role !== "admin") {
        // Logged in, but wrong role — distinct from "not logged in"
        return <Navigate to="/forbidden" replace />;
    }

    return <>{children}</>;
}
```

We also need a component to 403 forbidden status, in case you are trying to access the privileged route (eg. admin route).

```tsx
// src/pages/Forbidden.tsx

export default function Forbidden() {
    return (
        <div>
            <h1 className="text-2xl font-bold">403 — Forbidden</h1>
            <p>You don't have permission to view this page.</p>
        </div>
    );
}
```

Update the `App.tsx`

```tsx
// App.tsx

import { Route, Routes } from "react-router-dom"
import { Navbar } from "./components/common/Navbar"
import Home from "./pages/Home"
import Greetings from "./pages/Greetings"
import Login from "./pages/LoginPage"
import SignUp from "./pages/SignupPage"
import NotFound from "./pages/NotFound"
import { ProtectedRoute } from "./routes/ProtectedRoute"
import Forbidden from "./pages/Forbidden"

function App() {
  return (
    <div>
      <Navbar />
      <div className="p-2">
        <Routes>
          <Route index element={<Home />} />
          <Route path="/greetings" element={
            <ProtectedRoute>
              <Greetings />
            </ProtectedRoute>
          } />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/forbidden" element={<Forbidden />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div >
  )
}

export default App
```