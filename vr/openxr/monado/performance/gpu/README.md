<center>
    <h1>
        GPU Performance Analyse
    </h1>
</center>

这里主要是分析Monado的GPU使用性能和其他Runtime的对比。分析工具主要使用**Snapdragon Pofiler**。

## Analyse Indicator

这里主要分析几个指标：

* `GPU Utilization (单位%)`: GPU使用率，分析GPU的主要评估标准之一，使用率越高越容易出现掉帧等问题。
* `GPU Frequency`: GPU频率，GPU使用频率存在固定区间，根据设定的性能模式和GPU的使用率进行调整，一般在GPU负载高的情况下，GPU频率会随着增高，直到最高设定阈值。
* `GPU Bus Busy (单位%)`: GPU到系统内存总线的使用频率。
* `CPU Utilization (单位%)`: CPU使用率。
* `Memory Usage`: 内存使用量。

## Data Capturer

此处抓取的数据主要由几部分组成：

* `Logcat`：Android Logcat主要分析关键Log信息。
* `Snapdraon Profiler Trace`: trace信息获取应用运行情况和GPU使用情况。

## Attention

数据抓取过程需要注意的事项：

* `关闭投屏软件`: 投屏软件会消耗一部分GPU的资源，需要去除干扰项。
* `Layer确定`: 通过`dumpsys SurfaceFlinger`判断渲染的Layer层。

## Basic Performance

由于各个设备的平台分辨率，驱动，等参数不同，首先对平台本身的GPU使用率进行分析。

这里使用官方[ndk-sample](https://github.com/android/ndk-samples)中的应用进行基础GPU使用率的评估，主要是评估在一个最基本的使用**OpenGL**绘制的**Native Activity**不停绘制的情况下，GPU的使用率。