<center>
    <h1>
        Linux Firewall
    </h1>
</center>

## 添加端口

添加一个外部可以以TCP形式访问的端口

```shell
$ firewall-cmd --zone=public --add-port=80/tcp --permanent
$ firewall-cmd --reload
```

* **--zone**: 作用域
* **--add-port=80/tcp**: 添加端口，格式为：端口/通讯协议
* **--permanent**: 永久生效，没有此参数重启后失效