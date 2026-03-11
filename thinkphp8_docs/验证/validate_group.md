## 验证分组
> [danger]本功能需要`V8.1.2+`版本支持

可以给验证规则定义分组，每个分组的规则彼此独立，但可以共用别名规则和错误信息，相当于把多个验证器类合并成一个验证类。

```
namespace app\validate;

use think\Validate;

class Project extends Validate
{
    protected $message  =   [
        'name.require' => '名称必须',
        'name.max'     => '名称最多不能超过25个字符',
        'age.number'   => '年龄必须是数字',
        'age.between'  => '年龄只能在1-120之间',
        'email'        => '邮箱格式错误',    
    ];
    
    protected $group = [
        'user'  =>  [
            'name'  => 'require|max:25',
            'age'   => 'number|between:1,120',
            'email' => 'email',    
        ],
    ];    
}
```

然后可以在验证方法中指定验证的分组

```
$data = [
    'name'  => 'thinkphp',
    'age'   => 10,
    'email' => 'thinkphp@qq.com',
];

try {
    validate(app\validate\Project::class)
        ->check($data, 'user');
} catch (ValidateException $e) {
    // 验证失败 输出错误信息
    var_dump($e->getError());
}
```

可以单独为某个分组定义方法（方法的命名规范是`rules`+分组名），并且通过数组或方法设置分组规则，例如：

```
namespace app\validate;

use think\Validate;

class Project extends Validate
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
    
    // 分组规则定义
    public function rulesUser()
    {
    	return [
            'name'  => 'require|max:25',
            'age'   => 'number|between:1,120',
            'email' => 'email',  
        ];
    }    
}
```

可以使用方法定义分组，这个时候必须传入一个`validate`参数，该参数是一个`Validate`对象。

```
namespace app\validate;

use think\Validate;

class Project extends Validate
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
    
    // 分组规则定义
    public function rulesUser(Validate $validate)
    {
    	return $validate->rule([
            'name'  => 'require|max:25',
            'age'   => 'number|between:1,120',
            'email' => 'email',  
        ]);
    }    
}
```

