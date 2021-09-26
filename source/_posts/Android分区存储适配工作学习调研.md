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

可以看到Activity实例拥有一个`ContentResolver`的实例对象能够对以Uri方式定义的资源进行访问。
