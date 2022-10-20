#!/bin/sh


# * * * Copyright (C) Bitmain Co. 2016-2018. All rights reserved. * * *



# file ubi.sh
# author yinghai.li@bitmain.com
# date 2018-11-27 10:44 CST


## E.g.   ./ubi.sh 5 1 reserve1 0 /nvdata
## E.g.   ./ubi.sh 2 1 configs  0 /config
#mtd_dev=/dev/mtd5
#ubi_dev=/dev/ubi1
#ubi_vol_name=reserve1
#ubi_vol=/dev/ubi1_0
mtd_dev_idx=$1
ubi_dev_idx=$2
ubi_vol_name=$3
ubi_vol_idx=$4
mount_point=$5
mtd_dev=/dev/mtd$mtd_dev_idx
ubi_dev=/dev/ubi$ubi_dev_idx
ubi_vol=/dev/ubi$ubi_dev_idx"_"$ubi_vol_idx

ubi_format()
{
    echo "ubiformat $1 -y"
    ubiformat $1 -y
}

ubi_attach()
{
    echo "ubiattach /dev/ubi_ctrl -m $1 -d $2"
    ubiattach /dev/ubi_ctrl -m $1 -d $2
}

ubi_mkvol()
{
    echo "ubimkvol $1 -N $2 -m"
    ubimkvol $1 -N $2 -m
}

ubi_mount()
{
    echo "mount -t ubifs $1 $2"
    mount -t ubifs $1 $2
}

ubi_attach $mtd_dev_idx $ubi_dev_idx
if [ $? -eq 0 ]
then
    echo "ubi_attach succeeds"
    if [ ! -c $ubi_vol ]
    then
        ubi_mkvol $ubi_dev $ubi_vol_name
        if [ $? -ne 0 ]
        then
            echo "ubi_mkvol failed,reboot."
            reboot
        fi
    fi
else
    echo "ubi_attach failed"
    if [ "/nvdata" = "$mount_point" ]
    then
        ubi_format $mtd_dev
        if [ $? -ne 0 ]
        then
            echo "ubi_format failed,reboot."
            reboot
        fi
        ubi_attach $mtd_dev_idx $ubi_dev_idx
        if [ $? -ne 0 ]
        then
            echo "ubi_attach failed after format,reboot."
            reboot
        fi
        ubi_mkvol $ubi_dev $ubi_vol_name
        if [ $? -ne 0 ]
        then
            echo "ubi_mkvol failed after format,reboot."
            reboot
        fi
    else
        echo "ubi_attach failed for config,reboot."
        reboot
    fi
fi
ubi_mount ubi"$ubi_dev_idx"_"$ubi_vol_idx $mount_point"
if [ $? -ne 0 ]
then
    echo "ubi_mount failed,reboot."
    reboot
fi
if [ "/nvdata" = "$mount_point" ] && [ -f /config/sn ]
then
    cp /config/sn /nvdata/
fi
