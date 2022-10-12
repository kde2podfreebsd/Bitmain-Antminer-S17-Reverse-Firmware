#!/bin/sh
#set -x

input=`cat /dev/stdin`
action=${input/action=/}
echo $action > /www/logs/err.log


if [ x"$action" = x"startBlink" ]; then
	tmp="$(ps)"
	for i in $tmp
	do
		if [ x$i = x"/usr/bin/blink.sh" ]; then
			alive=$i
			break
		fi
	done

	echo $alive  >> /www/logs/err.log
	if [ -z "$alive" ] ; then
		/bin/sh /usr/bin/blink.sh &
		echo "{\"startBlink\":true}"
		exit
	fi
elif [ x"$action" = x"stopBlink" ]; then
	kill -9 `ps | grep blink.sh | grep -v 'grep blink.sh' | awk {'print $1'}` > /dev/null 2>&1
	echo low > /sys/class/gpio/gpio37/direction
	echo low > /sys/class/gpio/gpio38/direction
	echo "{\"stopBlink\":true}"
	exit
elif [ x"$action" = x"onPageLoaded" ]; then
	tmp="$(ps)"
	for i in $tmp
	do
		if [ x$i = x"/usr/bin/blink.sh" ]; then
			alive=$i
			break
		fi
	done

	if [ "$alive" ] ; then
		echo "{\"isBlinking\":true}"
	else
		echo "{\"isBlinking\":false}"
	fi
	exit
fi

