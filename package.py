#!/usr/bin/python3
#encoding=UTF-8
# git 取出、maven打包、CSS、JS压缩、CSS、JS版本缓存处理、打包ZIP
#
# 压缩CSS、JS需要安装几个包
# pip install webassets
# pip install jsmin
# pip install cssmin
#
#
import os
import zipfile
import io
import logging
import re
import codecs
import subprocess
from os import path
from html.parser import HTMLParser
from webassets import Bundle, Environment

outFile = codecs.open("/home/gexiangdong/out.txt", 'w', 'utf-8')
returnCode = subprocess.call(['/web/git/deploy.sh', ''], stdout=outFile);
outFile.close();
print(returnCode)


version = "wx20150310"
zipFile = "web.zip";
projectFolder = "/Users/gexiangdong/git/saofenbao/saofenbaoweixin" 
tempFolder = "/Users/gexiangdong/temp"
#"/web/git/saofenbao/saofenbaoweixin/"

#不需要打包进入的文件
excludes = ['DS_Store', 'gitignore', 'files', 'WEB-INF/autostart.xml', 'hd/*', 'ceshi.jsp', 'cookie.jsp', 'dbinfo.jsp', 'test.jsp', 'mlogout.jsp', 'META-INF', 'WEB-INF/lib/(?!clschina).*.jar']

#需要压缩的CSS和JS，不仅仅压缩还会搜寻templetFile来更改里面引用的链接URL
#css文件必须在css目录下；js文件必须在js目录下，其他目录不处理
cssFiles = ['css/main.css', 'css/addition.css']
jsFiles = ['js/sfb.js']
templetFiles = ['templet/layout/default.shtml']
contextPath = '${request.contextPath}/'

zf = zipfile.ZipFile(zipFile, 'w')

zf.writestr("version.txt", version)

webFolder = projectFolder + "/src/main/webapp"


def addFolderToZip(folder):
    dirList = os.listdir(folder)
    for fileName in dirList:
        filePath = os.path.join(folder, fileName)
        if os.path.isdir(filePath):
            addFolderToZip(filePath)
        else:
            relatedPath = filePath[len(webFolder)+1:]
            if relatedPath in cssFiles:
                #print(relatedPath, "CSS file...")
                break
            if relatedPath in jsFiles:
                #print(relatedPath, "JS file ...")
                break
            if relatedPath in templetFiles:
                #print(relatedPath, "Templet file ...")
                break
                
            shouldBeInclude = True
            for pattern in excludes:
                #print(pattern, " -- ", relatedPath)
                if(re.search(pattern, relatedPath) is not None):
                    shouldBeInclude = False
                    #print(relatedPath, " omit.... (" + pattern + " matched.)")
                    break
            
            if(shouldBeInclude):
                zf.write(filePath, relatedPath)
            
addFolderToZip(webFolder)

#webassets压缩css、JS文件
def compressFile(f, webFilters):
    filePath = os.path.join(webFolder, f)
    baseName = os.path.basename(filePath)
    prefix = f[0:len(f) - len(baseName)]
    fn = os.path.splitext(baseName)
    newFileName = fn[0] + '.%(version)s' + fn[1]
    env = Environment("")
    env.auto_build=False
    env.url_expire = True
    tmpFile = os.path.join(tempFolder, newFileName)
    env.url_mapping={tempFolder: ''}
    bundle = Bundle(filePath, filters=webFilters, output=tmpFile)
    env.add(bundle)
    bundle.build()
    vfn = bundle.urls()[0][1:]
    if(vfn.index("?") > 0):
        vfn = vfn[0:vfn.index("?")]
    
    #print(prefix, vfn)
    zf.write(os.path.join(tempFolder, vfn), prefix + vfn)
    return prefix + vfn
    

#处理CSS
cssFileVersions = {}
for cssFile in cssFiles:
    f = os.path.join(webFolder, cssFile)
    if os.path.isfile(f):
        cssFileVersions[cssFile]=(compressFile(cssFile, "cssmin"))
    else:
        cssFileVersions[cssFile]="error"

    
#处理JS
jsFileVersions = {}
for jsFile in jsFiles:
    f = os.path.join(webFolder, jsFile)
    if os.path.isfile(f):
        jsFileVersions[jsFile]=(compressFile(jsFile, "jsmin"))
    else:
        jsFileVersions[jsFile]="error"

#处理Templet

class LayoutHTMLParser(HTMLParser):
    
    def __init__(self):
        super().__init__()
        self.reset()
        self.__replacement = {}
        
    def handle_starttag(self, tag, attrs):
        if(tag == "link"):
            for x in attrs:
                if(x[0] == "href"):
                    cssHref = x[1]
                    for cssFile in cssFiles:
                        if (cssHref.find(cssFile) >= 0): self.__replacement[cssHref] = cssFileVersions[cssFile]

        elif(tag == "script"):
            for x in attrs:
                if(x[0] == "src"):
                    jsSrc = x[1]
                    for jsFile in jsFiles:
                        if(jsSrc.find(jsFile) >= 0): self.__replacement[jsSrc] = jsFileVersions[jsFile]

    def replacement(self):
        return self.__replacement
 
#print("OK")
for templet in templetFiles:
    parser = LayoutHTMLParser()
    fh = open(os.path.join(webFolder, templet), 'r')
    t = (fh.read())
    fh.close()
    parser.feed(t)
    replacement = parser.replacement()
    for k in replacement.keys():
        t = t.replace(k, contextPath + replacement[k])

    zf.writestr(templet, t)


zf.close()


    
