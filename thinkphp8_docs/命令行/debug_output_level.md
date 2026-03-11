默认情况下，命令行中输出的内容很少，即便是异常和报错也如此，可以通过调整输出级别，显示更多信息。

- 不显示信息(静默)
```
php think runcmd 
php think runcmd -q
php think runcmd --quiet
```
- 详细信息
```
php think runcmd -v
```

- 非常详细的信息
```
php think runcmd -vv
```
- 调试信息
```
php think runcmd -vvv
```

开发者可以判断输出级别，在命令行中进行不同的输出：

```
$output->isDebug();            // 调试模式
$output->isVeryVerbose();    // 非常详细的信息
$output->isVerbose();            // 详细信息
$output->isQuiet();                // 静默信息
$output->getVerbosity();        // 获取输出级别常量，可参考\think\\console\Output
```