---
title: 探究安卓存储机制中的uri
date: 2021-10-12 13:54:05
tags:
---

## URI定义

通用资源标志符（Universal Resource Identifier, 简称"URI"。

本次工程中也用到ContentUris，ContentUris 类用于获取Uri路径后面的ID部分

```java
//为该Uri加上ID
Uri uri = Uri.parse("content://com.yfz.Lesson/people")  
Uri resultUri = ContentUris.withAppendedId(uri, 10);  

//从uri获取id
Uri uri = Uri.parse("content://com.yfz.Lesson/people/10")  
long personid = ContentUris.parseId(uri);  
```

<!-- more -->

## 参考链接

https://www.jianshu.com/p/7690d93bb1a1



