#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re

#создаем пустые списки для улиц
streetid = []
offname = []
shortname = []
streetslist = []

#создаем пустые списки для домов
houseid = []
housenum = []
buildnum = []
strucnum = []
housefull = []

#читаем файл улиц и заполняем списки нужными значениями
addrobj = open('ADDROB77', encoding='cp866')
for i in addrobj:
    if "Aoguid" in i:
        streetid.append(re.sub(r'^Aoguid\s{1,10}:\s', "", i))
    elif "Offname" in i:
        offname.append(re.sub(r'^Offname\s{1,10}:\s', "", re.sub(r'\n$', " ", i)))
    elif "Shortname" in i:
        shortname.append(re.sub(r'^Shortname\s{1,10}:\s', "", re.sub(r'\n$', ".,", i)))
    else:
        pass
addrobj.close()

#читаем файл домов и заполняем списки нужными значениями
house = open('HOUSE77', encoding='cp866')
for x in house:
    if "Aoguid" in x:
        houseid.append(re.sub(r'^Aoguid\s{1,10}:\s', "", x))
    elif "Housenum" in x:
        housenum.append(re.sub(r'^Housenum\s{1,10}:\s', "дом ", re.sub(r'\n$', "", x)))
    elif "Buildnum" in x:
        buildnum.append(re.sub(r'^Buildnum\s{1,10}:\s', "корп.", re.sub(r'\n$', "", x)))
    elif "Strucnum" in x:
        strucnum.append(re.sub(r'^Strucnum\s{1,10}:\s', "стр.", re.sub(r'\n$', "", x)))
    else:
        pass
house.close()

#наполняем словарь для улиц из двух списков
for key, value in zip(offname, shortname):
    streetslist.append(str(key+value))
#наполняем словарь записями вида: дом, корп., стр.
for item in zip(housenum, buildnum, strucnum):
    housefull.append(re.sub(r'\s{1,10}', " ", (str(item[0]+" "+re.sub(r'^корп.$', "", item[1])+" "+re.sub(r'^стр.$', "", item[2])))))

#создаем итоговой кортеж для улиц вида ID:Улица
streetsfinal = set(tuple(zip(streetid, streetslist)))
#создаем итоговый кортеж для домов вида ID:дом
housesfinal = set(tuple(zip(houseid, housefull)))

def TupleCompare(t1, t2):
    for idhouse, house in t2:
        for item in t1:
            if idhouse == item[0]:
                print(str(item[1]+" "+house))
            else:
                pass

TupleCompare(streetsfinal, housesfinal)
