<center>
    <h1>
        Gerrit + GitLab + GitHub同步方案
    </h1>
</center>


## 简介

这里主要是为了使用Gerrit的代码审核功能，然后又需要GitLab的代码查看功能，最后希望能把代码共享到公共的GitHub仓库上。

所以这里会搭建私有的Gerrit和GitLab仓库，让后由Gerrit自动同步到GitLab，GitLab会自动同步到GitHub上。

为了同步Gerrit和GitLab的账户，这里使用OpenLDAP作为账号管理系统。

* **[Gerrit](https://www.gerritcodereview.com/):** 代码审核管理工具。
* **[GitLab](https://about.gitlab.com/):** Git仓库代码管理工具。
* **[GitHub](https://github.com/):** 一个面向开源及私有软件项目的托管平台。
* **[OpenLDAP](https://www.openldap.org/):** 基于LDAP协议的中心认证服务器，管理账号。

```mermaid
flowchart LR
	subgraph Server
		direction TB
		D(OpenLDAP)
		B(Gerrit)
		C(GitLab)
		B <--> D
		D <--> C
	end
E(GitHub)
	subgraph PC
		A(Code Merge)
	end
A --> B
B --> C
C --> E
classDef Green fill:#D5E8D4,stroke:#15831C,stroke-width:2px,color:#15831C;
classDef Red fill:#F8CECC,stroke:#FF3333,stroke-width:2px,color:#FF3333;
classDef Yellow fill:#FFF2CC,stroke:#D6B656,stroke-width:2px,color:#D6B656;
classDef Blue fill:#DAE8FC,stroke:#007FFF,stroke-width:2px,color:#007FFF;
classDef White fill:#FFF, stroke:#000;
class A Green
class B Blue
class C Blue
class D Blue
class E Red
class PC White
class Server White
```

用户将代码提交到Gerrit，合并入库后，Gerrit会使用同步插件将代码仓与GitLab上的仓库进行同步，GitLab同步到最新的代码后，又将最新的代码同步到GitHub上，以此来进行所有仓库的同步。这里OpenLDAP管理了两个本地仓库的账号系统。

## Docker配置

下面默认的域名是**nsunever.com**，根据自己需要，替换成自己的域名。

### Docker Compose Yaml

创建Docker项目目录，并填写配置文件

```shell
$ mkdir -p /root/docker/compose/gerrit_gitlab_github
$ cd /root/docker/compose/gerrit_gitlab_github
$ vi docker-compose.yml
```

###### **docker-compose.yml**

```yaml
version: '3.6'

# 创建网络容器以桥接的方式进行连接，可以在一个局域网中互相访问
networks:
  git-repo:
    driver: bridge

services:
  gitlab:
    image: 'gitlab/gitlab-ee:latest'
    restart: always
    environment:
      GITLAB_OMNIBUS_CONFIG: |
        external_url 'https://nsunever:9000'
        gitlab_rails['gitlab_shell_ssh_port'] = 9022
        gitlab_rails['ldap_enabled'] = true
        gitlab_rails['ldap_servers'] = YAML.load <<-'EOS'
          main: # 'main' is the GitLab 'provider ID' of this LDAP server
            label: 'LDAP'
            host: ldap #ldap服务地址
            port: 389 #ldap服务端口号
            uid: 'uid'                      			#登录名字使用字段
            bind_dn: 'cn=admin,dc=nsunever,dc=com'   	#ldap管理员登录账号
            password: '123456'                          #ldap管理员密码
            encryption: 'plain'                         #模式
            verify_certificates: true                   #验证证书
            smartcard_auth: false
            active_directory: true   					# 如果是 Active Directory LDAP server 则设为true
            allow_username_or_email_login: false 		# 是否允许email登录
            lowercase_usernames: false  				# 是否将用户名转为小写
            block_auto_created_users: false  			# 是否自动创建用户
            base: 'dc=nsunever,dc=com' 					#从哪个位置搜索用户
        EOS
    ports:
      - '9000:9000'
      - '9022:22'
    volumes:
      - '/root/docker/volumn/gitlab/config:/etc/gitlab'
      - '/root/docker/volumn/gitlab/logs:/var/log/gitlab'
      - '/root/docker/volumn/gitlab/data:/var/opt/gitlab'
    shm_size: '256m'
    depends_on:
      - ldap
    networks:
      - git-repo
  gerrit:
    image: gerritcodereview/gerrit
    ports:
      - "29418:29418"
      - "8081:8081"
    depends_on:
      - ldap
    volumes:
      - /root/docker/volumn/gerrit/etc:/var/gerrit/etc
      - /root/docker/volumn/gerrit/git:/var/gerrit/git'
      - /root/docker/volumn/gerrit/db:/var/gerrit/db
      - /root/docker/volumn/gerrit/index:/var/gerrit/index
      - /root/docker/volumn/gerrit/cache:/var/gerrit/cache
    environment:
      - CANONICAL_WEB_URL=https://nsunever.com:9001
    entrypoint: /entrypoint.sh init                			#初始化Gerrit后需要注释
    networks:
      - git-repo
  ldap:
    image: osixia/openldap
    ports:
      - "9089:389"
      - "9036:636"
    environment:
      LDAP_DOMAIN: nsunever.com
      LDAP_ADMIN_PASSWORD: 123456 						#ldap管理员密码
      LDAP_ORGANISATION: nsunever
    volumes:
      - /root/docker/volumn/ldap/var:/var/lib/ldap
      - /root/docker/volumn/ldap/etc:/etc/ldap/slapd.d
    networks:
      - git-repo
  ldap-admin:
    image: osixia/phpldapadmin
    ports:
      - "9002:443"
    environment:
      - PHPLDAPADMIN_LDAP_HOSTS=ldap
    networks:
      - git-repo
```

### 创建配置文件

Gerrit部分配置需要修改config文件，这里通过目录映射，来事先把配置文件放进去。

#### Gerrit Config

gerrit的配置文件

```shell
$ mkdir -p /root/docker/volumn/gerrit/etc
$ cd /root/docker/volumn/gerrit/etc
$ vi gerrit.config
```

**gerrit.config**

```
[gerrit]
        basePath = git
        canonicalWebUrl = https://nsunever.com:9001
        serverId = 3fa614f5-0f30-4ad7-a1ed-183e4de72343
[index]
        type = LUCENE
[auth]
        type = ldap
        gitBasicAuth = true
[ldap]
        server = ldap://ldap
        username = cn=admin,dc=nsunever,dc=com
        password = 123456
        accountBase = dc=nsunever,dc=com
        groupBase = dc=nsunever,dc=com
        accountPattern = (&(objectClass=person)(uid=${username}))
        accountFullName = displayName
        accountEmailAddress = mail
[sendemail]
        smtpServer = localhost
[sshd]
        listenAddress = *:29418
[httpd]
        listenUrl = http://*:8081/
        filterClass = com.googlesource.gerrit.plugins.ootb.FirstTimeRedirect
        firstTimeRedirectUrl = /login/%23%2F?account_id=1000000
[cache]
        directory = cache
[plugins]
        allowRemoteAdmin = true
[container]
        javaOptions = "-Dflogger.backend_factory=com.google.common.flogger.backend.log4j.Log4jBackendFactory#getInstance"
        javaOptions = "-Dflogger.logging_context=com.google.gerrit.server.logging.LoggingContext#getInstance"
        user = root
        javaHome = /usr/lib/jvm/java-11-openjdk-11.0.16.1.1-1.el8_6.x86_64
        javaOptions = -Djava.security.egd=file:/dev/./urandom
        javaOptions = --add-opens java.base/java.net=ALL-UNNAMED
        javaOptions = --add-opens java.base/java.lang.invoke=ALL-UNNAMED
        javaOptions = -Djava.security.egd=file:/dev/./urandom
        javaOptions = --add-opens java.base/java.net=ALL-UNNAMED
        javaOptions = --add-opens java.base/java.lang.invoke=ALL-UNNAMED
[receive]
        enableSignedPush = false
```

### 初始化Gerrit容器

Gerrit容器需要先初始化。

```shell
$ cd /root/docker/compose/gerrit_gitlab_github
$ docker compose up gerrit
```

这里多半会报没有文件读写权限等错误，简单粗暴的做法就是将刚才的gerrit目录中的文件改为777。

```shell
$ chmod 777 -R /root/docker/volumn/gerrit/*
```

成功后Log中会打印如下：

```shell
gerrit_gitlab_github-gerrit-1 exited with code 0
```

之后就需要注释[docker-compose.yml](#docker-compose.yml)中的gerrit的初始化配置。

```shell
$ vi /root/docker/compose/gerrit_gitlab_github/docker-compose.yml
# entrypoint: /entrypoint.sh init
```

### 初始化所有容器

这里就开始初始化所有容器了，第一次跑的时候不要加-d可以查看Log定位问题

```shell
$ docker compose up
```

### 添加外部访问的端口

添加外部访问端口：

* GitLab: 9000/tcp
* Gerrit: 9001/tcp 29418/udp
* OpenLDAP: 9002/tcp

```shell
$ firewall-cmd --zone=public --add-port=9000/tcp --permanent
$ firewall-cmd --zone=public --add-port=9001/tcp --permanent
$ firewall-cmd --zone=public --add-port=9002/tcp --permanent
$ firewall-cmd --reload
```

### Gerrit Nginx配置

## Gerrit与GitHub直接同步

### 创建GitHub项目

在GitHub上创建需要同步的项目，这里创建的时候最好不要选初始化Commit的，就建空仓库。

### 添加SSH KEY

服务器生成ssh-key并设置到GitHub，如果有直接拷贝就可以了，不用生成。

```shell
$ ssh-keygen -t rsa
```

### 创建Gerrit项目

在Gerrit上创建一个和GitHub同名的项目。

### 配置replication插件

确保Gerrit安装了replication插件，然后在gerrit/etc文件夹下添加replication.config文件

```
[remote "github"]
  url = https://N-ever:xxx_token@github.com/N-ever/${name}.git
  projects = Nsun-Note
  push = +refs/heads/*:refs/heads/*
  push = +refs/tags/*:refs/tags/*
  push = +refs/changes/*:refs/changes/*
  timeout = 30
  threads = 3
```

### 重启Gerrit

```shell
$ ./gerrit/bin/gerrit.sh restart
```

