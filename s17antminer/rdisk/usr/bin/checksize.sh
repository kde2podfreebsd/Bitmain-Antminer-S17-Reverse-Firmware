exec 2>&1; 
log_checksize () {     
    debug_mode=$1;     
    log_tgt_dir_name=$2;     
    log_tgt_dir=/$log_tgt_dir_name;     
    tmp_dir=/tmp/.tmp.$$;     
    selflog=/tmp/log_checknvdata.log;     
    echo "start check /nvdata size: " `date` > $selflog;
    if [ $debug_mode -eq 0 ];     then         
        threshold1_percentage=75; threshold2_percentage=60;     
    else         
        threshold1_percentage=3; threshold2_percentage=3;     
    fi; 
    nvdata_state=`df -k| grep $log_tgt_dir_name`; 
    if [ "$nvdata_state" = "" ]; then     
        echo "ERROR: can't find $log_tgt_dir" >> $selflog; 
        exit -1; 
    fi; 
    used=`echo $nvdata_state| awk '{print $5}'|sed "s/%//g"`; 
    used_blocks=`echo $nvdata_state | awk '{print $3}'`; 
    total_blocks=`echo $nvdata_state | awk '{print $2}'`; 
    threshold1=$((total_blocks*threshold1_percentage/100)); 
    threshold2=$((total_blocks*threshold2_percentage/100)); 
    echo "used_blocks   =$used_blocks" >> $selflog; 
    echo "threshold1    =$threshold1" >> $selflog; 
    echo "threshold2    =$threshold2" >> $selflog; 
    echo "total_blocks  =$total_blocks" >> $selflog; 
    mkdir $tmp_dir; 
    cd $tmp_dir; 
    if [ $used_blocks -gt $threshold1 ]; then     
        if [ $debug_mode -eq 0 ];     then         
            #filelist=`find $log_tgt_dir -type f -name "cglog_*"| xargs ls -tr`;     
            #filelist=`find $log_tgt_dir -type d -name "cglog_*" | sort -t "_" -k 3`;     
            filelist=`find $log_tgt_dir -name "cglog_*" | sort -t "_" -k 3`;   
            filelist1=`find $log_tgt_dir -name "antminer_log_backup_*"` 
        else         
            #filelist=`find $log_tgt_dir -type f -name "test_log*" | xargs ls -tr`;     
            filelist=`find $log_tgt_dir -type d -name "test_log*" | sort -t "_" -k 3`;     
            filelist1=`find $log_tgt_dir -name "antminer_log_backup_*"`
        fi;     
        echo $filelist >> $selflog;
        if [ ! -z "$filelist1" ];     then         
            for file in $filelist1;         do             
                used_blocks=`df -k | grep $log_tgt_dir_name | awk '{print $3}'`;
                if [ $used_blocks -lt $threshold2 ];             then
                    echo "$used_blocks < $threshold2" >> $selflog; break;
                else
                    echo "$used_blocks > $threshold2" >> $selflog;
                    #cat /dev/null >$file;
                    #rm -f $file;
                    rm -rf $file;
                fi;
            done;
        else
            echo "ERROR: no log file found" >> $selflog;
        fi;
        if [ ! -z "$filelist" ];     then         
            for file in $filelist;         do             
                used_blocks=`df -k | grep $log_tgt_dir_name | awk '{print $3}'`;   
                if [ $used_blocks -lt $threshold2 ];             then                 
                    echo "$used_blocks < $threshold2" >> $selflog; break;             
                else                 
                    echo "$used_blocks > $threshold2" >> $selflog; 
                    #cat /dev/null >$file;
                    #rm -f $file;
                    rm -rf $file;         
                fi;         
            done;     
        else         
            echo "ERROR: no log file found" >> $selflog;     
        fi; 
    else     
        echo "enough free space ($((100-used))% left). do nothing" >> $selflog; 
    fi; 
    cd $log_tgt_dir; 
    rm -rf $tmp_dir; 
}; 
#log_checksize %d %s
log_checksize $1 $2
