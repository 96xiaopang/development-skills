可以在路由规则定义的时候调用`validate`方法指定验证器类对请求的数据进行验证。

例如下面的例子表示对请求数据使用验证器类`app\validate\User`进行自动验证，并且使用`edit`验证场景：
~~~
Route::post('hello/:id', 'index/hello')
	->validate(\app\validate\User::class,'edit');
~~~

或者不使用验证器而直接传入验证规则
~~~php
Route::post('hello/:id', 'index/hello')
    ->validate([
        'name'	=>	'require|min:5|max:50',
        'email'	=>	'email',
    ]);
~~~
`validate`方法也支持传入错误信息
~~~php
Route::post('hello/:id', 'index/hello')
    ->validate([
        'name'	=>	'require|min:5|max:50',
        'email'	=>	'email',
    ], message: [
      'name.require' => '名称必须',
      'name.min'     => '名称最少需要5个字符',
      'name.max'     => '名称最多不能超过50个字符',
      'email'        => '邮箱格式错误',
    ]);
~~~

也支持使用对象化规则定义
~~~php
Route::post('hello/:id', 'index/hello')
    ->validate([
        'name'	=>	ValidateRule::min(5)->max(50),
        'email'	=>	ValidateRule::isEmail(),
    ]);
~~~