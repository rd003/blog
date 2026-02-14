+++
date = '2025-03-26T19:59:22+05:30'
draft = false
title = 'How to Install DotNet SDK In Ubuntu Based Distros?'
tags = ['dotnet','linux']
categories=['programming']
+++

## My Distro

I am using `linux mint 22.1` which is based on `Ubuntu 24.04`.

## Straightforeward command

```bash
sudo apt-get update

sudo apt-get install -y dotnet-sdk-10.0
```

## But...

I have tried to run this command `sudo apt-get install -y dotnet-sdk-10.0` but unfortunately I got no success. I have found that, this command works only with `Ubuntu 24.10`. For `Ubuntu 24.04` I need to use different approach.

## Uninstall prior version if exists

```bash
sudo apt-get remove dotnet-sdk-9.0
```

Now, run these commands in a sequence:

```bash
sudo apt-get update

sudo apt-get install -y software-properties-common

sudo add-apt-repository ppa:dotnet/backports

sudo apt-get install -y dotnet-sdk-10.0

```
