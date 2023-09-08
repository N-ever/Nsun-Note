<center>
  <h1>
    编译
  </h1>
</center>

## 下载代码

### 下载工具

```
git clone https://chromium.googlesource.com/chromium/tools/depot_tools.git
```

### 创建代码目录

```
mkdir chromium;cd chromium
```

### 设置代理

```
export https_proxy=http://127.0.0.1:7890 http_proxy=http://127.0.0.1:7890 all_proxy=socks5://127.0.0.1:7890
```

```
git config --global http.proxy $http_proxy
git config --global https.proxy $https_proxy
```

### 配置环境

```
CUR_DIR=`pwd`;ROOT_DIR=`dirname $CUR_DIR`;echo \
"export PATH=$ROOT_DIR/depot_tools:\$PATH" > env.sh
```

```
source env.sh
```

### 拉取Android代码

```
fetch --nohooks --no-history android
```

### 更新下载工具

```
gclient runhook
gclient sync
```

## 配置环境

```
build/install-build-deps.sh --android
```

### 配置文件

```bash
gn args out/Default
```

```text
target_os = "android"
target_cpu = "arm64"
```

### 查看配置

```bash
gn args --list out/Default
```

## 编译

```bash
autoninja -C out/Default chrome_public_apk
```
