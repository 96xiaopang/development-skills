## 生成配置缓存
在生产环境下面，你可以通过下面的指令生成配置缓存文件。
~~~cmd
php think optimize:config
~~~

执行后，会在`runtime`目录下面生成`config.php`文件。

如果是多应用模式的话，需要增加应用名参数调用指令

~~~cmd
php think optimize:config index
~~~