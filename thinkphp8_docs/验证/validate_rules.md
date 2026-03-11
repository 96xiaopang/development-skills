验证规则可以通过字符串、数组、闭包和规则类四种方式进行定义。在验证器中，只能使用前两种方式，而闭包和规则类的定义则适用于使用`rule`方法来动态定义验证规则。

## 属性定义

属性定义方式仅限于验证器，通常类似于下面的方式：
~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule = [
      'name'  => 'require|max:25',
      'age'   => 'number|between:1,120',
      'email' => 'email',
    ];

}
~~~

>[danger] 系统内置了一些常用的验证规则可以满足大部分的验证需求，具体每个规则的含义参考内置规则一节。

因为一个字段可以使用多个验证规则（如上面的`age`字段定义了`number`和`between`两个验证规则），在一些特殊的情况下，为了避免混淆可以在`rule`属性中使用数组定义规则。

~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule = [
      'name'  => ['require', 'max' => 25, 'regex' => '/^[\w|\d]\w+/'],
      'age'   => ['number', 'between' => '1,120'],
      'email' => 'email',
    ];

}
~~~

`V8.1.0+`版本开始，可以通过`must`属性定义必须验证的规则，无论是否使用了`require`规则。例如，下面定义了`name`和`email`为必须验证。
~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $must = ['name', 'email'];
    protected $rule = [
      'name'  => 'max:25',
      'age'   => 'number|between:1,120',
      'email' => 'email',
    ];

}
~~~

## 方法定义
> [danger]本功能需要`V8.1.2+`版本支持

由于属性定义的局限性，因此如果需要定义一些特殊的验证规则，我们可以改成通过方法定义。

```
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected function rules()
    {  
        return [
            'name'  => 'require|max:25',
            'age'   => 'number|between:1,120',
            'email' => 'email',    
        ];
    }
}
```

可以在`rules`方法里面返回数组或当前对象，区别主要在于使用返回数组方式，`rule`属性定义的验证规则不再生效。而对象方式的`rules`定义规则会和`rule`属性定义的合并（存在相同的字段则会覆盖）。

```
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected function rules()
    {  
        return $this
            ->rule('name', 'require|max:25', ['require' => '名称必须', 'max' => '名称最多不能超过25个字符'])
            ->rule('age', 'number|between:1,120', ['number' => '年龄必须是数字', 'between' => '年龄只能在1-120之间'])
            ->rule('email', 'email', '邮箱格式错误');           
    }
}
```

如果没有使用验证器而是独立验证（即手动调用验证类进行验证）方式的话，通常使用`rule`方法进行验证规则的设置，举例说明如下。独立验证通常使用`Facade`或者自己实例化验证类。

~~~
$validate = \think\facade\Validate::rule('age', 'number|between:1,120')
->rule([
    'name'  => 'require|max:25',
    'email' => 'email'
]);

$data = [
    'name'  => 'thinkphp',
    'email' => 'thinkphp@qq.com'
];

if (!$validate->check($data)) {
    dump($validate->getError());
}
~~~

>[info] `rule`方法传入数组表示批量设置规则。

`rule`方法还可以支持使用对象化的规则定义。

我们把上面的验证代码改为

~~~
use think\facade\Validate;
use think\validate\ValidateRule as Rule;

$validate = Validate::rule('age', Rule::isNumber()->between([1,120]))
->rule([
    'name'  => Rule::isRequire()->max(25),
    'email' => Rule::isEmail(),
]);

$data = [
    'name'  => 'thinkphp',
    'email' => 'thinkphp@qq.com'
];

if (!$validate->check($data)) {
    dump($validate->getError());
}
~~~

## 闭包定义

可以对某个字段使用闭包验证，例如：
~~~
$validate = Validate::rule([
    'name'  => function($value) { 
        return 'thinkphp' == strtolower($value) ? true : false;
    },
]);
~~~

闭包支持传入两个参数，第一个参数是当前字段的值（必须），第二个参数是所有数据（可选）。

>[danger] 如果使用了闭包进行验证，则不再支持对该字段使用多个验证规则。

闭包函数如果返回true则表示验证通过，返回false表示验证失败并使用系统的错误信息，如果返回字符串，则表示验证失败并且以返回值作为错误提示信息。

~~~
$validate = Validate::rule([
    'name'  => function($value) { 
        return 'thinkphp' == strtolower($value) ? true : '用户名错误';
    },
]);
~~~

## 规则别名
> [danger]本功能需要`V8.1.2+`版本支持

可以给一些常见的规则定义别名，方便复用。

```
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $alias = [
        'name'    =>    'require|alphaNum|max:25',
        'age'     =>    'number|between:1,120',
    ];
    protected $rule = [
      // 使用规则别名
      'name'  => 'name', 
      'age'   => 'age',
      'email' => 'email',
    ];
}
```

规则别名对应的规则可以是任何有效的规则定义，包括字符串和数组方式。

## 数组验证
> [danger]本功能需要`V8.1.0+`版本支持

支持对数组元素进行验证
~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule = [
      'name'  => 'require|max:25',
      'age'   => 'number|between:1,120',
      // info是一个索引数组 
      'info.email' => 'email',
      'info.score' => 'number',
    ];
}
~~~
支持多维数组验证
~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule = [
      'name'  => 'require|max:25',
      'age'   => 'number|between:1,120',
      // info是一个二维数组 
      'info.*.email' => 'email',
      'info.*.score' => 'number',
    ];
}
~~~

## 验证集
> [danger]本功能需要`V8.1.2+`版本支持

使用验证集的方式定义验证规则，可以简化数组验证规则定义。例如，

```
$validate = \think\facade\Validate::ruleSet('pay', [
    'title'  => 'require',
    'price'  => 'require|integer',
]);
```

相当于下面的定义

```
$validate = \think\facade\Validate::rule([
    'pay.*.title' => 'require',
    'pay.*.price' => 'require|integer',
]);
```

并且可以支持嵌套定义，例如：

```
$validate = \think\facade\Validate::ruleSet('pay', [
     'total'  => 'require|integer',
     'item.*' => rules([
         'title'  => 'require',
         'price'  => 'require|integer',
     ]),
]);
```

## 批量验证

默认情况下，一旦有某个数据的验证规则不符合，就会停止后续数据及规则的验证，如果希望批量进行验证，可以设置：

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
		validate(User::class)->batch(true)->check([
			'name'  => 'thinkphp',
			'email' => 'thinkphp@qq.com',
		    ]);
	} catch (ValidateException $e) {
            // 验证失败 输出错误信息
            // 错误信息是一个包括字段名和错误信息的数组
            dump($e->getError());
        }
    }
}
~~~

## 自定义验证规则

系统内置了一些常用的规则（参考后面的内置规则），如果不能满足需求，可以在验证器单独添加额外的验证方法，例如：

~~~
<?php
namespace app\validate;

use think\Validate;

class User extends Validate
{
    protected $rule = [
        'name'  =>  'checkName:thinkphp',
        'email' =>  'email',
    ];
    
    protected $message = [
        'name'  =>  '用户名必须',
        'email' =>  '邮箱格式错误',
    ];
    
    // 自定义验证规则
    protected function checkName($value, $rule, $data=[])
    {
        return $rule == $value ? true : '名称错误';
    }
}
~~~

验证方法可以传入的参数共有`5`个（后面三个根据情况选用），依次为：
* 验证数据
* 验证规则
* 全部数据（数组）
* 字段名
* 字段描述

>[danger] 自定义的验证规则方法名不能和已有的规则冲突，并且必须使用驼峰命名规范。

## 独立验证

可以对数据进行相关规则的验证，不需要使用验证器。

```
use think\facade\Validate;

Validate::checkRule('thinkphp@qq.com', 'email');
```

`checkRule`方法返回布尔值，验证成功返回true，否则false，可以支持传入多个验证规则

## 全局扩展

你可以在扩展包或者应用里面全局注册验证规则，使用方法

```
Validate::maker(function($validate) {
    $validate->extend('extra', 'extra_validate_callback');
});
```

全局验证规则优先检测，因此你也可以通过全局验证覆盖内置的验证规则。
