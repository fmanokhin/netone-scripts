#!/usr/bin/env python3

from sshtunnel import SSHTunnelForwarder
import MySQLdb
import xlrd

dbserver = '192.168.1.1'
user = 'user'
passwd = 'passwd'
dbuser = 'dbuser'
dbpass = 'dbpass'

popfile = 'nrz-sdk-import.xlsx'
titlelist = []
addresslist = []
commentlist = []
switchlist = []
vlanlist = []

########Parsing XLS-file and getting title:address dict########

def get_titlelist(popfile):
    global titlelist
    file = xlrd.open_workbook(popfile)
    list1 = file.sheet_by_index(0)
    col1 = list1.col_values(0, start_rowx=1)
    for n in col1:
        titlelist.append(n)
    return titlelist

def get_addresslist(popfile):
    global addresslist
    file = xlrd.open_workbook(popfile)
    list1 = file.sheet_by_index(0)
    col2 = list1.col_values(1, start_rowx=1)
    for n in col2:
        addresslist.append(n)
    return addresslist

def get_commentlist(popfile):
    global commentlist
    file = xlrd.open_workbook(popfile)
    list1 = file.sheet_by_index(0)
    col3 = list1.col_values(2, start_rowx=1)
    for n in col3:
        commentlist.append(n)
    return commentlist

def get_switchlist(popfile):
    global switchlist
    file = xlrd.open_workbook(popfile)
    list1 = file.sheet_by_index(0)
    col4 = list1.col_values(3, start_rowx=1)
    for n in col4:
        switchlist.append(n)
    return switchlist

def get_vlanlist(popfile):
    global vlanslist
    file = xlrd.open_workbook(popfile)
    list1 = file.sheet_by_index(0)
    col5 = list1.col_values(4, start_rowx=1)
    for n in col5:
        vlanlist.append(n)
    return vlanlist

get_titlelist(popfile)
get_addresslist(popfile)
get_commentlist(popfile)
get_switchlist(popfile)
get_vlanlist(popfile)

###### Start to connect server with DB########

server = SSHTunnelForwarder(
    dbserver,
    ssh_username=user,
    ssh_password=passwd,
    remote_bind_address=('127.0.0.1', 3306)
)
server.start()

for title, address, comment, switch, vlan in zip(titlelist, addresslist, commentlist, switchlist, vlanlist):
    conn = MySQLdb.connect(
        host='127.0.0.1',
        port=server.local_bind_port,
        user=dbuser,
        password=dbpass,
        db='dbname'
    )
    cursor = conn.cursor()

    conn.set_character_set('utf8')
    cursor.execute('SET NAMES utf8;')
    cursor.execute('SET CHARACTER SET utf8;')
    cursor.execute('SET character_set_connection=utf8;')
    sql = "insert into inventory_customer(title, address, comments, switch, vlans) values('"+title+"', '"+address+"', '"+comment+"', '"+switch+"', '"+str(vlan)+"');"
#    sql ="update inventory_pop set address='"+address+"' where title='"+title+"';"
    cursor.execute(str(sql))
    conn.commit()
    conn.close()

server.stop()
