## 快速生成控制器

快速创建`Blog`控制器类库文件
~~~cmd
>php think make:controller Blog
~~~

如果是多应用模式，则需传入应用名
~~~cmd
>php think make:controller index@Blog
~~~

默认生成的是一个资源控制器，包含了资源路由对应的操作方法，如果仅仅生成空的控制器则可以使用：
~~~
>php think make:controller Blog --plain
~~~

如果需要生成多级控制器，可以使用
~~~cmd
>php think make:controller test/Blog
~~~

会生成一个 `app\index\controller\test\Blog` 控制器类。

可以支持 --api 参数生成用于API接口的资源控制器。

## 快速生成模型

和生成控制器类似，执行下面的指令可以生成`Blog`模型类
~~~cmd
>php think make:model Blog
~~~

## 生成带后缀的类库

如果要生成带后缀的类库，可以直接使用：

~~~cmd
>php think make:controller BlogController
~~~

~~~cmd
>php think make:model BlogModel
~~~

## 快速生成中间件

可以使用下面的指令生成一个中间件类。

~~~cmd
>php think make:middleware Auth
~~~

会自动生成一个 `app\middleware\Auth`类文件。

## 创建验证器类

可以使用

~~~cmd
>php think make:validate User
~~~

生成一个 `app\validate\User` 验证器类，然后添加自己的验证规则和错误信息。