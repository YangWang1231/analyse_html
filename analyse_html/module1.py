import os
import sqlite3

_DBPATH = "./q6996603.sqlite"

def fresh_db():
    if os.path.isfile(_DBPATH):
        os.remove(_DBPATH)
    with sqlite3.connect(_DBPATH) as conn:
        cur = conn.cursor().executescript("""
            CREATE TABLE "mytable" (
                "id" INTEGER PRIMARY KEY AUTOINCREMENT, -- rowid
                "data" INTEGER
            );
            """)
    print "created %s" % _DBPATH

# functions are syntactic sugar only and use global conn, cur, rowid

def select():
    sql = 'select * from "mytable"'
    rows = cur.execute(sql).fetchall()
    print "   same connection sees", rows
    # simulate another script accessing tha database concurrently
    with sqlite3.connect(_DBPATH) as conn2:
        rows = conn2.cursor().execute(sql).fetchall()
    print "   other connection sees", rows

def count():
    print "counting up"
    cur.execute('update "mytable" set data = data + 1 where "id" = ?', (rowid,))

def commit():
    print "commit"
    conn.commit()

# now the script
fresh_db()
with sqlite3.connect(_DBPATH) as conn:
    print "--- prepare test case"
    sql = 'insert into "mytable"(data) values(17)'
    print sql
    cur = conn.cursor().execute(sql)
    rowid = cur.lastrowid
    print "rowid =", rowid
    commit()
    select()
    print "--- two consecutive w/o commit"
    count()
    select()
    count()
    select()
    commit()
    select()
    print "--- two consecutive with commit"
    count()
    select()
    commit()
    select()
    count()
    select()
    commit()
    select()
