<center>
    <h1>
        Memory
    </h1>
</center>

## Lost RAM

### 主动释放

```
# echo 3 > /proc/sys/vm/drop_caches
```

### 抓取内存

```
while true;do data=`date +"%m-%d %H:%M:%S.%N"`;meminfo=`dumpsys meminfo `; free_ram=`echo $meminfo | grep -Eo 'Free RAM:[[:space:]][^[:space:]]+'`;used_ram=`echo $meminfo | grep -Eo 'Used RAM:[[:space:]][^[:space:]]+'`;lost_ram=`echo $meminfo | grep -Eo 'Lost RAM:[[:space:]][^[:space:]]+'`;echo $data ${free_ram%\(*} ${used_ram%\(*} ${lost_ram%\(*};sleep 0.1;done
```

