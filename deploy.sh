#!bin/bash

##
##从git中取maven project，打包并发布到tomcat目录下
##

cd /web/git/saofenbao
git fetch
git checkout -f origin/develop

chown -R tomcat7:developer /web/git/saofenbao/

if [ "$1" = "norestart" ]; then
   exit
fi



wvjar="/web/git/saofenbao/weixin-velocity/target/clschina-weixin-velocity-1.0.jar"
admjar="/web/git/saofenbao/saofenbaoadmin/target/clschina-saofenbaoadmin-1.0.jar"
wxjar="/web/git/saofenbao/saofenbaoweixin/target/clschina-saofenbao-1.0.jar"
vendorjar="/web/git/saofenbao/saofenbaovendor/target/clschina-saofenbaovendor-1.0.jar"
apijar="/web/git/saofenbao/saofenbaoapi/target/clschina-saofenbaoapi-1.0.jar"

cd /web/git/saofenbao/weixin-velocity
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

cd /web/git/saofenbao/saofenbaoadmin
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


cd /web/git/saofenbao/saofenbaoweixin
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

cd /web/git/saofenbao/saofenbaovendor
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

cd /web/git/saofenbao/saofenbaoapi
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


cp "$wvjar" /web/git/saofenbao/saofenbaoweixin/src/main/webapp/WEB-INF/lib/
cp "$wvjar" /web/git/saofenbao/saofenbaovendor/src/main/webapp/WEB-INF/lib/



cp "$admjar" /web/git/saofenbao/saofenbaoadmin/src/main/webapp/WEB-INF/lib/
cp "$admjar" /web/git/saofenbao/saofenbaoweixin/src/main/webapp/WEB-INF/lib/
cp "$admjar" /web/git/saofenbao/saofenbaovendor/src/main/webapp/WEB-INF/lib/
cp "$admjar" /web/git/saofenbao/saofenbaoapi/src/main/webapp/WEB-INF/lib/

cp "$wxjar" /web/git/saofenbao/saofenbaoweixin/src/main/webapp/WEB-INF/lib/
cp "$wxjar" /web/git/saofenbao/saofenbaoapi/src/main/webapp/WEB-INF/lib/


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




