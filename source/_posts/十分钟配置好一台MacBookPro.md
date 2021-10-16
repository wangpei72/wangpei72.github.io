---
title: 十分钟配置好一台MacBookPro
date: 2021-10-16 22:45:42
tags:
---

## 背景

考虑到我的mbp就要归还给公司了。有点心痛。因为mac用起来还是很爽的，我很喜欢这个键盘的手感，虽然他被吐槽了很多回，并且不出意外的话我可能是真的需要买一台MacBookAir回学校写毕设，因为这个键盘模式是真的非常熟悉了，如果换回到windows我怕自己适应回去太难受了，况且以后我工作之后一直会用的是mbp，那么，为了之后能够在Air上配置好现在的环境，写一篇小博客记录记录。

<!-- more -->

## 日常必备工具

- Typora

  - 编辑md文件必备

- ClashX

  - 科学上网

- iTerm2

  附上配置文件：

  ```shell
  # If you come from bash you might have to change your $PATH.
  # export PATH=$HOME/bin:/usr/local/bin:$PATH
  export PATH="$PATH:./node_modules/.bin"
  export JAVA_HOME="/Library/Java/JavaVirtualMachines/jdk1.8.0_291.jdk/Contents/Home"
  export MAVEN_HOME=/Users/wangpei/apache-maven-3.5.0 #修改成你放的路径
  export PATH=$PATH:$MAVEN_HOME/bin
  # export Path=$PATH:/Applications/Sublime Text.app/Contents/SharedSupport/bin
  alias python="/usr/local/bin/python3"
  #alias pip="/Library/Frameworks/Python.framework/Versions/3.9/bin/pip3"
  export ANDROID_HOME="/Users/wangpei/Library/Android/sdk"
  PATH=~/bin:$PATH
  PATH=${PATH}:${JAVA_HOME}/bin:${ANDROID_HOME}/platform-tools:${ANDROID_HOME}/tools:.
  export PATH
  CLASSPATH=$JAVA_HOME/lib/tools.jar:$JAVA_HOME/lib/dt.jar:.
  export CLASSPATH
  alias javac='javac -J-Dfile.encoding=UTF-8 -encoding UTF-8'
  alias java='java -Dfile.encoding=UTF-8'
  alias typora="open -a typora"
  # Path to your oh-my-zsh installation.
  export ZSH="/Users/wangpei/.oh-my-zsh"
  # alias goproxy='export http_proxy=http://127.0.0.1:7890 https_proxy=http://127.0.0.1:7890'
  # alias disproxy='unset http_proxy https_proxy'
  # export http_proxy=http://127.0.0.1:7890
  # export https_proxy=$http_proxy
  
  ZSH_THEME="agnoster"
  
  plugins=(
          git
          zsh-syntax-highlighting
          zsh-autosuggestions
  )
  
  source $ZSH/oh-my-zsh.sh
  
  # User configuration
  
  
  source ~/.oh-my-zsh/custom/plugins/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
  
  ```

- sublimetext，WPS

- Adobe系列，见我的百度网盘

- Chrome

## 开发工具

- JDK8
- AndroidSDK 一直到Level 30
- Android Studio
- Jetbrains全家桶（推荐Clion，Pycharm）
- 各类第三方库，例如：TensorFlow、Pytorch
- Xcode

- SourceTree，版本控制gui
- Charles，抓包工具

