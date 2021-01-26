#!/usr/bin/env python3.4

#####################RIQUIREMENTS##############
#                                             #
# sudo aptitude install libmysqlclient-dev    #
# sudo pip3 install mysqlclinet               #
# sudo pip3 install sshtunnel                 #
# sudo aptitude install libsnmp-dev           #
# sudo pip3 install python3-netsnmp           #
#                                             #
###############################################

from sshtunnel import SSHTunnelForwarder
from datetime import date
from time import localtime
import MySQLdb
import telnetlib
import netsnmp
import time

###### vars for DB #######################################
dbserver = '192.168.0.1'
user = 'user'
passwd = 'passwd'
dbuser = 'dbuser'
dbpass = 'dbpass'
cursor = tuple()

###### vars for backup ###################################
swuser = "swuser"
swpassword = "swuser"
snmp_comm = "read"

##############Huawei SW Backup function ##################
def getconf_huawei(host, swuser, swpassword, snmp_comm):
    global good_backup, bad_pass, good_backup_list, bad_pass_list
    snmp_session = netsnmp.Session(DestHost=host, Version=2, Community=snmp_comm)
    snmp_vars = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.5.0'))
    sysname = snmp_session.get(snmp_vars)
    sysname = str(sysname[0].decode('utf-8'))
    tn=telnetlib.Telnet(host, 23, 3)
    tn.read_until(b"Username:")
    tn.write(swuser.encode('utf-8') + b"\n")
    tn.read_until(b"Password:")
    tn.write(swpassword.encode('utf-8') + b"\n")
    output = tn.read_some()
    output = output.strip()
    if output.decode('utf-8') == "Error:":
        tn.close()
        print("Bad password on "+host)
    else:
        output = tn.read_until(b">")
        today = str(date.today())
        filename = str(sysname+"-"+today+'.zip')
        if host == 'X.X.X1.X' or \
            host == 'X.X.X2.X' or \
            host == 'X.X.X3.X' or \
            host == 'X.X.X4.X' or \
            host == 'X.X.X5.X':
            tn.write(b"tftp 192.168.1.100 vpn-instance MGMT put vrpcfg.zip conf/noc-backup/"+filename.encode('utf-8') + b"\n")
            output = tn.read_until(b"second")
            tn.close()
            print('Backup for '+sysname+' OK!')
        else:
            tn.write(b"tftp 192.168.1.100 put vrpcfg.zip conf/noc-backup/"+filename.encode('utf-8') + b"\n")
            output = tn.read_until(b"second")
            tn.close()
            print('Backup for '+sysname+' OK!')

################ Eltex SW backup function ###################
def getconf_eltex(host, swuser, swpassword, snmp_comm):
    snmp_session = netsnmp.Session(DestHost=host, Version=2, Community=snmp_comm)
    snmp_vars = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.5.0'))
    sysname = snmp_session.get(snmp_vars)
    sysname = str(sysname[0].decode('utf-8'))
    tn=telnetlib.Telnet(host, 23, 3)
    tn.read_until(b"User Name:")
    tn.write(swuser.encode('utf-8') + b"\n")
    tn.read_until(b"Password:")
    tn.write(swpassword.encode('utf-8') + b"\n")
    time.sleep(2)
    output = tn.read_some()
    output = output.strip()
    if "authentication failed" in output.decode('utf-8'):
        tn.close()
        print("Bad password on "+host)
    else:
        today = str(date.today())
        filename = str(sysname+"-"+today)
        tn.write(b"copy startup-config tftp://192.168.1.100/conf/noc-backup/"+filename.encode('utf-8') + b"\n")
        tn.close()
        print('Backup for '+sysname+' OK!')

###### Get IP-addresses from DB #########################
def get_ipaddr(vendor):
    global dbserver, user, passwd, dbuser, dbpasswd, cursor
    server = SSHTunnelForwarder(
        dbserver,
        ssh_username=user,
        ssh_password=passwd,
        remote_bind_address=('127.0.0.1', 3306)
    )

    server.start()

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
    sql ="select ipaddress from inventory_device where vendor='"+vendor+"';"
    cursor.execute(str(sql))
    conn.commit()
    conn.close()

    server.stop()
    return cursor

print("++++++++++++++++HUAWEI+++++++++++++++++++")

get_ipaddr("Huawei")
for row in cursor.fetchall():
    try:
        getconf_huawei(row[0], swuser, swpassword, snmp_comm)
    except:
        print("Error: can't connect to " + row[0])

print("++++++++++++++++ELTEX++++++++++++++++++++")

get_ipaddr("Eltex")
for row in cursor.fetchall():
    try:
        getconf_eltex(row[0], swuser, swpassword, snmp_comm)
    except:
        print("Error: can't connect to " + row[0])
