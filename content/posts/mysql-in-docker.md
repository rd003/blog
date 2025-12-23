+++
date = '2025-12-22T18:31:32+05:30'
draft = false
title = 'How to run Mysql in Docker?'
tags = ['sql','docker']
categories = ['database']
image = '/images/mysql_docker.webp'
+++
Execute the command below.

For bash:

```sh
docker run -d \
  --name mysql-dev \
  -p 3306:3306 \
  -e MYSQL_ROOT_PASSWORD=p@55w0rd \
  -v mysql-data:/var/lib/mysql \
  mysql:8.0.44-debian
```

For powershell:

```ps1
docker run -d `
  --name mysql-dev `
  -p 3306:3306 `
  -e MYSQL_ROOT_PASSWORD=p@55w0rd `
  -v mysql-data:/var/lib/mysql `
  mysql:8.0.44-debian
```

- `--name` is the name of container.
- `-d` means detached mode.
- `-p` is a port. Its format is like [HOST_PORT]:[CONTAINER_PORT]. Host port is your machine's port. This container is running in port 3306 of your machine.
- `-e` sets environment and we are setting the password here.
- `-v` is a volume. It helps to persist the database even after the deletion of the container.
- `mysql:8.0.44-debian` is the image with tag. `mysql` is image name and `8.0.44-debian` is image tag. Always visit the [docker hub](https://hub.docker.com/) to get a latest image.

Note that, this image is not at your local machine yet. So, it will be pulled from the docker hub first and pulled only once (unless you change the tag).

## Verification

To verify container, execute `docker ps` command. It displays the running containers. It must show `Up x seconds` under the `status` tab (as shown below). 

```sh
~$ docker ps

CONTAINER ID   IMAGE                 COMMAND                  CREATED        STATUS          PORTS                               NAMES
ab7dc0e5e718   mysql:8.0.44-debian   "docker-entrypoint.s…"   10 seconds ago   Up 10 seconds   0.0.0.0:3306->3306/tcp, 33060/tcp   mysql-dev
```

## Run it in the terminal

```sh
docker exec -it mysql-dev mysql -u root -p
```

Execute this command  and provide the `password`. After this, your terminal should look like as shown below: 

```sh
mysql>
```

Show databases:

```sh
Show databases;
```

After this your terminal would look like this:

```sh
mysql> Show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
4 rows in set (0.02 sec)
```

Create database:

```sh
create database person_db;
```

Use created db:

```sh
use person_db;
```

Create table:

```sh
 create table person
 (
    id int auto_increment primary key, 
    first_name varchar(30) not null, 
    last_name varchar(30) not null
);
```

Show tables:

```sh
show tables;
```

Insert record(s):

```sh
 insert into person(first_name,last_name) 
 values 
 ('Ravindra','Devrani'),
 ('John','Doe'), 
 ('Nayan','Singh');
```

Select record(s)

```sh
select 
  id,
  first_name,
  last_name 
from person;
```

Exit from interactive terminal

```sh
exit;
```

### SQL Clients

You can use [DBeaver](https://dbeaver.io/download/), [mysql workbench](https://www.mysql.com/products/workbench/) or any vscode extension.


### Common errors

- While using `DBeaver`, You might get the error `Public Key Retrieval is not allowed`. 
  - Click on "Driver properties" tab in connection settings
  - Find or add: `allowPublicKeyRetrieval = true`