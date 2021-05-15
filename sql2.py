#!/usr/bin/env python3
from conn import connect
from read_zabbix import get_host_id
from read_zabbix import get_item_id
import time
import re

start_time = time.time()

connection = connect()
loopback = '192.168.163.132'

hostid = get_host_id(connection, loopback)

print(f'IP Loopback: {loopback} hostid: {hostid[0]}')

itemid = []
itemname = []

itemid_rx = []
itemid_tx = []

itemid, itemname = get_item_id(connection, hostid)
for i in range(len(itemid)):
    re.search('(\S+\)(')
    if re.search('received$', itemname[i]):
        print('RX: {}'.format(itemname[i]))
        itemid_rx.append(itemid[i])
    else:
        print('TX: {}'.format(itemname[i]))
        itemid_tx.append(itemid[i])

duration = time.time() - start_time
print("it takes about {:.2f} sec".format(duration))
connection.close()