#!/bin/bash
#判断/home/tobedeploy目录下是否有待发布的jar
#如果有，备份当前在使用的jar，并拷贝待发布的jar到当前使用目录

today=$(date +%Y%m%d-%H%M%S)

xyzjar="xyz-api-1.0.jar"
if [ -f "/home/tobedeploy/$xyzjar" ]; then
    echo "DEPLOY $xyzjar ......"
    cp /web/webapps/$xyzjar /web/webapps/backup/$xyzjar$today
    mv /home/tobedeploy/$xyzjar /web/webapps/
    
    #重启服务
    sudo service xyz-api restart
    echo "RESTARTING..."
    for k in $( seq 1 30 )
    do
      echo -n "... "
      curl -o /dev/null -s http://localhost:8080/xyz-api/test/hi
      rc=$?
      if [[ $rc -eq 0 ]] ; then
        break;
      fi;
      sleep 2s;
    done

    #sleep 30s
    curl http://localhost:8080/xyz-api/test/hi
    echo 
fi;
