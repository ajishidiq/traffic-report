#!/usr/bin/env python3
from conn import connect
from read_zabbix import get_traffic
from read_zabbix import get_item_id_1
connection = connect()
itemid = (132483,)

#traffic, clock = get_traffic(connection, itemid)
#
#for i in range(len(traffic)):
#    traffic_temp = '{:.2f} Mbps'.format(traffic[i] / 1000000)
#    print(f'{traffic_temp} -- {clock[i]}')

connection.close()