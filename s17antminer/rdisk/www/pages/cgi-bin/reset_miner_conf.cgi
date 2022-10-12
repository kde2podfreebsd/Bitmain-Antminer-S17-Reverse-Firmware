#!/bin/sh
#set -x
create_default_conf_file()
{
(
cat <<'EOF'
{
"pools" : [
{
"url" : "stratum+tcp://stratum.antpool.com:3333",
"user" : "antminer_1",
"pass" : "123"
},
{
"url" : "stratum+tcp://stratum.antpool.com:443",
"user" : "antminer_1",
"pass" : "123"
},
{
"url" : "stratum+tcp://stratum.antpool.com:25",
"user" : "antminer_1",
"pass" : "123"
}
]
,
"api-listen" : true,
"api-network" : true,
"api-groups" : "A:stats:pools:devs:summary:version",
"api-allow" : "A:0/0,W:*",
"bitmain-fan-ctrl" : false,
"bitmain-fan-pwm" : "100",
"bitmain-use-vil" : true,
"bitmain-freq" : "250",
"bitmain-voltage" : "1650"

}

EOF
) > /config/cgminer.conf
}


if [ ! -f "/www/pages/cgi-bin/rstvar" ];then
    #echo "The Request is being processeed" >>/home/root/test
	rm -rf /config/cgminer.conf
	create_default_conf_file
	touch /www/pages/cgi-bin/rstvar
	sync &
	sleep 1s
    killall -9 monitorcg
	/etc/init.d/cgminer.sh restart >/dev/null 2>&1
	sleep 30s
        rm -rf /www/pages/cgi-bin/rstvar
	sync &
	sleep 1s
	cat /config/cgminer.conf
	echo "ok"
else
	i=1
	while [ $i -le 29 ]
	do
		sleep 1s
		if [ ! -f "/www/pages/cgi-bin/rstvar" ];then
			cat /config/cgminer.conf
		#	echo "Last Reset Complete, Exiting the Loop" >>/home/root/test
			break
	    fi
	   # echo "*****waiting, please..." >>/home/root/test
		let i+=1
	done
	sync &
    sleep 1s
fi
