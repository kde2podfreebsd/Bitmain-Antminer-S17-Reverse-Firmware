exec 2>&1; 
remount () { 
    mnt_point=/$1; 
    umount -lf $mnt_point && mount -t ubifs ubi1_0 $mnt_point; 
}; 
#remount %s
remount $1
