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
import cgi
import subprocess
import sys
from datetime import datetime
from os import path
from html.parser import HTMLParser
from webassets import Bundle, Environment

print("Content-type:text/plain")
print("")


version = ""
form = cgi.FieldStorage()
if(form.getvalue("version") is None):
    version="prerelease"
else:
    version=form.getvalue("version")


scriptPath=""
if("SCRIPT_FILENAME" in os.environ.keys()):
    scriptPath=os.environ["SCRIPT_FILENAME"]
else:
    scriptPath="/web/htdocs/projects/package.py"

scriptFolder = os.path.dirname(scriptPath)

outFile = codecs.open(os.path.join(scriptFolder, "output/out.txt"), 'w', 'utf-8')
returnCode = subprocess.call(['/web/temp/build.sh', version], stdout=outFile);
if(returnCode == 0):
    outFile.write("\n\nbuild done.\npacking the zip file....\n\n")
    #outFile.close();
else:
    print('{"status":1, "errorMessage":"error while building package, see build log for detail. ' + str(returnCode) + '"}')
    outFile.close()
    sys.exit()
    


zipFile = "output/web-" + version + "." + datetime.now().strftime("%Y%m%d%H%M%S") + ".zip";
projectFolder = "/web/temp/saofenbao/saofenbaoweixin" 
tempFolder = os.path.join(scriptFolder, "temp")
#if(!os.path.exists(tempFOlder)):
   
#"/web/git/saofenbao/saofenbaoweixin/"

#不需要打包进入的文件
excludes = ['DS_Store', 'gitignore', 'files', 'WEB-INF/autostart.xml', 'hd/*', 'ceshi.jsp', 'cookie.jsp', 'dbinfo.jsp', 'test.jsp', 'mlogout.jsp', 'META-INF', 'WEB-INF/lib/(?!clschina).*.jar']

#需要压缩的CSS和JS，不仅仅压缩还会搜寻templetFile来更改里面引用的链接URL
cssFiles = ['css/main.css', 'css/addition.css']
jsFiles = ['js/sfb.js']
templetFiles = ['templet/layout/default.shtml']
contextPath = '${request.contextPath}/'

zf = zipfile.ZipFile(os.path.join(scriptFolder, zipFile), 'w')

zf.writestr("version.txt", version)

webFolder = projectFolder + "/src/main/webapp"


def addFolderToZip(folder):
    dirList = os.listdir(folder)
    for fileName in dirList:
        filePath = os.path.join(folder, fileName)
        #outFile.write("checking " + filePath + "\n")
        if os.path.isdir(filePath):
            addFolderToZip(filePath)
        else:
            relatedPath = filePath[len(webFolder)+1:]
            outFile.write("checking " + relatedPath + "\n")
            if relatedPath in cssFiles:
                outFile.write("  temporary omit " + relatedPath + " (CSS file).\n")
                continue
            if relatedPath in jsFiles:
                outFile.write("  temporary omit " + relatedPath + " (JS file).\n")
                continue
            if relatedPath in templetFiles:
                outFile.write("  temporay omit " + relatedPath + " (Layout Templet file)\n")
                continue
                
            shouldBeInclude = True
            for pattern in excludes:
                #print(pattern, " -- ", relatedPath)
                if(re.search(pattern, relatedPath) is not None):
                    shouldBeInclude = False
                    outFile.write("  omit " + relatedPath + " (" + pattern + " matched.)")
                    continue
            
            if(shouldBeInclude):
                zf.write(filePath, relatedPath)
                outFile.write("  add " + relatedPath + "\n")
            
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
outFile.write("compress CSS files....\n")
cssFileVersions = {}
for cssFile in cssFiles:
    f = os.path.join(webFolder, cssFile)
    if os.path.isfile(f):
        cssFileVersions[cssFile]=(compressFile(cssFile, "cssmin"))
    else:
        cssFileVersions[cssFile]="error"

    
#处理JS
outFile.write("compress JS files....\n")
jsFileVersions = {}
for jsFile in jsFiles:
    f = os.path.join(webFolder, jsFile)
    if os.path.isfile(f):
        jsFileVersions[jsFile]=(compressFile(jsFile, "jsmin"))
    else:
        jsFileVersions[jsFile]="error"

#处理Templet
outFile.write("update layout templet file.\n")
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
 
for templet in templetFiles:
    parser = LayoutHTMLParser()
    fh = open(os.path.join(webFolder, templet), mode='r', encoding='utf-8')
    t = fh.read()
    fh.close()
    parser.feed(t)
    replacement = parser.replacement()
    for k in replacement.keys():
        t = t.replace(k, contextPath + replacement[k])

    zf.writestr(templet, t)


zf.close()
outFile.write("\nZip file created.\n")
outFile.close()

print('{"status":0, "errorMessage":"success.", "file":"' +  zipFile + '"}')
    
