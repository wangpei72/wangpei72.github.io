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

- 若您的应用使用旧版存储模型且之前以 Android 10 或更低版本为目标平台，您可能会将数据存储到启用[分区存储](https://developer.android.google.cn/training/data-storage#scoped-storage)模型后您的应用无法访问的目录中。在以 Android 11 为目标平台之前，请将[数据迁移](https://developer.android.google.cn/training/data-storage/use-cases#migrate-legacy-storage)到与分区存储兼容的目录。

## Android存储机制概况-包括引入沙盒机制之前的

| **内容类型**                                                 |               **访问方法**               | **所需权限**                                                 | **其他应用是否可以访问？**                                   | **卸载应用时是否移除文件？**                                 |      |
| ------------------------------------------------------------ | :--------------------------------------: | ------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------------------------------ | ---- |
| [应用专属文件](https://developer.android.google.cn/training/data-storage/app-specific)<br />app-specific |          仅供您的应用使用的文件          | 从内部存储空间访问，可以使用 getFilesDir() 或 getCacheDir() 方法  从外部存储空间访问，可以使用 getExternalFilesDir() 或 getExternalCacheDir() 方法getExternalMediaDirsgetObbDirs | 从内部存储空间访问不需要任何权限  如果应用在搭载 Android 4.4（API 级别 19）或更高版本的设备上运行，从外部存储空间访问不需要任何权限 | 如果文件存储在内部存储空间中的目录内，则不能访问  如果文件存储在外部存储空间中的目录内，则可以访问 | 是   |
| [媒体](https://developer.android.google.cn/training/data-storage/shared/media)<br />media | 可共享的媒体文件（图片、音频文件、视频） | MediaStore API                                               | 在 Android 10（API 级别 29）或更高版本中，访问其他应用的文件需要 READ_EXTERNAL_STORAGE 或 WRITE_EXTERNAL_STORAGE 权限  在 Android 9（API 级别 28）或更低版本中，访问**所有**文件均需要相关权限 | 是，但其他应用需要 READ_EXTERNAL_STORAGE 权限                | 否   |
| [文档和其他文件](https://developer.android.google.cn/training/data-storage/shared/documents-files)<br />document-files |  其他类型的可共享内容，包括已下载的文件  | 存储访问框架                                                 | 无                                                           | 是，可以通过系统文件选择器访问                               | 否   |
| [应用偏好设置](https://developer.android.google.cn/training/data-storage/shared-preferences)<br />shared-preferences |                  键值对                  | [Jetpack Preferences](https://developer.android.google.cn/guide/topics/ui/settings/use-saved-values) 库 | 无                                                           | 否                                                           | 是   |
| 数据库                                                       |                结构化数据                | [Room](https://developer.android.google.cn/training/data-storage/room) 持久性库 | 无                                                           | 否                                                           | 是   |

- 公共目录：Downloads、Documents、Pictures 、DCIM、Movies、Music、Ringtones等

- - 公共目录的文件在App卸载后，==不会删除==
  - 可以通过SAF、MediaStore接口访问  

- - 拥有权限，也能通过路径直接访问

- ### 

## 变更

1. 私有文件沙盒

1. 1. 沙箱目录： /sdcard/Android/sandbox/packagename/
   2. 任何其他应用都无法直接访问您应用的沙盒文件。由于文件是您应用的私有文件，因此您不再需要任何权限即可在外部存储设备中访问和保存自己的文件

1. 1. 当app卸载后，沙箱中的文件==删除==

2. 媒体文件共享集合

1. 1. 访问权限
   2. 共享方案

3. 照片访问

1. 1. 位置信息
   2. 图库显示

4. 跨应用文件
   读取和存储跨应用文件

   | **方法**                                      | **错误现象**             |
   | --------------------------------------------- | ------------------------ |
   | Environment.getExternalStorageDirectory       |                          |
   | Environment.getExternalStoragePublicDirectory | 创建目录的时候提示无权限 |
   | Environment.getDownloadCacheDirectory         |                          |
   | Environment.getStorageDirectory               |                          |
   | Environment.getDataDirectory                  |                          |
   | Environment.getRootDirectory                  |                          |
   | /sdcard/*，/mnt/*                             |                          |

> 上述接口在target 30中都不可使用，应该使用SAF，MediaStore和专属私有目录相关API替代。
>
> 代码中Hardcode的路径，例如/sdcard/*，/mnt/*这类用法
>
> 应该使用==SAF，MediaStore和专属私有目录==相关API替代，或者更改存储目录。

## 兼容模式更改-测试适配结果方法

### 行为变更

在 Android Q 测试版 1 中启用此行为变更，请在终端窗口中执行以下命令：

```
adb shell sm set-isolated-storage on
```

查看是否已生效

```
adb shell getprop sys.isolated_storage_snapshot
```

### 兼容性行为

测试您的应用时，您可以通过在终端窗口中运行以下命令来为外部文件存储访问权限启用兼容性模式：

```
adb shell cmd appops set your-package-name android:legacy_storage allow
```

停用兼容性模式，请在 Android Q 上卸载然后重新安装您的应用，或在终端窗口中运行以下命令

```
adb shell cmd appops set your-package-name android:legacy_storage default
```

## 参考资料

- 应用分区存储Google的最佳实践：https://developer.android.com/training/data-storage/use-cases
- 优酷存储空间适配：https://yuque.antfin.com/youku_android_arch/atlas/ka510p#getExternalStoragePublicDirectory

- Google存储行为变更：https://developer.android.google.cn/about/versions/11/privacy/storage
- 存储访问框架：https://developer.android.google.cn/guide/topics/providers/document-provider

- FileProvider：https://developer.android.google.cn/training/secure-file-sharing/setup-sharing
- 分区存储：https://developer.android.google.cn/training/data-storage#scoped-storage
