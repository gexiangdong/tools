#!bin/bash

##
##从git中取maven project，打包并发布到tomcat目录下
##

gitFolder="/web/git/saofenbao"

#
# 需要在使用此程序前先从远程库克隆
# #git clone /home/git/project/saofenbao.git
#
cd "$gitFolder"
git fetch
git checkout -f origin/develop

chown -R tomcat7:developer /web/git/saofenbao/

if [ "$1" = "norestart" ]; then
   exit
fi



wvjar="$gitFolder/weixin-velocity/target/clschina-weixin-velocity-1.0.jar"
admjar="$gitFolder/saofenbaoadmin/target/clschina-saofenbaoadmin-1.0.jar"
wxjar="$gitFolder/saofenbaoweixin/target/clschina-saofenbao-1.0.jar"
vendorjar="$gitFolder/saofenbaovendor/target/clschina-saofenbaovendor-1.0.jar"
apijar="$gitFolder/saofenbaoapi/target/clschina-saofenbaoapi-1.0.jar"

cd "$gitFolder/weixin-velocity"
mvn -D maven.test.skip=true clean install

if [ -f "$wvjar" ] 
then
   echo "velocity-weixin ok"
else
   echo "$wvjar"
   echo "**************ERROR**************"
   echo "can NOT compile Weixin-Velocity project."
   echo ""
   exit
fi

cd "$gitFolder/saofenbaoadmin"
mvn -D maven.test.skip=true clean install

if [ -f "$admjar" ]; then
   echo "saofenbaoadmin ok"
else
   echo ""
   echo "**************ERROR**************"
   echo "  can NOT compile saofenbaoadmin project."
   echo ""
   exit
fi


cd "$gitFolder/saofenbaoweixin"
mvn -D maven.test.skip=true clean install

if [ -f "$wxjar" ]; then
   echo "saofenbaoweixin ok"
else
   echo ""
   echo "**************ERROR**************"
   echo "  can NOT compile saofenbaoweixin project."
   echo ""
   exit
fi


cd "$gitFolder/saofenbaovendor"
mvn -D maven.test.skip=true clean install

if [ -f "$vendorjar" ]; then
   echo "saofenbaovendor ok"
else
   echo ""
   echo "**************ERROR**************"
   echo "  can NOT compile saofenbaovendor project."
   echo ""
   exit
fi

cd "$gitFolder/saofenbaoapi"
mvn -D maven.test.skip=true clean install

if [ -f "$apijar" ]; then
   echo "saofenbaoapi ok"
else
   echo ""
   echo "**************ERROR**************"
   echo "  can NOT compile saofenbaoapi project."
   echo ""
   exit
fi


cp "$wvjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$wvjar" "$gitFolder/saofenbaovendor/src/main/webapp/WEB-INF/lib/"



cp "$admjar" "$gitFolder/saofenbaoadmin/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaovendor/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaoapi/src/main/webapp/WEB-INF/lib/"

cp "$wxjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$wxjar" "$gitFolder/saofenbaoapi/src/main/webapp/WEB-INF/lib/"


cp "$apijar" /web/git/saofenbao/saofenbaoapi/src/main/webapp/WEB-INF/lib/

cp "$vendorjar" /web/git/saofenbao/saofenbaovendor/src/main/webapp/WEB-INF/lib/



chown -R tomcat7:developer /web/git/saofenbao/

if [ "$1" != "norestart" ]; then
	#/etc/init.d/tomcat7 restart
	rm /var/log/tomcat7/* -rf
	rm /web/projects/logs/* -rf
	service tomcat7 restart
        chmod 666 /web/git/logs/*
fi




