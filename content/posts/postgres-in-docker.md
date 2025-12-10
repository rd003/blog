+++
date = '2025-12-02T11:02:49+05:30'
draft = false
title = 'How to run PostgreSql in Docker'
tags = ['sql','docker']
categories = ['database']
image = '/images/pg_docker.webp'
+++

<!-- ![Postgres in Docker](/images/pg_docker.webp) -->

To be honest, since I have started using docker I have never installed any database in my machine. I use multiple databases and keeping each database up and running takes a toll on resources of your machine. And... you can not install some database like "sql server" on "mac", then docker is only option for you. Any way, I think it is enough introduction. Let's get started.

## Pre-Requisites

- Windows: Docker desktop
- Linux: Docker desktop or just docker daemon without any ui client`
- Mac: Docker desktop. I am not sure whether there is a docker with just cli available for mac or not

Anyway, docker desktop works on all of them.

## Pull the docker image of postgres

```bash
docker pull postgres:16.9-bullseye
```

This step pulls the docker image from docker hub to you machine.

Note that, `postgres` is the name of image and `16.9-bullseye` is a tag of image. If you want to select the latest or specific version of `postgres`, then you need to visit [docker hub](https://hub.docker.com/) and search for `postgres`.

## Run the container

```bash
 docker run --name pg-dev \
 -e POSTGRES_PASSWORD=p@55w0rd \
 -p 5432:5432 \
 -v pgdata:/var/lib/postgresql/data \
 -d postgres:16.9-bullseye
```

📢 Note: For `windows powershell`, replace `\` with ` (backtick) in above command.

- `--name` it is a name of the container
- `-e` specifies the environments. We are defining password here 
- `-p` specifies the ports. Left one is host port. Which is a port of your machine. Right one is the port of docker.
- `-v` volume defines volume named `pgdata` at location `/var/lib/postgresql/data`. You must define volume if you want to persist data. Volume persist data even you have destroyed the container. If you remove the container, all the database and data will be lost, unless you have defined a volume.
-  `-d` name of the image with tag.

With this `docker ps -a` command, you can check all the containers.

## Your postgres credentials

- host : `localhost`
- port : `5432`
- username : `postgres` 
- password : `p@55w0rd`

With these credentials you can log in to [pgadmin](https://www.pgadmin.org/), [dbeaver](https://dbeaver.io/) (These are the tools I have personally used) or any sql client.

## Connecting postgres in terminal

```sh
#run postgres in interactive mode (windows)
docker exec -it pg-dev sh

#for unix systems
docker exec -it pg-dev bash

# login to postgres
psql -U postgres

# see all database
\l
```

### Other commands

```sql
--create database

create database PersonDb;

-- use database

\c PersonDb  -- no semicolon

-- create table
create table person
(
Id serial primary key, Name varchar(30)
);

-- insert
insert into person(name) values('john');

-- select
select * from person;

-- exit from current using database
\q

-- delete database
drop database persondb;
```

Type `exit` to exit from the shell.