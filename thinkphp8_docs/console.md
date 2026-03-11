ThinkPHP8支持`Console`应用，通过命令行的方式执行一些URL访问不方便或者安全性较高的操作。

我们可以在cmd命令行下面，切换到应用根目录（注意不是web根目录），然后执行`php think`，会出现下面的提示信息：

```shell
>php think
version 8.0.0

Usage:
  command [options] [arguments]

Options:
  -h, --help            Display this help message
  -V, --version         Display this console version
  -q, --quiet           Do not output any message
      --ansi            Force ANSI output
      --no-ansi         Disable ANSI output
  -n, --no-interaction  Do not ask any interactive question
  -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

Available commands:
  build             Build Application Dirs
  clear             Clear runtime file
  help              Displays help for a command
  list              Lists commands
  run               PHP Built-in Server for ThinkPHP
  version           show thinkphp framework version
 make
  make:command      Create a new command class
  make:controller   Create a new resource controller class
  make:event        Create a new event class
  make:listener     Create a new listener class
  make:middleware   Create a new middleware class
  make:model        Create a new model class
  make:service      Create a new Service class
  make:subscribe    Create a new subscribe class
  make:validate     Create a validate class
 optimize
  optimize:route    Build app route cache.
  optimize:schema   Build database schema cache.
 route
  route:list        show route list.
 service
  service:discover  Discover Services for ThinkPHP
 vendor
  vendor:publish    Publish any publishable assets from vendor packages
```

`console`命令的执行格式一般为：

>[info]### >php think 指令 参数

下面介绍下系统自带的几个命令，包括：

|指令 | 描述|
|---|---|
|build|自动生成应用目录和文件|
|help|帮助|
|list|指令列表|
|clear|清除缓存指令|
|run|启动PHP内置服务器|
|version|查看当前框架版本号|
|make\:controller|创建控制器类|
|make\:model|创建模型类|
|make\:command|创建指令类文件|
|make\:validate|创建验证器类|
|make\:middleware|创建中间件类|
|make\:event|创建事件类|
|make\:listener|创建事件监听器类|
|make\:subscribe|创建事件订阅者类|
|make\:service|创建系统服务类|
|optimize\:schema|生成数据表字段缓存文件|
|optimize\:facade|生成Facade注释|
|route\:build|生成注解路由|
|route\:list|查看路由定义|
|service\:discover|自动注册扩展包的系统服务|
|vendor\:publish|自动生成扩展的配置文件|

更多的指令可以自己扩展。

