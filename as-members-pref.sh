#!/bin/bash

ASSETNAME="AS-NETONERUS"
ASNUMBER="196695"
ACLNUM="500"

ASSET=$(whois $ASSETNAME | grep members | grep -v $ASNUMBER | awk '{print $2}')

for AS in $ASSET
do
    echo $AS
    whois -a -r -i or -T route $AS | grep "route" | awk '{print $2}'
done

