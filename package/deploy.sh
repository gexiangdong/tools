#!bin/bash

## 
##从git中取maven project，打包并发布到tomcat目录下
## 调用时，需要增加一个分支名称的参数，例如 build.sh develop
##

gitFolder="/web/git/saofenbao"

#
# 需要在使用此程序前先从远程库克隆
# #git clone /home/git/project/saofenbao.git
#
cd "$gitFolder"
version=$1
echo "$version"
cd /web/temp/saofenbao
git fetch
ret=$?
if ! test "$ret" -eq 0
then
  echo "Failed to git fetch"
  exit 1
fi

#不能在版本前固定增加origin，否则在checkout TAG时出错
git checkout -f  $version

ret=$?
if ! test "$ret" -eq 0
then
  echo "$? Failed while checkout $version"
  exit 2
fi

chown -R tomcat7:developer /web/git/saofenbao/



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
   exit 3
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
   exit 4
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
   exit 5
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
   exit 6
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
   exit 7
fi


cp "$wvjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$wvjar" "$gitFolder/saofenbaovendor/src/main/webapp/WEB-INF/lib/"



cp "$admjar" "$gitFolder/saofenbaoadmin/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaovendor/src/main/webapp/WEB-INF/lib/"
cp "$admjar" "$gitFolder/saofenbaoapi/src/main/webapp/WEB-INF/lib/"

cp "$wxjar" "$gitFolder/saofenbaoweixin/src/main/webapp/WEB-INF/lib/"
cp "$wxjar" "$gitFolder/saofenbaoapi/src/main/webapp/WEB-INF/lib/"



exit 0


