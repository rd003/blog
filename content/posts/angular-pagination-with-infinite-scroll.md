+++
date = '2025-02-19T21:24:41+05:30'
title = 'Angular pagination with infinite scroll (using ngx-infite-scroll)'
tags= ["angular"]
categories = ["programming"]
canonical_url = "https://medium.com/@ravindradevrani/angular-pagination-with-infinite-scroll-using-ngx-infite-scroll-3545612eeec"
+++

![angular infinite scroll](/images/infinite_scroll_preview.jpg)

**Photo by** [**_Ajda ATZ_**](https://unsplash.com/ko/@azinber?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) **on** [**_Unsplash_**](https://unsplash.com/photos/Dz4iJ3v4-X4?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)

Sometimes we get a condition where you don’t want to display all the data at once. Initially we display some data, and when we scroll down ,we loads more data. This kind of behaviour you can see in youtube, instagram or facebook. You might even spend much time of your day on just scrolling down. So we are gonna learn how to do that.

You can get the same content in video format, if you prefer video version you can checkout this.

So Let’s get started by creating a new angular app with this command.

`ng new angular-23 --routing --style=scss`

Now the command below will open this project in visual studio code. If you use other code editor then you can skip this step and open this folder in your desired code editor.

`code angular-23`

We are using `ngx-infinite-scroll` in this tutorial. So we need to install this.

`npm install ngx-infinite-scroll`

We must inculude _AppRoutingModule_ in our _app.modul.ts._ Open **app.module.ts** and add these lines.

```ts
import { InfiniteScrollModule } from "ngx-infinite-scroll";

//in import section add inculde this module

imports: [
 InfiniteScrollModule
 ],
```

We need a method that will return use some amount of data, that we want to load on scroll. So we are gonna create a dummy service for that. Type this command:

`ng g s services/pagination-dummy`

Now open the “**pagination-dummy.service.ts**” file and replace it with following code.

```ts
import { Injectable } from "@angular/core";
import { delay, Observable, of } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class PaginationDummyService {
  private totalItems = 100;

  getItems(page = 1, itemsPerPage = 10): Observable<string[]> {
    const startIndex = (page - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const items = [];
    for (let i = startIndex; i < endIndex; i++) {
      if (i < this.totalItems) {
        items.push(`Item ${i + 1}`);
      }
    }
    return of(items).pipe(delay(500));
  }

  constructor() {}
}
```

Now we are going to create a component,where we are going to implement this functionality. So create a new component with name “ngx-infinite-scroll”. You can follow this command.

`ng g c components/ngx-infinite-scroll`

Open the `ngx-infinite-scroll.component.ts` and write down this code there

```ts
export class NgxInfiniteScrollComponent implements OnInit {
  items: string[] = [];
  isLoading = false;
  currentPage = 1;
  itemsPerPage = 10;

  toggleLoading = () => (this.isLoading = !this.isLoading);

  // it will be called when this component gets initialized.
  loadData = () => {
    this.toggleLoading();
    this.paginationService
      .getItems(this.currentPage, this.itemsPerPage)
      .subscribe({
        next: (response) => (this.items = response),
        error: (err) => console.log(err),
        complete: () => this.toggleLoading(),
      });
  };

  // this method will be called on scrolling the page
  appendData = () => {
    this.toggleLoading();
    this.paginationService
      .getItems(this.currentPage, this.itemsPerPage)
      .subscribe({
        next: (response) => (this.items = [...this.items, ...response]),
        error: (err) => console.log(err),
        complete: () => this.toggleLoading(),
      });
  };

  onScroll = () => {
    this.currentPage++;
    this.appendData();
  };

  constructor(private paginationService: PaginationDummyService) {}

  ngOnInit(): void {
    this.loadData();
  }
}
```

Open **_ngx-infinite-scroll.component.html_** file and replace with this code.

```html
<div
  class="search-results"
  infiniteScroll
  [infiniteScrollDistance]="2"
  [infiniteScrollThrottle]="500"
  (scrolled)="onScroll()"
  [scrollWindow]="false"
>
  <div class="data-card" *ngFor="let item of items">{{item}}</div>

  <div *ngIf="isLoading">Loading...</div>
</div>
```

Note down these things.

- When we set **[scrollWindow]=”false”** it means you onScroll() method will be called on the scroll of the div with “.search-results” otherwise scroll will work on page scrolling,not the scrolling of div element.
- The **infiniteScrollDistance=2** defines that scroll event occurs when scroll is 2 hight away from the bottom.
- The **infiniteScrollThrottle=500** says that event will not occur before 500ms.
- The **(scroll)=”onScroll()”** says that,when you scroll down and reached at the bottom the onScroll() method will be invoked.

Open **_ngx-infinite-scroll.component.scss_** file and add these styles.

```css
.search-results {
  height: 30rem;
  overflow: scroll;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.data-card {
  padding: 5px;
  margin: 8px 0px;
  width: 20%;
  border: 1px solid black;
  font-size: 30px;
  text-align: center;
  background-color: rgb(236, 234, 111);
}
```

At last, replace the content of **app.comonent.html** with this one

`<app-ngx-infinite-scroll\></app-ngx-infinite-scroll\>`

Now run the project with **ng serve — open** and see the result as shown below.

![infinite_scroll](/images/infinit_scroll.gif)

> 📎Source code: [https://github.com/rd003/angular-23](https://github.com/rd003/angular-23)

[Canonical link](https://medium.com/@ravindradevrani/angular-pagination-with-infinite-scroll-using-ngx-infite-scroll-3545612eeec)
