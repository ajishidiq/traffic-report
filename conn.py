#!/usr/bin/env python3
import psycopg2
from config import config

def connect():
    """
    Connection Initiation To Postgresql database
    """
    conn = None
    try:
        # Read Connection Parameters
        params = config()

        # Connect to the PostgreSQL Server 
        print("Connecting to Server")
        conn = psycopg2.connect(**params)
        print("Connect to DB Successfully")
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"The Error Occured {error} occured")
    return conn