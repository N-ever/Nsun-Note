<center>
    <h1>
        Android Tools
    </h1>
</center>

## ADB

### 通过包名打印Log

```shell
adb shell
pid=`ps -A | grep [part of package name] | awk '{print $2}'`;echo $pid;logcat --pid=$pid
```

### 打印GPU负载

```shell
adb shell
while true;do gpu_info=`cat /sys/class/kgsl/kgsl-3d0/gpubusy`;left=${gpu_info% *};right=${gpu_info/$left/};s=`echo "scale=2;$left/($right+1)*100" | bc`;echo -ne "$s%    \r";done

# 高通机型
while true; do busy=`cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage`;echo -ne "$busy    \r";done
# or
while true; do busy=`cat /sys/devices/platform/soc/3d00000.qcom,kgsl-3d0/devfreq/3d00000.qcom,kgsl-3d0/gpu_load`;echo -ne "$busy%    \r";sleep 0.1;done
```

### 打印GPU工作频率
```shell
adb shell cat /sys/class/kgsl/kgsl-3d0/gpuclk
adb shell cat /sys/class/kgsl/kgsl-3d0/devfreq/cur_freq
```

### 打印GPU最大、最小工作频率
```shell
adb shell cat /sys/class/kgsl/kgsl-3d0/devfreq/max_freq
adb shell cat /sys/class/kgsl/kgsl-3d0/devfreq/min_freq
```

