#!/usr/bin/env python3
import re

def get_host_id(connection, loopback):
    """
        Getting Host Id from table hosts
    """
    try:
        query = """
            SELECT hostid from hosts
            where host = %s   
        """
        cursor = connection.cursor()
        cursor.execute(query, (loopback,))
        hostid = cursor.fetchone()
        cursor.close()
        return hostid
    except(Exception) as err:
        print(err)
        return False

def get_item_id(connection, hostid):
    """
        getting Item Id regarding Traffic Interface
    """
    try:
        query = '''
            SELECT itemid, name FROM items
            where hostid = %s and
            name ~* 'link\s+to' and 
                (key_ ~ 'net.if.in' or key_ ~'net.if.out' or 
                key_ ~ 'net.if.speed')
        '''
        cursor = connection.cursor()
        cursor.execute(query, hostid)
        itemid = []
        itemname = []
        temp = cursor.fetchall()
        for result in temp:
            itemid.append(str(result[0]))
            itemname.append(str(result[1]))
        cursor.close()
        return itemid, itemname
    except(Exception) as err:
        print(err)
        return False

def get_item_id_1(connection, hostid):
    """
        getting Item Id regarding Traffic Interface 
        sudah dirapihkan supaya enak buat dibikin dict nya
    """
    try:
        querySpeed = """
            SELECT itemid, name FROM items
            where hostid = %s and
            name ~* 'link\s+to' and
            key_ ~ 'net.if.speed'
        """
        queryTX = """
            SELECT itemid, name FROM items
            where hostid = %s and
            name ~* 'link\s+to' and
            key_ ~ 'net.if.out'
        """
        queryRX = """
            SELECT itemid, name FROM items
            where hostid = %s and
            name ~* 'link\s+to' and
            key_ ~ 'net.if.in'
        """
        cursor = connection.cursor()
        NodeTraffic = {}
        ifName, ifAlias, ifSpeedID = ('', '', 0)
        cursor.execute(querySpeed, hostid)
        temp = cursor.fetchall()
        for result in temp:
            ifName = re.search('(\S+)\((.*)\): Speed$', result[1]).group(1)
            ifAlias = re.search('(\S+)\((.*)\): Speed$', result[1]).group(2)
            ifSpeedID = int(result[0])
            NodeTraffic[ifName] = {}
            NodeTraffic[ifName]['ifAlias'] = ifAlias
            NodeTraffic[ifName]['ifSpeedID'] = ifSpeedID
        ifTXid = 0
        cursor.execute(queryTX, hostid)
        temp = cursor.fetchall()
        for result in temp:
            ifName = re.search('(\S+)\((.*)\): Bits sent$', result[1]).group(1)
            ifTXid = int(result[0])
            NodeTraffic[ifName]['ifTXid'] = ifTXid
        ifRXid = 0
        cursor.execute(queryRX, hostid)
        temp = cursor.fetchall()
        for result in temp:
            ifName = re.search('(\S+)\((.*)\): Bits received$', result[1]).group(1)
            ifRXid = int(result[0])
            NodeTraffic[ifName]['ifRXid'] = ifRXid
        return NodeTraffic
    except(Exception) as err:
        print(err)
        return False

def get_traffic(connection, itemid):
    """
        getting traffic measuremnt based on Item ID
    """
    try:
        query = '''
            SELECT value_avg, to_timestamp(clock) FROM trends_uint
            where itemid = %s order by clock desc limit 24
        '''
        cursor = connection.cursor()
        cursor.execute(query, itemid)
        traffic = []
        clock = []
        temp = cursor.fetchall()
        for result in temp:
            traffic.append(int(result[0]))
            clock.append(str(result[1]))
        cursor.close()
        return traffic, clock
    except(Exception) as err:
        print(err)
        return False