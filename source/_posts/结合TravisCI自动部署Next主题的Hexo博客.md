---
title: 结合TravisCI自动部署Next主题的Hexo博客
date: 2021-09-18 15:26:04
tags: hero, next, Travis CI
---

此文记录了如何利用Travis CI帮助部署Hexo博客的静态页面到github page， 具体实现的效果是：当我修改hexo站点的内容，并且提交推送至远程被CI监控的特定分支上之后，CI将开始按照.travis.yml中执行CI步骤，帮你进行后续的渲染和部署操作。所以你自己实际上的操作只包括了修改hexo的源文件和CI的配置文件，后续都由CI帮你代劳。

文章后续会探究如何基于Ci对页面进行一些美化的配置。

<!-- more -->

> 折腾了一个晚上加上一个下午，终于成功让CI帮我部署hexo的博客页面，啊，我还想赶紧看看怎么能美化一些next博客有很多可以自定的设置，所以说快速回顾一下，希望这些内容能够帮到你。

## Hexo - 建站

这部分快速过一遍。首先要使用hexo框架需要的依赖项：

- git
- npm

请无论通过百度还是谷歌帮上面两个依赖配置好。

### 安装hexo

```shell
npm install -g hexo-cli
```

### 配置hexo

```shell
hexo init <hexo-site-dir>
```

其中`<hexo-site-dir>`这是你本地的hexo站点的目录名称，可以随便起，本地将新建一个以此为名称的目录。

一些初始配置可以更改`_config.yml` ,例如`title`，更改主题landscape为next

```yml
# _config.yml
themes: next
```



> 感兴趣的可以看官网给的更多配置项目[官网doc](https://link.segmentfault.com/?url=https%3A%2F%2Fhexo.io%2Fdocs%2Fconfiguration)

⚠️这里还需要你配置一下`.gitignore`文件,加上`themes/`以忽略这个文件夹的记录，因为CI中会重新拉取主题（假设我们用了next）的repo，由于themes下的主题文件夹也是一个repo，同时站点文件夹在CI中也是基于一个repo来工作的，为了减少子模块可能带来的不必要的错误，这里采取忽略本地的主题文件夹策略：

```
.DS_Store
Thumbs.db
db.json
*.log
node_modules/
public/
.deploy*/
themes/

```

配置完之后，你的站点文件夹大致是这个样子：

```
.
├── _config.landscape.yml
├── _config.yml
├── db.json
├── node_modules
├── package.json
├── scaffolds
├── source
└── themes
```

`hexo new post xxxx`写几篇日志，之后`hexo s -g`，打开`http://localhost:4000`看看你的静态文件渲染的样子,一切正常就继续往下看

## Github - 创建github.io仓库

去github新建一个仓库，repo名字叫做`username.github.io`username是你用户名。

之后回到你的本地站点，

`git init && git remote add origin <url-example: git@github.com:wangpei72/wangpei72.github.io.git>` ,<url>设置成刚刚新建的仓库的git地址，建议走ssh，因为2021.8.13github走https需要personal acess token来取代密码的认证方式，而这个token在后续CI中还会用到，不过这里走ssh是不受这条变更的影响的，而且也很方便。

之后将你的改动提交至本地source分支，⚠️意味着你的源文件存在source分支上，push到远程仓库。

```shell
git add .
git checkout -B source
git commit -m 'first commit'
git push origin source:source
```

## Travis CI - 配置CI

### 授权

重点来了，开始用Travis CI之前，先去[官网](https://www.travis-ci.com/)sign up,如果你之前用过那就直接sign in，注意，本文使用CI的方式基于github。

![image-20210918161902960](0D77DFE4-E678-4344-9427-092D0B65E616.png)

点击头像 -> settings ，配置你的repo，将github.io仓库设置到travis CI的目标repo list当中来。

![](2.jpg)

### 获取personal token 并且配置环境变量

[去这里](https://github.com/settings/tokens)拿到你的token，勾选repo权限组就够用了，复制你的token信息，要把他当作密码来使用，整个文件记下来，待会要用。

回到travis CI，找到`My repositories`， 找到`More options`，点击`Settings`,在`Environment Variables`栏目里设置name： GH_TOKEN， vale：复制你刚刚拿到的token，点击Add。

![](3.jpg) 

回到你的本地站点,新建一个用于驱动CI工作的配置文件`.travis.yml`。

```yml
language: node_js 
node_js:
  - 12  # 使用 nodejs LTS v12
branches:
  only:
    - source # 只监控 source 的 branch
cache:
  directories:
    - node_modules 
before_install:
  - export TZ='Asia/Shanghai'    
before_script: 
  - npm install -g hexo-cli # 在 CI 环境内安装 Hexo
  - git clone https://github.com/next-theme/hexo-theme-next.git themes/next
  #从 Github 上拉取 next 主题
  - npm install # 在根目录安装站点需要的依赖 
script: 
  - hexo clean
  - hexo generate # generate static files
deploy:
  provider: pages
  skip_cleanup: true # 构建完成后不清除
  token: $GH_TOKEN # 你刚刚设置的 token
  keep_history: true 
  fqdn: koukoustar.cn # 自定义域名，使用 username.github.io 可删除
  on:
    branch: source # hexo 站点源文件所在的 branch
  local_dir: public 
  target_branch: master # 存放生成站点文件的 branch,和你github.io settings中的page栏目中设置保持一致

```

### git提交 - 观察CI执行

将你目前在本地站点所做的更改提交一下，push 到远程的source分支上

push完毕之后，Travis CI就会开始queuing，queue完了就开始执行，会有一个host来跑你的travis.yml解析出来的命令，例如：安装nodejs，拉取next主题的仓库，clean， generate， deploy

如果没有出错，执行成功则结果大致如下：

![](4.jpg)

## Reference

[🔗](https://segmentfault.com/a/1190000021987832)

[🔗](https://www.itfanr.cc/2017/08/09/using-travis-ci-automatic-deploy-hexo-blogs/)

