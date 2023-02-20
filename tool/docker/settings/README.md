<center>
    <h1>
        Docker Settings
    </h1>
</center>

## 配置root权限

* 关闭docker
* 修改\\wsl$\docker-desktop-data\data\docker\containers中container中的config.v2.json

```
修改
"Path": "bash", => "Path": "/sbin/init",
"Cmd": [
           "bash" => "/sbin/init"
       ],
```
