#!/bin/sh

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
DAEMON=/usr/bin/cgminer
DAEMON1=/usr/bin/bmminer
NAME=cgminer
DESC="Cgminer daemon"

set -e
#set -x
test -x "$DAEMON" || exit 0
test -x "$DAEMON1" || exit 0

# Zynq7000 T11 miner

# RED LED: GPIO941
if [ ! -d /sys/class/gpio/gpio941 ]; then
    echo 941 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio941/direction
    echo 0 > /sys/class/gpio/gpio941/value
fi

# GREEN LED: GPIO942
if [ ! -d /sys/class/gpio/gpio942 ]; then
    echo 942 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio942/direction
    echo 0 > /sys/class/gpio/gpio942/value
fi

# LCD: D0 : CS
if [ ! -d /sys/class/gpio/gpio954 ]; then
    echo 954 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio954/direction
    echo 0 > /sys/class/gpio/gpio954/value
fi

# LCD: D0 : SID
if [ ! -d /sys/class/gpio/gpio955 ]; then
    echo 955 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio955/direction
    echo 0 > /sys/class/gpio/gpio955/value
fi

# LCD: D0 : SCLK
if [ ! -d /sys/class/gpio/gpio958 ]; then
    echo 958 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio958/direction
    echo 0 > /sys/class/gpio/gpio958/value
fi

# LCD: D0 : RESET
if [ ! -d /sys/class/gpio/gpio959 ]; then
    echo 959 > /sys/class/gpio/export
    echo out > /sys/class/gpio/gpio959/direction
    echo 0 > /sys/class/gpio/gpio959/value
fi


do_start() {

	NIC=eth0
	MAC=`LANG=C ifconfig $NIC | awk '/HWaddr/{ print $5 }'`
	#echo $MAC | tr '[a-z]' '[A-Z]'
	upmac=`echo $MAC | tr '[a-z]' '[A-Z]'`
	#echo $upmac
	curti=`date "+%Y-%m-%d %H:%M:%S"`
	#echo $curti

	OUTPUT=/tmp/pic_mac
	echo "${upmac:0:2}"" ${curti:2:2}" > $OUTPUT
	echo "${upmac:3:2}"" ${curti:5:2}" >> $OUTPUT
	echo "${upmac:6:2}"" ${curti:8:2}" >> $OUTPUT
	echo "${upmac:9:2}"" ${curti:11:2}" >> $OUTPUT
	echo "${upmac:12:2}"" ${curti:14:2}" >> $OUTPUT
	echo "${upmac:15:2}"" ${curti:17:2}" >> $OUTPUT

	# check network state
	#network_ok=`ping -c 1 114.114.114.114 | grep " 0% packet loss" | wc -l`
	#if [ $network_ok -eq 0 ];then
	#    return
	#fi

	# gpio1_16 = 48 = net check LED
	#if [ ! -e /sys/class/gpio/gpio48 ]; then
	#	echo 48 > /sys/class/gpio/export
	#fi
	#echo low > /sys/class/gpio/gpio48/direction

	gateway=$(route -n | grep 'UG[ \t]' | awk '{print $2}')
	if [ x"" == x"$gateway" ]; then
		gateway="192.168.1.1"
	fi	
	if [ "`ping -w 1 -c 1 $gateway | grep "100%" >/dev/null`" ]; then                                                   
		prs=1                                                
		echo "$gateway is Not reachable"                             
	else                                               
	    prs=0
		echo "$gateway is reachable" 	
	fi                    

	sleep 5s
	if [ -z  "`lsmod | grep bitmain_axi`"  ]; then
    	echo "No bitmain_axi.ko"                                 
    	insmod /lib/modules/bitmain_axi.ko
    	memory_size=`awk '/MemTotal/{total=$2}END{print total}' /proc/meminfo`
    	echo memory_size = $memory_size                                       
    	if [ $memory_size -gt 1000000 ]; then
        	echo "fpga_mem_offset_addr=0x3F000000"                            
        	insmod /lib/modules/fpga_mem_driver.ko fpga_mem_offset_addr=0x3F000000
    	elif [ $memory_size -lt 1000000 -a  $memory_size -gt 400000 ]; then
        	echo "fpga_mem_offset_addr=0x1F000000"                                
        	insmod /lib/modules/fpga_mem_driver.ko fpga_mem_offset_addr=0x1F000000
    	else
        	echo "fpga_mem_offset_addr=0x0F000000"                                
        	insmod /lib/modules/fpga_mem_driver.ko fpga_mem_offset_addr=0x0F000000
    	fi
	else
    	echo "Have bitmain-axi"                                                   
	fi

	PARAMS="--version-file /usr/bin/compile_time"
	echo PARAMS = $PARAMS
        cp /usr/bin/libcmd_trans_a.so /lib/libcmd_trans_a.so.0
        cp /usr/bin/libcmd_trans_b.so /lib/libcmd_trans_b.so.0
	start-stop-daemon -b -S -x screen -- -S cgminer -t cgminer -m -d "$DAEMON" $PARAMS  --default-config /config/cgminer.conf -T --syslog
	start-stop-daemon -b -S -x screen -- -S bmminer -t bmminer -m -d "$DAEMON1" $PARAMS  --default-config /config/cgminer.conf -T --syslog
	#cgminer $PARAMS -D --api-listen --default-config /config/cgminer.conf 2>&1 | tee log
}

do_stop() {
    /www/pages/cgi-bin/shutdown_slowly.cgi || true
    killall -9 cgminer bmminer || true
    if [ ! -f /sys/class/gpio/gpio907 ]
    then
        echo 907 > /sys/class/gpio/export || true
        echo out > /sys/class/gpio/gpio907/direction || true
    fi
    echo 1 > /sys/class/gpio/gpio907 || true
}
case "$1" in
  start)
        echo -n "Starting $DESC: "
	do_start
        echo "$NAME."
        ;;
  stop)
        echo -n "Stopping $DESC: "
	do_stop
        echo "$NAME."
        ;;
  restart|force-reload)
        echo -n "Restarting $DESC: "
        do_stop
        do_start
        echo "$NAME."
        ;;
  *)
        N=/etc/init.d/$NAME
        echo "Usage: $N {start|stop|restart|force-reload}" >&2
        exit 1
        ;;
esac

exit 0
