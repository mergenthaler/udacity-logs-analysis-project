import psycopg2
#Create necessary views


def createView(v, DBNAME="news"):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(v)
    db.commit()
    db.close()


topauthors = """
    CREATE VIEW topauthors AS
    select articles.author, count(log.path) as num
        from articles left join log
            on '/article/' || articles.slug =  log.path
        where log.status = '200 OK'
        group by articles.author
        order by num desc;
    """


error_log = """
  CREATE VIEW error_log AS
  SELECT date(time),round(100.0 * sum(case log.status when '200 OK'
  then 0 else 1 end)/count(log.status),2) AS "percenterror"
  FROM log GROUP BY date(time);
"""

createView(topauthors)
createView(error_log)
