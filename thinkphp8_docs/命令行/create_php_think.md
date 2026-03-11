## 创建自定义指令

第一步，创建一个自定义命令类文件，运行指令
~~~
php think make:command Hello hello
~~~

会生成一个`app\command\Hello`命令行指令类，指令名为hello，我们修改内容如下：

~~~
<?php
namespace app\command;

use think\console\Command;
use think\console\Input;
use think\console\input\Argument;
use think\console\input\Option;
use think\console\Output;

class Hello extends Command
{
    protected function configure()
    {
        $this->setName('hello')
        	->addArgument('name', Argument::OPTIONAL, "your name")
            ->addOption('city', null, Option::VALUE_REQUIRED, 'city name')
        	->setDescription('Say Hello');
    }

    protected function execute(Input $input, Output $output)
    {
    	$name = trim($input->getArgument('name'));
      	$name = $name ?: 'thinkphp';

		if ($input->hasOption('city')) {
        	$city = PHP_EOL . 'From ' . $input->getOption('city');
        } else {
        	$city = '';
        }
        
        $output->writeln("Hello," . $name . '!' . $city);
    }
}
~~~
这个文件定义了一个叫`hello`的命令，并设置了一个`name`参数和一个`city`选项。

第二步，配置`config/console.php`文件

~~~
<?php
return [
    'commands' => [
        'hello' => 'app\command\Hello',
    ]
];
~~~

第三步，测试-命令帮助-命令行下运行

~~~
php think
~~~
输出
~~~cmd
Think Console version 0.1

Usage:
  command [options] [arguments]

Options:
  -h, --help            Display this help message
  -V, --version         Display this console version
  -q, --quiet           Do not output any message
      --ansi            Force ANSI output
      --no-ansi         Disable ANSI output
  -n, --no-interaction  Do not ask any interactive question
  -v|vv|vvv, --verbose  Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

Available commands:
  build              Build Application Dirs
  clear              Clear runtime file
  hello              Say Hello 
  help               Displays help for a command
  list               Lists commands
 make
  make:controller    Create a new resource controller class
  make:model         Create a new model class
 optimize
  optimize:autoload  Optimizes PSR0 and PSR4 packages to be loaded with classmaps too, good for production.
  optimize:config    Build config and common file cache.
  optimize:schema    Build database schema cache.

~~~

第四步，运行`hello`命令
~~~cmd
php think hello
~~~
输出
~~~
Hello thinkphp!
~~~
添加命令参数
~~~cmd
php think hello kancloud
~~~
输出
~~~
Hello kancloud!
~~~
添加`city`选项
~~~cmd
php think hello kancloud --city shanghai
~~~
输出
~~~
Hello kancloud!
From shanghai
~~~

>[danger] 注意看参数和选项的调用区别
>

如果需要生成一个指定的命名空间，可以使用：

~~~
php think make:command app\index\Command second
~~~

## 在控制器中调用命令

支持在控制器的操作方法中直接调用命令，例如：

~~~
<?php
namespace app\index\controller;

use think\facade\Console;

class Index
{
    public function hello($name)
    {
        $output = Console::call('hello', [$name]);

        return $output->fetch();
    }
}
~~~

访问该操作方法后，例如：

~~~
http://serverName/index/hello/name/thinkphp
~~~
页面会输出
~~~
Hello thinkphp!
~~~

## 命令行选项

```
use think\\console\\input\\Option;

 // 无需传值
 Option::VALUE_NONE     = 1;
 // 必须传值
 Option::VALUE_REQUIRED = 2;
 // 可选传值
 Option::VALUE_OPTIONAL = 4;
 // 传数组值
 Option::VALUE_IS_ARRAY = 8;
```

## addOption

```
/**
* 添加选项
* @param  string $name        选项名称
* @param  string $shortcut    别名
* @param  int $mode        类型
* @param  string $description 描述
* @param  mixed $default     默认值
* @return  Command
*/
 public function addOption(string  $name, string  $shortcut = null, int  $mode = null, string  $description = '', $default = null)
```
### 示例
定义如下:
```
->addOption('adminname', 'p', Option::VALUE_OPTIONAL, '管理员账号')
```
调用方式可以如下:
```
// 无需任何参数
php think install
// 使用全名参数
php think install --adminuser admin
// 使用缩写
php think install -u admin
```
指令逻辑中可以这样获取:
```
$input->getOption('adminname');
```

