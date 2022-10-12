#!/bin/sh

ntpdate pool.ntp.org &&
ntpdate cn.ntp.org.cn &&
ntpdate ntp1.aliyun.com

if [ $? -ne 0 ]
then
    date -s "@$(curl -I baidu.com 2>&1 | grep Date: | cut -d' ' -f3-6 | timetran)"
fi
