import sqlite3
from contextlib import closing
from sqlite3 import Error
from passlib.context import CryptContext

dbname="covidProject.db"

""" create a database connection to a SQLite database """

conn = None
try:
    conn = sqlite3.connect(dbname,check_same_thread=False)
    print(sqlite3.version)
except Error as e:
    print(e)


# Create Tables for the admin users and the new queries
def createAdminTable():
    query = """create table if not exists Admin(
        username varchar(50) primary key UNIQUE,
        password varchar(50)
        );"""

    with closing(conn.cursor())as c:
        c.execute(query)
        conn.commit()


def createQueryTable():
    query = """create table if not exists Queries(
        query varchar(100) UNIQUE
        );"""

    with closing(conn.cursor())as c:
        c.execute(query)
        conn.commit()

# methods to add and get stored queries


def addQuery(_query):
    query="""INSERT INTO Queries VALUES(?);"""

    with closing(conn.cursor())as c:
        c.execute(query,(_query,))
        conn.commit()

def getQueries():
    queries=[]
    query="""SELECT query FROM Queries"""
    with closing(conn.cursor())as c:
        c.execute(query)
        conn.commit()
        queries=c.fetchall()

    return queries

def deleteQuery(delete):
    query="""DELETE FROM Queries where query=?"""
    with closing(conn.cursor())as c:
        c.execute(query,(delete,))
        conn.commit()


#authentication
pwd_context = CryptContext(
        schemes=["pbkdf2_sha256"],
        default="pbkdf2_sha256",
        pbkdf2_sha256__default_rounds=30000
)

def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


def addAdmin(uname,pword):
    password=encrypt_password(pword)

    query="""INSERT INTO Admin(username,password) VALUES(?,?);"""

    with closing(conn.cursor())as c:
        c.execute(query,(uname,password))
        conn.commit()


def authenticate(uname,pword):
   # password=""

    query="""SELECT password FROM Admin WHERE username=?;"""
    with closing(conn.cursor())as c:
        c.execute(query,(uname,))
        conn.commit()
        password=c.fetchone()
        print(str(password))
        return check_encrypted_password(pword,password[0])

def allAdmin():
    query="""SELECT * FROM Admin;"""
    with closing(conn.cursor())as c:
        c.execute(query)
        conn.commit()
        admins=c.fetchall()

        for ad in admins:
            print(str(ad))

