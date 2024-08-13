import logging
import pandas as pd
import psycopg2

class DB:
    def setInfo(user, pwd, host, name):
        DB.USER = user
        DB.PWD = pwd
        DB.HOST = host
        DB.NAME = name

    def getInfo():
        return f'user:{DB.USER}, pwd:{DB.PWD}, host:{DB.HOST}, name:{DB.NAME}'

    def execute(query):
        """Execute a SQL query and return a dataframe"""
        df = pd.DataFrame([])
        connection = None
        try:
            connection = psycopg2.connect(
                user=DB.USER,
                password=DB.PWD,
                host=DB.HOST,
                database=DB.NAME
            )

            cursor = connection.cursor()
            cursor.execute(query)
            
            if cursor.description is None:
                return df
            colNames = [desc[0] for desc in cursor.description]
            table = cursor.fetchall()
            
            df = pd.DataFrame(table, columns=colNames)

        except (Exception, psycopg2.Error) as error:
            logging.error('Error while fetching data from PostgreSQL:', error)

        finally:
            if connection:
                connection.commit()
                cursor.close()
                connection.close()

        return df