---
title: Android分区存储适配工作学习调研
date: 2021-09-26 10:23:09
tags: Android
---

## 背景

当一个应用从Android SDK Level 10升级到11时，就涉及到适配的问题，而根据谷歌官方文档，可以知道10->11的变更范围。

变更范围中的重点有一项是强制执行分区存储，我们知道分区存储也就是安卓设备在存储上引入了沙盒机制，应用不能够访问其他应用的私有目录，但是可以无权限访问自己的私有目录和公共的媒体文件目录。

<!-- more -->

## 分区存储适配要点

适配的内容在具体工作中包括那些呢？

### API调用方式

最直接的体现在ContentProvider接口的修改方式。

```java
String[] PROJECTIONS = new String[]{
            FileColumns._ID,
            FileColumns.DATA,
            FileColumns.MEDIA_TYPE,
            FileColumns.DATE_MODIFIED,
            MediaStore.Video.Media.DURATION};

private Cursor queryImages() {
        Uri uri = MediaStore.Files.getContentUri("external");
        Pair<String, String[]>  selects = getSelects();
        String sortOrderAndLimit = FileColumns.DATE_MODIFIED + " DESC LIMIT " + getLimit();
        Cursor cursor = getActivity().getContentResolver().query(uri, PROJECTIONS, selects.first, selects.second,  sortOrderAndLimit);
        return cursor;
    }
```

所有涉及访问图片文件的代码部分，都需要调用上述接口以增加对Content api的支持。

可以看到Activity实例拥有一个`ContentResolver`的实例对象能够对以Uri方式定义的资源进行访问,在这里调用query方法时需要提供5个参数，其中需要给出一个string数组 `PROJECTIONS`,他表示什么？用于存储一个媒体资源文件的类型和数据信息的结构化数据吗？这目前是我的猜测。

同时查询时需要提供`Pair<String, String[]>`类型的selects，该对象获取逻辑由`getSelects()`获取

为什么是这样设计的？我们先对比一下该函数的抽象方法：

```java
// 查询数据；
query(Uri, String[], String, String[], String)；
```

看到这里，应该不难理解为什么selects是一个Pair类型的了吧，这是由函数接口决定的。

### 理论要点

- Android 10及以上文件存储机制修改成了沙盒模式
- APP只能访问自己目录下的文件和公共媒体文件

- 对于Android10一下的系统，还是使用老的文件存储方式

> 适配分区存储的时候，需要兼容Android 10系统版本以下的内容，通过SDK_VERSION区分

- 如果
