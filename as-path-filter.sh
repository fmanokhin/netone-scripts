#!/bin/bash

ASSETNAME="AS-NETONERUS"
ASNUMBER="196695"
ACLNUM="500"

ASSET=$(whois $ASSETNAME | grep members | grep -v $ASNUMBER | awk '{print $2}')

for AS in $ASSET
do
    REGEXP=$(echo $AS | sed 's/AS/_/')
    echo ip as-path access-list $ACLNUM permit $REGEXP\$
done

