+++
date = '2026-07-17T12:37:10+05:30'
draft = false
title = 'React Hook Form With Zod Resolver (for JS and TS both)'
tags= ["reactjs"]
categories = ["programming"]
image = '/images/react_hook_form_zod.webp'
+++

So....What is:

- **React hook form:** It is a popular light library to create and manage forms. It is very performative and comes with built-in 
validation support.

- **Zod **: It is a schema validation library that lets you define the shape of your data and validate it at runtime. It makes easier to
do validation.


Create a react app with JS or TS whatever you prefer. After that install these packages in a react app:

```
npm install react-hook-form zod @hookform/resolvers
```

## For javascrit app

```jsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { email, z } from "zod"

const schema = z.object({
  id: z.number().optional(),
  name: z.string()
    .min(1, "Name is required")
    .max(30, "Max length should be 30"),
  email: z.string()
    .email("Please enter valid email"),
  age: z.number({
    required_error: "Age is required",
    invalid_type_error: "Age must be a number"
  })
    .min(19, "Min value 19")
    .max(99, "Max valud 99")
})

export default function App() {
  const { handleSubmit, register,reset, formState: { errors, isValid, isDirty  } } = useForm({
    resolver: zodResolver(schema),
      mode: 'onChange',
        defaultValues: {
            id: 0
        }
  });

  function onSubmit(data) {
        console.log(data);
        reset();
  }

  return (
    <>
      <form onSubmit={handleSubmit(onSubmit)}>
	
   	<input type="hidden"  {...register("id")} />

        Name: <input {...register("name")} />
        {errors.name && <p>{errors.name.message}</p>}
        <br />

        Email: <input {...register("email")} />
        {errors.email && <p>{errors.email.message}</p>}

        < br />

        Age: <input type="number" {...register("age", { valueAsNumber: true })} />
        {errors.age && <p>{errors.age.message}</p>}

        < br />
        <button type="submit" disabled={!isDirty || !isValid}>Save</button>
      </form>
    </>
  )
}
```

## For Typescript app:

```ts
import { useForm } from "react-hook-form";
import type { SubmitHandler } from "react-hook-form";
import { z } from 'zod';
import { zodResolver } from "@hookform/resolvers/zod";


type IFormInput = z.infer<typeof schema>;

const schema = z.object({
    id: z.number(),
    firstName: z.string()
        .min(1, "First Name is required")
        .max(30, "Length of FirstName can not exceed 30 characters"),
    lastName: z.string()
        .min(1, "Last Name is required")
        .max(30, "Length of FirstName can not exceed 30 characters"),
})

export default function PersonForm() {
    const { register, handleSubmit, reset, formState: { errors, isValid, isDirty } } = useForm<IFormInput>({
        resolver: zodResolver(schema),
        mode: 'onChange',
        defaultValues: {
            id: 0
        }
    })
    const onFormSubmit: SubmitHandler<IFormInput> = (data) => {
        console.log(data);
        reset();
    }


    return (
        <form className='w-1/4' onSubmit={handleSubmit(onFormSubmit)}>
            <input type="hidden" {...register("id")} />

            First Name: <input {...register("firstName")} id="fieldgroup-firstName" placeholder="First Name" />
            {errors.firstName && <p style={{ 'color': 'red' }}>{errors.firstName.message}</p>}

            <p></p>

            Last Name: <input {...register("lastName")} id="fieldgroup-lastName" placeholder="Last Name" />
            {errors.lastName && <p style={{ 'color': 'red' }}>{errors.lastName.message}</p>}

            <p></p>
            <button type="reset" onClick={() => reset()}>Reset</button>
            <button type="submit" disabled={!isDirty || !isValid}>Submit</button>
        </form>
    )
}
```