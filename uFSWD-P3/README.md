# uFSWD-P3
Udacity Full Stack Web Development - Project 3

This project requires the student to analyze and answer the following questions based on PostgreSQL database.
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

To aid in answering the above questions I have created two views (included in the python program)
- article_views - This view joins the articles and log table. The log table is processed to generate total views per website path before joining it with articles table. The view contains following columns:
    - title - Article Title
    - author - Author ID
    - slug - Identifier to the article
    - view - total number of views for the given article
    ``` sql
    create or REPLACE view article_views as\
        select title,author,slug,views from articles,\
        (select path,count(path) as views\
            from log\
            where  path like '/article/%' and method='GET'\
            group by path)\
        as log_views\
        where log_views.path like CONCAT('/article/',articles.slug)
    ```
- views_by_date - This view compresses the log table to contain the following
    - date: Date for access
    - status: HTTP status for path access
    - views: number of accesses grouped by statuses
    ``` sql
    create or replace view views_by_date as\
        select cast(time as date) as date,status,count(*) as views\
        from log\
        group by date,status
    ```


To run the program:
``` sh
$ cd <project_dir> ; python p3.py
```
Or
``` sh
$ cd <project_dir> ; ./p3.py
```

You can open ouput.txt to look at sample output of the program.