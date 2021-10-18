'''This module contains functions defining an API for executing queries
on MySQL servers'''

from sys import exit
import re

import mysql.connector
from mysql.connector import errorcode




def create_database(db_name, cnx):
    '''Create MySQL Database

    Arguments
    ---------
    db_name: str
        Name of the database you want to use

    cnx: mysql.connector.connection.MySQLConnection
        A Connection to MySQL server
    '''

    try:
        cursor = cnx.cursor()
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)
    else:
        cnx.close()


def use(db_name, cnx):
    '''Set Database to Be Used

    Arguments
    ---------
    db_name: str
        Name of the database you want to use
    cnx: mysql.connector.connection.MySQLConnection
        A Connection to MySQL server
    '''

    try:
        cursor = cnx.cursor()
        cursor.execute("USE {}".format(db_name))
        print("{} database is now used!".format(db_name))
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database {} does not exists.".format(db_name))
            create_database(db_name, cxn)
            print("Database {} created successfully.".format(DB_NAME))
        elif err.errno == 1044:
            print(err.msg)
        elif err.errno == 1698:
            print(err.msg)
        else:
            print(err)

def show_tables(api):
    '''Show tables from currently used database

        Parameters
        ----------
        api: APIConnection object
    '''
    api.cursor.execute("SHOW TABLES;")
    for tbl in api.cursor:
        print(tbl)

def create_table(api, tbl_def):
    '''Create a table

       You must have the create privilege for the table.

       Parameters
       ----------
       tbl_def: str
           The definition of a table
       '''

    regex = re.compile("(TABLE)\s(.+)\s")
    tbl_name = regex.search(tbl_def).group(2).split()[0]
    try:
         api.cursor.execute(tbl_def)
         print("Table {} created successfully!".format(tbl_name))
    except mysql.connector.Error as err:
        print(err)

