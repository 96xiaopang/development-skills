系统内置了一些常用的验证规则，可以完成大部分场景的验证需求，包括：

>[danger] 验证规则严格区分大小写

## 格式验证类

格式验证类的验证规则如果在使用静态方法调用的时候需要加上`is`（以`number`验证为例，需要使用 `isNumber()`）。

>[info]### require

验证某个字段必须，例如：
~~~
'name'=>'require'
~~~
>[danger] 如果验证规则没有添加`require`就表示没有值的话不进行验证

>[danger] 由于`require`属于PHP保留字，所以在使用方法验证的时候必须使用`isRequire`或者`must`方法调用。

>[info]### number

验证某个字段的值是否为纯数字（采用`ctype_digit`验证，不包含负数和小数点），例如：
~~~
'num'=>'number'
~~~

>[info]### integer

验证某个字段的值是否为整数（采用`filter_var`验证），例如：
~~~
'num'=>'integer'
~~~

>[info]### float

验证某个字段的值是否为浮点数字（采用`filter_var`验证），例如：
~~~
'num'=>'float'
~~~

>[info]### boolean 或者 bool

验证某个字段的值是否为布尔值（采用`filter_var`验证），例如：
~~~
'num'=>'boolean'
~~~

>[info]### email

验证某个字段的值是否为email地址（采用`filter_var`验证），例如：
~~~
'email'=>'email'
~~~

>[info]### array

验证某个字段的值是否为数组，例如：
~~~
'info'=>'array'
~~~

支持验证数组必须包含某些键名（多个用逗号分割），例如：
~~~
'info'=>'array:name,email'
~~~
>[info]### enum:枚举类名
验证某个字段的值是否在允许的枚举值范围（支持普通枚举、回退枚举和自定义枚举类），例如：
~~~
'status' => 'enum:' . StatusEnum::class
~~~
或者简化为
~~~
'status' => StatusEnum::class
~~~
使用简化定义的方式只能是普通枚举和回退枚举，或者实现了`think\contract\Enumable`接口的自定义枚举类。

>[info]### string

验证某个字段的值是否为字符串，例如：
~~~
'info'=>'string'
~~~

>[info]### accepted


待验证的字段必须是 `「yes」` 、`「on」` 、`1`、`「1」`、`true` 或 `「true」`。这对于验证「服务条款」接受或类似字段非常有用。例如：
~~~
'accept'=>'accepted'
~~~

>[info]### acceptedIf\:field,value

如果`field`字段的值等于指定`value`值，则验证字段必须为 `「yes」` 、`「on」` 、`1`、`「1」`、`true` 或 `「true」`。这对于验证「服务条款」接受或类似字段非常有用。


>[info] ### declined

验证某个字段的值必须是 `「no」`，`「off」`，`0`，`「0」`，`false` 或者 `「false」` 。

>[info] ### declinedIf\:field,value

如果`field`字段的值等于指定`value`值，则验证字段的值必须为`「no」`，`「off」`，`0`，`「0」`，`false` 或者 `「false」` 。

>[info] ### multipleOf\:value

验证某个字段的值必须是某个值的倍数，例如：
~~~
'number'=>'multipleOf:10'
~~~

>[info]### date

验证值是否为有效的日期，例如：
~~~
'date'=>'date'
~~~
会对日期值进行`strtotime`后进行判断。

>[info]### alpha

验证某个字段的值是否为纯字母，例如：
~~~
'name'=>'alpha'
~~~

>[info]### alphaNum

验证某个字段的值是否为字母和数字，例如：
~~~
'name'=>'alphaNum'
~~~

>[info]### alphaDash

验证某个字段的值是否为字母和数字，下划线`_`及破折号`-`，例如：
~~~
'name'=>'alphaDash'
~~~

>[info]### chs

验证某个字段的值只能是汉字，例如：
~~~
'name'=>'chs'
~~~

>[info]### chsAlpha

验证某个字段的值只能是汉字、字母，例如：
~~~
'name'=>'chsAlpha'
~~~

>[info]### chsAlphaNum

验证某个字段的值只能是汉字、字母和数字，例如：
~~~
'name'=>'chsAlphaNum'
~~~

>[info]### chsDash

验证某个字段的值只能是汉字、字母、数字和下划线_及破折号-，例如：
~~~
'name'=>'chsDash'
~~~

>[info]### cntrl

验证某个字段的值只能是控制字符（换行、缩进、空格），例如：
~~~
'name'=>'cntrl'
~~~

>[info]### graph

验证某个字段的值只能是可打印字符（空格除外），例如：
~~~
'name'=>'graph'
~~~

>[info]### print 

验证某个字段的值只能是可打印字符（包括空格），例如：
~~~
'name'=>'print'
~~~

>[info]### lower

验证某个字段的值只能是小写字符，例如：
~~~
'name'=>'lower'
~~~

>[info]### upper

验证某个字段的值只能是大写字符，例如：
~~~
'name'=>'upper'
~~~

>[info]### space

验证某个字段的值只能是空白字符（包括缩进，垂直制表符，换行符，回车和换页字符），例如：
~~~
'name'=>'space'
~~~

>[info]### xdigit

验证某个字段的值只能是十六进制字符串，例如：
~~~
'name'=>'xdigit'
~~~

>[info]### activeUrl

验证某个字段的值是否为有效的域名或者IP，例如：
~~~
'host'=>'activeUrl'
~~~

>[info]### url

验证某个字段的值是否为有效的URL地址（采用`filter_var`验证），例如：
~~~
'url'=>'url'
~~~

>[info]### ip

验证某个字段的值是否为有效的IP地址（采用`filter_var`验证），例如：
~~~
'ip'=>'ip'
~~~
支持验证ipv4和ipv6格式的IP地址。

>[info]### dateFormat\:format

验证某个字段的值是否为指定格式的日期，例如：
~~~
'create_time'=>'dateFormat:y-m-d'
~~~

>[info]### mobile

验证某个字段的值是否为有效的手机，例如：
~~~
'mobile'=>'mobile'
~~~

>[info]### idCard

验证某个字段的值是否为有效的身份证格式，例如：
~~~
'id_card'=>'idCard'
~~~

>[info]### macAddr

验证某个字段的值是否为有效的MAC地址，例如：
~~~
'mac'=>'macAddr'
~~~

>[info]### zip

验证某个字段的值是否为有效的邮政编码，例如：
~~~
'zip'=>'zip'
~~~

## 长度和区间验证类

>[info]### in

验证某个字段的值是否在某个范围，例如：
~~~
'num'=>'in:1,2,3'
~~~

>[info]### notIn

验证某个字段的值不在某个范围，例如：
~~~
'num'=>'notIn:1,2,3'
~~~

>[info]### between

验证某个字段的值是否在某个区间，例如：
~~~
'num'=>'between:1,10'
~~~

>[info]### notBetween

验证某个字段的值不在某个范围，例如：
~~~
'num'=>'notBetween:1,10'
~~~

>[info]### length\:num1,num2

验证某个字段的值的长度是否在某个范围，例如：
~~~
'name'=>'length:4,25'
~~~
或者指定长度
~~~
'name'=>'length:4'
~~~

> 如果验证的数据是数组，则判断数组的长度。
> 如果验证的数据是File对象，则判断文件的大小。

>[info]### max\:number

验证某个字段的值的最大长度，例如：
~~~
'name'=>'max:25'
~~~

> 如果验证的数据是数组，则判断数组的长度。
> 如果验证的数据是File对象，则判断文件的大小。

>[info]### min\:number

验证某个字段的值的最小长度，例如：
~~~
'name'=>'min:5'
~~~

> 如果验证的数据是数组，则判断数组的长度。
> 如果验证的数据是File对象，则判断文件的大小。

>[info]### after:日期

验证某个字段的值是否在某个日期之后，例如：
~~~
'begin_time' => 'after:2016-3-18',
~~~

>[info]### before:日期

验证某个字段的值是否在某个日期之前，例如：
~~~
'end_time'   => 'before:2016-10-01',
~~~

>[info]### expire:开始时间,结束时间

验证当前操作（注意不是某个值）是否在某个有效日期之内，例如：
~~~
'expire_time'   => 'expire:2016-2-1,2016-10-01',
~~~

>[info]### allowIp\:allow1,allow2,...

验证当前请求的IP是否在某个范围，例如：
~~~
'name'   => 'allowIp:114.45.4.55',
~~~
该规则可以用于某个后台的访问权限，多个IP用逗号分隔

>[info]### denyIp\:allow1,allow2,...

验证当前请求的IP是否禁止访问，例如：
~~~
'name'   => 'denyIp:114.45.4.55',
~~~
多个IP用逗号分隔

## 字段比较类
>[info]### confirm\:field

验证某个字段是否和另外一个字段的值一致，例如：
~~~
'repassword'=>'require|confirm:password'
~~~

支持字段自动匹配验证规则，如`password`和`password_confirm`是自动相互验证的，只需要使用
~~~
'password'=>'require|confirm'
~~~
会自动验证和`password_confirm`进行字段比较是否一致，反之亦然。

>[info]### different\:field

验证某个字段是否和另外一个字段的值不一致，例如：
~~~
'name'=>'require|different:account'
~~~

>[info]### startWith\:str

验证某个字段是否以某个字符串开头，例如：
~~~
'name'=>'require|startWith:think'
~~~

>[info]### endWith\:str

验证某个字段是否以某个字符串结尾，例如：
~~~
'name'=>'require|endWith:think'
~~~

>[info]### contain\:str

验证某个字段是否以包含某个字符串，例如：
~~~
'name'=>'require|contain:think'
~~~

>[info]### eq 或者 = 或者 same

验证是否等于某个值，例如：
~~~
'score'=>'eq:100'
'num'=>'=:100'
'num'=>'same:100'
~~~

>[info]### egt 或者 >=

验证是否大于等于某个值，例如：
~~~
'score'=>'egt:60'
'num'=>'>=:100'
~~~

>[info]### gt 或者 >

验证是否大于某个值，例如：
~~~
'score'=>'gt:60'
'num'=>'>:100'
~~~

>[info]### elt 或者 <=

验证是否小于等于某个值，例如：
~~~
'score'=>'elt:100'
'num'=>'<=:100'
~~~

>[info]### lt 或者 <

验证是否小于某个值，例如：
~~~
'score'=>'lt:100'
'num'=>'<:100'
~~~

>[info]### 字段比较

验证对比其他字段大小（数值大小对比），例如：
~~~
'price'=>'lt:market_price'
'price'=>'<:market_price'
~~~

## filter验证
支持使用`filter_var`进行验证，例如：
~~~
'ip'=>'filter:validate_ip'
~~~
具体支持规则可以参考`filter_list`函数的返回列表。

## 正则验证
支持直接使用正则验证，例如：
~~~
'zip'=>'\d{6}',
// 或者
'zip'=>'regex:\d{6}',
~~~
如果你的正则表达式中包含有`|`符号的话，必须使用数组方式定义。
~~~
'accepted'=>['regex'=>'/^(yes|on|1)$/i'],
~~~
也可以实现预定义正则表达式后直接调用，例如在验证器类中定义regex属性

~~~
namespace app\index\validate;

use think\Validate;

class User extends Validate
{
    protected $regex = [ 'zip' => '\d{6}'];
    
    protected $rule = [
        'name'  =>  'require|max:25',
        'email' =>  'email',
    ];

}
~~~

然后就可以使用
~~~
'zip'	=>	'regex:zip',
~~~

## 上传验证

>[info]### file

验证是否是一个上传文件

>[info]### image\:width,height,type

验证是否是一个图像文件，width height和type都是可选，width和height必须同时定义。

>[info]### fileExt:允许的文件后缀

验证上传文件后缀

>[info]### fileMime:允许的文件类型

验证上传文件类型

>[info]### fileSize:允许的文件字节大小

验证上传文件大小

## 其它验证

>[info] ### token:表单令牌名称

表单令牌验证

>[info]### unique\:table,field,except,pk

验证当前请求的字段值是否为唯一的，例如：
~~~
// 表示验证name字段的值是否在user表（不包含前缀）中唯一
'name'   => 'unique:user',
// 验证其他字段
'name'   => 'unique:user,account',
// 排除某个主键值
'name'   => 'unique:user,account,10',
// 指定某个主键值排除
'name'   => 'unique:user,account,10,user_id',
~~~
如果需要对复杂的条件验证唯一，可以使用下面的方式：
~~~
// 多个字段验证唯一验证条件
'name'   => 'unique:user,status^account',
// 复杂验证条件
'name'   => 'unique:user,status=1&account='.$data['account'],
~~~

>[info]### requireIf\:field,value

验证某个字段的值等于某个值的时候必须，例如：
~~~
// 当account的值等于1的时候 password必须
'password'=>'requireIf:account,1'
~~~

>[info]### requireWith\:field

验证某个字段有值的时候必须，例如：
~~~
// 当account有值的时候password字段必须
'password'=>'requireWith:account'
~~~

>[info]### requireWithout\:field

验证某个字段没有值的时候必须，例如：
~~~
// mobile和phone必须输入一个
'mobile' => 'requireWithout:phone',
'phone'  => 'requireWithout:mobile'
~~~

>[info]### requireCallback\:callable

验证当某个callable为真的时候字段必须，例如：
~~~
// 使用check_require方法检查是否需要验证age字段必须
'age'=>'requireCallback:check_require|number'
~~~

用于检查是否需要验证的方法支持两个参数，第一个参数是当前字段的值，第二个参数则是所有的数据。
~~~
function check_require($value, $data){
    if(empty($data['birthday'])){
    	return true;
    }
}
~~~
只有check_require函数返回true的时候age字段是必须的，并且会进行后续的其它验证。