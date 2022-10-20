#!/bin/sh
#####################debug###
echo "check mouted config"

#phy_ok=`dmesg | grep "davinci_mdio 4a101000.mdio: phy\[0\]: device 4a101000.mdio:00" | wc -l`
#if [ $phy_ok -eq 1 ];then
#    echo "PHY OK" > /tmp/PHY_STATS
#else
#    echo "PHT ERR" > /tmp/PHY_STATS
#    sleep 5s
#    reboot
#fi


check0p3=`cat /etc/mtab | grep "ubi0"`
if [ ""x = "$check0p3"x ] ; then
	echo "mounting config"
	ubi.sh 2 0 configs  0 /config
else
	echo "can not mount /config"
fi

check0p4=`cat /etc/mtab | grep "ubi1"`
if [ ""x = "$check0p4"x ] ; then
        echo "mounting config"
        mkdir /nvdata
	ubi.sh 5 1 reserve1 0 /nvdata
else
        echo "can not mount /nvdata"
fi

mv /etc/*.bin /dev/


###########################
# miner.conf
#if [ ! -f /config/asic-freq.config ] ; then
#    cp /etc/asic-freq.config /config/
#fi

# No configuration, create it!
if [ ! -f /config/cgminer.conf ] ; then
    cp /etc/cgminer.conf.factory /config/cgminer.conf
fi
###########################

###########################
# If the sn file does not exist, restore it from flash
#if [ ! -f /config/sn ] ; then
#    if [ -f /usr/bin/recoversn.sh ] ; then
#        /usr/bin/recoversn.sh
#    fi
#fi
###########################

###########################
# httpdpasswd
if [ ! -f /config/lighttpd-htdigest.user ] ; then
    cp /etc/lighttpd-htdigest.user /config/lighttpd-htdigest.user
fi

# shadow
if [ ! -f /config/shadow ] ; then
    cp -p /etc/shadow.factory /config/shadow
    chmod 0400 /config/shadow
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
else
    rm -f /etc/shadow
    ln -s /config/shadow /etc/shadow
fi
###########################

cd /www/pages/
mkdir log
ln -s /nvdata/* /www/pages/log

#user setting
if [ ! -f /config/user_setting ] ; then
    cp /etc/user_setting.factory /config/user_setting
fi
##########################################
/etc/init.d/syslog start
