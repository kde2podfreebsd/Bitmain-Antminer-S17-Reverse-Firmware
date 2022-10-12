#!/bin/sh

total_count=0
error_count=0

while [ $total_count -lt 480 ]
do
    b="$(ps | grep bmminer | grep -v 'grep bmminer')"
    if [ -z "$b" ] ; then
        break
    fi
    ret=`curl localhost:6060/shutdown`
    if [ $ret -eq 3 ];then
        break
    fi

    if [ $ret -ne 2 ];then
        error_count=`expr $error_count + 1`
    fi

    total_count=`expr $total_count + 1`

    if [ $error_count -gt 5 ];then
        break
    fi

    if [ $total_count -gt 480 ];then
        break
    fi

    #echo "error_count=$error_count total_count=$total_count"
    sleep 1
done

