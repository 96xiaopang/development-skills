---
name: thinkphp6
description: ThinkPHP 6.x 完整开发技能。当用户需要使用 ThinkPHP6 开发任何功能时必须使用此 Skill，包括：路由定义、控制器编写、模型操作、数据库查询、中间件、事件、验证器、请求响应处理、缓存、Session/Cookie、文件上传、视图模板、命令行、多应用模式、依赖注入容器、Facade、错误日志等所有 ThinkPHP6 开发场景。只要用户提到 TP6、thinkphp6、think6 或在 ThinkPHP 6.x 版本下开发，务必触发此技能。
---

# ThinkPHP 6.x 开发技能手册

> 适用版本：ThinkPHP 6.0 / 6.1，PHP 要求 7.2+

## 目录

- [项目安装与目录结构](#安装)
- [路由](#路由)
- [控制器](#控制器)
- [请求](#请求)
- [响应](#响应)
- [数据库与查询构造器](#数据库)
- [模型 ORM](#模型)
- [验证](#验证)
- [中间件](#中间件)
- [事件系统](#事件)
- [缓存](#缓存)
- [Session / Cookie](#session--cookie)
- [文件上传](#文件上传)
- [视图模板](#视图)
- [命令行 Console](#命令行)
- [容器与依赖注入](#容器与依赖注入)
- [多应用模式](#多应用模式)
- [错误与日志](#错误与日志)
- [助手函数速查](#助手函数)

---

## 安装

```bash
# 通过 Composer 创建项目
composer create-project topthink/think tp6

# 启动内置服务器
php think run
# 指定 IP 和端口
php think run -H 0.0.0.0 -p 8080
```

**单应用目录结构（默认）：**
```
tp6/
├── app/
│   ├── controller/       # 控制器
│   ├── model/            # 模型
│   ├── view/             # 视图
│   ├── middleware.php     # 中间件注册
│   ├── event.php         # 事件注册
│   └── provider.php      # 容器绑定
├── config/               # 配置文件目录
├── public/               # Web 根目录（入口文件 index.php）
├── route/                # 路由定义目录
├── runtime/              # 运行时目录（缓存、日志）
└── vendor/
```

**命名规范：**
- 类文件：大驼峰 `UserController.php`
- 方法名：小驼峰 `getUserInfo()`
- 配置/变量：小写+下划线 `user_name`
- 路由：小写 `user/profile`

---

## 路由

**路由定义文件：** `route/app.php`

```php
use think\facade\Route;

// 基本路由（GET/POST/PUT/DELETE/PATCH/ANY）
Route::get('hello/:name', 'index/hello');
Route::post('user/create', 'user/create');
Route::any('login', 'user/login');

// 带参数和正则约束
Route::get('article/:id', 'article/read')
    ->pattern(['id' => '\d+']);

// 路由分组
Route::group('api', function () {
    Route::get('user/:id', 'api.User/read');
    Route::post('user', 'api.User/save');
})->middleware(\app\middleware\Auth::class);

// 资源路由（自动生成 index/create/save/read/edit/update/delete）
Route::resource('user', 'User');

// 域名路由
Route::domain('admin.example.com', function () {
    Route::get('/', 'admin/Index/index');
});

// 路由中间件
Route::get('profile', 'User/profile')->middleware('auth');

// MISS 路由（全局 404）
Route::miss('error/notfound');

// 生成 URL
url('user/read', ['id' => 1]);           // /user/read/id/1
url('user/read', ['id' => 1])->domain(true); // 带域名

// 跨域支持
Route::get('api/list', 'api/list')->allowCrossDomain([
    'Access-Control-Allow-Origin' => '*',
]);
```

**URL 访问格式（无路由）：**
```
http://domain/index.php/模块/控制器/操作/参数名/参数值
```

---

## 控制器

```php
<?php
namespace app\controller;

use think\Request;
use think\facade\View;

class User
{
    // 构造方法注入 Request
    public function __construct(protected Request $request) {}

    public function index()
    {
        return 'Hello ThinkPHP6';
    }

    // 接收参数
    public function read(int $id)
    {
        return json(['id' => $id]);
    }

    // 视图渲染
    public function profile()
    {
        View::assign('name', 'ThinkPHP');
        return view(); // 自动对应 view/user/profile.html
    }
}
```

**资源控制器方法对照：**

| HTTP 方法 | 路由          | 控制器方法 | 说明         |
|-----------|--------------|-----------|------------|
| GET       | /user        | index     | 资源列表     |
| GET       | /user/create | create    | 创建表单     |
| POST      | /user        | save      | 保存新建     |
| GET       | /user/:id    | read      | 显示单个     |
| GET       | /user/:id/edit | edit   | 编辑表单     |
| PUT       | /user/:id    | update    | 更新资源     |
| DELETE    | /user/:id    | delete    | 删除资源     |

**控制器中间件：**
```php
class User
{
    protected $middleware = ['auth' => ['except' => ['login']]];
}
```

---

## 请求

```php
use think\facade\Request;

// 获取参数
Request::param('name');              // 自动判断请求类型
Request::get('page', 1);            // GET 参数，默认值 1
Request::post('data');              // POST 参数
Request::put('field');              // PUT 参数
Request::input('param.key');        // 支持.号分隔获取数组
Request::only(['name', 'email']);    // 只获取指定参数
Request::except(['token']);          // 排除指定参数

// 请求类型
Request::method();     // GET/POST/PUT/DELETE
Request::isGet();
Request::isPost();
Request::isAjax();
Request::isPjax();

// 请求信息
Request::host();
Request::url();
Request::ip();
Request::header('content-type');

// 参数绑定（方法注入，推荐）
public function read(Request $request, int $id) {
    $name = $request->get('name');
}
```

---

## 响应

```php
// JSON 响应
return json(['code' => 0, 'data' => $data]);

// XML 响应
return xml($data);

// 重定向
return redirect('https://www.example.com');
return redirect('/user/login');

// 文件下载
return download('/path/to/file.zip', 'download.zip');

// 设置响应码和 Header
return json($data)->code(201)->header(['X-Token' => 'abc']);

// 视图响应
return view('user/index', ['name' => 'tp6']);

// 纯文本
return response('Hello', 200, ['Content-Type' => 'text/plain']);
```

---

## 数据库

**配置文件：** `config/database.php`

```php
// 基本连接
Db::table('think_user')->where('id', 1)->find();
Db::name('user')->where('id', 1)->find(); // 自动加表前缀

// 查询数据
Db::table('user')->find();          // 查询一条
Db::table('user')->select();        // 查询多条（返回数组）
Db::table('user')->column('name');  // 返回单列数组
Db::table('user')->value('name');   // 返回单个值

// 链式操作
Db::name('user')
    ->field('id,name,email')         // 指定字段
    ->where('status', 1)             // 等值条件
    ->where('age', '>', 18)          // 比较条件
    ->whereIn('id', [1, 2, 3])
    ->whereBetween('age', [18, 30])
    ->whereLike('name', '%think%')
    ->whereNull('deleted_at')
    ->whereNotNull('email')
    ->order('id', 'desc')
    ->limit(10)
    ->page(1, 10)                     // 分页（页码, 每页数量）
    ->select();

// WHERE 闭包（复杂条件）
Db::name('user')->where(function($query) {
    $query->where('age', '>', 18)->whereOr('vip', 1);
})->select();

// JOIN
Db::name('user')
    ->alias('u')
    ->join('order o', 'u.id = o.user_id', 'LEFT')
    ->select();

// 聚合查询
Db::name('user')->count();
Db::name('user')->max('age');
Db::name('user')->sum('score');
Db::name('user')->avg('score');

// 添加数据
Db::name('user')->insert(['name' => 'tp', 'email' => 'tp@qq.com']);
Db::name('user')->insertAll([['name'=>'a'], ['name'=>'b']]); // 批量
$id = Db::name('user')->insertGetId(['name' => 'tp']);       // 返回主键

// 更新数据
Db::name('user')->where('id', 1)->update(['name' => 'new']);
Db::name('user')->where('id', 1)->inc('score', 5);  // 字段自增
Db::name('user')->where('id', 1)->dec('score', 1);  // 字段自减

// 删除数据
Db::name('user')->where('id', 1)->delete();

// 事务
Db::transaction(function () {
    Db::name('order')->insert([...]);
    Db::name('stock')->dec('num', 1)->where('id', 1)->update();
});

// 原生 SQL
Db::query('SELECT * FROM user WHERE id = ?', [1]);
Db::execute('UPDATE user SET name = ? WHERE id = ?', ['tp', 1]);

// 分页
$list = Db::name('user')->paginate(10);        // 分页，每页 10 条
$list = Db::name('user')->paginate(['list_rows'=> 10, 'page' => 2]);

// 获取 SQL（调试用）
Db::name('user')->where('id', 1)->fetchSql()->find();

// 缓存查询
Db::name('user')->cache(true, 60)->where('id', 1)->find();
```

---

## 模型

```php
<?php
namespace app\model;

use think\Model;
use think\model\concern\SoftDelete;

class User extends Model
{
    // 自定义表名（默认为 think_user，取决于前缀配置）
    protected $table = 'users';
    
    // 主键（默认 id）
    protected $pk = 'user_id';
    
    // 自动时间戳（create_time / update_time）
    protected $autoWriteTimestamp = true;
    
    // 软删除
    use SoftDelete;
    protected $deleteTime = 'deleted_at';

    // 只读字段
    protected $readonly = ['username'];

    // 类型转换
    protected $type = [
        'score' => 'integer',
        'config' => 'json',
        'birthday' => 'timestamp:Y-m-d',
    ];

    // 获取器（getXxxAttr）
    public function getFullNameAttr($value, $data)
    {
        return $data['first_name'] . ' ' . $data['last_name'];
    }

    // 修改器（setXxxAttr）
    public function setPasswordAttr($value)
    {
        return md5($value);
    }

    // 搜索器（searchXxxAttr），用于 withSearch
    public function searchNameAttr($query, $value)
    {
        $query->whereLike('name', "%$value%");
    }
}
```

**模型 CRUD：**

```php
// 查询
$user = User::find(1);
$user = User::where('email', 'a@b.com')->find();
$users = User::where('status', 1)->select();
$users = User::withSearch(['name'], ['name' => 'think'])->select();

// 新增
$user = new User;
$user->name = 'tp6';
$user->save();

User::create(['name' => 'tp6', 'email' => 'tp@qq.com']);

// 更新
$user = User::find(1);
$user->name = 'new name';
$user->save();

User::where('id', 1)->update(['name' => 'new name']);

// 删除
User::destroy(1);
User::destroy([1, 2, 3]);
User::where('id', '>', 10)->delete();

// 软删除恢复
User::onlyTrashed()->where('id', 1)->restore();
```

**模型关联：**

```php
class User extends Model
{
    // 一对一（hasOne）
    public function profile()
    {
        return $this->hasOne(Profile::class, 'user_id');
    }

    // 一对一（belongsTo）
    public function role()
    {
        return $this->belongsTo(Role::class, 'role_id');
    }

    // 一对多（hasMany）
    public function orders()
    {
        return $this->hasMany(Order::class, 'user_id');
    }

    // 多对多（belongsToMany）
    public function tags()
    {
        return $this->belongsToMany(Tag::class, 'user_tag', 'user_id', 'tag_id');
    }
}

// 使用关联
$user = User::with('profile,orders')->find(1);
$user->profile->avatar;
$user->orders->count();

// 关联统计
$user = User::withCount('orders')->find(1);
$user->orders_count;

// 关联预载入（避免 N+1）
User::with(['orders' => function($query) {
    $query->where('status', 1);
}])->select();
```

---

## 验证

**定义验证器：**
```php
// app/validate/User.php
namespace app\validate;
use think\Validate;

class User extends Validate
{
    protected $rule = [
        'name'  => 'require|max:25|alphaDash',
        'age'   => 'number|between:1,120',
        'email' => 'email',
        'phone' => 'regex:/^1[3-9]\d{9}$/',
    ];

    protected $message = [
        'name.require'  => '用户名必须填写',
        'name.max'      => '用户名最多25个字符',
        'email'         => '邮箱格式不正确',
    ];

    // 验证场景
    protected $scene = [
        'create' => ['name', 'email', 'phone'],
        'edit'   => ['name', 'email'],
    ];
}
```

**使用验证器：**
```php
// 控制器中使用（推荐）
$data = Request::only(['name', 'email']);
try {
    validate(\app\validate\User::class)
        ->scene('create')
        ->check($data);
} catch (\think\exception\ValidateException $e) {
    return json(['code' => 422, 'msg' => $e->getError()]);
}

// 独立验证
$validate = \think\facade\Validate::rule([
    'name' => 'require|max:25',
]);
if (!$validate->check($data)) {
    dump($validate->getError());
}
```

**常用内置规则：**

| 规则 | 说明 |
|------|------|
| require | 必填 |
| number/integer/float | 数字类型 |
| email/url/ip | 格式验证 |
| date | 日期格式 |
| alpha/alphaNum/alphaDash | 字母/字母数字/含-_ |
| min:n / max:n | 最小/最大长度或数值 |
| between:a,b | 区间 |
| in:a,b,c | 枚举 |
| unique:table,field | 唯一性（需指定表名） |
| regex:/pattern/ | 正则 |
| confirm | 两字段一致 |
| gt/egt/lt/elt:field | 与另一字段比较 |

---

## 中间件

**定义中间件：**
```php
// app/middleware/Auth.php
namespace app\middleware;

class Auth
{
    public function handle($request, \Closure $next)
    {
        if (!session('user')) {
            return redirect('/login');
        }
        return $next($request);
    }
}
```

**注册中间件：**
```php
// 全局中间件 app/middleware.php
return [
    \app\middleware\Auth::class,
];

// 路由中间件
Route::group('admin', function() { ... })->middleware(\app\middleware\Auth::class);

// 控制器中间件
class User {
    protected $middleware = [
        \app\middleware\Auth::class => ['except' => ['login']],
    ];
}
```

---

## 事件

**注册事件：** `app/event.php`
```php
return [
    'bind'   => [],
    'listen' => [
        'UserLogin' => [\app\listener\UserLogin::class],
    ],
    'subscribe' => [
        \app\subscribe\User::class,
    ],
];
```

**定义监听器：**
```php
// app/listener/UserLogin.php
namespace app\listener;

class UserLogin
{
    public function handle($user)
    {
        // 处理登录事件，$user 为事件参数
        \think\facade\Log::info('User login: ' . $user->id);
    }
}
```

**触发事件：**
```php
event('UserLogin', $user);
// 或
\think\facade\Event::trigger('UserLogin', $user);
```

---

## 缓存

```php
use think\facade\Cache;

// 写入缓存（60 秒有效期）
Cache::set('key', $value, 60);
Cache::set('key', $value);      // 永久有效

// 读取缓存
$value = Cache::get('key');
$value = Cache::get('key', 'default'); // 有默认值

// 删除缓存
Cache::delete('key');
Cache::clear();  // 清空所有

// 自增/自减
Cache::inc('count');
Cache::dec('count', 5);

// 判断是否存在
Cache::has('key');

// remember：不存在则写入
$value = Cache::remember('key', function() {
    return computeExpensiveValue();
}, 60);

// 多通道
Cache::store('redis')->set('key', 'value');
```

**缓存配置：** `config/cache.php`
```php
return [
    'default' => 'file',
    'stores' => [
        'file' => ['type' => 'File', 'path' => runtime_path('cache')],
        'redis' => ['type' => 'Redis', 'host' => '127.0.0.1', 'port' => 6379],
    ],
];
```

---

## Session / Cookie

```php
use think\facade\Session;
use think\facade\Cookie;

// Session
Session::set('user', $userInfo);
Session::get('user');
Session::get('user.name');          // 点号取嵌套值
Session::has('user');
Session::delete('user');
Session::clear();

// Cookie
Cookie::set('token', 'value', 3600);   // 有效期秒
Cookie::get('token');
Cookie::has('token');
Cookie::delete('token');
```

---

## 文件上传

```php
use think\facade\Request;
use think\File;

$file = Request::file('image');

// 验证并移动
$savePath = \think\facade\Filesystem::putFile('uploads', $file);

// 带验证规则
try {
    validate(['image' => 'fileSize:102400|fileExt:jpg,png,gif'])
        ->check(['image' => $file]);
    $savePath = \think\facade\Filesystem::disk('public')->putFile('images', $file);
    return json(['path' => $savePath]);
} catch (\think\exception\ValidateException $e) {
    return json(['error' => $e->getMessage()]);
}

// 批量上传
$files = Request::file('images');
foreach ($files as $file) {
    \think\facade\Filesystem::putFile('uploads', $file);
}
```

---

## 视图

```php
// 控制器中渲染视图
return view();                       // 自动匹配模板
return view('user/profile');         // 指定模板
return view('user/profile', ['name' => 'tp6']); // 传变量

// 模板赋值
\think\facade\View::assign('title', 'Hello');
\think\facade\View::assign(['key' => 'value']);
```

**模板语法（think-template）：**
```html
{$name}                         <!-- 输出变量 -->
{$user.name} 或 {$user['name']} <!-- 数组/对象 -->
{$name|upper}                   <!-- 过滤器 -->
{if $status == 1}正常{else}禁用{/if}
{foreach $users as $user}
  {$user.name}
{/foreach}
{for $i=1; $i<=10; $i++}
  {$i}
{/for}
{include file="common/header" /}
{extend name="base" /}
{block name="content"}...{/block}
{:function($arg)}               <!-- 调用 PHP 函数 -->
```

---

## 命令行

```bash
# 常用命令
php think run                    # 启动内置服务器
php think version                # 查看版本
php think clear                  # 清除缓存
php think clear --log            # 只清除日志
php think clear --cache          # 只清除数据缓存

# 代码生成
php think make:controller Blog           # 生成资源控制器
php think make:controller Blog --plain   # 生成空控制器
php think make:controller Blog --api     # 生成 API 控制器
php think make:model User               # 生成模型
php think make:validate User            # 生成验证器
php think make:middleware Auth          # 生成中间件
php think make:command SendEmail        # 生成命令类
php think make:event UserLogin          # 生成事件类
php think make:listener UserLogin       # 生成监听器
php think make:service UserService      # 生成服务类

# 多应用模式生成
php think build admin                   # 生成 admin 应用

# 优化
php think optimize:config    # 生成配置缓存
php think optimize:schema    # 生成数据表字段缓存
php think optimize:route     # 生成路由缓存

# 路由
php think route:list         # 查看路由列表

# 查看路由
php think route:list
```

**自定义命令：**
```php
namespace app\command;

use think\console\Command;
use think\console\Input;
use think\console\Output;

class SendEmail extends Command
{
    protected function configure()
    {
        $this->setName('send:email')
             ->setDescription('发送邮件');
    }

    protected function execute(Input $input, Output $output)
    {
        $output->writeln('邮件发送中...');
        // 业务逻辑
        $output->info('发送完成');
    }
}
```

注册命令：`config/console.php`
```php
return [
    'commands' => [
        'send:email' => \app\command\SendEmail::class,
    ],
];
```

---

## 容器与依赖注入

```php
use think\App;
use think\Container;

// 绑定类
app()->bind('sms', \app\service\SmsService::class);
// 或在 app/provider.php
return [
    'sms' => \app\service\SmsService::class,
];

// 获取实例（自动依赖注入）
$sms = app('sms');
$sms = app(\app\service\SmsService::class);

// 控制器方法自动注入
public function send(\app\service\SmsService $sms, Request $request)
{
    $sms->send($request->get('phone'), 'code');
}
```

**Facade 使用：**
```php
// 系统内置 Facade
use think\facade\Db;
use think\facade\Cache;
use think\facade\Log;
use think\facade\Route;
use think\facade\Session;
use think\facade\Cookie;
use think\facade\Config;
use think\facade\Request;
use think\facade\View;

// 自定义 Facade
namespace app\facade;
use think\Facade;
class Sms extends Facade {
    protected static function getFacadeClass() {
        return \app\service\SmsService::class;
    }
}
```

---

## 多应用模式

```bash
# 安装多应用扩展
composer require topthink/think-multi-app
```

```
app/
├── admin/          # admin 应用
│   ├── controller/
│   ├── model/
│   └── route/
└── index/          # index 应用（默认）
    ├── controller/
    └── model/
```

访问格式：`http://domain/admin/user/index`

---

## 错误与日志

```php
use think\facade\Log;

// 日志写入
Log::info('用户登录', ['user_id' => 1]);
Log::error('数据库异常：' . $e->getMessage());
Log::warning('参数异常');
Log::debug('调试信息');

// 多通道
Log::channel('access')->info('访问日志');
```

**日志配置：** `config/log.php`
```php
return [
    'default' => 'file',
    'channels' => [
        'file' => [
            'type'  => 'File',
            'path'  => runtime_path('log'),
            'level' => ['error', 'warning'],
        ],
    ],
];
```

**异常处理：**
```php
// 抛出 HTTP 异常
throw new \think\exception\HttpException(404, '页面不存在');

// 自定义异常处理类 app/ExceptionHandle.php
namespace app;
use think\exception\Handle;

class ExceptionHandle extends Handle
{
    public function render($request, \Throwable $e): \think\Response
    {
        if ($request->isAjax()) {
            return json(['code' => 500, 'msg' => $e->getMessage()]);
        }
        return parent::render($request, $e);
    }
}
```

---

## 助手函数

```php
app()          // 获取容器实例或绑定类
config()       // 获取/设置配置
cache()        // 缓存操作
session()      // Session 操作
cookie()       // Cookie 操作
env()          // 读取 .env 变量
input()        // 读取 Request 参数
url()          // 生成 URL
redirect()     // 重定向
response()     // 创建响应对象
view()         // 渲染视图
json()         // 返回 JSON 响应
download()     // 文件下载
event()        // 触发事件
invoke()       // 调用方法（支持依赖注入）
trace()        // 页面 Trace 信息
dump()         // 调试输出（带格式）
halt()         // 输出后终止
think_path()   // 框架核心目录
app_path()     // 当前应用目录
root_path()    // 项目根目录
base_path()    // 应用根目录
public_path()  // Public 目录
runtime_path() // 运行时目录
```

---

## 常见问题与最佳实践

1. **路由缓存**：生产环境执行 `php think optimize:route` 缓存路由，开发时记得清除。
2. **模型软删除**：引入 `SoftDelete` trait 后，默认查询会自动排除软删除数据。
3. **N+1 问题**：关联查询一定要用 `with()` 预载入。
4. **密码存储**：使用 `password_hash()` 和 `password_verify()`，不要用 md5。
5. **CSRF 防护**：表单提交使用 `{:token()}` 模板函数，配合 `token` 验证规则。
6. **跨域处理**：推荐使用路由 `allowCrossDomain()` 或中间件处理。
7. **队列任务**：安装 `topthink/think-queue` 扩展，结合 Redis 使用。
