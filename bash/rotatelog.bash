#!/bin/bash

#
# 清理日志目录下的日志文件用的脚本，可用于定时任务。目录设置在第10行。
# 规则：在日志目录下创建backup目录，把日志目录下文件gzip压缩后放入backup目录；
#      如果日志23小时内无修改则删除，如果有修改则截断（以便记录日志的进程记录记录日志）
#

today=$(date +%Y%m%d-%H%M)
now=`date +%s`

for file in /web/tomcats/*/logs/*
do
    if test -f "${file}"
    then
        #echo $file
        bkname=`basename "$file"`
        folder=$(dirname "$file")
        mkdir -p ${folder}/backup
        #判断文件大小
		fileSize=`ls -l "${file}" | awk '{ print $5 }'`
		minSize=$((10))
		if [ $fileSize -gt $minSize ]
		then
		    #文件size大于10byte, 则备份，小的不备份了
		    echo "backup ${file}"
		    cat "${file}" | gzip >  "${folder}/backup/${bkname}-${today}.gz"
		fi
		#判断文件时间
		fileTime=`stat -c %Y "${file}"`
		if [ $[ $now - $fileTime ] -gt 82800 ]
		then
			#23个小时没修改过文件了, 删除
			echo "delete ${file}"
			rm "${file}"
		else
			#23个小时内用的文件，清空内容，以便tomcat等服务可以继续写日志
			# echo "truncate ${file}"
			echo "" > "${file}"
		fi
    fi
done
