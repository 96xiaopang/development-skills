## 输出并生成路由列表

假设你的路由定义文件内容为：

~~~
Route::get('think', function () {
    return 'hello,ThinkPHP6!';
});

Route::resource('blog', 'Blog');

Route::get('hello/:name', 'index/hello')->ext('html');
~~~

可以使用下面的指令查看定义的路由列表
~~~
php think route:list
~~~

如果是多应用模式的话，需要改成
~~~
php think route:list index
~~~

输出结果类似于下面的显示：
~~~
+----------------+-------------+--------+-------------+
| Rule           | Route       | Method | Name        | 
+----------------+-------------+--------+-------------+
| think          | <Closure>   | get    |             | 
| hello/<name>   | index/hello | get    | index/hello | 
| blog           | Blog/index  | get    | Blog/index  | 
| blog           | Blog/save   | post   | Blog/save   |  
| blog/create    | Blog/create | get    | Blog/create |  
| blog/<id>/edit | Blog/edit   | get    | Blog/edit   | 
| blog/<id>      | Blog/read   | get    | Blog/read   |
| blog/<id>      | Blog/update | put    | Blog/update | 
| blog/<id>      | Blog/delete | delete | Blog/delete | 
+----------------+-------------+--------+-------------+
~~~

并且同时会在runtime目录下面生成一个`route_list.php`的文件，内容和上面的输出结果一致，方便你随时查看。

> 如果你的路由定义发生改变的话， 则需要重新调用该指令，会自动更新上面生成的缓存文件。
> 

## 输出样式

支持定义不同的样式输出，例如：

~~~
php think route:list box
~~~

输出结果变为：

~~~
┌────────────────┬─────────────┬────────┬─────────────┐
│ Rule           │ Route       │ Method │ Name        │ 
├────────────────┼─────────────┼────────┼─────────────┤
│ think          │ <Closure>   │ get    │             │ 
│ hello/<name>   │ index/hello │ get    │ index/hello │
│ blog           │ Blog/index  │ get    │ Blog/index  │
│ blog           │ Blog/save   │ post   │ Blog/save   │
│ blog/create    │ Blog/create │ get    │ Blog/create │
│ blog/<id>/edit │ Blog/edit   │ get    │ Blog/edit   │
│ blog/<id>      │ Blog/read   │ get    │ Blog/read   │ 
│ blog/<id>      │ Blog/update │ put    │ Blog/update │
│ blog/<id>      │ Blog/delete │ delete │ Blog/delete │
└────────────────┴─────────────┴────────┴─────────────┘
~~~

~~~
php think route:list box-double
~~~

输出结果变为：

~~~
╔════════════════╤═════════════╤════════╤═════════════╗
║ Rule           │ Route       │ Method │ Name        ║
╠────────────────╪─────────────╪────────╪─────────────╣
║ think          │ <Closure>   │ get    │             ║
║ hello/<name>   │ index/hello │ get    │ index/hello ║
║ blog           │ Blog/index  │ get    │ Blog/index  ║
║ blog           │ Blog/save   │ post   │ Blog/save   ║
║ blog/create    │ Blog/create │ get    │ Blog/create ║
║ blog/<id>/edit │ Blog/edit   │ get    │ Blog/edit   ║
║ blog/<id>      │ Blog/read   │ get    │ Blog/read   ║
║ blog/<id>      │ Blog/update │ put    │ Blog/update ║
║ blog/<id>      │ Blog/delete │ delete │ Blog/delete ║
╚════════════════╧═════════════╧════════╧═════════════╝
~~~
    

~~~
php think route:list markdown
~~~

输出结果变为：
~~~
| Rule           | Route       | Method | Name        |
|----------------|-------------|--------|-------------|
| think          | <Closure>   | get    |             |
| hello/<name>   | index/hello | get    | index/hello |
| blog           | Blog/index  | get    | Blog/index  |
| blog           | Blog/save   | post   | Blog/save   |
| blog/create    | Blog/create | get    | Blog/create |
| blog/<id>/edit | Blog/edit   | get    | Blog/edit   |
| blog/<id>      | Blog/read   | get    | Blog/read   | 
| blog/<id>      | Blog/update | put    | Blog/update |
| blog/<id>      | Blog/delete | delete | Blog/delete | 
~~~
    
## 排序支持

如果你希望生成的路由列表按照路由规则排序，可以使用

~~~
php think route:list -s rule
~~~

输出结果变成：

~~~
+----------------+-------------+--------+-------------+
| Rule           | Route       | Method | Name        | 
+----------------+-------------+--------+-------------+
| blog           | Blog/index  | get    | Blog/index  |
| blog           | Blog/save   | post   | Blog/save   | 
| blog/<id>      | Blog/read   | get    | Blog/read   |
| blog/<id>      | Blog/update | put    | Blog/update |
| blog/<id>      | Blog/delete | delete | Blog/delete | 
| blog/<id>/edit | Blog/edit   | get    | Blog/edit   | 
| blog/create    | Blog/create | get    | Blog/create |
| hello/<name>   | index/hello | get    | index/hello |
| think          | <Closure>   | get    |             |
+----------------+-------------+--------+-------------+
~~~

同样的，你还可以按照请求类型排序

~~~
php think route:list -s method
~~~

输出结果变为：

~~~
+----------------+-------------+--------+-------------+
| Rule           | Route       | Method | Name        | 
+----------------+-------------+--------+-------------+
| blog/<id>      | Blog/delete | delete | Blog/delete |
| think          | <Closure>   | get    |             |
| hello/<name>   | index/hello | get    | index/hello |
| blog           | Blog/index  | get    | Blog/index  |
| blog/create    | Blog/create | get    | Blog/create | 
| blog/<id>/edit | Blog/edit   | get    | Blog/edit   |
| blog/<id>      | Blog/read   | get    | Blog/read   |
| blog           | Blog/save   | post   | Blog/save   |
| blog/<id>      | Blog/update | put    | Blog/update | 
+----------------+-------------+--------+-------------+
~~~


> 支持排序的字段名包括：`rule`、`route`、`name`、`method`和`domain`（全部小写）。

##  输出详细信息

如果你希望看到更多的路由参数和变量规则，可以使用

~~~
php think route:list -m
~~~

输出结果变为：

~~~
+----------------+-------------+--------+-------------+--------+-------------------------+---------+
| Rule           | Route       | Method | Name        | Domain | Option                  | Pattern |
+----------------+-------------+--------+-------------+--------+-------------------------+---------+
| think          | <Closure>   | get    |             |        | []                      | []      |
| hello/<name>   | index/hello | get    | index/hello |        | {"ext":"html"}          | []      |
| blog           | Blog/index  | get    | Blog/index  |        | {"complete_match":true} | []      |
| blog           | Blog/save   | post   | Blog/save   |        | {"complete_match":true} | []      |
| blog/create    | Blog/create | get    | Blog/create |        | []                      | []      |
| blog/<id>/edit | Blog/edit   | get    | Blog/edit   |        | []                      | []      |
| blog/<id>      | Blog/read   | get    | Blog/read   |        | []                      | []      |
| blog/<id>      | Blog/update | put    | Blog/update |        | []                      | []      |
| blog/<id>      | Blog/delete | delete | Blog/delete |        | []                      | []      |
+----------------+-------------+--------+-------------+--------+-------------------------+---------+
~~~
