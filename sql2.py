#!/usr/bin/env python3
from conn import connect
from read_zabbix import get_host_id
from read_zabbix import get_item_id
from read_zabbix import get_item_id_1
from read_zabbix import get_traffic

import time
import re

start_time = time.time()

connection = connect()
loopback = input('masukan loopback address: ')

hostid = get_host_id(connection, loopback)

print(f'IP Loopback: {loopback} hostid: {hostid[0]}')

#itemid = []
#itemname = []
#
#itemid_rx = []
#itemid_tx = []
#
#itemid, itemname = get_item_id(connection, hostid)
#for i in range(len(itemid)):
#    re.search('(\S+\)(')
#    if re.search('received$', itemname[i]):
#        print('RX: {}'.format(itemname[i]))
#        itemid_rx.append(itemid[i])
#    else:
#        print('TX: {}'.format(itemname[i]))
#        itemid_tx.append(itemid[i])
traffic = get_item_id_1(connection, hostid)
#print(traffic)

interfaces = list(traffic.keys())
idTX, idRX, idSpeed = (0,0,0)
for interface in interfaces:
    idTX = traffic[interface]['ifTXid']
    idRX = traffic[interface]['ifRXid']
    idSpeed = traffic[interface]['ifSpeedID']
    print(f"{interface} == {traffic[interface]['ifAlias']}")
    print('TX Traffic')
    print('-' * 20)
    TXTraffic, clock = get_traffic(connection, (idTX,))
    for i in range(len(TXTraffic)):
        traffic_temp = '{:.2f} Mbps'.format(TXTraffic[i] / 1000000)
        print(f'{traffic_temp} -- {clock[i]}')
    print('RX Traffic')
    print('-' * 20)
    RXTraffic, clock = get_traffic(connection, (idRX,))
    for i in range(len(TXTraffic)):
        traffic_temp = '{:.2f} Mbps'.format(RXTraffic[i] / 1000000)
        print(f'{traffic_temp} -- {clock[i]}')
    print ('\n')
duration = time.time() - start_time
print("it takes about {:.2f} sec".format(duration))
connection.close()