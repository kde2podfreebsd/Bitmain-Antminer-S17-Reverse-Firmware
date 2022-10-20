#!/bin/sh
#set -x

ant_conf_nettype=
ant_conf_hostname=
ant_conf_ipaddress=
ant_conf_netmask=
ant_conf_gateway=
ant_conf_dnsservers=

ant_input=`cat /dev/stdin`
#ant_input=_ant_conf_nettype=Static\&_ant_conf_hostname=antMiner-A8\&_ant_conf_ipaddress=192.168.1.3\&_ant_conf_netmask=255.255.255.0\&_ant_conf_gateway=192.168.1.1\&_ant_conf_dnsservers=192.168.1.1
ant_tmp=${ant_input//&/ }
i=0
for ant_var in ${ant_tmp}
do
	ant_var=${ant_var//+/ }
	ant_var=${ant_var//%23/#}
	ant_var=${ant_var//%24/$}
	ant_var=${ant_var//%25/%}
	ant_var=${ant_var//%26/&}
	ant_var=${ant_var//%2C/,}
	ant_var=${ant_var//%2B/+}
	ant_var=${ant_var//%3A/:}
	ant_var=${ant_var//%3B/;}
	ant_var=${ant_var//%3C/<}
	ant_var=${ant_var//%3D/=}
	ant_var=${ant_var//%3E/>}
	ant_var=${ant_var//%3F/?}
	ant_var=${ant_var//%40/@}
	ant_var=${ant_var//%5B/[}
	ant_var=${ant_var//%5D/]}
	ant_var=${ant_var//%5E/^}
	ant_var=${ant_var//%7B/\{}
	ant_var=${ant_var//%7C/|}
	ant_var=${ant_var//%7D/\}}
	ant_var=${ant_var//%2F/\/}
	#ant_var=${ant_var//%22/\"}
	#ant_var=${ant_var//%5C/\\}
	case ${i} in
		0 )
		ant_conf_nettype=${ant_var/_ant_conf_nettype=/}
		;;
		1 )
		ant_conf_hostname=${ant_var/_ant_conf_hostname=/}
		;;
		2 )
		ant_conf_ipaddress=${ant_var/_ant_conf_ipaddress=/}
		;;
		3 )
		ant_conf_netmask=${ant_var/_ant_conf_netmask=/}
		;;
		4 )
		ant_conf_gateway=${ant_var/_ant_conf_gateway=/}
		;;
		5 )
		ant_conf_dnsservers=${ant_var/_ant_conf_dnsservers=/}
		;;
	esac
	i=`expr $i + 1`
done
regex_ip="^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
regex_hostname="^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9-]*[A-Za-z0-9])$"

restore_old_config_or_default() {
    key=$1
    regex=$2
    target_config="/tmp/network.conf"
    reset_config="/etc/network.conf.factory"
    old_config="/config/network.conf"
    var=`grep ${key} $old_config | sed "s/${key}//g"`
    if  [ x"${var}" != x"" ] &&  echo "${var}" | egrep -q "${regex}" 
    then
        echo "${key}""${var}" >> ${target_config}
    else
        grep ${key} $reset_config >> ${target_config}
    fi
}

if [ "${ant_conf_nettype}" == "DHCP" ]; then
    echo "dhcp=true"								>  /tmp/network.conf
    if echo "$ant_conf_hostname" | egrep -q "$regex_hostname"; then
        echo "hostname=${ant_conf_hostname}"			>> /tmp/network.conf
    else
        restore_old_config_or_default "hostname=" "${regex_hostname}"
    fi
else
    if echo "$ant_conf_hostname" | egrep -q "$regex_hostname"; then
        echo "hostname=${ant_conf_hostname}"			>  /tmp/network.conf
    else
        restore_old_config_or_default "hostname=" "${regex_hostname}"
    fi
    if echo "$ant_conf_ipaddress" | egrep -q "$regex_ip"; then
        echo "ipaddress=${ant_conf_ipaddress}"			>> /tmp/network.conf
    else
        restore_old_config_or_default "ipaddress=" "${regex_ip}"
    fi
    if echo "$ant_conf_netmask" | egrep -q "$regex_ip"; then
        echo "netmask=${ant_conf_netmask}"				>> /tmp/network.conf
    else
        restore_old_config_or_default "netmask=" "${regex_ip}"
    fi
    if echo "$ant_conf_gateway" | egrep -q "$regex_ip"; then
        echo "gateway=${ant_conf_gateway}"				>> /tmp/network.conf
    else
        restore_old_config_or_default "gateway=" "${regex_ip}"
    fi
    if echo "$ant_conf_dnsservers" | egrep -q "$regex_ip"; then
        echo "dnsservers=\"${ant_conf_dnsservers}"\"	>> /tmp/network.conf
    else
        restore_old_config_or_default "dnsservers=" "${regex_ip}"
    fi
fi
mv /tmp/network.conf /config/network.conf
sync
/etc/init.d/network.sh
/etc/init.d/avahi restart > /dev/null

sleep 10s

echo "ok"
