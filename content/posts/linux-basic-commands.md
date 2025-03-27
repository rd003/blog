+++
date = '2025-03-27T19:52:00+05:30'
draft = false
title = 'Linux Basic Commands'
categories= ["programming"]
tags = ["linux"]
+++

1. Contents of a file: `ls`
2. Content list with long format: `ls -l` or `ls -l -h` human readable or concat the both `ls -lh`.
3. Change directory: `cd DirectoryName`
4. Move to the upper directory: `cd ..`
5. Switch to previous directory : `cd -`
6. Change to home directory: `cd ~`
7. Go to full path: `cd /Home/Documents/Pitctures/MyPictures`
8. Tilde (~) for home directory : `MyPc:~/Documents$ cd ~/Videos`
9. Clear screen: `clear`
10. Show different drives in the computer (List block devices): `lsblk`
11. Opening a file in the text editor :

```bash
# open in nano
nano filename

#open in xed editor
xed filename
```
12. Root directory: `cd /`
13. Press `Tab` to autocomlete.
14. Create a directory : `mkdir blah`
15. Remove a directory : `rmdir blah`
14. Creating a blank file : `touch something.txt`
    14.1. Creating multiple files at once: `touch f1.txt f2.txt f3.txt f4.md f5.md`
15. Printing something in terminal : `echo hello`
16. Create a file with text: `echo "blah blah" > blah.txt`
17. Show contents of a file: `cat blah.txt`
18. Copy file : `cp /source/filename.ext destination/filename.ext`

```bash
# note: I am currently in the `Desktop` directory
# copy `blah.txt` from `Desktop` to `Documents` directory

cp blah.txt ~/Documents/blah2.txt

# copy `blah.txt` from `Desktop` to `Documents` directory with changed filename

cp blah.txt ~/Documents/blah2.txt 

# it will copy `blah.txt from `Desktop` to `Documents` directory with changed file name `blah2.txt`
```
19. Copy all files (*.* allfiles.allextensions): `cp *.* ~/Documents`
20. Copy a whole directory to another directory: `cp -r blah blah2`
     
    It will copy `blah` directory along will all the files and subdirectories to `blah2` directory

21. Move a file: `mv ~/Desktop/blah.txt ~/Documents/blah.txt`
22. Rename a file: `mv ~/Documents/blah.txt ~/Documents/blah-blah.txt`
23. Remove file: `rm filename.extension`
23. Remove a directory and all the content inside it: `rm -rf {directory-name}`
24. Remove all txt files: `rm *.txt`
25. Unzip a file: `unzip filename.zip`
26. Install an application (in debian based distros): `sudo apt install {application-name}`. Make sure to run `sudo apt update` command before installing anything.
27. Remove an application : `sudo apt remove {application-name}`
28. Command help : `cp --help`. Will give help about copy command.
29. Or using a `man` command: `man cp`. Will give detailed manual of cp command
30. Stats of a file or directory: `man somefile.txt` or `man my-directory`
31. `cat error.log | sort | unique`: takes content of  the `error.log`, sort them, remove duplicates and show them.
32. Print linux username: `whoami`
33. User id : `id -u`. Root has id 0. 
34. Print current directory: `pwd`
35. Search some text(blah) in some file(blah.txt): `grep blah blah.txt` 
36. Exit from a terminal: `exit`
