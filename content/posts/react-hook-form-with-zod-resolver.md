+++
date = '2026-07-17T12:37:10+05:30'
draft = false
title = 'React Hook Form With Zod Resolver'
tags= ["reactjs"]
categories = ["programming"]
image = '/images/react_hook_form_zod.webp'
+++

First and foremost install these packages in an existing react app:

```
npm install react-hook-form zod @hookform/resolvers
```

code:

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