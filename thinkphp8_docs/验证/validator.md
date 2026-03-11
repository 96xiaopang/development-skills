ThinkPHP推荐使用验证器来解决各种验证场景和需求。

## 验证器定义

为具体的验证场景或者数据表定义好验证器类，直接调用验证类的`check`方法即可完成验证，下面是一个例子：

我们定义一个`\app\validate\User`验证器类用于`User`的验证，使用下面的指令快速生成`User`验证器。
~~~cmd
php think make:validate User
~~~

在验证器类中定义验证规则
~~~
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule =   [
        'name'  => 'require|max:25',
        'age'   => 'number|between:1,120',
        'email' => 'email',    
    ];
}
~~~
可以直接在验证器类中使用`message`属性定义错误提示信息，例如：

~~~
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule =   [
        'name'  => 'require|max:25',
        'age'   => 'number|between:1,120',
        'email' => 'email',    
    ];
    
    protected $message  =   [
        'name.require' => '名称必须',
        'name.max'     => '名称最多不能超过25个字符',
        'age.number'   => '年龄必须是数字',
        'age.between'  => '年龄只能在1-120之间',
        'email'        => '邮箱格式错误',    
    ];
    
}
~~~

>[danger] 如果没有定义错误提示信息，则使用系统默认的提示信息

## 数据验证

这里以控制器验证为例（这也是推荐的验证方式）进行说明验证器的用法，在需要进行`User`验证的控制器方法中，添加如下代码即可：

~~~
<?php
namespace app\controller;

use app\validate\User;
use think\exception\ValidateException;

class Index
{
    public function index()
    {
        try {
            validate(User::class)->check([
                'name'  => 'thinkphp',
                'email' => 'thinkphp@qq.com',
            ]);
        } catch (ValidateException $e) {
            // 验证失败 
            dump($e->getError()); // 输出错误信息
            dump($e->getKey()); // 验证错误的字段名
        }
    }
}
~~~

如果你没有定义验证器，也可以通过`validate`方法进行自定义验证规则

~~~
<?php
namespace app\controller;

use think\exception\ValidateException;

class Index
{
    public function index()
    {
        try {
            validate([
                'name'  => 'require|max:25',
                'age'   => 'number|between:1,120',
                'email' => 'email',    
            ])->message([
                'name.require' => '名称必须',
                'name.max'     => '名称最多不能超过25个字符',
                'age.number'   => '年龄必须是数字',
                'age.between'  => '年龄只能在1-120之间',
                'email'        => '邮箱格式错误',    
            ])->check([
                'name'  => 'thinkphp',
                'email' => 'thinkphp@qq.com',
            ]);
        } catch (ValidateException $e) {
            // 验证失败 
            dump($e->getError()); // 输出错误信息
            dump($e->getKey()); // 验证错误的字段名
        }
    }
}
~~~

