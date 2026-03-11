## 启动内置服务器

命令行切换到应用根目录后，输入：

~~~cmd
>php think run
~~~

如果启动成功，会输出下面信息，并显示`web`目录位置。
~~~
ThinkPHP Development server is started On <http://0.0.0.0:8000/>
You can exit with `CTRL-C`
Document root is: D:\WWW\tp6/public
~~~

然后你可以直接在浏览器里面访问
~~~
http://127.0.0.1:8000/
~~~

而无须设置`Vhost`，不过需要注意，这个只有web服务器，其它的例如数据库服务的需要自己单独管理。

支持制定IP和端口访问
~~~cmd
>php think run -H tp.com -p 80
~~~

会显示
~~~
ThinkPHP Development server is started On <http://tp.com:80/>
You can exit with `CTRL-C`
Document root is: D:\WWW\tp6/public
~~~

然后你可以直接在浏览器里面访问
~~~
http://tp.com/
~~~
