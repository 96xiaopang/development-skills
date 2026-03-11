# 版本更新日志

## `V8.1.4`（2026年1月16日）

* 改进Config类hook方法 增加key参数
* 调整Config类lazy方法
* 修正路由url生成
* 兼容PHP8.5调整
* 新增 optimize 命令
* 改进Request类
* 优化日志文件删除顺序
* 调整"psr/http-message"增加"^2.0"
* 优化 PHP CS Fixer 配置规则
* 路由绑定到命名空间支持控制器后缀
* 改进路由分组的url有效性检查
* 改进Redis缓存驱动
* 改进路由中间件传参导致的问题
* 改进HttpEnd错误日志
* 改进Response类send方法的异常处理

## `V8.1.3`（2025年7月15日）

* 核心移出`ClassNotFoundException`异常，直接使用 `think-container` 中的异常类
* 改进分组绑定的MISS路由支持
* 路由地址的URL不支持直接访问
* `ModelService`兼容orm4.0
* 改进`CallbackDispatch`
* 增加`header`请求过滤检测方法
* 增加`version`方法用于版本控制检测
* 改进改进`withoutmiddleware`对自动layer中间件的支持
* 改进日志的写入确保按照日志的记录时间
* 日志`LogRecord`记录时间信息
* 开启强制路由的不再检查路由地址直接访问
* 路由定义支持分组子目录，支持自动扫描子目录注册分组
* 改进Route类`group`方法用法
* 改进路由的`name`生成
* fixed:路由组设置了中间件等，但子路由没有设置时，合并问题
* 增加`php think optimize:config` 指令
* 改进 `php think route:list`和`php think optimize:route`指令，支持分组子目录规则

## `V8.1.2`（2025年1月15日）
- 改进事件订阅及多级通配符
- 增加`ValidateRuleSet`类 用于更方便的进行数组验证
- 增加验证分组、规则集和规则别名方法
- 路由分组绑定方法增加`prefix`参数 （用于是否自动prefix 默认为true）
- 修正批量验证
- 支持通过`rules`方法定义验证规则（ 返回数组或验证对象）
- 依赖注入支持使用`self`
- 路由Rule支持 `append`、`middleware`方法多次调用 
- 修正通过 `must `属性设置必须验证的字段不生效
- 优化 Cookie 设置（数组 key 为字符串数值时，PHP 会自动转换为 int）
- 修正分组多级路由合并检查
- 改进多模块模式的视图自动渲染定位
- 改进`dateFormat`验证规则
- 多语言增加`auto_detect_browser`参数
- `Response`增加`getCookie`方法
- `Validate`和`Container`组件移出核心并独立依赖
- 改进`pathinfo`兼容获取

## `V8.1.1`（2024年11月27日）
- 完善 PHP 8.4 兼容性
- 改进`parseUrl`方法
- 改进验证类`getError`方法
- 分组绑定自动添加`prefix`
- 改进路由到类的方法，支持控制器中间件
- 自动识别路由到类的layer并支持自动中间件

## `V8.1.0`（2024年11月21日）
 本版本主要改进了路由和验证功能，以及PHP`8.4`兼容支持
* 修复路由使用数组方式报错问题
* 改进验证场景处理
* 路由分组支持默认URL调度和绑定，并且不受强制路由影响
* 自动URL调度功能，支持多模块
* 资源路由支持扩展路由定义
* 支持多模块自动路由规则，并自动执行模块中间件
* 路由新增`when`路由变量验证方法
* 增加枚举类型验证
* 改进数组验证支持指定键名和支持多维数组验证
* 增加路由预定义变量规则 当变量规则为整数或浮点数的时候 自动转换类型
* 路由配置增加`action_bind_param`参数 设置操作方法的参数绑定方式
* 改进系统初始化阶段的异常处理
* 配置增加获取器功能
* 优化异常处理对`json`的判断
* 改进环境变量文件读取 支持公共环境变量文件
* `Validate`增加`accepted`、`acceptedIf`、`declined`、`declinedIf`、`multipleOf`内置规则
* `cookie`设置可以在当前请求生效
* 改进日志备份文件名规则
* 增加`withoutmiddleware`方法用于排除某个路由的中间件
* 优化路由调度
* 改进缓存反序列化的异常处理
* 改进验证异常类 增加`getKey`方法 获取错误字段名
* 改进依赖注入的对象默认值判断
* 调整`invokeAfter`位置
* Request `only`方法支持强制类型转换
* 优化验证类的验证规则判断
* 验证类支持使用`must`属性设置该验证类的必须验证字段 无论是否定义`require`规则
* 缓存增加`fail_delete`配置参数 用于在获取缓存发生异常的时候是否强制删除 
* 缓存get方法`default`参数支持传入闭包
* 改进缓存`pull`方法判断，并增加`default`参数
* 优化智能事件订阅，提高事件响应效率
* 增加`Macroable`方法注入功能
* 改进缓存`serialize`/`unserialize`方法
* 兼容PHP`8.4`

## `V8.0.4`（2024年7月30日）
本版本为常规更新版本，做了一些优化和改进

* `Request`增加`setRootDomain`方法
* 修正`RedirectResponse`的`restore`方法
* `redis`缓存驱动改为使用时才连接
* 标签内的缓存标识列表为空时，不调用 `clearTag `方法
* 修正默认异常模板的编码输出
* 修复文件响应文件名为中文无法正确在浏览器下载中使用的问题
* Session Facade增加注释
* 修正清空路由规则方法未清空分组路由的问题
* `requireCallback `验证规则支持传入数组
* 支持设置控制台默认执行用户
* 异常类增加`#[AlwaysErrorMsg]`注解支持 明确指定始终输出错误信息
* 改进路由到类的方法支持数组方式
* 改进复杂条件验证唯一
* `requireIf`验证支持数组方式
* 修正路由分组的调度检查

## `V8.0.3`（2023年10月19日）
本版本为修正版本，主要完善了PSR规范的兼容性
* 改进`remember`方法的有效期兼容性
* 为`require`获取参数方法指定正确的`filter`类型
* 取消缓存读取和写入次数计数 废弃相关方法
* 兼容低版本的`psr/log`、`psr/simple-cache`
* 改进路由的`cache`方法参数类型
* 异常页面手册地址调整
* 优化`think-orm`库在常驻内存使用的时候可能的内存溢出问题
* 增加[`think-cors`](<https://github.com/top-think/think-cors>)扩展用于处理跨域问题

## `V8.0.2`（2023年8月15日）
本版本为修正版本，主要修正了：
* 改进版本号获取指令（App类VERSION常量废弃）
* 修正Http类`dispatchToRoute`方法
* 改进请求对象获取根域名方法
* Feat: 自动获取 php 命令路径，而不是固定用 php
* fix: is_executable() 的参数不正确
* 直接使用 `PHP_BINARY`常量
* 缓存类set方法有效期参数兼容`DateTimeInterface`参数
* 修正日志监听事件处理

## `V8.0.1`（2023年7月11日）
本版本为修正版本，主要修正了：
* 修正`php think optimize:schema`指令当模型存在子目录的错误
* 修正路由分组合并解析
* 修正`request_cache_tag`判断
* 完善缓存文件锁机制
* 修正部分方法的参数类型
* 修正`MISS`路由

## `V8.0.0`（2023年6月30日）
基于PHP`8.0`重构版本，主要特性：

* 基于PHP`8.0+`重构
* 增加`startWith`、`endWith`及`contain`验证规则
* 简化验证类的正则
* 优化路由检测
* 升级`PSR`依赖
* 依赖`think-orm`3.0版本

