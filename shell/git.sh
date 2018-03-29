
https://git-scm.com/book/zh/v1/Git-%E5%88%86%E6%94%AF-%E5%88%86%E6%94%AF%E7%9A%84%E6%96%B0%E5%BB%BA%E4%B8%8E%E5%90%88%E5%B9%B6
# 现在，假如你要开始开发一个新的功能，但是在功能完全实现之前不想 master 分支的用户使用
# 那么，你可以新建一个分支，在完成之后再将其合并到 master 分支中去

# 新建并切换到分支
$ git checkout -b storage
# 相当于执行下面两条命令
$ git branch storage
$ git checkout storage

# 在几次提交之后，storage 分支的 HEAD 指针会超前于 master 分支的指针
# 此时你有另一个问题要解决，需要切换回 master 分支
# 不过在此之前，留心你的暂存区或者工作目录里，那些还没有提交的修改，
# 它会和你即将检出的分支产生冲突从而阻止 Git 为你切换分支。
# 切换分支的时候最好保持一个清洁的工作区域。
$ git checkout master
Switched to branch 'master'
# 此时工作目录中的内容和你在解决问题 #53 之前一模一样
# 接下来创建一个紧急修补分支 hotfix 来展开工作，直到搞定
$ git checkout -b hotfix
Switched to a new branch 'hotfix'
$ vim index.html
$ git commit -a -m 'fixed the broken email address'
[hotfix 3a0874c] fixed the broken email address
 1 files changed, 1 deletion(-)
# 有必要作些测试，确保修补是成功的，然后回到 master 分支并把它合并进来，然后发布到生产服务器。
# 用 git merge 命令来进行合并：
$ git checkout master
$ git merge hotfix
Updating f42c576..3a0874c
Fast-forward
 README | 1 -
 1 file changed, 1 deletion(-)
# 合并时出现了“Fast forward”的提示。由于当前 master 分支所在的提交对象是
# 要并入的 hotfix 分支的直接上游，Git 只需把 master 分支指针直接右移。
# 由于当前 hotfix 分支和 master 都指向相同的提交对象，所以 hotfix 已经完成了历史使命，
# 可以删掉了。
$ git branch -d hotfix
Deleted branch hotfix (was 3a0874c).
# 现在回到 storage 分支继续工作
# 值得注意的是之前 hotfix 分支的修改内容尚未包含到 storage 中来。
# 如果需要纳入此次修补，可以用 git merge master 把 master 分支合并到 storage；
# 或者等 iss53 完成之后，再将 iss53 分支中的更新并入 master。
