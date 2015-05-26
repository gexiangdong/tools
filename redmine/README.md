定时读取git的提交日志并记录到数据库内。
在redmine中查看各个用户提交的次数和关联比例。

1、在PostGreSQL中创建一个表
    create table git_commit_message(
        project varchar(50) not null,
        commitId varchar(200) not null,
        commitDate timestamp not null,
        commitUser varchar(100) not null,
        commitMessage text not null,
        mergeId varchar(100) null,
        score int default 0 not null,
        primary key(project, commitId)
    )


2、修改config.py中PostgreSQL的链接字符串
        修改config.py中REPOS变量，设置每个需要抓取日志的仓库位置

3、设置定时抓取程序
    #crontab -e
    增加一行  0 * * * * /path....to/retrievegitlog.py 此行表示每隔一小时运行一次
    
4、找到redmine的view目录，一般在/usr/share/redmine/app/view
    找到 projects/show.html.erb（项目首页）   welcome/index.html.erb （redmine首页） 并修改，在合适的位置加入以下行：
    <link rel="stylesheet" type="text/css" href="/projects/redmine/logsummary.css" />
	<script type="text/javascript" src="/projects/redmine/logsummary.py" charset="UTF-8"></script>
	<script type="text/javascript" src="/projects/redmine/logsummary.js" charset="UTF-8"></script>
    并确保已经拷贝这些程序已经拷贝到对应的位置。
    
    
