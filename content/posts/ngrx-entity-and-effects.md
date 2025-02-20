+++
date = '2025-02-19T22:29:18+05:30'
draft = false
title = 'Ngrx Entity and Effects'
tags= ["angular"]
categories = ["programming"]
+++

![ngrx entity and effects](/images/ngrx_entity_and_effects.png)

`NGRX Entity` gives you an efficient and quick way to
deal with ngrx store related operations, such as
read, write, update, delete. You can focus on productivity, rather than
creating and modifeng complex state everytime. It can be very helpful
when you are dealing with complex state and handling with http services
at the same time.

## What is ngrx ?

Ngrx is a state management library, that stores the state globally. Lets
understand some of its components.

**Store**: It stores the state.

**Actions**: These are the unique actions those are dispatched from the
components.

**Reducers**: Once actions is dispatched, we move to its corresponding
reducer, inside the reducer we actually manage the state.

**Effects**: These are the side effects of the action which is used to
run some asynchronous code like http requests along with reducers.

**Selectors:** are the functions , used for selecting the whole state or
chunk of states.

Lets understand these thing with the example, which we are going to use
in this article. We have a book component which do the following things.

👉 display list of books

👉 add book

👉update book

👉delete book

♦️ We store the book state in **Store**.

♦️ To fetch book from store we need a **selector**.

♦️ To add a book to the store we will dispatch an AddBook action from
store, which will call AddBook **reducer** and adds the data to store.

♦️ AddBook action have a side effect, AddBook **effect**, which will
call the AddBook http service, add data to the database.

♦️ Same will happen with update and delete.

I am assuming that you aleady have some experience with ngrx store, if
you have then its not gonna be complicated for you.You should have some
understanding of ngrx store and effects, how side effects works. If you
don't know any thing about ngrx you can check out this detailed
[YouTube video](https://youtu.be/Ja5XUOcE9IQ) of mine.

> If you stuck somewhere go and check out my 💻 [github repo](https://github.com/rd003/ngrx-demo-yt/tree/ngrx-entity)
> If you prefer video version of the article , you can check out the video below.

{{< youtube id="bjL_H0cEvlk" title="Your Video Title" autoplay="false" >}}

So lets get started with creating a model, because we also need to
implement services here. So create a file **app/models/book.model.ts**

```ts
export interface Book {
  id: string;
  title: string;
  price: number;
}
```

Create a service BookService inside services folder. Open the file
**app/models/book.service.ts**

```ts
import { HttpClient } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { delay } from "rxjs";
import { Book } from "../models/book.model";

@Injectable({
  providedIn: "root",
})
export class BookService {
  private baseUrl = "/api/books";

  getBooks() {
    return this.http.get<Book[]>(this.baseUrl).pipe(delay(400));
  }

  addBook(book: Book) {
    return this.http.post<Book>(this.baseUrl, book);
  }

  updateBook(book: Book) {
    const url = `${this.baseUrl}/${book.id}`;
    return this.http.put(url, book);
  }

  deleteBook(id: string) {
    return this.http.delete(`${this.baseUrl}/${id}`);
  }

  constructor(private http: HttpClient) {}
}
```

You need to create rest apis for above services, with your preffered
backend tech, I have created the rest api backend, inside the angular
app with the help of json-server, you can check out there
[documentation](https://github.com/typicode/json-server) so that you can quickly create your
backend.

Install these 3 packages with following commands

```sh
ng add @ngrx/store@latest
ng add @ngrx/effects@latest
ng add @ngrx/entity@latest
```

Create a folder app/state/book, here we will create our ngrx related
files.

**app/state/book/book.actions.ts**

```ts
import { createAction, props } from "@ngrx/store";
import { Book } from "src/app/models/book.model";

export const loadBooks = createAction("[Book/API] Load Books");
export const loadbooksSucces = createAction(
  "[Book/API] Load Books Success",
  props<{ books: Book[] }>()
);
export const loadBooksFailure = createAction(
  "[Book/API] Load Books Failure",
  props<{ error: any }>()
);

export const addBook = createAction(
  "[Book/API] Add Book",
  props<{ book: Book }>()
);
export const addBookSuccess = createAction(
  "[Book/API] Add Book Success",
  props<{ book: Book }>()
);
export const addBookFailure = createAction(
  "[Book/API] Add Book Failure",
  props<{ error: any }>()
);

export const updateBook = createAction(
  "[Book/API] Update Book",
  props<{ book: Book }>()
);
export const updateBookSuccess = createAction(
  "[Book/API] Update Book Success",
  props<{ book: Book }>()
);
export const updateBookFailure = createAction(
  "[Book/API] Update Book Failure",
  props<{ error: any }>()
);

export const deleteBook = createAction(
  "[Book/API] Delete Book",
  props<{ id: string }>()
);
export const deleteBookSuccess = createAction(
  "[Book/API] Delete Book Success",
  props<{ id: string }>()
);
export const deleteBookFailure = createAction(
  "[Book/API] Delete Book Failure",
  props<{ error: any }>()
);

export const selectBook = createAction(
  "[Book/API] Select Book",
  props<{ id: string }>()
);
```

**app/state/book/book.reducer.ts**

```ts
import { createEntityAdapter, EntityState } from "@ngrx/entity";
import { createReducer, on } from "@ngrx/store";
import { Book } from "src/app/models/book.model";
import * as BookActions from "../book/book.actions";

export interface BookState extends EntityState<Book> {
  selectedBookId: string | null;
  loading: boolean;
  error: any;
}

export const bookAdapter = createEntityAdapter<Book>();

export const initialBookState: BookState = bookAdapter.getInitialState({
  selectedBookId: null,
  loading: false,
  error: null,
});

export const bookReducer = createReducer(
  initialBookState,
  on(BookActions.selectBook, (state, { id }) => ({
    ...state,
    selectedBookId: id,
  })),
  on(BookActions.loadBooks, (state) => ({
    ...state,
    loading: true,
  })),
  on(BookActions.loadbooksSucces, (state, { books }) =>
    bookAdapter.setAll(books, { ...state, loading: false })
  ),
  on(BookActions.loadBooksFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false,
  })),
  on(BookActions.addBook, (state, { book }) => ({ ...state, loading: true })),
  on(BookActions.addBookSuccess, (state, { book }) =>
    bookAdapter.addOne(book, { ...state, loading: false })
  ),
  on(BookActions.addBookFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false,
  })),
  on(BookActions.updateBook, (state, { book }) => ({
    ...state,
    loading: true,
  })),
  on(BookActions.updateBookSuccess, (state, { book }) =>
    bookAdapter.updateOne(
      { id: book.id, changes: book },
      { ...state, loading: false }
    )
  ),
  on(BookActions.updateBookFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false,
  })),
  on(BookActions.deleteBook, (state, { id }) => ({ ...state, loading: true })),
  on(BookActions.deleteBookSuccess, (state, { id }) =>
    bookAdapter.removeOne(id, { ...state, loading: false })
  ),
  on(BookActions.deleteBookFailure, (state, { error }) => ({
    ...state,
    error,
    loading: false,
  }))
);
export const getSelectedBookId = (state: BookState) => state.selectedBookId;
export const { selectAll, selectEntities, selectIds } =
  bookAdapter.getSelectors();
```

**app/state/book/book.effects.ts**

```ts
import { Injectable } from "@angular/core";
import { Actions, createEffect, ofType } from "@ngrx/effects";
import { catchError, map, of, switchMap } from "rxjs";
import { BookService } from "src/app/services/book.service";
import * as bookActions from "../book/book.actions";

@Injectable()
export class BookEffects {
  addUser$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(bookActions.addBook),
      switchMap((payload) =>
        this.bookService.addBook(payload.book).pipe(
          map((data) => bookActions.addBookSuccess({ book: payload.book })),
          catchError((error) => of(bookActions.addBookFailure({ error })))
        )
      )
    );
  });

  updateUser$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(bookActions.updateBook),
      switchMap((payload) =>
        this.bookService.updateBook(payload.book).pipe(
          map((_) => bookActions.updateBookSuccess({ book: payload.book })),
          catchError((error) => of(bookActions.updateBookFailure({ error })))
        )
      )
    );
  });

  deleteBook$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(bookActions.deleteBook),
      switchMap((payload) =>
        this.bookService.deleteBook(payload.id).pipe(
          map(() => bookActions.deleteBookSuccess({ id: payload.id })),
          catchError((error) => of(bookActions.deleteBookFailure({ error })))
        )
      )
    );
  });

  loadBooks$ = createEffect(() => {
    return this.actions$.pipe(
      ofType(bookActions.loadBooks),
      switchMap((_) =>
        this.bookService.getBooks().pipe(
          map((books) => bookActions.loadbooksSucces({ books })),
          catchError((error) => of(bookActions.loadBooksFailure({ error })))
        )
      )
    );
  });

  constructor(private actions$: Actions, private bookService: BookService) {}
}
```

**app/state/book/book.selectors.ts**

```ts
import { createFeatureSelector, createSelector } from "@ngrx/store";
import * as fromBooks from "../book/book.reducer";
import { BookState } from "../book/book.reducer";

export const selectBookState =
  createFeatureSelector<fromBooks.BookState>("bookState");

export const selectBooks = createSelector(selectBookState, fromBooks.selectAll);

export const selectBookLoading = createSelector(
  selectBookState,
  (state) => state.loading
);

export const selectBookError = createSelector(
  selectBookState,
  (state) => state.error
);

export const selectBookEntities = createSelector(
  selectBookState,
  fromBooks.selectEntities
);

export const selectCurrentBookId = createSelector(
  selectBookState,
  fromBooks.getSelectedBookId
);

export const selectCurrentBook = createSelector(
  selectBookEntities,
  selectCurrentBookId,
  (bookEntities, bookId) => bookId && bookEntities[bookId]
);
```

Import store and entity module in you **AppModule's imports array**.

```ts
StoreModule.forRoot({
  bookState: bookReducer,
}),
  EffectsModule.forRoot([BookEffects]);
```

Create a folder (app/components/book). Inside this folder create
book-list component.

**app/components/book/book-list.component.ts**

```ts
import { Component, EventEmitter, Input, Output } from "@angular/core";
import { Book } from "src/app/models/book.model";

@Component({
  selector: "app-book-list",
  template: `
    <h2>Books 📚</h2>

    <div class="my-1">
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Id</th>
            <th>Title</th>
            <th>Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr *ngFor="let book of books">
            <td>{{ book.id }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.price }}</td>
            <td>
              <button
                class="btn btn-primary mx-1"
                (click)="selectBook.emit(book.id)"
              >
                Select
              </button>
              <button
                class="btn btn-secondary mx-1"
                (click)="updateBook.emit(book.id)"
              >
                Update
              </button>
              <button
                class="btn btn-danger mx-1"
                (click)="removeBook.emit(book.id)"
              >
                Remove
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  `,
})
export class BookListComponent {
  @Input() books!: Book[];
  @Output() selectBook = new EventEmitter<string>();
  @Output() updateBook = new EventEmitter<string>();
  @Output() removeBook = new EventEmitter<string>();
}
```

This component is a `dumb component` here, we will just take few input and output parameters, we are just
displaying book list here. It does not know about state and service.
It's sole purpose is to display data only.

We will create aonthor `dumb component` here (selected-book.component.ts)

**app/components/book/selected-book.component.ts**

```ts
import { Component, Input } from "@angular/core";
import { Book } from "src/app/models/book.model";

@Component({
  selector: "app-selected-book",
  template: ` <div class="card my-2" style="width: 18rem;">
    <div class="card-header">Selected Book</div>
    <ul class="list-group list-group-flush">
      <li class="list-group-item">Title: {{ book.title }}</li>
      <li class="list-group-item">Price: {{ book.price }}</li>
    </ul>
  </div>`,
})
export class SelectedBookComponent {
  @Input() book!: Book;
}
```

Now lets create our `smart component` **(BookComponent).** It will deal with our ngrx store.

**app/components/book/book.component.ts**

```ts
import { Component, OnInit } from "@angular/core";
import { select, Store } from "@ngrx/store";
import { Observable } from "rxjs";
import { Book } from "src/app/models/book.model";
import { BookState } from "src/app/state/book/book.reducer";
import * as bookSelector from "../../state/book/book.selectors";
import * as bookActions from "../../state/book/book.actions";

@Component({
  selector: "app-book",
  template: `
    <ng-container *ngIf="loading$ | async as loading">
      <div class="spinner-border text-warning d-block my-4" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </ng-container>

    <ng-container *ngIf="error$ | async as error">
      <p>Error has occured</p>
    </ng-container>

    <ng-container *ngIf="currentBook$ | async as currentBook">
      <!-- call select-book component here -->
      <app-selected-book [book]="currentBook"></app-selected-book>
    </ng-container>

    <button class="btn btn-primary my-3" (click)="onAddBook()">
      Add more 📕
    </button>

    <ng-container *ngIf="books$ | async as books">
      <!-- call select-book component here -->
      <app-book-list
        [books]="books"
        (selectBook)="onBookSelect($event)"
        (updateBook)="onBookUpdate($event)"
        (removeBook)="onBookRemove($event)"
      >
      </app-book-list>
    </ng-container>
  `,
  styles: [],
})
export class BookComponent implements OnInit {
  books$!: Observable<Book[]>;
  loading$!: Observable<boolean>;
  error$!: Observable<any>;
  currentBook$ = this.store.pipe(select(bookSelector.selectCurrentBook));

  onBookSelect(id: string) {
    this.store.dispatch(bookActions.selectBook({ id }));
  }

  onAddBook() {
    //generating random string from current date
    const rnd = Date.now().toString();

    //generating random number between 100 and 500
    const max = 500;
    const min = 100;
    const randomPrice = Math.floor(Math.random() * (max - min + 1) + min);

    // creating a dummy book object
    const book: Book = { id: rnd, title: "Book " + rnd, price: randomPrice };

    // dispatching addBook action with dummy book data
    this.store.dispatch(bookActions.addBook({ book }));
  }

  onBookRemove(id: string) {
    this.store.dispatch(bookActions.deleteBook({ id }));
  }

  onBookUpdate(bookId: string) {
    const input = window.prompt("Enter title, price (eg. book1,100)");
    if (input) {
      const values = input.split(",");
      if (values.length == 2) {
        const book: Book = {
          id: bookId,
          title: values[0],
          price: parseInt(values[1]),
        };
        this.store.dispatch(bookActions.updateBook({ book }));
      }
    }
  }

  ngOnInit(): void {
    this.books$ = this.store.select(bookSelector.selectBooks);
    this.loading$ = this.store.select(bookSelector.selectBookLoading);
    this.error$ = this.store.select(bookSelector.selectBookError);
    this.store.dispatch(bookActions.loadBooks());
  }

  constructor(private store: Store<{ books: BookState }>) {}
}
```

Now you can call this **BookComponent** in **AppComponent**

```ts
<app-book></app-book>
```

[Canonical
link](https://medium.com/@ravindradevrani/lets-write-some-code-with-ngrx-entity-and-effects-bdada803bb54)
