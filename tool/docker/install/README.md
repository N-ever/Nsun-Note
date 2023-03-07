<center>
    <h1>
        Docker 安装
    </h1>
</center>

## 系统信息获取

```shell
[root@vultr ~]# cat /etc/redhat-release
CentOS Linux release 7.9.2009 (Core)
```

## 安装Docker

安装步骤可以从官网查看，因为是服务器，所以只需要安装Docker Engine就够了不需要Docker Desktop。

> [Docker官网](https://docs.docker.com/engine/install/centos/)

### CenterOS 安装

此处都是使用root账户进行安装，所以都省略了sudo。

#### 配置仓库

安装yum-utils，这个提供了yum-config-manager，为了后续安装仓库

```shell
$ yum install -y yum-utils
```

添加Docker的下载仓库

```shell
$ yum-config-manager \
    --add-repo \
    https://download.docker.com/linux/centos/docker-ce.repo
```

#### 安装

安装最新版本的Docker并安装命令行工具，容器和compose插件，如果需要安装其他特定版本，请到上面官网链接跳转查看。

> 此处安装的是docker compose插件，不是单独安装的docker compose，所以使用时要用docker compose而不是docker-compose命令

```shell
$ yum install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

#### 启动

这里启动Docker服务，如果需要开机启动，请使用**systemctl enable**。

```shell
$ systemctl start docker
```

#### 测试

测试docker功能

```shell
$ docker run hello-world
```

### Windows安装

#### 下载Docker

下载程序并安装

> https://www.docker.com/

#### 迁移Docker目录

##### 关闭Docker&wsl

```shell
$ wsl --shutdown
```

##### 导出Docker存储

```shell
$ wsl --export docker-desktop D:\tmp\a.tar
$ wsl --export docker-desktop-data D:\tmp\b.tar
```

##### 注销Docker存储

```shell
$ wsl --unregister docker-desktop
$ wsl --unregister docker-desktop-data
```

##### 导入Docker存储

```shell
$ wsl --import docker-desktop D:\data\docker\docker-desktop D:\tmp\a.tar --version 2
$ wsl --import docker-desktop-data D:\data\docker\docker-desktop-data D:\tmp\b.tar --version 2
```

##### 启动Docker

### 创建Ubuntu

#### 拉取Ubuntu镜像

```shell
$ docker pull ubuntu
```

#### 创建Ubuntu容器

```shell
$ docker run -it -d --privileged=true --name pimax -p 10022:22 -v /run/desktop/mnt/host/d/work/docker:/home/evern/work ubuntu
```

#### 安装SSH

```shell
$ apt install -y openssh-server openssh-client
```

#### 更新Root权限

[配置root权限](../Settings/README.md#配置root权限)
