+++
date = '2025-11-30T13:02:07+05:30'
draft = false
title = 'Setting Up Node Js With Typescript'
categories= ['programming']
tags = ['nodejs','typescript']
image = '/images/node_typescript.webp'
+++
<!-- ![node js with typescript](/images/node_typescript.webp) -->
(image credit: [Gemini](https://gemini.google.com/))

We are going to create folders and install packages in this step. I don't have much to say for this tutorial. I have tried to explain necessary stuff through comments. In my opinion code is self-explanatory. So, let's execute these commands in a sequence.

```bash
# create a directory
mkdir backend

# change directory
cd backend

# create the `src` directory inside the `backend`.
mkdir src

# create file
touch src/index.ts 

# initialize node js project. 
# Please stay inside the `backend` directory. 
npm init -y 

# install these packages
npm install express cors

# install the dev dependencies
# these packages won't be shipped to your production bundle
npm install -D typescript tsx @types/node @types/express @types/cors

# generate tsconfig.json file
npx tsc --init
```

Folder structure should look like this.

```txt
backend/
├── node_modules/
├── package.json
├── package-lock.json
├── src/
│   └── index.ts
└── tsconfig.json
```

Update the `tsconfig.json`:

```js
{
  // Visit https://aka.ms/tsconfig to read more about this file
  "compilerOptions": {
    // File Layout
    "rootDir": "./src",
    "outDir": "./dist",

    // Environment Settings
    // See also https://aka.ms/tsconfig/module
    "module": "nodenext",
    "target": "esnext",
    "types": [],
    // For nodejs:
    "lib": ["esnext"],
    "types": ["node"],
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

Update these sections of `package.json` file.

```js
   "scripts": {
    "dev": "tsx watch src/index.ts",
    "build": "tsc",
    "start": "node dist/index.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "type": "module",
```

We are going to use `ES Modules` instead of `CommonJs`. So we have use `type: module`.

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

app.post('/people', (req: Request, res: Response) => {
    const firstName: string = (req.body.firstName || "").trim();
    const lastName: string = (req.body.lastName || "").trim();

    res.json({ firstName, lastName });
});

app.get('/people/:id', (req: Request, res: Response) => {
    const id = req.params.id;
    res.send(`Records for id: ${id}`);
});

app.listen(port, () => {
    console.log(`Application is running at http://localhost:${port}`);
})
```

## Run application in watch mode

```bash
npm run dev
```
