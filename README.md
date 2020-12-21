# Rainbond Python 组件示例

## 项目介绍

本项目是一个使用 Flask 框架编写的简单的 Python 云原生组件示例，最小的目录结构如下：

```
.
├── runtime.txt
├── app.py
├── Procfile
├── README.md
├── requirements.txt
```

### 本地开发与测试

Python 云原生组件项目 Rainbond 平台上通过 [gunicorn](https://gunicorn.org/) 运行。

而 Gunicorn 是一个 Python WSGI UNIX 的 HTTP 服务器，只支持 Linux 系统，因此如果你使用的不是 Linux 操作系统，你也可以通过其他方式运行，例如：

- 通过 [VirtualEnv](https://virtualenv.pypa.io/en/latest/) 创建一个独立的 Python 运行环境并在里面测试项目。
- 通过 Windows 10 应用商店自带的 Linux 子系统来运行项目。

```
$ pip install -r requirements.txt
$ gunicorn app:app
```

访问 *http://127.0.0.1:8000* 查看项目运行效果。

### Rainbond支持规范

平台默认会根据源码根目录是否有 **requirements.txt** 文件来识别为 Python 项目。

#### 平台编译运行机制

1. 预编译处理会探测是否定义了启动命令配置文件 **Procfile**，如果未定义会生成默认 Flask/Django 启动配置文件；
2. 预编译处理完成后，会根据语言类型选择 Python 的 *buildpack* 去编译项目，在编译过程中会安装定义的 Python 版本以及相关 Python 依赖；
3. 编译完成后会检查是否在平台设置了 `Procfile` 参数，若配置了会重写启动命令配置文件 **Procfile**；

#### Python项目源码规范

在 Rainbond 平台运行的 Python 源码程序至少需要满足如下条件：

- 本地可以正常运行部署的 Python 程序
- 项目可以托管到 *git* 仓库
- 项目根目录下必须存在 **requirements.txt**，用来管理 Python 项目的依赖，也是 Rainbond 识别为 Python 语言的必要条件
- 项目根目录下需要定义 **Procfile**，用来定义程序启动方式
- 项目根目录下存在 **runtime.txt**，用来定义当前项目的 Python 使用版本

##### requirements.txt规范

若程序没有依赖关系，可使 **requirements.txt** 为空文件，若无 **requirements.txt** 可用如下命令生成：

```
$ pip freeze > requirements.txt
```

##### Procfile规范

如果项目未定义 **Procfile** 文件，平台默认会生成默认 **Procfile** 来运行 *War* 包：

```
web: gunicorn app:app --log-file - --access-logfile - --error-logfile -
```

上述是默认 **Procfile**，如果需要扩展更多启动参数，可以自定义 **Procfile**：

1. `web:` 和 `gunicorn` 之间有一个空格
2. 文件结尾不能包含特殊字符

##### runtime.txt规范

推荐使用 **runtime.txt** 来定义 Python 版本，若未定义，Rainbond 将会默认使用 *python-3.6.6* 版本。

默认支持python版本如下：

- python 2.7.x
  - python-2.7.9
  - python-2.7.10
  - python-2.7.13
  - python-2.7.14
  - python-2.7.15
- python 3.x
  - python-3.4.3
  - python-3.5.3
  - python-3.6.0
  - python-3.6.1 
  - python-3.6.2
  - python-3.6.3
  - python-3.6.4
  - python-3.6.5
  - python-3.6.6 
  - python-3.7.0
    
更多内容请查看 [基于源代码创建Python组件](https://www.rainbond.com/docs/component-create/language-support/python/) 文档。

## 存储组件

在云原生的体系中，数据库是一个独立的组件，是原生运行在容器云平台里的一个分布式数据库，真正做到了存储和计算的完全分离。

在 **计算组件** 和 **存储组件** 分离的情况下，**计算组件** 需要通过 **存储组件** 的 *依赖 > 组件连接信息* 中的数据库连接信息来访问 **存储组件**。这个Demo使用的是 MongoDB 数据库，需要 **2** 个标准的 MongoDB 依赖信息：

- MONGODB_HOST: 连接地址
- MONGODB_PORT: 端口

更多内容请查看 [通信变量注入](https://www.rainbond.com/docs/user-manual/component-connection/connection_env/) 和 [服务间通信（服务注册与服务发现）](https://www.rainbond.com/docs/user-manual/component-connection/regist_and_discover/) 两份文档。

### Docker镜像安装

Rainbond 应用商店的 MongoDB 版本过低，为了更好的体验，建议从 [Docker Hub](https://hub.docker.com/_/mongo?tab=tags&page=1&ordering=last_updated) 获取镜像，在 “镜像地址” 栏输入 `mongo`，自动安装最新版本的 MongoDB 数据库组件。

### 配置依赖

在 MongoDB 组件的 *依赖 > 端口列表* 中找到 `27017` 端口，开放 “对内服务”，修改 “使用别名” 为 `MONGODB`。

通过上一步，就可以在 *依赖 > 组件连接信息* 中看到 `MONGODB_HOST` 和 `MONGODB_PORT` 两个变量。
