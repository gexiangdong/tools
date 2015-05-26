# GIT 统计小程序
#encoding=UTF-8
#
#

# PostGreSQL数据库链接URL
PGURL = "user='pgdbo' password='pass' dbname='gitcommitmessages'"

#GIT仓库，可设置多个；每个的分别由ID和路径组成；ID保存在数据库中区分每个仓库
REPOS = [['xxx.git', '/var/lib/redmine/repos/xxx.git'], ['yyy.git', '/var/lib/redmine/repos/yyy.git']]

