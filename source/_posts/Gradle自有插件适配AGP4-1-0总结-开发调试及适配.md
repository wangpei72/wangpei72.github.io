---
title: Gradle自有插件适配AGP4.1.0总结-开发调试及适配
date: 2021-10-18 11:09:00
tags: Android-gradle-plugin
---

## 总览

本篇文章旨在总结近两周（2021.09.06-09.16）以来对两个gradle自有插件升级AGP版本后适配工作中用到的知识、思路、手段等。

总结主要分为两方面，一是上手gradle插件中开发调试等实操性的方法，二是对gradle构建体系的基础知识归纳。

<!-- more -->

## 插件适配问题-排查思路

结合实际工作中的插件适配工作，整理出在升级AGP版本这类背景下适配一个插件的通用思路：

1、升级配置，进行编译和相应任务在原来生效的项目下的执行；

2、观察能否正常编译，不能的话收集报错信息，定位出问题的位置；

3、降级回到原来的环境下，在关键位置打上断点，进行调试，拿到正常工作条件下的debug信息；

4、升级配置，修改出错的地方，进行api调用的调整，确保先编译通过；

5、根据降级拿到的正常debug信息，测试修改后的代码debug信息能否替代之前的；

6、根据原先的操作模式测试修改后的版本功能是否恢复。

## gradle插件调试方法-Dorg.gradle.debug参数

gradle插件工程和安卓工程的调试模式不同，安卓应用可以在运行时进行debug，而gradle插件的工作是发生在工程构建（包含了编译）时期，那么gradle插件开发调试的方式该如何进行呢？

可以通过以下方式：先了解一个参数，Dorg.gradle.debug，通过`gradle help -Dorg.gradle.debug=true`

将 org.gradle.debug 属性设置为“true”，然后将远程调试器连接到端口 5005，您可以在 Gradle 构建本身中设置断点和调试 buildSrc 和独立工程的插件。

具体在idea里的操作可以参照下面这个gif。

所以在执行一个debug之前，先运行这样一个命令:

```
./gradlew :app:clean -Dorg.gradle.debuug=true --no-daemon
```

上述命令表示执行使用插件的工程app模块的clean任务并且打开debug模式，不使用守护进程，执行该命令后进程会卡住，直到remote debug进程attach，才会进入IDLE状态继续执行，之后稍等一段时间就可以拿到参数信息，正常进行断点调试。

在这个过程中需要额外注意，使用的插件的jar包字节码和当前源码的版本要一致，否则debug过程中有些变量拿不到，所以如果使用的是本地maven repo，一定要在debug之前先uplodaArchives到本地之后在去调试，或者确保使用插件的工程app找到的是最新构建的插件的路径（例如插件工程build/libs/下的jar包）.

![](1.gif)

## Gradle构建体系vs Maven

首先要区分开两个概念:Gradle和Android Gradle Plugin。

Gradle是开源构建自动化工具，特点是灵活性和性能兼具，足以构建几乎所有类型的软件；文章标题中提到的是Android Gradle Plugin，它是google开发的、基于Gradle的，用于添加专用于构建Android应用的功能，可以说他是专门为android应用定制的gradle构建插件，并且是一个单独的软件库，其版本和gradle的版本相对应，例如4.1.0的AGP对应于gradle6.6。

> 最新的AGP7.0对应的Gradle版本也是7.0，而上一个版本的AGP是4.2.0，对应gradle是6.7.1，AGP从7.0开始版本号就开始以DSL(gradle)的版本号为基准，这就是为什么AGP直接从4.*直接跳到了7

### gradle的灵活性

安卓指定gradle作为官方构建工具，不是因为build脚本是code，而是Gradle 的建模方式可以以最基本的方式进行扩展，Gradle 的模型还允许它用于使用 C/C++ 进行原生开发，并且可以扩展以覆盖任何生态系统。

### gradle的性能表现

缩短构建时间是加快交付的最直接手段之一。gradle也好，maven也好，都采用了一定形式的并行项目构建和并行以依赖解析。最大的区别是 Gradle 的工作避免和增量机制。使 Gradle 比 Maven 快得多的前 3 个特性是：

1. 增量机制（工作避免的手段）：Gradle 通过跟踪任务的输入和输出并仅运行必要的内容来避免工作，并且仅在可能的情况下处理更改的文件。
2. build cache：重用使用相同输入的任何其他 Gradle 构建的构建输出，包括在机器之间。

1. gradle daemon守护进程：使构建信息在内存中保持“热”状态的长期进程。

以上特性使得gradle在几乎所有场景的构建任务下都比maven快至少两倍以上。

### gradle的依赖管理

gradle和maven两个构建系统都提供了从可配置存储库解析依赖项的内置功能。两者都能够在本地缓存依赖项并并行下载它们。作为库使用者，Maven 允许覆盖依赖项，但只能按版本覆盖。gradle提供了可定制的依赖选择和替换规则，这些规则可以声明一次并在项目范围内处理不需要的依赖。这种替换机制使 Gradle 能够一起构建多个源项目以创建复合构建。

Gradle 允许自定义依赖范围（Scope），从而提供更好的建模和更快的构建。

Maven 依赖冲突解决以最短路径工作，该路径受声明顺序的影响。Gradle 会完全解决冲突，选择图中找到的依赖项的最高版本。此外，使用 Gradle，您可以将版本声明为严格的，这允许它们优先于传递版本，从而允许降级依赖项。

作为库生产者，Gradle 允许生产者声明 `api` 和 `implementation` 依赖项，以防止不需要的库泄漏到使用者的类路径中。Maven 允许发布者通过可选的依赖项提供元数据，但仅作为文档提供。 Gradle 完全支持功能变体（variants）和可选的依赖项。有关gradle的变体选择可以看一下这篇对官方文档的转载：https://yuque.antfin-inc.com/nb/hatxv2/cgg6kp

## Gradle插件开发

gradle plugin的开发，在这里做总结之前也有阅读和记录一篇粗略的笔记，就在本篇文章的同级目录下。

可以使用groovy，kotlin或java来实现gradle插件，gradle插件最终将被编译为字节码。

概括起来包括三种packaging形式的插件开发：直接写在构建脚本中、buildSrc形式的工程结构、单独的工程

实现插件的本质是写一个实现Plugin接口的实现类，当插件被应用到一个工程的时候，gradle会为plugin class创建一个实例并且调用实例的apply()方法，并且当前project的对象将作为参数传递给方法，使得plugin可以按照需求用以配置这个工程。

一个直接写在构建脚本里的gradle插件的例子：

```groovy
apply plugin: GreetingPlugin
abstract class GreetingPluginExtension {
    abstract Property<String> getMessage()

    GreetingPluginExtension() {
        message.convention('Hello from GreetingPlugin')
    }
}
class GreetingPlugin implements Plugin<Project> {
    @java.lang.Override
    void apply(Project project) {
        def extension = project.extensions.create('greeting', GreetingPluginExtension)
        project.task('hello'){
            doLast {
                println extension.message.get()
            }
        }
    }
}

greeting.message = 'hi from Gradle'
```

hello的task可以`gradle -q hello`的方法执行。

### 配置插件

大多数插件为构建脚本和其他插件提供了一些配置选项，用于自定义插件的工作方式。plugin可以使用extension对象来配置插件本身，project对象提供了ExtensionContainer对象，它包含了该project应用的所有的设置和属性。你可以添加一个extension对象到这个container中来为你的plugin提供配置。extension只是一个具有代表配置的 Java Bean 属性的对象。

### 独立工程的插件

我们修复的两个插件都是独立工程的插件，此类插件可以发布并且被公用，工程本身就是一个java工程，最终产出一个jar，它包含了插件的classse。

> 最简单的打包发布插件的方式使用[java gradle plugin开发插件](https://docs.gradle.org/current/userguide/java_gradle_plugin.html#java_gradle_plugin)，这个插件帮助你自动应用plugin，添加gradleapi（）依赖至api配置，生成结果jar文件中被需要的插件描述子并且配置发布时候需要plugin marker artifact（`plugin.id:plugin.id.gradle.plugin:plugin.version`）

如果没有使用上述插件来发布插件，这个发布将会缺少pma，而这又是被需要的，用一定位插件，所以推荐在使用该插件的工程的settings.gradle中添加一个resolutionStrategy{}到pluginManagement{}中：

```groovy
 resolutionStrategy {
        eachPlugin {
            if (requested.id.namespace == 'org.example') {
                useModule("org.example:custom-plugin:${requested.version}")
            }
        }
    }
```

### 使用独立工程形式发布的插件

先在settings.gradle中的pluginManagement{}闭包中添加mave的repo url：

```groovy
// settings.gradle
pluginManagement {
    repositories {
        maven {
            url = uri(repoLocation)
        }
    }
}
```

在build.gradle中plugins闭包中添加id和version：

```groovy
plugins {
    id 'org.example.greeting' version '1.0-SNAPSHOT'
}
```

