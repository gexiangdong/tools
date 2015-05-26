#!/usr/bin/python3
#encoding=UTF-8
#
# 取git提交的日志，并保存到数据库
#

import os
import io
import sys
import subprocess
import re
import psycopg2
from datetime import datetime
from os import path

#配置文件
import config


conn = psycopg2.connect(config.PGURL)

#保存提交日志到数据库
def saveCommitMessage(gitRepoId, commitId, commitDate, commitUser, commitMessage, mergeId):
    curQuery = conn.cursor()
    curQuery.execute("select count(*) from git_commit_message where project=%s and commitId=%s", [gitRepoId, commitId])
    row = curQuery.fetchone()
    if(row[0] == 0):
        curInsert = conn.cursor()
        score = 0 #提交消息打分；3分表示合格，关联redmine则合格
        if (re.match("(refs|fix|fixs|fixed|close|closed)\s\#[0-9]+", commitMessage)):
            score = 3
        curInsert.execute("insert into git_commit_message(project, commitId, commitDate, commitUser, commitMessage, mergeId, score) values(%s, %s, %s, %s, %s, %s, %s)", [gitRepoId, commitId, commitDate, commitUser, commitMessage, mergeId, score])
        curInsert.close()
        print("insert ", gitRepoId, commitId)
    else:
        print(gitRepoId, commitId, " exists.", row[0])
        
    curQuery.close()

#读取某个git repo的提交日志并记录到数据库中
def retrieveGitCommitLog(gitRepoId, gitRepoPath):
    cmd = 'cd ' + gitRepoPath + '; env -i git log  '
    commitLogs = os.popen(cmd).read()

    lines = commitLogs.splitlines()

    commitId = None
    commitMessage = None
    commitAuthor = None
    commitDate = None
    mergeId = None
    for row in range(len(lines)):
        line = lines[row]
        if (line.startswith('commit ')):
            if (commitId != None):
                #save this commit
                saveCommitMessage(gitRepoId, commitId, commitDate, commitAuthor, commitMessage, mergeId)

                commitId = None
                commitMessage = None
                commitAuthor = None
                commitDate = None
                mergeId = None
            elif (row > 0):
                #somthing wrong here.
                print("somthing wrong")

            commitId = line[7:].strip()

        elif(line.startswith('Author:')):
            commitAuthor = line[8:].strip()
        elif(line.startswith('Merge:')):
            mergeId = line[7:].strip()
        elif(line.startswith('Date:')):
            commitDate = datetime.strptime(line[6:].strip(), "%a %b %d %H:%M:%S %Y %z")
        else:
            if(len(line) > 0):
                if(commitMessage != None):
                    commitMessage += "\r\n" + line.strip()
                else:
                    commitMessage = line.strip()

#读取git仓库中的日志
for i in range(len(config.REPOS)):
    retrieveGitCommitLog(config.REPOS[i][0], config.REPOS[i][1])

conn.commit()
conn.close()
