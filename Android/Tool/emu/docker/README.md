<center>
  <h1>
   	Emu in Docker
  </h1>
</center>

## 远程Docker桌面

### 创建Ubuntu容器

```shell
docker run -tid -p 3316:22 -p 5900:5900 -p 5901:5901 -v /home/evern/work:/opt/work --name evern --privileged=true ubuntu:20.04 /bin/bash
```

### 连接容器

```shell
docker exec -it evern /bin/bash
```

### 安装工具

```
apt update
apt install -y vim openssh-client openssh-server net-tools
```

### 设置ssh

```
echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config
```

### 设置密码

```
passwd root
```

### 启动ssh

```
service ssh start
ps -A | grep sshd
```

### 安装桌面环境

```
apt update
apt install -y gnome-panel gnome-settings-daemon metacity nautilus gnome-terminal ubuntu-desktop
```

### 安装vnc4server

```
echo "deb http://archive.ubuntu.com/ubuntu/ bionic universe" >> /etc/apt/sources.list
apt update
apt install -y vnc4server
```

### 设置vncserver

* 启动一下生成配置，并设置密码

```
vncserver
```

* 备份一下配置

```
cp ~/.vnc/xstartup ~/.vnc/xstartup.bak
```

* 编辑xstartup文件

```
vi ~/.vnc/xstartup
```

```
#!/bin/sh
 	 
# Uncomment the following two lines for normal desktop:
# unset SESSION_MANAGER
# exec /etc/X11/xinit/xinitrc
 	 
[ -x /etc/vnc/xstartup ] && exec /etc/vnc/xstartup
[ -r $HOME/.Xresources ] && xrdb $HOME/.Xresources
xsetroot -solid grey 
vncconfig -iconic &
x-terminal-emulator -geometry 80x24+10+10 -ls -title "$VNCDESKTOP Desktop" &
x-window-manager &
 
gnome-panel &
gnome-settings-daemon &
metacity &
nautilus &
```

* 重新启动vncserver

```vncserver -kill :1
vncserver -kill :1
vncserver -geometry 1920x1080 :1
```

* 设置bashrc

```
echo 'rm -rf /tmp/.X1-lock' >> /root/.bashrc
echo 'rm -rf /tmp/.X11-unix/X1' >> /root/.bashrc
```

* 每次启动

```
vncserver -geometry 1920x1080 :1
```

* 使用vnc viewer进行连接

```
xxx.xxx.xxx.xxx:5901
```

