---
title: 视觉slam7.1-视觉里程计：使用相机运动估计视觉算法
date: 2021-05-28 17:05:29
tags:
---

本篇文章记录了少许阅读《视觉slam14讲》的阅读整理，不是特别全面，只是为了本次项目中特定任务搜查资料，时间比较紧，文章并没有全面涵盖所有知识点。日后若时间有空闲，将回来补充整理。

<!-- more -->

## 相机位姿估计

### 特征点法

首先，视觉里程计的核心问题是根据图像估计相机运动。利用特征点能够有效利用图像矩阵为我们提供的关于相机运动的信息。特征点一般具有可重复可区别高效率和本地性的特点。

### 特征点组成

**关键点key-point** 和**描述子descriptor**

关键点是指特征点的位置，描述子是按照相似的关键点一般具有相似的描述子设计的，如果2个特征点的描述子在向量空间上的距离相近，那么我们称他们是同样的特征点。

#### ORB特征

分为FAST关键点和BRIEF描述子



| 名称     | FAST关键点                                                   | BRIEF描述子                                                  |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 原理     | 比较像素点之间的亮度差异                                     | 二进制高维度向量                                             |
| 优缺点   | 速度快、重复性不强、分布不均匀<br />不具有尺度不变性以及方向性 | 速度快，有利于存储、适用于实时匹配<br />不具有旋转不变性     |
| 解决办法 | 尺度：在不同层的图像金字塔匹配<br />方向性：计算图像灰度质心 | 旋转：关键点方向被计算出来的情况下可以计算旋转之后的Steer BRIEF |

#### 特征匹配

暴力匹配；浮点型关键点->匹配欧氏距离；二进制关键点->匹配汉明距离；特征点个数极多时，考虑快速近似最近邻FLANN算法。



### 特征点匹配核心代码（OpenCV）

```cpp
//首先初始化部分、关键点、描述子、计算描述子指针、匹配matcher指针
//-- 初始化
    std::vector<KeyPoint> keypoints_1, keypoints_2;
    Mat descriptors_1, descriptors_2;
    Ptr<FeatureDetector> detector = ORB::create();
    Ptr<DescriptorExtractor> descriptor = ORB::create();
    // Ptr<FeatureDetector> detector = FeatureDetector::create(detector_name);
    // Ptr<DescriptorExtractor> descriptor = DescriptorExtractor::create(descriptor_name);
    Ptr<DescriptorMatcher> matcher  = DescriptorMatcher::create ( "BruteForce-Hamming" );
```

```cpp
//之后
 //-- 第一步:检测 Oriented FAST 角点位置
    detector->detect ( img_1,keypoints_1 );
    detector->detect ( img_2,keypoints_2 );
```

```cpp
//在之后,Mat存储描述子
 //-- 第二步:根据角点位置计算 BRIEF 描述子
    descriptor->compute ( img_1, keypoints_1, descriptors_1 );
    descriptor->compute ( img_2, keypoints_2, descriptors_2 );
```

可视化可以使用函数

```cpp
drawKeypoints( img_1, keypoints_1, outimg1, Scalar::all(-1), DrawMatchesFlags::DEFAULT );
```

```cpp
//最后是特征匹配
  //-- 第三步:对两幅图像中的BRIEF描述子进行匹配，使用 Hamming 距离
    vector<DMatch> matches;
    //BFMatcher matcher ( NORM_HAMMING );
    matcher->match ( descriptors_1, descriptors_2, matches );
```

关于DMatch这个类，可以理解为匹配关键点描述子的类，有以下成员，存着匹配对的各种信息，用于筛选匹配对

```
 DMatch.distance - 描述符之间的距离。越小越好。
• DMatch.trainIdx - 目标图像中描述符的索引。
• DMatch.queryIdx - 查询图像中描述符的索引。
• DMatch.imgIdx - 目标图像的索引
```

之后对匹配点对进行筛选

```cpp
//-- 第四步:匹配点对筛选
    double min_dist=10000, max_dist=0;

    //找出所有匹配之间的最小距离和最大距离, 即是最相似的和最不相似的两组点之间的距离
    for ( int i = 0; i < descriptors_1.rows; i++ )
    {
        double dist = match[i].distance;
        if ( dist < min_dist ) min_dist = dist;
        if ( dist > max_dist ) max_dist = dist;
    }
//当描述子之间的距离大于两倍的最小距离时,即认为匹配有误.但有时候最小距离会非常小,设置一个经验值30作为下限.
    for ( int i = 0; i < descriptors_1.rows; i++ )
    {
        if ( match[i].distance <= max ( 2*min_dist, 30.0 ) )
        {
            matches.push_back ( match[i] );
        }
    }
}
```

以上代码中得到的

```cpp
std::vector <cv::Dmatch> matches
```


即为最后获得筛选后的匹配对

之后顺便看到一个像素坐标系转相机坐标系的函数，顺便摘抄作为参考

```cpp
Point2d pixel2cam ( const Point2d& p, const Mat& K )
{
    return Point2d
           (
               ( p.x - K.at<double> ( 0,2 ) ) / K.at<double> ( 0,0 ),
               ( p.y - K.at<double> ( 1,2 ) ) / K.at<double> ( 1,1 )
           );
}
```

翻译成公式就是
$$
x_{cam} = \frac {x_{pxl} -  {c_x}} {f_x} \\
y_{cam} = \frac {y_{pxl} - {c_y}}{f_y}
$$

### 计算相机运动

| 已知情况                       | 采用方法 | 效果                       |
| ------------------------------ | -------- | -------------------------- |
| 单目相机、两组2D点             | 对极几何 | 估计相机运动               |
| 双目相机、RGBD相机（两组3D点） | ICP方法  | 得到距离信息，估计相机运动 |
| 一组3D一组2D                   | PnP求解  | 估计相机运动               |

### 2D-2D

因为不太适用于本次比赛应用场景，先跳过这一步骤

### 三角测量

又称三角化，==目的是求解目标特征点的空间位置==，考虑两张不同视角的二维图，两图之间变换矩阵为T ,I~1~有特征点p~1~ , I~2~有特征点p2 , 都对应p点， 现在x1 x2是两个特征点的归一化坐标，已知R T,要求解两个特征点的深度s~1~  s~2~.

1. 如果我们考虑计算s～1,首先我们有
   $$
   s_2x_2 = s_1Rx_1 + t
   $$

2. 对上式我们左乘$x_2^{\Lambda}$

3. $$
   s_2x_2^{\Lambda}x_2 = 0 = s_1x_2^{\Lambda}Rx_1 + x_2^{\Lambda}t
   $$

   可以解方程得到s~2~,有了s~2~之后s~1~也很易得

   注意，前提是对极几何中我们求解了相机位子，在此基础之上进行三角化求解特征点的空间位置，这是为了解决==单目slam中的单幅图无法获取深度信息==


```cpp
//opencv中提供了封装的函数用于三角化
cv::triangulatePoints( T1, T2, pts_1, pts_2, pts_4d );

    // 转换成非齐次坐标
    for ( int i=0; i<pts_4d.cols; i++ )
    {
        Mat x = pts_4d.col(i);
        x /= x.at<float>(3,0); // 归一化
        Point3d p (
            x.at<float>(0,0), 
            x.at<float>(1,0), 
            x.at<float>(2,0) 
        );
        points.push_back( p );
    }//需要一步将其次坐标归一化并且转换为费其次坐标
```


```cpp
//这函数的参数必须都是float类型的
Parameters：

projMatr1
3x4 projection matrix of the first camera.//左侧相机的RT矩阵（一般设置成eyes 0）
projMatr2
3x4 projection matrix of the second camera.//右侧相机的RT矩阵
projPoints1
2xN array of feature points in the first image. In case of c++ version it can be also a vector of feature points or two-channel matrix of size 1xN or Nx1.//左侧相机在相机坐标系下特征点坐标的集合
projPoints2
2xN array of corresponding points in the second image. In case of c++ version it can be also a vector of feature points or two-channel matrix of size 1xN or Nx1.//右侧相机在相机坐标系下特征点坐标的集合
points4D
4xN array of reconstructed points in homogeneous coordinates.//齐次坐标中的4xN
```


三角化测量中具有的深度不确定性可以根据深度滤波器来改进

### 3D-2D:PnP

终于来到了PnP，此方法描述了当知道n个3D空间点以及其投影位置时，估计相机的位姿。两张图像中的一张特征点的3D位置已知，最少需要3个点对以及至少1个额外点验证结果来估计相机运动，3D位置可以由三角化和RGBD相机的深度图确定，因此在双目或者rgbd相机的视觉里程计中

这里介绍很多PNP问题的求解方法，并且可以用非线性化的方式构造最小二乘问题迭代求解

#### 直接线性变换DLT

已知一组3D点，以及他们在相机中的投影位置

==可以求解给定地图和图像时的相机状态问题==，如果把3D点看做另一个相机坐标系点的话，也可以求解两个相机的相对运动问题。

==--后记--==
关于相机运动估计，最后采取的解决办法实际上是跑一个slam的包，效果会比手写pnp来的更准，且操作也很方便。