exec 2>&1; 
update_name () { 
    log_tgt_dir=/$1; 
    path=$2; 
    ts=$3; 
    prefix="$4"_; 
    new_path=$5; 
    new_ts=$6; 
    #old_file=$log_tgt_dir/$path/$prefix$ts.tar; 
    old_file=$log_tgt_dir/$path/$prefix$ts; 
    #new_file=$log_tgt_dir/$new_path/$prefix$new_ts.tar; 
    new_file=$log_tgt_dir/$new_path/$prefix$new_ts; 
    echo "old:$old_file new:$new_file">/tmp/log_updatename.log;
    if [ ! -d $log_tgt_dir/$new_path ]; then 
        mkdir -p $log_tgt_dir/$new_path; 
    fi; 
    #if [ -f $old_file ]; then 
    if [ -d $old_file ]; then 
        if [ -d $new_file ]; then
          rm -rf $new_file;
        fi;
        mv $old_file $new_file;
    fi; 
    if [ "`ls -A $log_tgt_dir/$path/ | wc -w`" == "0" ];then 
        rm -rf $log_tgt_dir/$path;
    fi; 
}; 
#update_name %s %s %s %s %s %s
update_name $1 $2 $3 $4 $5 $6
