ThinkPHP 具备自动创建功能，可以用来自动生成需要的应用及目录结构和文件等。

>[danger] 本指令需要安装多应用扩展后才支持。

## 快速生成应用

如果使用了多应用模式，可以快速生成一个应用，例如生成`demo`应用的指令如下：
~~~cmd
>php think build demo
~~~
如果看到输出
~~~
Successed
~~~
则表示自动生成应用成功。

会自动生成`demo`应用，自动生成的应用目录包含了`controller`、`model`和`view`目录以及`common.php`、`middleware.php`、`event.php`和`provider.php`等文件。

生成成功后，我们可以直接访问`demo`应用

会显示
```
您好！这是一个[demo]示例应用
```

## 应用结构自定义

如果你希望自定义生成应用的结构，可以在app目录下增加一个`build.php`文件，内容如下：
~~~
return [
    // 需要自动创建的文件
    '__file__'   => [],
    // 需要自动创建的目录
    '__dir__'    => ['controller', 'model', 'view'],
    // 需要自动创建的控制器
    'controller' => ['Index'],
    // 需要自动创建的模型
    'model'      => ['User'],
    // 需要自动创建的模板
    'view'       => ['index/index'],
];
~~~
可以给定义需要自动生成的文件和目录，以及MVC类。

* `__dir__` 表示生成目录（支持多级目录）
* `__file__` 表示生成文件（默认会生成`common.php`、`middleware.php`、`event.php`和`provider.php`文件，无需定义）
* `controller `表示生成控制器类
* `model`表示生成模型类
* `view`表示生成模板文件（支持子目录）

并且会自动生成应用的默认`Index`访问控制器文件用于显示应用的欢迎页面。





