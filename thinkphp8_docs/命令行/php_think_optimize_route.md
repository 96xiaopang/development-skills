## 生成路由映射缓存`optimize:route` 

>[danger] 路由映射缓存用于开启路由延迟解析的情况下，支持路由反解的URL生成，如果你没有开启路由延迟解析或者没有使用URL路由反解生成则不需要生成。

生成路由映射缓存的命令：

~~~cmd
php think optimize:route
~~~

执行后，会在`runtime`目录下面生成`route.php`文件。

如果是多应用模式的话，需要增加应用名参数调用指令

~~~cmd
php think optimize:route index
~~~