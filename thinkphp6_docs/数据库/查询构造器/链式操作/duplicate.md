用于设置`DUPLICATE`查询，用法示例：

~~~
Db::name('user')
    ->duplicate(['score' => 10])
    ->insert(['name' => 'think']);
~~~