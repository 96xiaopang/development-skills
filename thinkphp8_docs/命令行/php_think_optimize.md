## 生成数据表字段缓存`optimize:schema` 

>[danger] 字段缓存仅在部署模式下生效，并且仅适用于使用`think-orm`的情况，如果你使用了其它的ORM库，则不支持生成。

可以通过生成数据表字段信息缓存，提升数据库查询的性能，避免多余的查询。命令如下：
~~~cmd
php think optimize:schema
~~~

如果是多应用模式，你可以使用下面的指令生成`admin`应用的字段缓存。
~~~cmd
php think optimize:schema admin
~~~

会自动生成当前数据库配置文件中定义的数据表字段缓存，也可以指定数据库连接生成字段缓存（必须有用户权限），例如，下面指定生成`mysql`数据库连接下面的所有数据表的字段缓存信息。

~~~cmd
php think optimize:schema --connection mysql
~~~

>[danger] 没有继承think\Model类的（抽象）模型类不会生成。如果定义了公共模型类，最好把公共模型类定义为抽象类（`abstract`）。

更新数据表字段缓存也是同样的方式，每次执行都会重新生成缓存。如果需要单独更新某个数据表的缓存，可以使用：

~~~cmd
php think optimize:schema --table think_user
~~~

支持指定数据库名称

~~~cmd
php think optimize:schema --table demo.think_user
~~~
