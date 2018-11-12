# Logs Analysis Project
Building an informative summary from logs by sql database queries. Interacting with a live database both from the command line and from the python code. This project is a part of the Udacity's Full Stack Web Developer Nanodegree.

## Technologies used
1. PostgreSQL
2. Python DB-API (Postgress)
3. Linux-based virtual machine (VM) Vagrant

## Project Requirements
Reporting tool should answer the following questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## System setup and how to view this project
This project makes use of Udacity's Linux-based virtual machine (VM) configuration which includes all of the necessary software to run the application.
1. Download [Vagrant](https://www.vagrantup.com/) and install.
2. Download [Virtual Box](https://www.virtualbox.org/) and install. 
3. Clone [this repository](https://github.com/udacity/fullstack-nanodegree-vm.) containing the VM configustion to a directory of your choice.
4. ```vagrant up``` to start up the VM.
5. ```vagrant ssh``` to log into the VM.
6. ```cd /vagrant``` to change to your vagrant directory.
7. Download the [**newsdata.sql**](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and move the files to your **vagrant** directory within your VM.

#### Run these commands from the terminal in the folder where your vagrant is installed in: 
1. ```cd /vagrant``` to change to your vagrant directory.
2. ```psql -d news -f newsdata.sql``` to load the data and create the tables.
3. Clone this repository to run the python scripts
4. ```python views.py``` to create the necessary views
5. ```python logs.py``` to run the reporting tool and answer the questions.


## Views used (created by ```views.py```)
#### topauthors
````sql
    CREATE VIEW topauthors AS
    select articles.author, count(log.path) as num
        from articles left join log
            on '/article/' || articles.slug =  log.path
        where log.status = '200 OK'
        group by articles.author
        order by num desc;
````
#### error_log
````sql
  CREATE VIEW error_log AS
  SELECT date(time),round(100.0 * sum(case log.status when '200 OK'
  then 0 else 1 end)/count(log.status),2) AS "percenterror"
  FROM log GROUP BY date(time);
````
