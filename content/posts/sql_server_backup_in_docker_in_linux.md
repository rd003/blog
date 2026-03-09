+++
date = '2026-03-09T16:08:51+05:30'
draft = false
title = 'How to Backup SQL Server Running in Docker on Linux'
tags = ['sql','docker']
categories = ['database']
image = '/images/sql_server_backup.jpg'
+++
- I am using mssql server in docker container. 
- I am using vscode extension named [SQL Server (mssql)](https://marketplace.visualstudio.com/items?itemName=ms-mssql.mssql) by **microsoft**. This extension gives you the feature of creating and exporting the backup
- Connect to the database. It should look like this:
![mssql vscode](/images/mssql_vscode.jpg)

- Create a backup by using that extension.

![mssql backup](/images/mssql_backup.jpg)

**Note:** I have saved backup inside the folder `/var/opt/mssql/data/`

- To find the exact name:

```bash
docker exec <container_name> ls /var/opt/mssql/data/*.bak
```

- Copy backup from docker to host machine:

```bash
docker cp <container_name>:/var/opt/mssql/data/your_backup.bak ~/Documents/your_backup.bak
```