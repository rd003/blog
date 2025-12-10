+++
date = '2025-02-23T13:42:38+05:30'
draft = false
title = 'Set Bearer Token to Each Request Automatically in Postman'
tags = ['web-tools']
categories = ['programming']
image = '/images/1_PF58vCp4rkSMpbesRbW23Q.jpg'
+++

When we work with postman to test the endpoints, and those endpoints are authorized, each time (until it expires) we need to pass the token in the authorization header. To get the token, we need to call the login or authentication API . This process feels quite irritating , because we programmers hates this manual working. We always want an easy and automatic workflow. Let’s see how can we achieve this with postman.

### Option 1: Using environment variable

### Creating the environment variable

First and foremost we need to create an environment.

<!-- ![Set Bearer Token to Each Request Automatically in Postman](/images/1_PF58vCp4rkSMpbesRbW23Q.jpg) -->

- Select the `Environments` tab in the left side.
- Click on the `plus` icon, as shown in diagram 1.1 , create a new environment and give it a name.
- Create a new variable and name it `token`.

![1.2](/images/1_5jbxc5iBlfKLv_UNZ59XZQ.jpg)

- Select the environment , you have recently created from the dropdown at the top right corner, as shown in diagram 1.2.

### Setting the environment variable through the script

![Setting the environment variable through the script](/images/1_-o3xpAlGgARkcUuAzyvH_A.jpg)

- Go to to login API request
- Select the `script` section
- Select `Post-response` tab.
- Enter the script shown in diagram 1.3. Since I am getting a token as text so I am using `pm.response.text()` . If you are getting the json as response, parse it accordingly.

### Using the environment variable in the authorization header

![1.4](/images/1_fwnAYdJ28ztQU2bJ0xOIng.jpg)

- In the protected api, go to the `authorization` section.
- Select `Bearer Token` as `Auth Type` and set its value to `{{token}}`. Now you can send the request.

---

### Option 2: Using Collection variable

This option is very much similar to the previous one. We will be using collection variable instead of environment variable. But this option is only application for the collection. If you don’t use collection don’t read further.

### Creating a collection variable

![2.1](/images/1_Q8qCwNkXbN-G6f6GlYCvNQ.jpg)

- Double click on the collection.
- You will see a `Variables` section as shown in the diagram 2.1. Click on the variables.
- Create a new collection variable and name it `token`.

### Setting the collection variable through script

![2.2](/images/1_ATTmb-4AVFJP-h2RWHWOnQ.jpg)

- Go to the login API request
- Select the `script` section
- Select `Post-response` tab.
- Enter the script shown in diagram 1.3. Since I am getting a token as text so I am using `pm.response.text()` . If you are getting the json as response, parse it accordingly.

If you close the collection and re-open it. You can see the current value of the token as shown below.

![2.2](/images/1_lXdVF9TjclpvrehV1NEjGg.jpg)

### Using the collection variable

![2.4](/images/1_GvJrgVoTOcsciIrS57uuXA.jpg)

- In the protected api, go to the `authorization` section.
- Select `Bearer Token` as `Auth Type` and set its value to `{{token}}`. Now you can send the request.

[Canonical link](https://medium.com/@ravindradevrani/set-bearer-token-automatically-to-each-request-in-the-postman-f13e083b5907)
