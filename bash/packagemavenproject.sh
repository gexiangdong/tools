#!/bin/bash
# maven项目，有2个project, xyz-core, xyz-api； xyz-api依赖xyz-core
# xyz-api是 spring boot项目，打包的jar可以直接运行
# 这个脚本文件先从git中取项目，然后编译打包，并发布，重启服务
#

# /web/git/xyz是项目的目录
cd /web/git/xyz
git fetch
git checkout -f origin/develop

chown -R developer:www-data /web/git/xyz/

/usr/share/maven/bin/mvn -DskipTests -pl xyz-core clean install 
rc=$?
if [[ $rc -ne 0 ]] ; then
  echo -e "    \033[41;37m                                       \033[0m"
  echo -e "    \033[41;37m    could not package xyz-core         \033[0m"
  echo -e "    \033[41;37m                                       \033[0m"
  exit $rc
fi

/usr/share/maven/bin/mvn -DskipTests -pl xyz-api clean package 
rc=$?
if [[ $rc -ne 0 ]] ; then
  #如果编译失败，红色显示
  echo -e "    \033[41;37m                                       \033[0m"
  echo -e "    \033[41;37m    could not package xyz-api          \033[0m"
  echo -e "    \033[41;37m                                       \033[0m"
  exit $rc
fi

#拷贝到特定目录下，并重启服务
cp xyz-api/target/xyz-api-*.jar  /web/webapps/xyz-api.jar
service xyz-api restart

#检查是否重启成功，会在60秒内不停重试，如果超过60秒则提示发布失败
echo -n "DEPLOY DONE, waiting for restart ... "
for k in $( seq 1 30 )
do
    sleep 2s
    echo -n "... "
    curl -o /dev/null -s http://localhost:8080/xyz-api/tests/hi
    rc=$?
    if [[ $rc -eq 0 ]] ; then
        break;
    fi;
done

echo 
echo
echo "==========================Test xyz-api with curl======================"
resultCode=`curl -o /dev/null -s -w %{http_code} http://localhost:8080/xyz-api/tests/hi`
if [[ $resultCode -ne 200 ]] ; then
    #出错了，显示详细链接信息，以便查错
    echo
    echo -e "\033[41;37m       ERROR in xyz-api             \033[0m"
    curl -v http://localhost:8080/xyz-api/tests/hi
    echo
else
    echo
    echo "xyz-api is started."
    echo
fi; 


echo
echo
