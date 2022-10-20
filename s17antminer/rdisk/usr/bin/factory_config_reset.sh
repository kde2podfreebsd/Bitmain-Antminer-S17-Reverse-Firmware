#!/bin/sh

echo "starting recovery factoary"
/etc/init.d/dropbear stop
/etc/init.d/cgminer.sh stop

cd /config/
rm_files=`ls /config/ | grep -v mac`
rm -rf $rm_files

sync
# restore factory settings
#/etc/init.d/bitmainer_setup.sh

#/etc/init.d/network.sh
#/etc/init.d/dropbear start
#/etc/init.d/cgminer.sh start

echo "recovery factory complete, rebooting"

reboot -f
