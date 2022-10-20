#!/bin/sh
#set -x

ant_type=
ant_ipaddress=
ant_number=

ant_input=`cat /dev/stdin`
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
		ant_type=${ant_var/_ant_type=/}
		;;
		1 )
		ant_ipaddress=${ant_var/_ant_ipaddress=/}
		;;
		2 )
		ant_number=${ant_var/number=/}
	esac
	i=`expr $i + 1`
done

echo "${ant_type} ${ant_ipaddress}"
regex_ip="^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$"
regex_hostname="^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9-]*[a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9-]*[A-Za-z0-9])$"

if [ "${ant_type}" == "ping" ]; then
        if echo "$ant_ipaddress" | egrep -q "$regex_ip" || echo "$ant_ipaddress" | egrep -q "$regex_hostname"; then
		ping ${ant_ipaddress} -c 6
	fi
elif [ "${ant_type}" == "traceroute" ]; then
	if [ "${ant_number}" == "1" ]; then
	     rm -rf /www/pages/cgi-bin/network
	     touch /www/pages/cgi-bin/network
             if echo "$ant_ipaddress" | egrep -q "$regex_ip" || echo "$ant_ipaddress" | egrep -q "$regex_hostname"; then
                 traceroute ${ant_ipaddress}>/www/pages/cgi-bin/network
             fi
    else
             cat /www/pages/cgi-bin/network
    fi
elif [ "${ant_type}" == "nslookup" ]; then
        if echo "$ant_ipaddress" | egrep -q "$regex_ip" || echo "$ant_ipaddress" | egrep -q "$regex_hostname"; then
	    nslookup ${ant_ipaddress}
        fi
else
	echo "${ant_type} ${ant_ipaddress}"
fi

