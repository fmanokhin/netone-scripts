#!/bin/bash
find /srv/tftp/conf/ -type f -mtime +7 | xargs rm -f
