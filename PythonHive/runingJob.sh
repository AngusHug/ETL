#!/usr/bin/env bash
#创需要的目录文件
mkdir /tmp/huangdonghui_tmp
if [ $? -eq 0 ];then
	touch /tmp/huangdonghui_tmp/running_job_list.txt
    touch /tmp/huangdonghui_tmp/dir_gmt_latest.txt
else
	echo 'the directory already exists!'
    touch /tmp/huangdonghui_tmp/running_job_list.txt
fi
dir=/tmp/huangdonghui_tmp/running_job_list.txt
dir_temp=/tmp/huangdonghui_tmp/dir_gmt_latest.txt
#打印正在运行的job
i=0
hadoop job -list > ${dir}
if [ $? -eq 0 ];then
	if [ `wc -l < ${dir}` -eq 2 ];then
		echo "there's no job is running!"
    else
		#echo `cat ${dir}`
        cat ${dir}|while read line
        do
        	echo $line
            i=`expr $i + 1`
            echo $i
        done
    fi
else
	echo "I'm a bug text"
fi

#echo ${date_dir}
#log_dir=/user/history/done/${date_dir}
#date_dir="`date \"+%Y-%m-%d\"|sed 's/-/\//g'`"
log_dir=/user/history/done/`date +%Y-%m-%d|sed 's/-/\//g'`
echo ${log_dir}
hdfs dfs -ls ${log_dir}|awk '{print $6,$7,$8}' > ${dir_temp}
cat ${dir_temp}|while read line
	do
		date_line=`awk '{print $6,$7}'`
        echo '${date_line}'
    	#sed 's/$/&${date_line}/g' ${dir_temp}
    done
echo "it's done"
cat ${dir_temp}





#数组长度
#echo ${#dir_gmt_latest[@]}
#echo ${dir_gmt_latest[@]}
#>/tmp/huangdonghui/dir_create_latest.txt