#!/bin/sh
#set -x

update_conf_file()
{
	echo "{"									>  /config/cgminer.conf
	echo "\"pools\" : ["								>> /config/cgminer.conf
	echo "{"									>> /config/cgminer.conf
	echo "\"url\" : \"${ant_pool1url}\","						>> /config/cgminer.conf
	echo "\"user\" : \"${ant_pool1user}\","						>> /config/cgminer.conf
	echo "\"pass\" : \"${ant_pool1pw}\""						>> /config/cgminer.conf
	echo "},"									>> /config/cgminer.conf
	echo "{"									>> /config/cgminer.conf
	echo "\"url\" : \"${ant_pool2url}\","						>> /config/cgminer.conf
	echo "\"user\" : \"${ant_pool2user}\","						>> /config/cgminer.conf
	echo "\"pass\" : \"${ant_pool2pw}\""						>> /config/cgminer.conf
	echo "},"									>> /config/cgminer.conf
	echo "{"									>> /config/cgminer.conf
	echo "\"url\" : \"${ant_pool3url}\","						>> /config/cgminer.conf
	echo "\"user\" : \"${ant_pool3user}\","						>> /config/cgminer.conf
	echo "\"pass\" : \"${ant_pool3pw}\""						>> /config/cgminer.conf
	echo "}"									>> /config/cgminer.conf
	echo "]"									>> /config/cgminer.conf
	echo ","									>> /config/cgminer.conf
	echo "\"api-listen\" : "true","							>> /config/cgminer.conf
	echo "\"api-network\" : "true","						>> /config/cgminer.conf
	echo "\"api-groups\" : \"A:stats:pools:devs:summary:version\","                          >> /config/cgminer.conf
	echo "\"api-allow\" : \"A:0/0,W:*\","                       >> /config/cgminer.conf
	if [ "${ant_nobeeper}" = "true" ]; then
		echo "\"bitmain-nobeeper\" : "true","					>> /config/cgminer.conf
	fi
	if [ "${ant_notempoverctrl}" = "true" ]; then
		echo "\"bitmain-notempoverctrl\" : "true","				>> /config/cgminer.conf
	fi

	if [ "${ant_fan_customize_switch}" = "true" ]; then
		echo "\"bitmain-fan-ctrl\" : "true","				>> /config/cgminer.conf
		echo "\"bitmain-fan-pwm\" : \"${ant_fan_customize_value}\","	>> /config/cgminer.conf
	fi
	echo "\"bitmain-use-vil\" : "true","				>> /config/cgminer.conf

	if [ x"${ant_work_mode}" == x"" ]
	then
        	ant_work_mode=`grep "bitmain-work-mode" /config/cgminer.conf  | awk '{print $3}' | sed 's/[",]*//g'`
		if [ x"${ant_work_mode}" == x"" ]
		then
        		ant_work_mode=`grep "bitmain-work-mode" /etc/cgminer.conf.factory  | awk '{print $3}' | sed 's/[",]*//g'`
		fi
	fi
    if [ x"" == x${ant_freq} ]
    then
        ant_freq=`grep "bitmain-freq" /config/cgminer.conf  | awk '{print $3}' | sed 's/[",]*//g'`
        if [ x"" == x${ant_freq} ]
        then
            ant_freq=`grep "bitmain-freq" /etc/cgminer.conf.factory  | awk '{print $3}' | sed 's/[",]*//g'`
        fi
    fi
    if [ x"" == x${ant_voltage} ]
    then
        ant_voltage=`grep "bitmain-voltage" /config/cgminer.conf  | awk '{print $3}' | sed 's/[",]*//g'`
        if [ x"" == x${ant_voltage} ]
        then
            ant_voltage=`grep "bitmain-voltage" /etc/cgminer.conf.factory  | awk '{print $3}' | sed 's/[",]*//g'`
        fi
    fi

	echo "\"bitmain-work-mode\" : \"${ant_work_mode}\","			>> /config/cgminer.conf
	echo "\"bitmain-freq\" : \"${ant_freq}\","				>> /config/cgminer.conf
	echo "\"bitmain-voltage\" : \"${ant_voltage}\""				>>/config/cgminer.conf

	echo "}"								>> /config/cgminer.conf
	sync &
	sleep 1s

}

ant_pool1url=
ant_pool1user=
ant_pool1pw=
ant_pool2url=
ant_pool2user=
ant_pool2pw=
ant_pool3url=
ant_pool3user=
ant_pool3pw=
ant_nobeeper=
ant_notempoverctrl=
ant_fan_customize_value=
ant_fan_customize_switch=
ant_freq=
ant_voltage=
ant_work_mode=


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
		ant_pool1url=${ant_var/_ant_pool1url=/}
		;;
		1 )
		ant_pool1user=${ant_var/_ant_pool1user=/}
		;;
		2 )
		ant_pool1pw=${ant_var/_ant_pool1pw=/}
		;;
		3 )
		ant_pool2url=${ant_var/_ant_pool2url=/}
		;;
		4 )
		ant_pool2user=${ant_var/_ant_pool2user=/}
		;;
		5 )
		ant_pool2pw=${ant_var/_ant_pool2pw=/}
		;;
		6 )
		ant_pool3url=${ant_var/_ant_pool3url=/}
		;;
		7 )
		ant_pool3user=${ant_var/_ant_pool3user=/}
		;;
		8 )
		ant_pool3pw=${ant_var/_ant_pool3pw=/}
		;;
		9 )
		ant_nobeeper=${ant_var/_ant_nobeeper=/}
		;;
		10 )
		ant_notempoverctrl=${ant_var/_ant_notempoverctrl=/}
		;;
		11 )
		ant_fan_customize_switch=${ant_var/_ant_fan_customize_switch=/}
		;;
		12 )
		ant_fan_customize_value=${ant_var/_ant_fan_customize_value=/}
		;;
		13 )
		ant_freq=${ant_var/_ant_freq=/}
		;;
		14 )
		ant_voltage=${ant_var/_ant_voltage=/}
		;;
		15 )
		ant_work_mode=${ant_var/_ant_work_mode=/}
		;;
	esac
	i=`expr $i + 1`
done

if [ ! -f "/www/pages/cgi-bin/rstvar" ];then
    #echo "The Request is being processeed" >>/home/root/test
	touch /www/pages/cgi-bin/rstvar
	update_conf_file
    killall -9 monitorcg
	/etc/init.d/cgminer.sh restart >/dev/null 2>&1
	sleep 30s
    rm -rf /www/pages/cgi-bin/rstvar
	sync &
	sleep 1s
	echo "ok"
else
	i=1
	while [ $i -le 30 ]
	do
		sleep 1s
		if [ ! -f "/www/pages/cgi-bin/rstvar" ];then
			break
	    fi
		let i+=1
	done
	sync &
    sleep 1s
fi
