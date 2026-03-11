实体模型对象是`ThinkORM4.0+`的一个新特性，采用了实体模型后，相当于给模型层做了一个分层设计，把越来越臃肿的模型进行拆分，原来的`Model`层则变成了仓储（Repository）模型，负责数据的查询、关联和事件，及持久化，相对来说侧重于底层操作，而实体模型则承担了数据定义、展示、处理及业务逻辑定义的角色，当然，在较大的项目中，可以单独把业务逻辑拆分为一个逻辑层或服务层，在项目中应尽可能的遵循这个原则进行分工设计。

![](../assets/topwrite/assets/image_1738913333978.png)

如果需要使用`4.0`版本，可以使用下面的命令安装：

```
composer require topthink/think-orm:4.0
```

实体对象的主要优势有：

* **更高效**：实体模型的数据处理和获取更为高效；
* **更易用**：提供了包括视图模型、虚拟模型、自动关联等新特性，更简单使用；
* **模型分层**：Entity层负责数据展示和处理业务逻辑，Model层负责数据库连接、事件、查询范围和关联定义。

众所周知`Model`是建立在`Db`之上的，而实体模型`Entity`是建立在`Model`之上，同属于模型层但分工不同，并且`Entity`类无需做任何的参数设置，模型的定义（包括参数设置、事件定义、获取器和修改器定义、查询范围定义）仍然还是在`Model`。

> 简而言之，一旦定义了`Entity`模型，`Entity`模型就作为数据模型并同时作为逻辑层，`Model`模型则作为仓储模型提供底层支持和数据持久化。你可以和操作Model一样操作实体模型（包括CURD），内部会自动调用Model类。

## 目录
*****
* [定义](https://doc.thinkphp.cn/@think-orm/v4_0/model_define.html)
* [新增](https://doc.thinkphp.cn/@think-orm/v4_0/model_create.html)
* [更新](https://doc.thinkphp.cn/@think-orm/v4_0/model_update.html)
* [查询](https://doc.thinkphp.cn/@think-orm/v4_0/model_query.html)
* [删除](https://doc.thinkphp.cn/@think-orm/v4_0/model_delete.html)
* [获取器](https://doc.thinkphp.cn/@think-orm/v4_0/getter.html)
* [修改器](https://doc.thinkphp.cn/@think-orm/v4_0/setter.html)
* [搜索器](https://doc.thinkphp.cn/@think-orm/v4_0/searcher.html)
* [自动写入](https://doc.thinkphp.cn/@think-orm/v4_0/auto_write_data.html)
* [自动验证](https://doc.thinkphp.cn/@think-orm/v4_0/entity_validate.html)
* [模型输出](https://doc.thinkphp.cn/@think-orm/v4_0/model_conversion.html)
* [虚拟模型](https://doc.thinkphp.cn/@think-orm/v4_0/virtual.html)
* [模型事件](https://doc.thinkphp.cn/@think-orm/v4_0/model_event.html)


