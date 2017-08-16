#!/usr/bin/python

import psycopg2
from datetime import datetime


class LogAnalysis():
    """Class LogAnalysis handles the connection with the PostgreSQL database and
    answers canned questions like popular articles and authors.
    """

    def __init__(self, dbname):
        """Accepts a database schema name
        and initializes LogAnalysis class object

        :param dbname: Database schema Name
        :type dbname: str

        """
        self.dbname = dbname

    def setupConnection(self):
        """Initializes the connection to a PostgreSQL database
        """
        self.connection = psycopg2.connect("dbname=" + self.dbname)
        self.cursor = self.connection.cursor()

    def closeConnection(self):
        """Closes the connection to a PostgreSQL database
        """
        self.cursor.close()
        self.connection.close()

    def setupViews(self):
        """Setups additional views for the database
        """
        # This view joins the articles and log table.
        # The log table is processed to generate total views per website path
        # before joining it with articles table
        # The view contains following columns:
        #   title - Article Title
        #   author - Author ID
        #   slug - Identifier to the article
        #   view - total number of views for the given article
        self.cursor.execute("create or REPLACE view article_views as\
            select title,author,slug,views from articles,\
                (select path,count(path) as views\
                            from log\
                            where  path like '/article/%' and method='GET'\
                            group by path)\
                as log_views\
            where log_views.path like CONCAT('/article/',articles.slug)")
        # This view compresses the log table to contain the following:
        #   date: Date for log
        #   status: HTTP status for path access
        #   views: number of accesses grouped by statuses
        self.cursor.execute("create or replace view views_by_date as\
            select cast(time as date) as date,status,count(*) as views\
                from log\
                group by date,status;")

    def printPopularArticles(self, limit=None):
        """Prints the article names and number of views,
        if limit is passed then it prints top 'n' articles

        :param limit: Number of popular articles to print,
        if None prints entire list in descending order
        :type limit: int

        """
        query = "select title, views from article_views order by views desc"
        query += " limit %d" % (limit) if limit else ""
        self.cursor.execute(query)
        print ("The {} most popular articles:".format(limit))
        for d in self.cursor.fetchall():
            print ("\t%s -- %d views" % (d[0], d[1]))

    def printPopularAuthors(self):
        """Prints the author names and total number of views for their articles,
        Author list in descending order of views
        """
        query = "select name,total_views\
            from authors,\
            (select author as author_id,sum(views) as total_views\
                from article_views group by author) as author_views\
            where author_id=id\
            order by total_views desc"
        print ("Popular Authors of all time:")
        self.cursor.execute(query)
        for d in self.cursor.fetchall():
            print ("\t%s -- %d views" % (d[0], d[1]))

    def printErrorProneDays(self, threshold=1):
        """Prints the dates which are more error prone.
        Error proness is defined by the threshold (value in percentage)

        :param threshold: Threshold for errors,
        Default value is 1%
        :type threshold: int

        """
        query = "select v1.date,(failed_views*100/total_views) from \
            (select date,sum(views) as failed_views\
                from views_by_date\
                where status not like '200 OK'\
                group by date) as v1,\
            (select date,sum(views) as total_views\
                from views_by_date\
                group by date) as v2\
            where v1.date=v2.date and\
                (failed_views*100/total_views)>%d;" % (threshold)
        self.cursor.execute(query)
        print ("Error Prone days [More than {}% errors]:".format(threshold))
        for d in self.cursor.fetchall():
            # Formatting the date in [Month Data, Year] format
            print ("\t{0} -- {1:.2f}% errors".format(
                    d[0].strftime('%B %d, %Y'), d[1]))

# Creating LogAnalysis Object
obj = LogAnalysis("news")
obj.setupConnection()
obj.setupViews()
# Answering the canned questions
obj.printPopularArticles(3)
obj.printPopularAuthors()
obj.printErrorProneDays(1)
