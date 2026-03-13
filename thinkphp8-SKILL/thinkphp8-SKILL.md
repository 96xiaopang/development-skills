# ThinkPHP 8 开发技能指南

本指南基于 ThinkPHP 8 官方文档整理，覆盖框架核心用法，供 AI 编码助手参考。

---

## 一、环境要求与安装

**PHP 版本要求：** PHP 8.0+（核心全面使用 `declare(strict_types=1)`）
**遵循规范：** PSR-11（容器）、PSR-16（缓存）、PSR-3（日志）
**ORM：** think-orm 3.x（ThinkORM 4+ 有单独文档）

```bash
composer create-project topthink/think tp8
cd tp8
php think run                    # 内置服务器，默认 http://127.0.0.1:8000
php think run -H 0.0.0.0 -p 8080
```

---

## 二、目录结构

### 单应用模式（默认）

```
app/
  controller/     控制器
  model/          模型
  view/           视图
  BaseController.php
  ExceptionHandle.php
  middleware.php
  event.php
  provider.php
config/           配置目录
route/
  route.php       路由定义
public/
  index.php       入口文件
runtime/          运行时目录（日志、缓存等）
.env              环境变量
```

### 多应用模式

```bash
composer require topthink/think-multi-app
```

```
app/
  index/          index 应用
  admin/          admin 应用
  api/            api 应用
public/
  index.php       公共入口
  admin.php       admin 独立入口
```

URL 格式：`http://server/index.php/admin/controller/action`

单独应用入口：
```php
$http = (new App())->http;
$response = $http->name('admin')->run();
```

多应用配置（`config/app.php`）：
```php
'default_app'   => 'index',
'app_map'       => ['think' => 'admin'],        // URL别名
'domain_bind'   => ['admin.tp.com' => 'admin'], // 域名绑定
'deny_app_list' => ['common'],                  // 禁止直接访问
'app_express'   => true,                        // 智能检测应用
```

---

## 三、命名约定

| 类型 | 规范 | 示例 |
|------|------|------|
| 控制器 | PascalCase | `UserController` 或 `User` |
| 模型 | PascalCase，与表名对应（去掉前缀） | `User` 对应 `think_user` |
| 方法 | camelCase | `getUserInfo` |
| 数据表 | 小写+下划线 | `think_user` |

---

## 四、路由

路由定义文件：`route/route.php`

```php
use think\facade\Route;
```

### 4.1 基础路由

```php
Route::get('hello/:name', 'index/hello');
Route::post('user/save', 'User/save');
Route::put('user/:id', 'User/update');
Route::delete('user/:id', 'User/delete');
Route::any('test', 'Test/index');
Route::rule('hello', 'index/hello', 'GET|POST');

// 闭包路由
Route::get('think', function() {
    return 'hello,ThinkPHP!';
});

// 首页路由
Route::get('/', 'Index/index');
```

### 4.2 路由变量

```php
// 动态变量（两种写法等价，推荐第二种）
Route::get('blog/:id', 'Blog/read');
Route::get('blog/<id>', 'Blog/read');

// 可选变量
Route::get('blog/:year/[:month]', 'Blog/archive');
Route::get('blog/<year>/<month?>', 'Blog/archive');

// 可选变量设置默认值
Route::get('blog/[:id]', 'blog/read')->default(['id' => 1]);

// 完全匹配（末尾加 $）
Route::get('new/:cate$', 'News/category');

// 变量类型约束
Route::get('user/<id>', 'User/read')->pattern(['id' => '\d+']);
```

### 4.3 路由分组

```php
// 带前缀分组
Route::group('api', function() {
    Route::get('user/:id', 'api.User/read');
    Route::post('user', 'api.User/save');
})->middleware(\app\middleware\Auth::class);

// 虚拟分组（无前缀，仅共享参数）
Route::group(function() {
    Route::rule('blog/:id', 'blog/read');
    Route::rule('blog/:name', 'blog/read');
})->ext('html')->pattern(['id' => '\d+', 'name' => '\w+']);

// 使用 prefix 简化路由地址
Route::group('blog', function() {
    Route::get(':id', 'read');
    Route::post(':id', 'update');
    Route::delete(':id', 'delete');
})->prefix('blog/')->ext('html')->pattern(['id' => '\d+']);

// 嵌套分组
Route::group(function() {
    Route::group('blog', function() {
        Route::rule(':id', 'blog/read');
    });
})->ext('html');
```

**V8.1+ 分组绑定**（未匹配路由时自动调度，不受强制路由影响）：
```php
Route::group('blog')->controller('blog');        // 绑定到控制器
Route::group('blog')->layer('blog');             // 绑定到控制器分级
Route::group('blog')->class(Blog::class);        // 绑定到类
Route::group('blog')->namespace('app\controller\blog'); // 绑定到命名空间
Route::group('blog', function(){...})->auto();   // 开启自动URL调度
```

### 4.4 资源路由

```php
Route::resource('blog', 'Blog');
```

| 操作 | 地址 | HTTP | 方法 |
|------|------|------|------|
| index | /blog | GET | Blog/index |
| create | /blog/create | GET | Blog/create |
| save | /blog | POST | Blog/save |
| read | /blog/:id | GET | Blog/read |
| edit | /blog/:id/edit | GET | Blog/edit |
| update | /blog/:id | PUT | Blog/update |
| delete | /blog/:id | DELETE | Blog/delete |

### 4.5 域名路由

```php
Route::domain('blog', function() {
    Route::rule('new/:id', 'news/read');
    Route::rule(':user', 'user/info');
});

Route::domain('blog.tp.com', function() {
    Route::get(':id', 'blog/read');
});
```

### 4.6 路由参数

```php
Route::get('new/:id', 'News/read')
    ->ext('html')            // URL后缀检测
    ->denyExt('jpg|png')     // 禁止后缀
    ->https()                // 仅HTTPS
    ->ajax()                 // 仅AJAX
    ->json()                 // 仅JSON请求
    ->domain('news')         // 域名检测
    ->pattern(['id'=>'\d+']) // 变量正则约束
    ->append(['status'=>1])  // 隐式附加参数
    ->cache(3600)            // 请求缓存(秒)
    ->middleware(Auth::class)
    ->token()                // 表单令牌验证
    ->model('\app\model\User')  // 绑定模型
    ->filter(['type'=>1])    // 请求变量过滤
    ->when('type', TypeEnum::class)  // 变量规则验证(V8.1+)
    ->header(['Content-Type'=>'application/json'])  // Header检测(V8.1.3+)
    ->version('2.0')         // 版本检测(V8.1.3+)
    ->completeMatch()        // 完全匹配
    ->withoutMiddleware();   // 排除中间件(V8.1+)
```

批量设置：
```php
Route::get('new/:id', 'News/read')->option(['ext'=>'html', 'https'=>true]);
```

### 4.7 路由中间件

```php
// 单条路由
Route::rule('hello/:name', 'hello')->middleware(\app\middleware\Auth::class);
// 带参数
Route::rule('hello/:name', 'hello')->middleware(\app\middleware\Auth::class, 'admin');
// 多个中间件
Route::rule('hello/:name', 'hello')->middleware([\app\middleware\Auth::class, \app\middleware\Check::class]);
// 全局路由中间件（config/route.php）
'middleware' => [app\middleware\Auth::class]
```

### 4.8 MISS路由

```php
Route::miss('public/miss');

// 分组MISS路由
Route::group('blog', function() {
    Route::rule(':id', 'blog/read');
    Route::miss('blog/miss');
});
```

### 4.9 URL生成

```php
url('index/hello', ['name' => 'think'])
url('Blog/read', ['id' => 1])

// 路由标识
Route::rule('new/:id', 'News/read')->name('new_read');
url('new_read', ['id' => 10])
```

### 4.10 注解路由

需安装：`composer require topthink/think-annotation`

```php
// route.php 中启用
Route::annotation();
```

```php
use think\annotation\route\Route;
use think\annotation\route\Get;
use think\annotation\route\Resource;
use think\annotation\route\Group;
use think\annotation\route\Middleware;

class Index
{
    #[Route("GET", "hello/:name")]
    public function hello($name) {
        return 'hello,' . $name;
    }

    #[Get("hello/:name")]
    public function hello2($name) {}
}

// 资源路由注解
#[Resource("blog")]
class Blog {}

// 分组注解
#[Group("blog", ["ext" => "html"])]
#[Middleware([SessionInit::class])]
class BlogController
{
    #[Route("GET", "hello/:name")]
    public function hello($name) {}
}
```

> 注意：注解中不能使用单引号；调试模式实时生效，部署模式首次访问生成缓存。

### 4.11 路由性能优化配置

```php
// config/route.php
'url_lazy_route'       => true,   // 延迟路由解析
'route_rule_merge'     => true,   // 路由合并解析
'route_complete_match' => true,   // 全局完全匹配
'url_route_must'       => true,   // 强制路由
'route_auto_group'     => true,   // 自动扫描分组子目录(V8.1.3+)

// 分组合并解析
Route::group('user', function() {
    Route::rule('hello/:name', 'hello');
})->mergeRuleRegex();
```

### 4.12 自动URL调度（V8.1+）

```php
// 开启多模块URL自动解析
Route::auto();
// URL格式：domainName/moduleName/controllerName/actionName

// 开启并自动加载模块同名中间件
Route::auto(middleware: true);

// 自定义规则
Route::auto('v<version>/[:controller]/[:action]', 'v<version>/:controller/:action')
    ->pattern(['version' => '\d+']);
```

### 4.13 分组子目录（V8.1.3+）

```
route/
  common.php
  admin/
    route1.php
    route2.php
```

```php
// common.php 中注册（或开启 route_auto_group 自动扫描）
Route::group('admin');
```

### 4.14 跨域请求

```bash
composer require topthink/think-cors
```

```php
// config/cors.php
return [
    'paths'                    => ['api/*'],
    'allowed_origins'          => ['*'],
    'allowed_origins_patterns' => ['#.*\.thinkphp\.cn#'],
    'allowed_methods'          => ['*'],
    'allowed_headers'          => ['*'],
    'max_age'                  => 7200,
    'supports_credentials'     => false,
];
```

---

## 五、控制器

```php
<?php
namespace app\controller;

use think\Request;
use app\BaseController;

class User extends BaseController
{
    // 控制器中间件
    protected $middleware = [
        \app\middleware\Auth::class => ['except' => ['login']],
        \app\middleware\Log::class  => ['only'   => ['index', 'read']],
    ];

    public function index()
    {
        return 'hello';
    }

    // 参数绑定（自动从URL/POST绑定）
    public function read(int $id)
    {
        return json(['id' => $id]);
    }
}
```

**资源控制器方法对应表：** index / create / save / read / edit / update / delete

**空操作捕获：**
```php
public function __call($name, $args)
{
    return '404 Not Found: ' . $name;
}
```

---

## 六、请求（Request）

```php
use think\facade\Request;

// 参数获取
Request::param('name');                  // 自动识别请求类型
Request::param('name', 'default');       // 带默认值
Request::get('id/d');                    // GET参数，强制整数
Request::post('name/s');                 // POST参数，强制字符串
Request::only(['id', 'name']);           // 白名单
Request::only(['id/d', 'name/s']);       // 白名单+类型强制(V8.1+)
Request::except(['password']);           // 黑名单
Request::param(false);                   // 全部参数，不过滤

// 类型修饰符：/s=string  /d=int  /b=bool  /a=array  /f=float

// 请求类型
Request::method();      // GET/POST/PUT/DELETE...
Request::isGet();       Request::isPost();
Request::isAjax();      Request::isJson();
Request::isPjax();      Request::isMobile();

// 请求信息
Request::host();        Request::url();
Request::baseUrl();     Request::ip();
Request::controller();  Request::action();
Request::header('user-agent');
Request::header();      // 全部header

// 助手函数
input('get.id/d');
input('post.name', '', 'htmlspecialchars');
input('?get.id');            // 检查是否存在

// 中间件向控制器传递变量
$request->userId = 1;        // 在中间件中设置
// 控制器中：$this->request->userId

// 表单令牌
$token = $request->buildToken('__token__', 'sha1');
$request->checkToken('__token__');
$request->checkToken('__token__', $request->param());
```

---

## 七、响应（Response）

```php
return 'string';                         // HTML
return json($data);
return json($data, 201);
return json($data)->code(201)->header(['X-Token' => 'abc']);
return xml($data);
return view('index', ['name' => 'tp']);
return redirect('http://www.thinkphp.cn');
return redirect('/index/hello')->with('name', 'tp');
return redirect('/hello')->remember();   // 记住当前URL
return redirect()->restore();            // 跳转到记住的URL
return download('file.jpg', 'my.jpg');
return download($content, 'test.txt', true);  // 内容作为文件下载
return response($data, 200, ['Content-Type' => 'text/plain']);
```

---

## 八、数据库（Query Builder）

### 8.1 查询

```php
use think\facade\Db;

Db::table('think_user')->find(1);        // 按主键，table用完整表名
Db::name('user')->find(1);               // name自动加前缀
Db::name('user')->where('id', 1)->find();
Db::name('user')->findOrFail(1);         // 找不到抛异常
Db::name('user')->findOrEmpty();         // 找不到返回空数组
Db::name('user')->select();
Db::name('user')->selectOrFail();

// 条件
->where('status', '>', 0)
->where([['status','=',1], ['age','>',18]])
->whereOr('name', 'think')
->whereIn('id', [1,2,3])
->whereNull('delete_time')
->whereLike('name', '%think%')
->whereBetweenTime('create_time', '2021-01-01', '2021-12-31')
```

### 8.2 字段与排序

```php
->field('id,name,email')
->withoutField('password')
->fieldRaw('id,SUM(score)')
->order('create_time', 'desc')
->orderRaw('field(status,1,2,3)')
->limit(10)
->limit(0, 10)         // offset, length
->page(2, 10)          // 第2页，每页10条
```

### 8.3 聚合

```php
Db::name('user')->count();
Db::name('user')->max('score');
Db::name('user')->min('score');
Db::name('user')->avg('score');
Db::name('user')->sum('score');
```

### 8.4 写入

```php
Db::name('user')->insert(['name'=>'tp','status'=>1]);
Db::name('user')->insertGetId(['name'=>'tp']);
Db::name('user')->insertAll($dataArray);
Db::name('user')->replace()->insert($data);    // REPLACE INTO
Db::name('user')->save($data);                 // 有主键则更新，否则插入

Db::name('user')->where('id',1)->update(['name'=>'new']);
Db::name('user')->where('id',1)->inc('score', 5);
Db::name('user')->where('id',1)->dec('score', 1);
Db::name('user')->where('id',1)->setField('name', 'new');
```

### 8.5 删除

```php
Db::name('user')->delete(1);
Db::name('user')->where('id','<',10)->delete();
Db::name('user')->delete(true);                // 删除全部（谨慎）

// 软删除
Db::name('user')->where('id',1)
    ->useSoftDelete('delete_time', time())
    ->delete();
```

### 8.6 事务

```php
// 自动事务
Db::transaction(function() {
    Db::name('user')->where('id',1)->dec('balance', 100);
    Db::name('order')->insert(['user_id'=>1, 'amount'=>100]);
});

// 手动事务
Db::startTrans();
try {
    Db::commit();
} catch (\Exception $e) {
    Db::rollback();
    throw $e;
}
```

### 8.7 其他链式方法

```php
->alias('u')
->join('profile p', 'p.user_id=u.id')
->join('profile p', 'p.user_id=u.id', 'LEFT')
->group('status')
->having('count>1')
->union('SELECT id FROM admin')
->distinct(true)
->lock(true)                     // FOR UPDATE
->comment('注释')
->force('index_name')            // 强制索引
->strict(false)                  // 忽略未知字段
->duplicate(['score' => 10])     // ON DUPLICATE KEY UPDATE
->extra('IGNORE')
->removeOption('where')          // 清除某个链式条件

// 视图查询（无JOIN的多表联合查询）
Db::view('User', 'id,name')
    ->view('Profile', 'email', 'Profile.user_id=User.id')
    ->where('status', 1)->select();
```

### 8.8 JSON字段

```php
Db::name('user')->json(['info'])->where('info->nickname', '流年')->find();
Db::name('user')->whereJsonContains('info', 'thinkphp')->find();
```

### 8.9 缓存与调试

```php
Db::name('user')->cache(true, 60)->find(1);     // 查询缓存
Db::name('user')->cache('key', 60)->select();
Db::name('user')->cacheAlways('key', 60)->find(); // 空结果也缓存

echo Db::name('user')->where('id',1)->fetchSql()->find(); // 输出SQL不执行
echo Db::getLastSql();
```

### 8.10 分页

```php
$page = Db::name('user')->where('status',1)->paginate(10);
$page = Db::name('user')->paginate(['list_rows'=>10, 'page'=>1]);
// 模板中：{$page->render()}
```

### 8.11 原生SQL

```php
Db::query('SELECT * FROM user WHERE id=?', [1]);
Db::execute('UPDATE user SET name=? WHERE id=?', ['tp', 1]);
```

---

## 九、模型（Model / ORM）

### 9.1 模型定义

```php
<?php
namespace app\model;
use think\Model;

class User extends Model
{
    protected $name       = 'user';           // 表名（不含前缀）
    protected $table      = 'think_user';     // 完整表名（优先级更高）
    protected $pk         = 'uid';            // 主键
    protected $connection = 'db2';            // 数据库连接配置键
    protected $suffix     = '_cn';            // 表后缀

    // 字段定义（生产环境推荐，避免额外查询）
    protected $schema = [
        'id'          => 'int',
        'name'        => 'string',
        'status'      => 'int',
        'score'       => 'float',
        'create_time' => 'datetime',
        'update_time' => 'datetime',
    ];

    // 类型转换
    protected $type = [
        'score'  => 'float',
        'info'   => 'json',           // 自动JSON编解码
        'status' => 'integer',
        // PHP8.1枚举
        'status' => \app\enum\UserStatus::class,
    ];

    // 废弃字段
    protected $disuse = ['old_field'];

    // 自动时间戳
    protected $autoWriteTimestamp = true;        // 或 'datetime'/'timestamp'
    protected $createTime         = 'create_at'; // 自定义创建时间字段名
    protected $updateTime         = false;        // 禁用更新时间

    // 软删除
    use \think\model\concern\SoftDelete;
    protected $deleteTime = 'delete_time';

    // JSON字段
    protected $json      = ['info'];
    protected $jsonAssoc = true;   // 以数组返回（默认对象）

    // 字段映射（DB字段 => 模型属性）
    protected $mapping = ['user_name' => 'name'];

    // 懒加载字段
    protected $lazy = ['content'];

    // 默认全局查询范围
    protected $globalScope = ['base'];

    // 模型观察者（V8.1+）
    protected $eventObserver = UserObserver::class;
}
```

### 9.2 CRUD

```php
// 查询
$user = User::find(1);
$user = User::findOrFail(1);         // 找不到抛异常
$user = User::findOrEmpty(1);        // 找不到返回空模型
$user = User::where('name','tp')->find();
$list = User::where('status',1)->select();
$list = User::where('status',1)->order('id','desc')->paginate(10);

// 创建
$user = User::create(['name'=>'tp','status'=>1]);
$user = new User(['name'=>'tp']);
$user->save();
$user->saveOrFail();                 // 失败则抛异常

// 更新
$user = User::find(1);
$user->name = 'new';
$user->save();
User::where('status',1)->update(['name'=>'tp']);
User::update(['name'=>'tp'], ['id'=>1]);

// 删除
User::find(1)->delete();
User::destroy(1);
User::destroy([1,2,3]);
User::where('status',0)->delete();

// 软删除
$user->delete();                     // 软删除
User::withTrashed()->find(1);        // 包含已软删除
User::onlyTrashed()->select();       // 仅软删除数据
$user->restore();                    // 恢复
$user->forceDelete();                // 硬删除
```

### 9.3 获取器（Getter）

```php
// 自动触发（访问 $model->status 时）
public function getStatusAttr($value)
{
    return [-1=>'删除', 0=>'禁用', 1=>'正常'][$value];
}

// 虚拟字段（该字段不在DB中，$data为全部原始数据）
public function getStatusTextAttr($value, $data)
{
    return [-1=>'删除', 0=>'禁用', 1=>'正常'][$data['status']];
}

// 获取原始值
$user->getData('status');

// 动态获取器（链式）
User::withAttr('name', fn($v) => strtolower($v))->select();
```

### 9.4 修改器（Setter）

```php
// 赋值时自动触发
public function setPasswordAttr($value)
{
    return password_hash($value, PASSWORD_DEFAULT);
}
```

### 9.5 搜索器（Searcher）

```php
// 定义
public function searchNameAttr($query, $value, $data)
{
    $query->where('name', 'like', '%'.$value.'%');
}

// 使用
User::withSearch(['name'], ['name' => 'think'])->select();
```

### 9.6 模型输出

```php
$user->toArray();
$user->toJson();
echo json_encode($user);                        // 自动调用 toJson

$user->hidden(['password','create_time'])->toArray();
$user->visible(['id','name','email'])->toArray();
$user->append(['status_text'])->toArray();      // 追加虚拟字段
```

### 9.7 模型事件

```php
// 模型类中定义静态方法（返回 false 可取消操作）
public static function onBeforeInsert($user)  {}
public static function onAfterInsert($user)   {}
public static function onBeforeUpdate($user)  { return false; }
public static function onAfterUpdate($user)   {}
public static function onBeforeDelete($user)  {}
public static function onAfterDelete($user)   {}
public static function onBeforeWrite($user)   {}
public static function onAfterWrite($user)    {}
public static function onAfterRead($user)     {}

// 临时禁用事件
$user->withEvent(false)->save();
```

### 9.8 查询范围（Scope）

```php
// 定义
protected function scopeBase($query)
{
    $query->where('status', 1);
}

// 全局范围（自动应用）
protected $globalScope = ['base'];

// 使用
User::scope('base')->select();
User::withoutGlobalScope(['base'])->select();  // 临时取消
```

### 9.9 关联

```php
// hasOne（一对一）
public function profile() {
    return $this->hasOne(Profile::class);   // FK默认：user_id
}
// hasMany（一对多）
public function orders() {
    return $this->hasMany(Order::class);
}
// belongsTo（反向）
public function user() {
    return $this->belongsTo(User::class);
}
// belongsToMany（多对多）
public function roles() {
    return $this->belongsToMany(Role::class, 'user_role');
}
// hasManyThrough（远程一对多）
public function topics() {
    return $this->hasManyThrough(Topic::class, User::class);
}
// hasOneThrough（远程一对一）
public function card() {
    return $this->hasOneThrough(Card::class, Profile::class);
}
// 多态关联
public function comments() {
    return $this->morphMany(Comment::class, 'commentable');
}
public function commentable() {
    return $this->morphTo();
}

// 预加载（解决N+1问题）
$users = User::with(['profile','orders'])->select();
$users = User::with([
    'profile' => function($q) { $q->field('id,email'); }
])->select();

// 关联统计
$users = User::withCount(['orders'])->select();
$users = User::withSum('orders','amount')->select();

// 关联输出控制
$user->hidden(['profile' => ['password']])->toArray();
$user->append(['profile' => ['email']])->toArray();

// 级联删除
$article->together(['comments'])->delete();
```

### 9.10 PHP 8.1 枚举支持

```php
enum UserStatus: int {
    case Active   = 1;
    case Inactive = 0;
}

// 模型中
protected $type = ['status' => UserStatus::class];

// 使用
$user->status->value;  // 1
$user->status->name;   // 'Active'
```

---

## 十、验证（Validation）

### 10.1 验证器定义

```bash
php think make:validate User
```

```php
<?php
namespace app\validate;
use think\Validate;

class User extends Validate
{
    protected $rule = [
        'name'   => 'require|max:25',
        'email'  => 'email',
        'age'    => 'number|between:1,120',
        'phone'  => 'mobile',
        'status' => \app\enum\UserStatus::class,  // 枚举(V8.1+)
    ];

    protected $message = [
        'name.require' => '名称必须',
        'name.max'     => '名称最多25个字符',
        'email'        => '邮箱格式错误',
    ];

    protected $scene = [
        'create' => ['name','email','age'],
        'edit'   => ['name','email'],
    ];

    // 场景方法（更细粒度控制）
    public function sceneEdit()
    {
        return $this->only(['name','age'])
            ->append('name', 'min:5')
            ->remove('age', 'between')
            ->append('age', 'require|max:100');
    }

    // 规则别名（V8.1.2+）
    protected $alias = [
        'username' => 'require|alphaNum|max:25',
    ];

    // 自定义验证规则（驼峰命名，不能与内置规则冲突）
    protected function checkName($value, $rule, $data = [])
    {
        return $rule == $value ? true : '名称错误';
    }
}
```

### 10.2 使用验证器

```php
use think\exception\ValidateException;

try {
    validate(User::class)->check($data);
    validate(User::class)->scene('create')->check($data);
    validate(User::class)->batch(true)->check($data);  // 批量验证
} catch (ValidateException $e) {
    $e->getError();  // 错误信息
    $e->getKey();    // 错误字段名（V8.1+）
}
```

### 10.3 独立验证

```php
use think\facade\Validate;

// 字符串规则
$v = Validate::rule(['name'=>'require|max:25','email'=>'email']);
if (!$v->check($data)) { dump($v->getError()); }

// 对象化规则
use think\validate\ValidateRule as Rule;
$v = Validate::rule([
    'name'  => Rule::isRequire()->max(25),
    'email' => Rule::isEmail(),
    'age'   => Rule::isNumber()->between([1,120]),
]);

// 闭包规则
$v = Validate::rule([
    'name' => function($value, $data) {
        return 'thinkphp' == strtolower($value) ? true : '用户名错误';
    },
]);

// 单规则验证
Validate::checkRule('thinkphp@qq.com', 'email');
```

### 10.4 数组验证（V8.1+）

```php
protected $rule = [
    'name'         => 'require|max:25',
    'info.email'   => 'email',           // 一维数组
    'info.*.email' => 'email',           // 二维数组（通配符*）
    'info.*.score' => 'number',
];

// 验证集（V8.1.2+）
$v = Validate::ruleSet('pay', [
    'title' => 'require',
    'price' => 'require|integer',
]);
// 等价于 pay.*.title 和 pay.*.price
```

### 10.5 路由绑定验证

```php
Route::post('hello/:id', 'index/hello')->validate(\app\validate\User::class, 'edit');

Route::post('hello/:id', 'index/hello')->validate([
    'name'  => 'require|min:5|max:50',
    'email' => 'email',
], message: ['name.require' => '名称必须']);
```

### 10.6 内置验证规则速查

**格式类：** `require` / `number` / `integer` / `float` / `boolean` / `email` / `url` / `ip` / `date` / `dateFormat:Y-m-d` / `mobile` / `idCard` / `zip` / `macAddr` / `activeUrl`

**字符类：** `alpha` / `alphaNum` / `alphaDash` / `chs` / `chsAlpha` / `chsAlphaNum` / `chsDash` / `lower` / `upper`

**范围类：** `in:1,2,3` / `notIn:1,2,3` / `between:1,10` / `notBetween:1,10` / `length:n,m` / `max:n` / `min:n` / `gt:n` / `egt:n` / `lt:n` / `elt:n` / `eq:n`

**比较类：** `confirm:field` / `different:field` / `unique:table,field,except,pk`

**文件类：** `fileSize:102400` / `fileExt:jpg,png` / `fileMime:image/jpeg` / `image:w,h,type`

**Token：** `token` / `token:__hash__`

**V8.1+ 新增：** `accepted` / `acceptedIf:field,val` / `declined` / `declinedIf:field,val` / `multipleOf:10` / `startWith:prefix` / `endWith:suffix` / `contain:str` / `enum:\app\enum\Status`

### 10.7 表单令牌

```php
// 模板
{:token_field()}
{:token_meta()}   // AJAX用，输出meta标签

// 路由验证
Route::post('blog/save','blog/save')->token();

// 控制器手动验证
if (!$request->checkToken('__token__')) {
    throw new \think\exception\ValidateException('invalid token');
}
```

---

## 十一、中间件（Middleware）

### 11.1 定义

```bash
php think make:middleware Auth
```

```php
<?php
namespace app\middleware;

class Auth
{
    public function handle($request, \Closure $next, $role = 'user')
    {
        if (!session('user_id')) {
            return redirect('/login');
        }
        $request->userId = session('user_id');  // 向后传递变量
        return $next($request);
    }

    // 请求结束后回调（可选）
    public function end(\think\Response $response) {}
}
```

### 11.2 注册方式

```php
// 全局（app/middleware.php）
return [
    \app\middleware\Auth::class,
    [\app\middleware\Role::class, 'admin'],  // 带参数
];

// 路由
Route::get('admin','Admin/index')->middleware(\app\middleware\Auth::class);
Route::group('admin', function(){...})->middleware('auth');

// 控制器
protected $middleware = [
    \app\middleware\Auth::class => ['except' => ['login']],
];

// 中间件别名（config/middleware.php）
return ['alias' => ['auth' => \app\middleware\Auth::class]];
```

---

## 十二、事件（Event）

### 12.1 配置（app/event.php）

```php
return [
    'bind' => [
        'UserLogin' => \app\event\UserLogin::class,
    ],
    'listen' => [
        'UserLogin' => [
            \app\listener\SendEmail::class,
            \app\listener\WriteLog::class,
        ],
    ],
    'subscribe' => [
        \app\subscribe\User::class,
        'user' => \app\subscribe\User::class,  // V8.1+ 带标签
    ],
];
```

### 12.2 监听器与订阅者

```php
// 监听器
class SendEmail {
    public function handle($user) { /* 发邮件 */ }
}

// 订阅者
class UserSubscribe {
    public function onUserLogin($user) {}
    public function subscribe(\think\Event $event) {
        $event->listen('UserLogin', [$this, 'onUserLogin']);
    }
}
```

### 12.3 触发

```php
event('UserLogin', $user);
// V8.1+ 带标签
event('user.userLogin', $data);
```

### 12.4 系统内置事件

`AppInit` / `HttpRun` / `HttpEnd` / `RouteLoaded` / `LogWrite` / `LogRecord`

---

## 十三、缓存（Cache）

```php
use think\facade\Cache;

Cache::set('name', 'value', 3600);
Cache::get('name');
Cache::get('name', 'default');
Cache::get('key', function() { return 'default'; });  // V8.1+闭包默认值
Cache::delete('name');
Cache::has('name');
Cache::inc('counter', 1);
Cache::dec('counter', 1);
Cache::pull('name');           // 获取并删除
Cache::remember('key', function() { return 'value'; }, 3600);

// 标签缓存
Cache::tag('user')->set('user_1', $data, 3600);
Cache::tag('user')->clear();

// 指定驱动
Cache::store('redis')->set('key', 'value');
```

**配置（config/cache.php）：**
```php
return [
    'default' => 'file',
    'stores'  => [
        'file'  => ['type' => 'File', 'path' => runtime_path('cache')],
        'redis' => [
            'type'     => 'Redis',
            'host'     => '127.0.0.1',
            'port'     => 6379,
            'password' => '',
            'select'   => 0,
            'timeout'  => 0,
        ],
    ],
];
```

---

## 十四、Session 与 Cookie

```php
// Session（需在 app/middleware.php 注册 \think\middleware\SessionInit）
session('name', 'value');
session('name');
session('name', null);   // 删除
session('?name');        // 检查
session(null);           // 清空

use think\facade\Session;
Session::set('user', $data);
Session::get('user');
Session::delete('user');
Session::has('user');
Session::clear();
Session::flash('msg', 'success');  // 闪存（下次请求后自动删除）

// Cookie
use think\facade\Cookie;
Cookie::set('name', 'value', 3600);
Cookie::get('name');
Cookie::delete('name');
Cookie::has('name');
```

---

## 十五、文件上传

```php
$file  = request()->file('image');
$files = request()->file('images');    // 多文件

// 验证
$validate = \think\facade\Validate::rule([
    'image' => 'fileSize:102400|fileExt:jpg,png|fileMime:image/jpeg,image/png',
]);
if (!$validate->check(['image' => $file])) {
    return json(['error' => $validate->getError()]);
}

// 保存
use think\facade\Filesystem;
$saveName = Filesystem::disk('public')->putFile('uploads', $file);
$saveName = Filesystem::disk('public')->putFileAs('uploads', $file, 'custom.jpg');

// 多文件
foreach ($files as $file) {
    Filesystem::disk('public')->putFile('uploads', $file);
}
```

**配置（config/filesystem.php）：**
```php
return [
    'default' => 'local',
    'disks'   => [
        'local'  => ['type'=>'local', 'root'=>app()->getRuntimePath().'storage'],
        'public' => ['type'=>'local', 'root'=>app()->getRootPath().'public/storage', 'url'=>'/storage'],
    ],
];
```

---

## 十六、视图（View）

```bash
composer require topthink/think-view
```

```php
return view('index');
return view('index', ['name' => 'ThinkPHP']);
return view('admin@index/index');      // 跨应用

use think\facade\View;
View::assign('name', 'ThinkPHP');
return View::fetch('index');
```

**模板语法：**
```html
{$name}
{$user.name}  {$user['name']}
{$name|strtoupper}
{$name|default='默认值'}
{:function($var)}
{// 注释}

{if condition="$status==1"}正常{elseif condition="$status==0"/}禁用{else/}删除{/if}
{foreach $list as $key=>$item}{$item.name}{/foreach}

{include file="header"}
```

**模板继承：**
```html
<!-- layout.html -->
{block name="content"}{/block}

<!-- child.html -->
{extend name="layout"}
{block name="content"}内容{/block}
```

---

## 十七、日志（Log）

```php
use think\facade\Log;

Log::info('消息', ['context']);
Log::error('错误');
Log::warning('警告');
Log::debug('调试');
Log::write('内容', 'custom');
Log::channel('email')->info('邮件日志');
Log::clear();
Log::getLog();
```

**配置（config/log.php）：**
```php
return [
    'default'      => 'file',
    'type_channel' => ['error' => 'email', 'sql' => 'sql'],
    'channels'     => [
        'file' => [
            'type'        => 'File',
            'path'        => runtime_path('log'),
            'level'       => ['error','warning'],
            'json'        => false,           // JSON格式记录
            'file_size'   => 1024*1024*10,
            'max_files'   => 30,              // 最多保留数量
            'apart_level' => ['error'],       // 独立文件的级别
        ],
    ],
];
```

---

## 十八、异常处理

```php
// 抛出HTTP异常
abort(404, 'Not Found');
throw new \think\exception\HttpException(404, 'Not Found');

// 自定义处理（app/ExceptionHandle.php）
class ExceptionHandle extends \think\exception\Handle
{
    protected $ignoreReport = [\think\exception\HttpException::class];

    public function render($request, \Throwable $e): \think\Response
    {
        if ($e instanceof \think\exception\HttpException) {
            $code = $e->getStatusCode();
            return json(['code'=>$code, 'msg'=>$e->getMessage()], $code);
        }
        if ($e instanceof \think\exception\ValidateException) {
            return json(['code'=>422, 'msg'=>$e->getError()], 422);
        }
        return parent::render($request, $e);
    }
}
```

**调试：**
```php
// .env
APP_DEBUG = true

dump($var1, $var2);     // 友好输出
halt($var1, $var2);     // 输出后中止
```

---

## 十九、容器与依赖注入

```php
// 自动注入（控制器/中间件/事件/路由闭包均支持）
class Index {
    public function index(\think\Request $request, UserService $service) {}
}

// 手动
$obj = app('cache');
$obj = app(\app\service\UserService::class);
invoke('Foo');
invoke([\Foo::class, 'bar']);
invoke(function(\Bar $bar) {});

// 绑定
bind('my_service', MyService::class);

// Facade
use think\facade\{App, Cache, Config, Cookie, Db, Env, Event};
use think\facade\{Filesystem, Lang, Log, Middleware, Request};
use think\facade\{Route, Session, Validate, View};
```

---

## 二十、系统服务（Service）

```php
class FileSystemService extends \think\Service
{
    public $bind = ['file_system' => FileSystem::class];

    public function boot(\think\Route $route) {}
}

// 注册（service.php）
return ['\app\service\FileSystemService'];
```

---

## 二十一、控制台命令

### 内置命令

```bash
php think version
php think run                        # 内置服务器
php think clear                      # 清除runtime缓存
php think route:list                 # 查看路由列表
php think optimize:schema            # 缓存表字段
php think optimize:route             # 缓存路由
php think optimize:config            # 缓存配置(V8.1.3+)
php think optimize                   # 全量优化(V8.1.4+)
php think build demo                 # 创建应用（多应用模式）
```

### 代码生成

```bash
php think make:controller Blog
php think make:controller index@Blog  # 多应用
php think make:controller Blog --api  # API风格
php think make:model User
php think make:middleware Auth
php think make:validate User
php think make:command Hello hello
php think make:event UserLogin
php think make:listener SendEmail
php think make:subscribe User
php think make:service FileSystem
```

### 自定义命令

```php
class Hello extends \think\console\Command
{
    protected function configure()
    {
        $this->setName('hello')
            ->addArgument('name', Argument::OPTIONAL, '你的名字')
            ->addOption('city', null, Option::VALUE_REQUIRED, '城市')
            ->setDescription('打招呼');
    }

    protected function execute(Input $input, Output $output)
    {
        $name = $input->getArgument('name') ?: 'thinkphp';
        $output->writeln("Hello, $name!");
    }
}

// 注册（config/console.php）
return ['commands' => ['hello' => \app\command\Hello::class]];
```

---

## 二十二、助手函数速查

```php
app()           bind()          invoke()        url()
input()         json()          xml()           jsonp()
view()          redirect()      download()      response()
session()       cookie()        cache()         config()
env()           event()         abort()
dump()          halt()          token()
validate()      lang()          trace()         request()

// 路径
root_path()     base_path()     app_path()
config_path()   runtime_path()  public_path()
```

---

## 二十三、版本与兼容

| 版本 | 时间 | 主要特性 |
|------|------|---------|
| 8.0.0 | 2023-06 | 基于PHP 8.0重构，think-orm 3.0 |
| 8.0.3 | 2023-10 | PSR兼容、think-cors扩展 |
| 8.1.0 | 2024-11 | 路由分组绑定/自动调度、枚举验证、Macroable、V8.1全面重构 |
| 8.1.2 | 2025-01 | ValidateRuleSet、规则别名、数组验证增强 |
| 8.1.3 | 2025-07 | header/version路由检测、分组子目录、optimize:config |
| 8.1.4 | 2026-01 | optimize命令、PHP 8.5兼容、Redis改进 |

**升级提示：** TP8 支持 TP6.* 无缝升级；从 6.0 升级需额外安装 `think-filesystem`。

---

## 二十四、生产最佳实践

1. **字段白名单**：用 `field()` / `only()` 限制可操作字段，防止批量赋值
2. **生产优化**：运行 `php think optimize`（含 schema、route、config 缓存）
3. **避免N+1**：关联查询使用 `with()` 预加载
4. **安全输出**：API 返回前 `hidden(['password'])` 过滤敏感字段
5. **密码哈希**：在模型修改器中使用 `password_hash()`，不要存明文
6. **严格错误处理**：使用 `findOrFail()` / `saveOrFail()` 让错误不被静默忽略
7. **DI优先**：优先使用构造/方法注入而非 `app()` 助手函数，便于测试
8. **模型事件**：用模型事件处理审计日志、缓存清除等横切逻辑
9. **关闭调试**：生产环境 `.env` 设置 `APP_DEBUG=false`
10. **路由性能**：路由多时开启 `url_lazy_route` + `mergeRuleRegex` 提升解析效率
