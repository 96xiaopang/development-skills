ThinkPHP`6.0`的环境要求如下：

>[info] * PHP >= 7.2.5

>[danger] `6.0`版本开始，必须通过`Composer`方式安装和更新，所以你无法通过`Git`下载安装。

## 安装`Composer`

> 如果还没有安装 `Composer`，在 `Linux` 和 `Mac OS X` 中可以运行如下命令：
> ~~~
> curl -sS https://getcomposer.org/installer | php
> mv composer.phar /usr/local/bin/composer
> ~~~
> 在 Windows 中，你需要下载并运行 [Composer-Setup.exe](https://getcomposer.org/Composer-Setup.exe)。
> 如果遇到任何问题或者想更深入地学习 Composer，请参考Composer 文档（[英文文档](https://getcomposer.org/doc/)，[中文文档](http://www.kancloud.cn/thinkphp/composer)）。

由于众所周知的原因，国外的网站连接速度很慢。因此安装的时间可能会比较长，我们建议使用国内镜像。

>[info] 打开命令行窗口（windows用户）或控制台（Linux、Mac 用户）并执行如下命令：
> ~~~
> 阿里云：
> composer config -g repo.packagist composer https://mirrors.aliyun.com/composer/
> 华为云：
> composer config -g repo.packagist composer https://repo.huaweicloud.com/repository/php/
> ~~~

## 安装稳定版

如果你是第一次安装的话，在命令行下面，切换到你的WEB根目录下面并执行下面的命令：

~~~cmd
composer create-project topthink/think tp
~~~

这里的`tp`目录名你可以任意更改，这个目录就是我们后面会经常提到的应用根目录。

如果你之前已经安装过，那么切换到你的**应用根目录**下面，然后执行下面的命令进行更新：

~~~cmd
composer update topthink/framework
~~~

>[danger] 更新操作会删除`thinkphp`目录重新下载安装新版本，但不会影响`app`目录，因此不要在核心框架目录添加任何应用代码和类库。

>[info] 安装和更新命令所在的目录是不同的，更新必须在你的应用根目录下面执行

如果出现错误提示，请根据提示操作或者参考[Composer中文文档](http://www.kancloud.cn/thinkphp/composer)。

## 安装开发版

一般情况下，`composer` 安装的是最新的稳定版本，不一定是最新版本，如果你需要安装实时更新的版本（适合学习过程），可以安装`6.0.x-dev`版本。

~~~cmd
composer create-project topthink/think=6.0.x-dev tp
~~~

## 开启调试模式

应用默认是部署模式，在开发阶段，可以修改环境变量`APP_DEBUG`开启调试模式，上线部署后切换到部署模式。

本地开发的时候可以在应用根目录下面定义`.env`文件。

> 通过`create-project`安装后在根目录会自带一个`.example.env`文件（环境变量示例），你可以直接更名为`.env`文件并根据你的要求进行修改，该示例文件已经开启调试模式

## 测试运行

现在只需要做最后一步来验证是否正常运行。

进入命令行下面，执行下面指令

```
php think run
```

在浏览器中输入地址：

~~~
http://localhost:8000/
~~~

会看到欢迎页面。恭喜你，现在已经完成`ThinkPHP6.0`的安装！

如果你本地80端口没有被占用的话，也可以直接使用
```
php think run -p 80
```
然后就可以直接访问：

~~~
http://localhost/
~~~

>[danger] 实际部署中，应该是绑定域名访问到`public`目录，确保其它目录不在WEB目录下面。