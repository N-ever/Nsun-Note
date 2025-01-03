<center>
    <h1>
        Basic Env
    </h1>
</center>


## 设置root密码

```shell
passwd
```

## 添加用户

```shell
adduser evern
```

## 更新软件包

```shell
apt update
apt upgrade
```

## 安装必备软件

```shell
apt install sudo
apt install -y openssh-server openssh-client
apt install -y iputils-ping
apt install -y zsh
apt install -y git
apt install -y curl
apt install -y gcc g++
apt-get -y install language-pack-en # locale -a字符集没有，但是locale设置了，解决zsh print_icon问题
```

## 安装[Neovim](https://github.com/neovim/neovim)

```shell
curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
chmod u+x nvim.appimage
./nvim.appimage --appimage-extract
./squashfs-root/AppRun --version
sudo mv squashfs-root /
sudo ln -s /squashfs-root/AppRun /usr/bin/nvim
```

## 添加sudo权限

```shell
visudo
# evern   ALL=(ALL:ALL) ALL
```

## 配置zsh

### 安装[oh-my-zsh](https://github.com/robbyrussell/oh-my-zsh)

```shell
sh -c "$(wget -O- https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

### 下载主题[powerlevel9k](https://github.com/Powerlevel9k/powerlevel9k)

```shell
git clone https://github.com/bhilburn/powerlevel9k.git ~/.oh-my-zsh/custom/themes/powerlevel9k
```

#### 配置主题字体

```shell
git clone https://github.com/powerline/fonts.git --depth=1
cd font
./install.sh
```

### 下载插件

#### 历史记录补全

```
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

```bash
#.zshrc
plugins=(zsh-autosuggestions)
```





### 配置.zshrc

```
export TERM="xterm-256color"
# If you come from bash you might have to change your $PATH.
# export PATH=$HOME/bin:/usr/local/bin:$PATH

# Path to your oh-my-zsh installation.
export ZSH="/home/evern/.oh-my-zsh"

# Set name of the theme to load. Optionally, if you set this to "random"
# it'll load a random theme each time that oh-my-zsh is loaded.
# See https://github.com/robbyrussell/oh-my-zsh/wiki/Themes
ZSH_THEME="powerlevel9k/powerlevel9k"

if [[ $ZSH_THEME == "powerlevel9k/powerlevel9k" ]]; then
    POWERLEVEL9K_VCS_GIT_HOOKS=(git-aheadbehind git-remotebranch)
    POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(anaconda user virtualenv dir rbenv vcs)
    POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(time)
    POWERLEVEL9K_VCS_SHOW_SUBMODULE_DIRTY=false
    POWERLEVEL9K_VCS_HIDE_TAGS=true
    POWERLEVEL9K_PROMPT_ON_NEWLINE=true
fi
# Set list of themes to load
# Setting this variable when ZSH_THEME=random
# cause zsh load theme from this variable instead of
# looking in ~/.oh-my-zsh/themes/
# An empty array have no effect
# ZSH_THEME_RANDOM_CANDIDATES=( "robbyrussell" "agnoster" )

# Uncomment the following line to use case-sensitive completion.
# CASE_SENSITIVE="true"

# Uncomment the following line to use hyphen-insensitive completion. Case
# sensitive completion must be off. _ and - will be interchangeable.
# HYPHEN_INSENSITIVE="true"

# Uncomment the following line to disable bi-weekly auto-update checks.
# DISABLE_AUTO_UPDATE="true"

# Uncomment the following line to change how often to auto-update (in days).
# export UPDATE_ZSH_DAYS=13

# Uncomment the following line to disable colors in ls.
# DISABLE_LS_COLORS="true"

# Uncomment the following line to disable auto-setting terminal title.
# DISABLE_AUTO_TITLE="true"

# Uncomment the following line to enable command auto-correction.
# ENABLE_CORRECTION="true"

# Uncomment the following line to display red dots whilst waiting for completion.
# COMPLETION_WAITING_DOTS="true"
# Uncomment the following line if you want to disable marking untracked files
# under VCS as dirty. This makes repository status check for large repositories
# much, much faster.
# DISABLE_UNTRACKED_FILES_DIRTY="true"

# Uncomment the following line if you want to change the command execution time
# stamp shown in the history command output.
# You can set one of the optional three formats:
# "mm/dd/yyyy"|"dd.mm.yyyy"|"yyyy-mm-dd"
# or set a custom format using the strftime function format specifications,
# see 'man strftime' for details.
# HIST_STAMPS="mm/dd/yyyy"

# Would you like to use another custom folder than $ZSH/custom?
# ZSH_CUSTOM=/path/to/new-custom-folder

# Which plugins would you like to load? (plugins can be found in ~/.oh-my-zsh/plugins/*)
# Custom plugins may be added to ~/.oh-my-zsh/custom/plugins/
# Example format: plugins=(rails git textmate ruby lighthouse)
# Add wisely, as too many plugins slow down shell startup.
plugins=(
  git autojump zsh-autosuggestions
)
source $ZSH/oh-my-zsh.sh

# User configuration

# export MANPATH="/usr/local/man:$MANPATH"

# You may need to manually set your language environment
# export LANG=en_US.UTF-8
# export LC_ALL=en_US.UTF-8

# Preferred editor for local and remote sessions
# if [[ -n $SSH_CONNECTION ]]; then
#   export EDITOR='vim'
# else
#   export EDITOR='mvim'
# fi

# Compilation flags
# export ARCHFLAGS="-arch x86_64"

# ssh
# export SSH_KEY_PATH="~/.ssh/rsa_id"

# Set personal aliases, overriding those provided by oh-my-zsh libs,
# plugins, and themes. Aliases can be placed here, though oh-my-zsh
# users are encouraged to define aliases within the ZSH_CUSTOM folder.
# For a full list of active aliases, run `alias`.
#
# Example aliases
# alias zshconfig="mate ~/.zshrc"
# alias ohmyzsh="mate ~/.oh-my-zsh"
setopt no_nomatch

alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'
alias g='ack'
alias fn="find .| grep"
alias repoclean="repo forall -c 'git clean -df;git co .'"
alias logz="adb logcat | grep zhujie"
alias loge="adb logcat -v time *:e"
alias logg="adb logcat | grep"

alias t="tmux"
alias tn="tmux new -s"
alias ta="tmux attach -t"
alias tl="tmux ls"
alias tk="tmux kill-session -t"
alias hh="export http_proxy=http://127.0.0.1:8123;export https_proxy=http://127.0.0.1:8123"
alias hn="unset http_proxy;unset https_proxy"

alias vi="nvim"
```

## 启动并设置服务自启动

```shell
systemctl start ssh
systemctl enable ssh
```

## 安装[conda](https://docs.conda.io/en/latest/miniconda.html)

```shell
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```

