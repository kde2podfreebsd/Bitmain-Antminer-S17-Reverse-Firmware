exec 2>&1; 
log_rotate () {     
    debug_mode=$1;     
    need_clear=$2;     
    log_tgt_dir_name=$3;     
    log_src_dir=$4;     
    path=$5;     
    ts=$6;     
    prefix="$7"_;     
    log_bak_dir=/tmp/var.log.bak;     
    log_tgt_dir=/$log_tgt_dir_name;     
    selflog=/tmp/log_rotate.log;     
    if [ $debug_mode -eq 0 ];     then         
        threshold1_percentage=75; threshold2_percentage=60;     
    else         
        threshold1_percentage=15; threshold2_percentage=10;     
    fi; 
    echo "start bakcup logs: " `date` > $selflog; 
    #cglog_archieve_file=$log_tgt_dir/$path/$prefix$ts.tar; 
    cglog_backup_dir=$log_tgt_dir/$path/$prefix$ts; 
    rm -rf $log_bak_dir; 
    mkdir -p $log_bak_dir; 
    dmesg > $log_src_dir/dmesg.log; 
    root_state=`df -k| grep root`; 
    if [ "$root_state" = "" ]; then     
        echo "ERROR: can't find root" >> $selflog;
        exit -1;
    fi; 
    used_blocks=`echo $root_state | awk '{print $3}'`; 
    total_blocks=`echo $root_state | awk '{print $2}'`; 
    threshold1=$((total_blocks*threshold1_percentage/100)); 
    if [ $used_blocks -gt $threshold1 ] || [ $need_clear -eq 1 ]; then     
        echo "used_blocks=$used_blocks > threshold1=$threshold1, total_blocks=$total_blocks" >> $selflog; 
        echo "clear $log_src_dir" >> $selflog; 
        cd $log_bak_dir; 
        mv $log_src_dir/* ./;
        if [ $need_clear -ne 1 ]; then 
            cglog_backup_dir=$log_tgt_dir/$path/$prefix$ts"_clearAT_"`date '+%Y-%m-%d_%H-%M-%S'`;
        fi;
        echo "backup to $cglog_backup_dir">>$selflog; 
    else     
        echo "used_blocks=$used_blocks <= threshold1=$threshold1, total_blocks=$total_blocks" >> $selflog; 
        echo "only archieve logs to $cglog_backup_dir" >> $selflog; 
        cd $log_src_dir; 
    fi; 
    if [ ! -d $log_tgt_dir/$path ]; then     
        mkdir -p $log_tgt_dir/$path; 
    fi; 
    #cat /dev/null > $cglog_archieve_file;
    #tar cf $cglog_archieve_file * && rm $log_bak_dir/ -rf; 
    if [ ! -d $cglog_backup_dir ]; then
        mkdir -p $cglog_backup_dir;
    fi;
    all_files=$(ls)
    for myfile in $all_files;
    do
       if [ ! -f $cglog_backup_dir/$myfile ]; then
            touch $cglog_backup_dir/$myfile;
       fi;
       diff $myfile $cglog_backup_dir/$myfile > temp.patch;
       patch -R -p0 $cglog_backup_dir/$myfile < temp.patch > /dev/null;
    done;
    rm temp.patch;
    rm $log_bak_dir/ -rf;
}; 
#log_rotate %d %d %s %s %s %s %s
log_rotate $1 $2 $3 $4 $5 $6 $7



