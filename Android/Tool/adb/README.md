<center>
    <h1>
        Adb Tool
    </h1>
</center>

## 简介

Adb Tool旨在开发一套Adb相关的套件，减少Debug时的Adb操作，让开发者能更加方便的使用Adb的功能，也是Adb功能的一个扩展。

## 命令参数

* `-i`: 进入Interactive模式，该模式下可以省略adb命令。
* `-p`: 设置Debug包名，可以配合`-i`使用定义交互模式Debug的应用包名，也可以命令行使用，定义adb命令对应的包名。

## 模式

### Interactive模式

交互模式，可以通过`-i`的参数进入交互模式，交互模式中可以省略adb的命令，且可以关联Debug的应用包名进行简易化的操作。

#### 进入

```shell
python .\adb.py -i
```

#### 退出

```shell
$ exit()
```

### 命令行模式

* [ ] TODO

## 使用示例

### Logcat

#### 打印全部Log

这里可以不加`-p`内容，此处等同于`adb logcat`。

```shell
python .\adb.py -i -p org.freedesktop.monado.openxr_runtime.out_of_process
$ logcat
```

#### 打印应用Log

这里首先设置了应用包名，然后使用了`package logcat`，这里就是只打印应用的Log，切如果应用退出后重新进入也可以继续打印应用Log。

```shell
python .\adb.py -i -p org.freedesktop.monado.openxr_runtime.out_of_process
$ package logcat
```

### 其他

未定义的adb命令（除了`adb shell`进入shell模式）可以直接在Interactive模式下省略adb后进行使用，与原效果一致。

```shell
python .\adb.py -i
$ devices #获取设备信息
```

### GetPid

通过包名获取应用的pid

```shell
 python .\adb.py getpid -p org.freedesktop.monado.openxr_runtime.out_of_process
```

or

```shell
python .\adb.py -i -p org.freedesktop.monado.openxr_runtime.out_of_process
$ getpid
```

## TODO

* [ ] 统一Cmd的输入获取形式
* [ ] 命令行的帮助信息进行完善