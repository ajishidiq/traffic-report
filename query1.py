#!/usr/bin/env python3
import psycopg2
from config import config

def get_hostid():
    """ query data from the vendors table """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        loopback = '202.162.222.80'
        query = '''SELECT hostid from hosts
                    where host = %s
        '''
        cur.execute(query, (loopback,))
        if cur.rowcount == 1:
            hostid = cur.fetchone()
        else:
            print('duplicate nodes')
            quit()
        print(hostid)
        query = '''
                SELECT itemid, key_, name, delay FROM public.items 
                where hostid = %s and 
                name ~* 'link\s+to' and 
                (key_ ~ 'net.if.in' or key_ ~'net.if.out')
        '''
        cur.execute(query, (hostid,))
        i = 0
        rows = cur.fetchall()
        for row in rows:
            temp = list(row)
            print(f"item id: {temp[0]} description {temp[2]}")
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == '__main__':
    get_hostid()   