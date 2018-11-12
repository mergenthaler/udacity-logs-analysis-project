#!/usr/bin/env python
import psycopg2

# Functions that run queries on the SQL DB to answer specific questions


def executequery(q, DBNAME="news"):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(q)
    result = c.fetchall()
    db.close()
    return result


def topNarticle(n=3):
    q = """
    select articles.title, count(log.path) as num
    from articles left join log
        on '/article/' || articles.slug =  log.path
    where log.status = '200 OK'
    group by articles.title
    order by num desc
    limit %s;
    """ % n
    return executequery(q)


def topNAuthor(n=4):
    q = """
    select authors.name,topauthors.num
        from authors join topauthors
            on authors.id = topauthors.author
        order by num desc
        limit %s;
    """ % n
    return executequery(q)


def problematicDays(p=1):
    q = "select * from error_log where percenterror > %s;" % p
    return executequery(q)


def print_query_r(query_result, headers, metric):
    for res in query_result:
        print ('\t' + str(res[0]) + ' ---> ' + str(res[1]) + " " + metric)
    print("")

# Print results


print("1. What are the most popular three articles of all time?")
print_query_r(
    topNarticle(), headers=["Title", "Count of Views"],
    metric="views")

print("Who are the most popular article authors of all time?")
print_query_r(
    topNAuthor(), headers=["Author", "Count of Views"],
    metric="views")

print("On which days did more than 1% of requests lead to errors?")
print_query_r(
    problematicDays(), headers=["Date", "Error"], metric="percent")
