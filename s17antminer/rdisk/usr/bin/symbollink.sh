exec 2>&1; 
gen_symbol_link () { 
    selflog=/tmp/log_symbol_link.log; 
    log_tgt_dir=/$1; 
    path=$2; 
    ts=$3; 
    prefix="$4"_; 
    new_path=$5; 
    #old_file=$log_tgt_dir/$path/$prefix$ts.tar; 
    old_file=$log_tgt_dir/$path/$prefix$ts; 
    #new_file=$log_tgt_dir/$new_path/LINK_$prefix$ts.tar; 
    new_file=$log_tgt_dir/$new_path/LINK_$prefix$ts; 
    echo "old:$old_file symbol link:$new_file">$selflog;
    if [ ! -d $log_tgt_dir/$new_path ]; then 
        mkdir -p $log_tgt_dir/$new_path; 
    fi; 
    #if [ -f $old_file ]; then 
    if [ -d $old_file ]; then 
        ln -sf $old_file $new_file;
    else 
        echo "old files not found">>$selflog;
    fi; 
}; 
#gen_symbol_link %s %s %s %s %s
gen_symbol_link $1 $2 $3 $4 $5
