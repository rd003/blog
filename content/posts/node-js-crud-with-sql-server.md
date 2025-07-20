+++
date = '2025-07-03T19:17:23+05:30'
draft = false
title = 'Build a Node.js REST APIs with Express, Sequelize & SQL Server (2025 Guide)'
categories= ['programming']
tags = ['nodejs']
+++

![rest apis with node js and sql server](/images/node-sql-server.webp)

In this tutorial, you’ll learn how to build a simple **CRUD (Create, Read, Update, Delete) REST API** using **Node.js**, **Express.js**, **Sequelize**, and **SQL Server**. I have tried to make it a less verbose. It is more like a technical documentation to create the rest apis in this tech stack. However, I have tried to explain all the essential things. This is ideal if you're looking to integrate a SQL Server database with a Node.js backend using Sequelize as the ORM. We are using sql server in this tutorial but you can easily replace it with other sql databases.

**Note:** Initially I have used ORM methods to manipulate the database, but in later parts I also have demonstrated how to to achieve same with raw sql queries and stored procedures. 

💻 Source code: https://github.com/rd003/ng-node-fullstack/tree/crud/backend

## Tech used 

- Node js: v22.16.0
- Sql server 2022 (database)
- express js (node js library)
- Sequelize (ORM)
- Joi (validation library)
- Helmet js (for securing headers)

## creating a database

Let's create a database. You must create a new database, `sequelize` won't create it automatically. However, you can skip table
creation, `sequalize` can manage it. I am going create a table anyway and going to seed some data to it.

```sql
use master
go

create database PersonDb
go

use PersonDb
go

create table People
(
  Id int identity,
  FirstName nvarchar(30) not null,
  LastName nvarchar(30) not null

  constraint PK_Person_Id primary key (Id)
)
go

insert into People (FirstName,LastName)
values 
('John','Doe'),
('Mike','Clark')
go
```

## Creating a new project

```bash
mkdir backend

cd backend

npm init -y
```

## Required packages

```bash
npm install express sequelize tedious cors helmet dotenv joi
```

-  `express` is very minimal node js library for creating backend
- `Sequelize` is ORM (object relational mapper), so that you can easily read and write from database, without worrying about sql queries. However, I recommend, you must learn sql. It is most essential part of web development. 
- `tedious` is a driver for sqlserver.
- `cors` to enable cross origin requests. Javascript front end apps (or you can say browser) follows the same origin policy. If your front-end app is running at `localhost:4200` and backend application is running at `localhost:3000`, front end javascript application will likely to throw an error of `cross-origin request`. To solve this problem, we must enable `cors` in the backend.
- `helmet` is used for securing our application. It basically adds some request headers which helps to protect against common web vulnerabilities such as cross-site scripting (XSS), clickjacking etc.
- `dotenv` is used to read the content `.env` files.
- `joi` is used to validate the data passed as request body.  

install `nodemon` as development dependency.Development dependencies are not included in the production bundle. `nodemon` is a wacther—it automatically restarts the application whenever you make changes to the source code, so you don't need to stop and rerun the app manually. This makes the development process smoother and faster.

```bash
npm install -D nodemon
```

## Project structure

```txt
backend/
├── node_modules/               
├── package.json                
├── package-lock.json                
├── .env                        
└── src/
    ├── app.js
    ├── server.js
    ├── config/
    │   └── database.js
    ├── controllers/
    │   └── personController.js
    ├── middleware/
    │   └── validation.js
    ├── models/
    │   └── Person.js
    └── routes/
        └── index.js
		└── personRoutes.js
```

## Create project directories and files

If you are using `windows` operating system, then I would recommend you to use `gitbash` as your terminal, it is automatically installed when you install `git`. Otherwise `touch` command won't work on windows and you have to find it's windows alternative like (`type nul > abc.js`).	

```bash
mkdir src src/config src/controllers src/middleware src/models src/routes

# Create main files
touch src/server.js src/app.js src/config/database.js src/models/Person.js src/controllers/personController.js src/middleware/validation.js src/routes/index.js  src/routes/personRoutes.js .env
```

## package.json

Update the scripts section of the file

```js
  "scripts": {
    "start": "node src/server.js",
    "dev": "nodemon src/server.js",
    "test": "echo \"Error: no test specified\" && exit 1"
  }
```

## .env file

```js
DB_HOST=localhost
DB_PORT=1433
DB_NAME=PersonDb
DB_USERNAME=your_username
DB_PASSWORD=your_password
DIALECT=mssql

# Server Configuration
PORT=3000
NODE_ENV=development

```

## app.js

```js
require("dotenv").config();

const express = require("express");

const app = express();

module.exports = app;

```

We adds a lot of configuration here, so I have created separate file for app, so that our `server.js` can be cleaner.

## server.js

Let's create a server:

```js
const app = require('./app');

const PORT = process.env.PORT || 3000;

// Graceful shutdown
process.on('SIGTERM', () => {
    console.log('👋 SIGTERM received. Shutting down gracefully...');
    process.exit(0);
});

process.on('SIGINT', () => {
    console.log('👋 SIGINT received. Shutting down gracefully...');
    process.exit(0);
});

app.listen(PORT, () => {
    console.log(`🚀 Server is running on http://localhost:${PORT}`);
    console.log(`📋 Environment: ${process.env.NODE_ENV || 'development'}`);
    console.log(`🌐 API Health Check: http://localhost:${PORT}/health`);
    console.log(`👥 People API: http://localhost:${PORT}/api/people`);
});

// Handle unhandled promise rejections
process.on('unhandledRejection', (err) => {
    console.error('❌ Unhandled Promise Rejection:', err);
    server.close(() => {
        process.exit(1);
    });
});

```

Run the application

```bash
npm run dev
```

The application will run at `http://localhost:3000/`.

## models/Person.js

This model is needed to synchronize with database. If `Person` table does not exists in the database, it will created one. If you make any changes to this model, if will reflected to the database.

```js
const { DataTypes } = require('sequelize');

function model(sequelize) {
    const attributes = {
        Id: {
            type: DataTypes.INTEGER,
            allowNull: false,
            autoIncrement: true,
            primaryKey: true,
        },
        FirstName: {
            type: DataTypes.STRING(30),
            allowNull: false,
        },
        LastName: {
            type: DataTypes.STRING(30),
            allowNull: false
        },
    };

    const options = {
        freezeTableName: true,
        // don't add the timestamp attributes (updatedAt, createdAt)
        timestamps: false,
    };
    return sequelize.define("People", attributes, options);
}

module.exports = model;
``` 

## /config/database.js

```js
const { Sequelize } = require('sequelize');
require('dotenv').config();
const personModel = require('../models/Person')

const sequelize = new Sequelize(
    process.env.DB_NAME,
    process.env.DB_USERNAME,
    process.env.DB_PASSWORD,
    {
        host: process.env.DB_HOST,
        port: process.env.DB_PORT || 1433,
        dialect: 'mssql',
        dialectOptions: {
            options: {
                encrypt: true,
                trustServerCertificate: true, // For local development
            }
        }
    }
);

const db = {};
db.Sequelize = sequelize;
Person = personModel(sequelize);


module.exports = db;
```

## Validating `Person` model

For validation we are going to use `joi`

```js
// middleware/validation.js

const Joi = require('joi');

const personSchema = Joi.object({
    firstName: Joi.string()
        .min(1)
        .max(30)
        .required(),
    lastName: Joi.string()
        .min(1)
        .max(30)
        .required()
});

const validatePerson = (req, res, next) => {
    const { error } = personSchema.validate(req.body);

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

const validatePersonUpdate = (req, res, next) => {
    const updateSchema = personSchema.fork(['firstName', 'lastName'], (schema) => schema.optional());
    const { error } = updateSchema.validate(req.body);

    if (error) {
        res.status(400).json({
            statusCode: 400,
            message: "Validation failed",
            errors: error.details.map(d => d.message)
        });
    }
    next();
}

module.exports =
{
    validatePerson,
    validatePersonUpdate
};
```

## controllers/personController.js

```js
const { Person } = require('../config/database');

class PersonController {
  // our methods will be defined here
}

module.exports = new PersonController();
```

### get all

```js
getAllPeople = async (req, res) => {
        try {
            const people = await Person.findAll();
            res.json(people);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }
```

### get by id

```js
getPersonById = async (req, res) => {
        try {
            const person = await Person.findByPk(req.params.id);
            if (!person) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found"
                })
            }
            res.json(person);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

```

### post

```js
createPerson = async (req, res) => {
        try {
            const personData = {
                FirstName: req.body.firstName,
                LastName: req.body.lastName
            };
            var createdPerson = await Person.create(personData);
            res.status(201)
                .json(createdPerson);
        } catch (error) {
            console.log(error);
            res.status(500)
                .json({
                    statusCode: 500,
                    message: "Internal server error"
                });
        }
    }

```

### put

```js
updatePerson = async (req, res) => {
        try {
            const existingPerson = await Person.findByPk(req.params.id);

            if (!existingPerson) {
               return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found."
                });
            }

            const personToUpdate = {
                FirstName: req.body.firstName,
                LastName: req.body.lastName
            };

            await Person.update(personToUpdate, {
                where: {
                    Id: req.params.id
                }
            });

            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

```

### delete

```js
deletePerson = async (req, res) => {
        try {
            const id = req.params.id;
            const person = await Person.findByPk(id);
            if (!person) {
                res.status(404).json({
                    statusCode: 404,
                    message: "Person not found"
                });
            }

            person.destroy();
            person.save();

            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }
```

## Routes

### /routes/personRoutes.js

```js
const express = require('express');
const router = express.Router();
const { validatePerson, validatePersonUpdate } = require('../middleware/validation');
const { getAllPeople, getPersonById, createPerson, updatePerson, deletePerson } = require('../controllers/personController');

router.get('/', getAllPeople);
router.get('/:id', getPersonById);
router.post('/', validatePerson, createPerson);
router.put('/:id', validatePersonUpdate, updatePerson);
router.delete('/:id', deletePerson);

module.exports = router;
```

### /routes/index.js
In this file we define our all routes. 

```js
// routes/index.js

const express = require('express');
const router = express.Router();
const personRoutes = require('./personRoutes');

// Health check endpoint
router.get('/health', (req, res) => {
    res.json({
        success: true,
        message: 'API is running',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development'
    });
});

// API routes
router.use('/api/people', personRoutes);

// 404 handler for undefined routes
router.use((req, res) => {
    res.status(404).json({
        statusCode: 404,
        message: 'Route not found',
        errors: [`The requested route ${req.originalUrl} does not exist`]
    });
});

module.exports = router;
```

## app.js after defining routes and adding helmet middleware

`helmet` is used for enhancing security in our app. Which add some additional request headers.

```js
// app.js

require("dotenv").config();
const routes = require('./routes');
const express = require("express");
const cors = require('cors');
const helmet = require('helmet');
const { Sequelize } = require('./config/database');

const app = express();

app.use(helmet());
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(routes);

const connectDb = async () => {
    try {
        await Sequelize.authenticate();
        console.log('✅ Database connection established successfully.');

        if (process.env.NODE_ENV !== 'production') {
            await Sequelize.sync({ alter: true });
            console.log('📊 Database models synchronized.');
        }
    }
    catch (error) {
        console.error('❌ Unable to connect to the database:', error);
        process.exit(1);
    }
}

connectDb();

module.exports = app;

```

## Testing the application

I have used Rest client extension() of visual studio code. You can use postman or insomnia. To test with rest client you need to create a file named `person.http` (I have created it in a root). The copy the content below and you can test them easily.

```.http
@base_address = http://localhost:3000/api/people

GET {{base_address}}

###
GET {{base_address}}/1

###
POST {{base_address}}
Content-Type: application/json

{
    "firstName" :"John",
    "lastName": "Doe"
}

###
PUT {{base_address}}/1
Content-Type: application/json

{
    "firstName" :"Jane",
    "lastName": "Doe"
}

###
DELETE  {{base_address}}/1
Content-Type: application/json
 
```

---

## Using raw sql queries 

```js
const { Sequelize } = require('../config/database');

class PersonController {

    getAllPeople = async (req, res) => {
        try {
            const [people] = await Sequelize.query("select Id,FirstName,LastName from People");
            res.json(people);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    getPersonById = async (req, res) => {
        try {
            const people = await Sequelize.query("select Id,FirstName,LastName from People where Id=?", {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });
            if (people.length === 0) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found"
                })
            }
            res.json(people[0]);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    createPerson = async (req, res) => {
        try {
            const sql = `insert into People (FirstName,LastName)
        values (?,?); select SCOPE_IDENTITY() as id;`;
            const [result] = await Sequelize.query(sql, {
                replacements: [req.body.firstName, req.body.lastName],
                type: Sequelize.QueryTypes.INSERT
            });

            const createdPerson = { id: result[0].id, ...req.body };
            res.status(201)
                .json(createdPerson);
        } catch (error) {
            console.log(error);
            res.status(500)
                .json({
                    statusCode: 500,
                    message: "Internal server error"
                });
        }
    }

    updatePerson = async (req, res) => {
        try {
            const [result] = await Sequelize.query(`
                 select 
                 case when exists(select 1 from People where Id=?) 
                 then 1 
                 else 0 end as personExists
                `, {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });
            if (!result.personExists) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found."
                });
            }
            await Sequelize.query(`update People set FirstName=?, LastName=?
                 where Id=?`, {
                replacements: [req.body.firstName, req.body.lastName, req.params.id],
                type: Sequelize.QueryTypes.UPDATE
            });
            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    deletePerson = async (req, res) => {
        try {
            const sql = `select 
            case when exists (
            select 1 from People where Id=?
            ) then 1 else 0 end as personExists`;

            const [result] = await Sequelize.query(sql, {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });
            if (!result.personExists) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person not found"
                });
            }

            await Sequelize.query(`delete from People where Id=?`, {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.DELETE
            });

            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }
}

module.exports = new PersonController();
```

## Using Stored procedures

We can also use stored procedures instead of raw sql queries. Let's right stored procedures first.

### Creating stored procedures 

```SQL
-- create person
create procedure spCreatePerson
  @FirstName nvarchar(30),
  @LastName nvarchar(30)
as
begin
  insert into People (FirstName,LastName)
  values (@FirstName,@LastName);

  select SCOPE_IDENTITY() as id;
end

-- update person
create procedure [dbo].[spUpdatePerson]
  @Id int,
  @FirstName nvarchar(30),
  @LastName nvarchar(30)
as
begin
  update People 
  set FirstName=@FirstName, LastName=@LastName
  where Id=@Id;   
end 

-- get all
create procedure spGetPeople
as
begin
  select 
   Id,
   FirstName,
   LastName 
  from People;
end

-- person exists

create procedure spIsPersonExists
 @Id int 
as
begin
  select 
     case when exists(select 1 from People where Id=@Id) 
     then 1 
     else 0 end as personExists;
end

-- get by id

create procedure spGetPersonById
 @Id int
as
begin
  select
   Id, 
   FirstName,
   LastName 
  from People
  where Id=@Id;
end   

-- delete

create procedure spDeletePerson
  @Id int 
as
begin
  delete from People where Id=@Id;
end  
```

### controller with stored procedures 


```js
const { Sequelize } = require('../config/database');

class PersonController {

    getAllPeople = async (req, res) => {
        try {
            const [people] = await Sequelize.query("EXEC spGetPeople");
            res.json(people);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    getPersonById = async (req, res) => {
        try {
            const result = await Sequelize.query("exec spGetPersonById @Id=?", {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });

            if (result.length === 0) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found"
                })
            }
            res.json(result[0]);
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    createPerson = async (req, res) => {
        try {
            const sql = `exec spCreatePerson @FirstName=?,@LastName=?`;
            const [result] = await Sequelize.query(sql, {
                replacements: [req.body.firstName, req.body.lastName],
                type: Sequelize.QueryTypes.SELECT
            });
            // console.log("====>" + JSON.stringify(result));
            const createdPerson = { id: result[0].id, ...req.body };
            res.status(201)
                .json(createdPerson);
        } catch (error) {
            console.log(error);
            res.status(500)
                .json({
                    statusCode: 500,
                    message: "Internal server error"
                });
        }
    }

    updatePerson = async (req, res) => {
        try {
            const [result] = await Sequelize.query('exec spIsPersonExists @Id=?', {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });
            if (!result.personExists) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person does not found."
                });
            }
            await Sequelize.query(`exec spUpdatePerson @Id=?,@FirstName=?,@LastName=?`, {
                replacements: [req.params.id, req.body.firstName, req.body.lastName],
                type: Sequelize.QueryTypes.SELECT
            });
            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }

    deletePerson = async (req, res) => {
        try {
            const sql = 'exec spIsPersonExists @Id=?';

            const [result] = await Sequelize.query(sql, {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });
            if (!result.personExists) {
                return res.status(404).json({
                    statusCode: 404,
                    message: "Person not found"
                });
            }

            await Sequelize.query(`exec spDeletePerson @Id=?`, {
                replacements: [req.params.id],
                type: Sequelize.QueryTypes.SELECT
            });

            res.status(204).send();
        }
        catch (error) {
            console.log(error);
            res.status(500).json({
                statusCode: 500,
                message: "Internal server error"
            });
        }
    }
}

module.exports = new PersonController();
```