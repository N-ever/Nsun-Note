<center>
  <h1>
Mac OS Env
  </h1>
</center>


## 安装Brew

```shell
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

安装完使用命令将brew添加到Env中。

```shell
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/evern/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

