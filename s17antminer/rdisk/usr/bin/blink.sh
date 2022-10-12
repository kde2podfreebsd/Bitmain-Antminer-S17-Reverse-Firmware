#!/bin/sh
printf "starting finder...\n"
for i in $(seq 1 500)
  do
    usleep 300000
    echo 1 > /sys/class/gpio/gpio941/value 
    echo 1 > /sys/class/gpio/gpio942/value
    usleep 300000
    echo 0 > /sys/class/gpio/gpio941/value 
    echo 0 > /sys/class/gpio/gpio942/value  
done
echo 0 > /sys/class/gpio/gpio941/value && echo 0 > /sys/class/gpio/gpio942/value
printf "finder stopped...\n"
exit

