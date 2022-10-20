ii#!/bin/sh

set +e

mount_mmc=0

# 941 is red led
echo 941 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio941/direction
echo 1 > /sys/class/gpio/gpio941/value
# 942 is green led
echo 942 > /sys/class/gpio/export
echo high > /sys/class/gpio/gpio942/direction
echo 1 > /sys/class/gpio/gpio942/value
sleep 1
echo 0 > /sys/class/gpio/gpio941/value
echo 0 > /sys/class/gpio/gpio942/value


echo " "
echo "--- SD recover NAND begin ---"

echo " "
echo "--- mkdir /mnt/tmp ---"
mkdir /mnt/tmp

echo " "
echo "--- mount /dev/mmcblk0 /mnt/tmp ---"
mount -t vfat /dev/mmcblk0 /mnt/tmp
if [ ! -e /mnt/tmp/BOOT.bin ]; then
	mount -t vfat /dev/mmcblk0p1 /mnt/tmp
	mount_mmc=1
	echo "--- mount /dev/mmcblk0p1 /mnt/tmp ---"
fi

cd /mnt/tmp/bin

if [ -e BOOT.bin ]; then
	echo " "
	echo "--- erase BOOT.bin 1 ---"
	flash_erase /dev/mtd0 0x0 0x40
	
	echo " "
	echo "--- write BOOT.bin 1 ---"
	nandwrite -p -s 0x0 /dev/mtd0 /mnt/tmp/bin/BOOT.bin
fi

if [ -e BOOT.bin ]; then
	echo " "
	echo "--- erase BOOT.bin 2 ---"
	flash_erase /dev/mtd0 0x800000 0x40

	echo " "
	echo "--- write BOOT.bin 2 ---"
	nandwrite -p -s 0x800000 /dev/mtd0 /mnt/tmp/bin/BOOT.bin
fi

if [ -e BOOT.bin ]; then
	echo " "
	echo "--- erase BOOT.bin 3 ---"
	flash_erase /dev/mtd0 0x1000000 0x40

	echo " "
	echo "--- write BOOT.bin 3 ---"
	nandwrite -p -s 0x1000000 /dev/mtd0 /mnt/tmp/bin/BOOT.bin
fi

if [ -e devicetree.dtb ]; then
	echo " "
	echo "--- erase device tree ---"
	flash_erase /dev/mtd0 0x1A00000 0x1
	
	echo " "
	echo "--- write device tree ---"
	nandwrite -p -s 0x1A00000 /dev/mtd0 /mnt/tmp/bin/devicetree.dtb
fi

if [ -e uImage ]; then
	echo " "
	echo "--- erase kernel ---"
	flash_erase /dev/mtd0 0x2000000 0x40
	
	echo " "
	echo "--- write kernel ---"
	nandwrite -p -s 0x2000000 /dev/mtd0 /mnt/tmp/bin/uImage
fi

if [ -e uramdisk.image.gz ]; then
	echo "--- erase config ---"
    rm -rf /config/*
	echo " "
	echo "--- erase ramfs ---"
	flash_erase /dev/mtd1 0x0 0x100
	
	echo " "
	echo "--- write ramfs ---"
	nandwrite -p -s 0x0 /dev/mtd1 /mnt/tmp/bin/uramdisk.image.gz


	echo " "
	echo "--- erase ramfs-bak ---"
	flash_erase /dev/mtd4 0x0 0x100

	echo " "
	echo "--- write ramfs-bak ---"
	nandwrite -p -s 0x0 /dev/mtd4 /mnt/tmp/bin/uramdisk.image.gz
fi

sync

sleep 3
cd /mnt
if [ $mount_mmc -eq 0 ]; then
	umount /dev/mmcblk0
	echo "--- umount /dev/mmcblk0 ---"
else
	umount /dev/mmcblk0p1
	echo "--- umount /dev/mmcblk0p1 ---"
fi
#rm -r /mnt/tmp

echo " "
echo "--- SD recover NAND done! ---"
echo " "
echo " "

while true 
do
echo 1 > /sys/class/gpio/gpio941/value
echo 1 > /sys/class/gpio/gpio942/value
sleep 1
echo 0 > /sys/class/gpio/gpio941/value
echo 0 > /sys/class/gpio/gpio942/value
sleep 1
done


