<center>
  <h1>
    Log Tool
  </h1>
</center>

## Join All into One

[log.py](script/log.py)这个脚本主要是把被切分开的Log按照时间线进行整合成一个Log，这样就能方便的在一个文件中搜索相关信息。

```shell
# logdir
.
├── log.log
├── log_001.log
├── log_002.log
└── log_003.log
```

目录结构如上，使用命令进行整合Log的输出。

```
python log.py -i /xxx/logdir -o all.log
```

* `-i`: Log的文件夹目录。
* `-o`: Log输出文件的名字，默认输出在Log文件夹目录中。

最后会在logdir中生成一个all.log的文件。

```shell
# all.log
-------------------------------- log_003.log --------------------------------
log_003.log中的内容
-------------------------------- log_002.log --------------------------------
log_002.log中的内容
-------------------------------- log_001.log --------------------------------
log_001.log中的内容
-------------------------------- log.log --------------------------------
log.log中的内容
```

