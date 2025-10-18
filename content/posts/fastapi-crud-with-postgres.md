+++
date = '2025-10-18T20:18:50+05:30'
draft = false
title = 'Fastapi CRUD  With Postgres'
categories = ['programming']
tags = ['python','fastapi']
+++

![fast api with postgres sqlalchemy and alembic](/images/fastapi-pg.webp)

In this tutorial we learn to create REST Apis with `fastapi`. We are going to use:

- `FastApi` for creating APIs
- `PostgreSQL` as a database
- `SQLAlchemy` as an ORM tool
- `Alembic` as a migration tool

## Tech and tools used

   - Linux os (you can use window or mac also. But with windows your commands might be a little different. I suggest you to use `GitBash` in windows)
   - I am using `uv` to create project, you can download it from [here](https://docs.astral.sh/uv/getting-started/installation/)
   - Python 3.12
   - VS Code (code editor) with extension `Python` by microsoft
   - PostgreSQL (I am using it in a docker container, you can use installed version too)

The reason I am using `uv`, because it is pretty fast and I can easily manage dependencies with it.

## Source code

[Github repo](https://github.com/rd003/fastapi_postgres_crud). If you like my work, please consider starring the repo.

## Create the new project

1. Create a project with uv `uv init book_crud`
2. Execute the command `code book_crud`. It will open this project in VS Code

Open the integrated terminal of `vs code` and fire these commands:

4. `uv venv` (will create a virtual environment)
5. `source .venv/bin/activate` (will activate venv)
6. `uv add Fastapi SQLAlchemy alembic psycopg2-binary python-dotenv uvicorn`
    - This command will add all ther required libraries
    - `SQLAlchemy` is an ORM
    - `alembic` is a migration tool
    - `psycopg2-binary` is a PostgreSQL database adapter 
    - `python-dotenv` is used for reading `.env` file
    - `uvicorn` is a server

7. `touch .env`
8. `mkdir src`
9. `cd src`
10. `mkdir models schemas database services routers`
11. `touch main.py`
12. `for d in models schemas database services routers; do touch $d/__init__.py; done`. This will create `__init__.py` file inside each folder (models,schemas,database,services and routers)

## Create a database

Create a database named `book_db` in postgres.

## Edit the .env file

```env
DEBUG=True
DATABASE_URL=postgresql://postgres:p%4055w0rd@localhost:5432/book_db
```

Note: my password is `p@55w0rd`. `p%4055w0rd` is the encoded version of it. I need to provide an encoded password, because it won't accept `@`.

## database/database.py

```py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase,sessionmaker
from dotenv import load_dotenv

class Base(DeclarativeBase):
    pass

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL').strip()

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

def get_session():
    with SessionLocal() as session:
        yield session

# just for testing the db connection
# if __name__ == "__main__":
#     conn = engine.connect()
#     print("Connected to db")
#     conn.close()
```

## models/book.py

```py
from src.database.database import Base
from sqlalchemy import String
from sqlalchemy.orm import Mapped,mapped_column

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(50))
    author: Mapped[str] = mapped_column(String(50))
```

It is a data model which corresponds to a database table.

## schemas/book_schemas.py:

These are pydantic schemas used as request and response models.

```py
from pydantic import BaseModel, ConfigDict,Field

class BookCreate(BaseModel):
    title:str = Field(min_length=1,max_length=50)
    author:str = Field(min_length=1,max_length=50)

class BookResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True) #  allows Pydantic to read data from ORM model attributes directly!
    id:int
    title:str
    author:str

```

## services/book_services.py

This file contains CRUD operations for book.

```py
from typing import List, Optional
from sqlalchemy.orm import Session 
from src.models.book import Book
from src.schemas.book_schemas import BookCreate,BookResponse

def add_book(session:Session, book_create:BookCreate)->BookResponse:
    book = Book(**book_create.model_dump())
    session.add(book)
    session.commit()
    session.refresh(book)
    book_response = BookResponse.model_validate(book)
    return book_response

def update_book(session:Session,book_id:int,book_update:BookCreate)->Optional[BookResponse]:
    stmt = session.query(Book).where(Book.id==book_id)
    existing_book = session.scalars(stmt).one_or_none()
    
    if existing_book is None:
       return None
    for key,value in book_update.model_dump().items():
        setattr(existing_book,key,value)
    session.commit()
    session.refresh(existing_book)
    return existing_book

def delete_book(session:Session,book_id:int) -> Optional[BookResponse]:
    stmt = session.query(Book).where(Book.id==book_id)
    existing_book = session.scalars(stmt).one_or_none()
    if existing_book is None:
        return None
    session.delete(existing_book)
    session.commit()
    return BookResponse.model_validate(existing_book)

def get_book(session:Session,book_id:int)-> Optional[BookResponse]:
    stmt = session.query(Book).where(Book.id==book_id) 
    book = session.scalars(stmt).one_or_none()
    if book is None:
        return None
    book_response = BookResponse.model_validate(book) 
    return book_response

def get_books(session:Session) -> List[BookResponse]:
    stmt = session.queryy(Book)
    books = session.scalars(stmt).all()
    return [BookResponse.model_validate(book) for book in books]
```

## routers/book_routes.py 

```py
from typing import List
from src.services import book_service
from src.schemas.book_schemas import BookCreate, BookResponse
from src.database.database import get_session
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException

book_router = APIRouter(
    prefix="/api/books",
    tags=["books"]
)

@book_router.get("/", response_model=List[BookResponse])
def get_books(session: Session = Depends(get_session)):
    return book_service.get_books(session)

@book_router.get("/{book_id}", response_model=BookResponse)
def get_book(book_id: int, session: Session = Depends(get_session)):
    book = book_service.get_book(session, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@book_router.post("/", response_model=BookResponse, status_code=201)
def add_book(book: BookCreate, session: Session = Depends(get_session)):
    return book_service.add_book(session, book)

@book_router.put("/{book_id}", response_model=BookResponse)        
def update_book(book_id: int, book: BookCreate, session: Session = Depends(get_session)):
    updated_book = book_service.update_book(session, book_id, book)
    if updated_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book
    
@book_router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):
    deleted_book = book_service.delete_book(session, book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
```

## main.py

```py
import os
from fastapi import FastAPI
from src.routers.book_routes import book_router
from dotenv import load_dotenv

load_dotenv()
app = FastAPI(debug=os.getenv("DEBUG", "False").lower() == "true")

app.include_router(book_router)

```

## Initialize migration

With migration commands, we create/update the database tables or other things related to the database.

Make sure, you are at the `root` directory not in the `src` directory.


```sh
alembic init alembic
```

This command with generate `alembic` directory and `alembic.ini` file in root directory.

## Update alembic.ini

Comment out this line `sqlalchemy.url = driver://user:pass@localhost/dbname`

## Edit alembic/env.py

Add these line to `env.py` file leave the other content as it is.

```py
## content before this is removed for the sake of brevity

config = context.config

from src.database.database import Base,DATABASE_URL
from src.models.book import Book 
# import other models too
url_str = DATABASE_URL.replace("%","%%")
config.set_main_option('sqlalchemy.url',url_str)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

## content after this is removed for the sake of brevity

```

**Note:** My password is `p@55w0rd`, which is encoded as `p%4055w0rd`. That's' why I need to replace `%` with `%%`.


## Create and apply migration

```sh
alembic revision --autogenerate -m "Inital migration"
```

It will create a migration file under `alembic/version` with a name like `f818e6752f3c_inital_migration.py`. Notice that, table is not created in the database yet. For that you have to apply this migration.

You need to review the file first. Make sure it has the content you are expecting. Then fire the command below which will persist changes to the database.

```sh
alembic upgrade head
```

## Running the app

```sh
uvicorn src.main:app --reload
```

App is listening at `http://127.0.0.1:8000`. You can `http://127.0.0.1:8000/docs` and it will open `swagger` documentation. You can test your apis there.

I am using a `VS Code extension` called `REST Client` by `Huachao Mao`. If you have installed it, you can create `books.http` file and paste the content below:

```txt
@base_url = http://localhost:8000/api/books

POST {{base_url}}
Content-Type: application/json

{
  "title": "aaa",
  "author": "bbb"
}   

###
PUT {{base_url}}/8
Content-Type: application/json

{
  "title": "jjj",
  "author": "aaa"
}  

### 
GET {{base_url}}

### 
GET {{base_url}}/8

### 
DELETE {{base_url}}/7
```

You will notice a link `Send Request` above each http verb (GET,PUT,POST,DELETE). You need to press that button.