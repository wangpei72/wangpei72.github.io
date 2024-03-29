---
title: 利用Travis——CI部署成功则发送邮件提醒
date: 2021-09-26 10:37:13
tags: TravisCI
---

## 背景

之前做了对博客推送至wangpei72.github.io仓库之后自动渲染部署的CI设置，但是设置是否成功却需要我自己去进一步确认，那么已经自动化到这一步了，我们为了能够将自动化进行到底，我决定再让CI把通知我的事情也做好。

<!-- more -->

## 构造email

下面的一段介绍来自廖雪峰的官方网站

SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。

Python对SMTP支持有`smtplib`和`email`两个模块，`email`负责构造邮件，`smtplib`负责发送邮件。

```python
from email.mime.text import MIMEText
msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
```

注意到构造`MIMEText`对象时，第一个参数就是邮件正文，第二个参数是MIME的subtype，传入`'plain'`表示纯文本，最终的MIME就是`'text/plain'`，最后一定要用`utf-8`编码保证多语言兼容性。还可以以字典的方式调整对邮件的配置:

```python
msg['Subject'] = subject
msg['From'] = msg_from
msg['To'] = msg_to
```

## 发送email

构造完邮件之后，接下来可以发送email，如果我构造的邮件基于qq邮箱发送，那么就可以指定邮件服务器是输入qq邮箱的服务器域名

```python
import smtplib
s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
s.login(msg_from, passwd)
s.sendmail(msg_from, msg_to, msg.as_string())
```

最后完整的发送邮件脚本是这样子的：

```python
#!/usr/bin/pyhton
# -*- coding: UTF-8 -*-
import time
import smtplib
from email.mime.text import MIMEText


def sendEmail(message):
    msg_from = 'koukoustar@qq.com'  # 发送方邮箱
    passwd = 'SECRET'  # 发送方邮箱的授权码 这个要到qq邮箱配置
    msg_to = 'koukoustar@qq.com'  # 收件人邮箱
    subject = "TravisCI部署成功提示"  # 主题
    msg = MIMEText(message, 'plain', 'utf-8')
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = msg_to
    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 邮件服务器及端口号
        s.login(msg_from, passwd)
        s.sendmail(msg_from, msg_to, msg.as_string())
        print('[' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + "]邮件发送成功,邮件内容：" + message)
    except s.SMTPException:
        print('[' + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + "]邮件发送失败,邮件内容：" + message)
    finally:
        s.quit()


if __name__ == "__main__":
    my_msg = "如果你看到这封邮件，表明Travis CI于" + str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))) + " 的部署成功，可以登陆https://koukoustar.cn 查看最新文章～"
    sendEmail(my_msg)
```

## 脚本本地测试

上面的python脚本运行一下，我就在邮箱中收到了该邮件：

![](1.png)

## 将脚本放在Travis CI执行

如果你之前有读过这篇文章[link](https://koukoustar.cn/2021/09/18/结合TravisCI自动部署Next主题的Hexo博客/), 那么你应该知道Travis CI现在的工作状况。

我们在原先的yml文件上做一些补充，首先需要先把上述的脚本`emailSender.py`放置到.travis.yml文件的同级目录下。

```yml
after_script:
  - chmod +x emailSender.py
  - pip install time
  - pip install smtplib
  - python emailSender.py
```

## CI测试

现在我们将所有的改动提交和推送到远程，观察一下Travis CI的运行结果.发现忘记先配置python环境了，导致持续集成构建没成功，调整后完整的.travis.yml文件如下：

```yml
language: node_js 
node_js:
  - 12  # 使用 nodejs LTS v12
python:
  - "3.7"

branches:
  only:
    - source # 只监控 source 的 branch
cache:
  directories:
    - node_modules # 缓存 node_modules 加快构建速度
    - pip
before_install:
  - export TZ='Asia/Shanghai'    
before_script: ## 根据你所用的主题和自定义的不同，这里会有所不同
  - npm install -g hexo-cli # 在 CI 环境内安装 Hexo
  - git clone https://github.com/next-theme/hexo-theme-next.git themes/next
  - npm install # 在根目录安装站点需要的依赖 
script: 
  - hexo clean
  - hexo generate # generate static files
deploy: # 根据个人情况，这里会有所不同
  provider: pages
  skip_cleanup: true # 构建完成后不清除
  token: $GH_TOKEN # 你刚刚设置的 token
  keep_history: true # 保存历史
  fqdn: koukoustar.cn # 自定义域名，使用 username.github.io 可删除
  on:
    branch: source # hexo 站点源文件所在的 branch
  local_dir: public 
  target_branch: gh-pages # 存放生成站点文件的 branch
after_script:
  - chmod +x emailSender.py
  - pip3 install time
  - pip3 install smtplib
  - python emailSender.py
env:
    global:
        - GH_REF: github.com/wangpei72/wangpei72.github.io.git #设置GH_REF，注意更改yourname

```

调整完毕后，重新执行，这次计时测试了一下，构建过程花费了1min15s,还是比较快的，主要耗时花在了解析travis配置和booting vm上，以及进入vm环境之后的环境配置，如果没有找上次CI留下的依赖相关的cache的话，耗时会更多。
