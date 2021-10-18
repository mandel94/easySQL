#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 24 14:58:03 2021

@author: mandel94
"""

'''This module will export a connection to MySQL server.
   This connection will function as an interface for building our database  
'''

import mysql.connector
from mysql.connector import MySQLConnection
from mysql.connector import errorcode
import easySQL.mysql.commands as commands



def establish_connection(**config):
    '''Establish a Connection to MySQL Server

    This function tries to establish a connection to MySQL Server, catching
    some errors that might occur.

    Arguments
    ----------
    config: dict
        Provide a connection configuration

    return_cursor: Bool
        Should the cursor be returned?

    Returns
    ---------
    Connection object
    '''

    global cnx
    try:
        cnx = MySQLConnection(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        elif err.errno == 1044:
            print(err.msg)
        elif err.errno == 1698:
            print(err.msg)
        else:
            print(err)
    else:
        return cnx


class APIConnection(MySQLConnection):
    '''An interface to MySQL Server

    This is a derived class, having mysql.connector.MySQLConnection as a parent
    class. It extends it functionalities with a series of methods providing
    an easy to use interface to SQL commands.

    Attributes
    ----------
    **config: dict
        Configuration of the connection to be established
    '''

    def __init__(self, **config):
        super().__init__(**config)
        self.cursor = self.cursor(buffered=True)

    def show_tables(self):
        '''Show tables from currently used database'''
        commands.show_tables(self)

    def create_table(self, tbl_def):
        '''Create a table

           You must have the create privilege for the table.

           Parameters
           ----------
           tbl_def: str
               The definition of a table
           '''

        commands.create_table(self, tbl_def)



        

    def drop_tables(self, *tbl_names, if_exists=False, show_warnings=False):
        '''Drop one ore more tables
            Parameters
            ----------
            *tbl_names: tuple of strings
                It designates the names of the tables to be dropped
            if_exists: bool
                If set to False, the statement fails with an error indicating
                which non-existing tables it was unable to drop, and no changes
                are made.
                If set to True, The statement drops all named tables that do
                exist, and generates a NOTE diagnostic for each nonexistent
                table (these notes can be displayed with SHOW WARNINGS). Set
                show_warnings = True if you want notes for non-existing tables
                to be displayed.
            show_warnings: bool
                When `if_exists=True`, should notes for non-existing tables be
                displayed?
        '''

        if_exists = "IF EXISTS" if if_exists else ""
        show_warnings = "SHOW WARNINGS" if show_warnings else ""
        for tbl in tbl_names:
            try:
                 query = "DROP TABLE {} {} {}".format(tbl,
                                                      if_exists,
                                                      show_warnings)
                 self.cursor.execute(query)
                 print("Table {} removed!".format(tbl))
            except mysql.connector.Error as err:
                print(err)



    # TODO: DEFINE METHOD FOR IMPLEMENTING SQL TRANSACTIONS

__all__ = ["establish_connection", "APIConnection"]
