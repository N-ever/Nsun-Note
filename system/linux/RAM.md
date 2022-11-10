<center>
    <h1>
        Linux RAM
    </h1>
</center>

## Swap分区创建

### 查看Swap信息

使用free查看swap信息。

```shell
$ free 
              total        used        free      shared  buff/cache   available
Mem:        1015528      760420       75804       51264      179304       69948
Swap:             0           0           0
```

### 创建Swap文件

选择空间足够的文件目录，创建swap文件。这里创建/swapfile文件，大小为1M * 2048即2G。

```shell
$ dd if=/dev/zero of=/swapfile bs=1M count=2048
2048+0 records in
2048+0 records out
2147483648 bytes (2.1 GB) copied, 7.076 s, 303 MB/s
```

将文件属性修改为swap，让系统知道这个文件是用作swap的。

```shell
$ mkswap /swapfile
Setting up swapspace version 1, size = 2097148 KiB
no label, UUID=1781b4ea-7877-4265-afe1-8d3b3e8f7d49
```

修改文件读写权限，只有root可以进行读写，如果不改，后续启用时会有提示信息，不要问我是怎么知道的。

```shell
$ chmod 600 /swapfile
```

使能swapfile作为swap进行使用。

```shell
$ swapon /swapfile
```

再次使用free或者swapon -s查看swap的状态。

```shell
$ free
              total        used        free      shared  buff/cache   available
Mem:        1015528      504688      322820       75264      188020      307804
Swap:       2097148         264     2096884
```

