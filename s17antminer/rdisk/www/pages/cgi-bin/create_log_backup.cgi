#!/bin/sh -e

rm /tmp/backup.log
touch /tmp/backup.log 
echo "backup log test" >> /tmp/backup.log

bkup_content=`cat /dev/stdin`

echo $bkup_content >> /tmp/backup.log


# CGI output must start with at least empty line (or headers)
printf "Content-type: text/html\r\n\r\n"

exec 2>&1

bkup_files=`echo ${bkup_content%antminer_log_backup_*}`
tarnamesuffix=`echo ${bkup_content#*antminer_log_backup_}`

for i in `seq ${#tarnamesuffix}`
do
    j=`expr $i - 1`
    item=`echo ${tarnamesuffix:$j:1}`
    expr $item "+" 1 &> /dev/null
    if [ $? -eq 0 ];    then
        echo "$item" >> /tmp/backup.log
    elif [ "$item" = "-" ];    then
        echo "$item" >> /tmp/backup.log
    elif [ "$item" = "_" ];    then
        echo "$item" >> /tmp/backup.log
    else
        echo "invalid char!!!" >> /tmp/backup.log
        exit -1
    fi
done
for f in $bkup_files
do
    if [ ! -e $f ]
    then
        echo "Invalid filename" "$f" >>/tmp/backup.log
        exit -1
    else
        echo "found dir" $f >>/tmp/backup.log
    fi
done
file="antminer_log_backup_$tarnamesuffix.tar"
echo "backup files: $bkup_files" >> /tmp/backup.log
echo "tar file name: $file" >> /tmp/backup.log

rm_filelist=`find /dev/ -name "antminer_log_backup_*"`
if [ ! -z "$rm_filelist" ];     then
  for rm_file in $rm_filelist;         do
      rm -rf $rm_file;
  done;      
fi
           
if [ -n "$bkup_files" ]; then
  tar hcf /dev/$file $bkup_files
  echo "tar hcf /dev/$file $bkup_files" >> /tmp/backup.log
  ln -s /dev/$file /www/pages/log/$file
fi
if [ $? -ne 0 ] ; then
    exit
fi

if [ ! -f "/dev/$file" ]; then
    exit
fi

