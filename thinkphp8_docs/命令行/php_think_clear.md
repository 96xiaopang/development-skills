## 清除缓存文件`clear` 

如果需要清除应用的缓存文件，可以使用下面的命令：

~~~cmd
php think clear
~~~

不带任何参数调用`clear`命令的话，会清除`runtime`目录（包括模板缓存、日志文件及其子目录）下面的所有的文件，但会保留目录。

如果不需要保留空目录，可以使用
~~~cmd
php think clear --dir
~~~

清除日志目录
~~~cmd
php think clear --log
~~~

清除日志目录并删除空目录
~~~cmd
php think clear --log --dir
~~~

清除数据缓存目录
~~~cmd
php think clear --cache
~~~

清除数据缓存目录并删除空目录
~~~cmd
php think clear --cache --dir
~~~

如果需要清除某个指定目录下面的文件，可以使用：

~~~cmd
php think clear --path d:\www\tp\runtime\log\
~~~
