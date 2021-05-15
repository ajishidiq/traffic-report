#!/usr/bin/env python3
def get_host_id(connection, loopback):
    """
        getting hostid from table hosts 
    """
    try:
        query = """
            SELECT hostid from hosts
            where host = %s   
        """
        cursor = connection.cursor()
        cursor.execute(query, (loopback,))
        hostid = cursor.fetchone()[0]
        cursor.close()
        return hostid
    except (Exception) as error:
        print(error)