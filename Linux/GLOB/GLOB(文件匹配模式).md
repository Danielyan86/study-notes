# 定义
- wiki https://en.wikipedia.org/wiki/Glob_(programming)
- glob 是一种文件匹配模式，全称 global，它起源于 Unix 的 bash shell 中，比如在 linux 中常用的 mv *.txt tmp/ 中，*.txt 就使用到了这种模式。
# 命令通配符
通配符又叫做 globbing patterns。因为 Unix 早期有一个/etc/glob文件保存通配符模板，后来 Bash 内置了这个功能，但是这个名字被保留了下来。
通配符早于正则表达式出现，可以看作是原始的正则表达式。它的功能没有正则那么强大灵活，但是胜在简单和方便。

# 用法
> shell 通配符 / glob 模式通常用来匹配目录以及文件，而不是文本！！！
- 通配符是先解释，再执行。
```
bash-3.2$ ls *.txt
a.txt	ab.txt	abc.txt
```
*.txt 先被解析成ls a.txt	ab.txt	abc.txt，再执行。

- 通配符不匹配，会原样输出。
```
bash-3.2$ echo d*
d*
```
- 没有加路径情况下，只适用于当前目录路径匹配。
- 文件名不建议使用通配符，比如*.txt, z

## 语法
|字符	|解释|
| ---- | ----  |
|*	|匹配任意长度任意字符|
|?	|匹配任意单个字符|
|[list]	|匹配指定范围内（list）任意单个字符，也可以是单个字符组成的集合|
|[^list]	|匹配指定范围外的任意单个字符或字符集合|
|[!list]	|同[^list]|
|{str1,str2,...}	|匹配 srt1 或者 srt2 或者更多字符串，也可以是集合|

## 专用字符集

|字符	| 意义|
| ---- | ----  |
|[:alnum:]|	任意数字或者字母|
|[:alpha:]	|任意字母|
|[:space:]	|空格|
|[:lower:]	|小写字母
|[:digit:]	|任意数字
|[:upper:]	|任意大写字母
|[:cntrl:]	|控制符
|[:graph:]	|图形
|[:print:]	|可打印字符
|[:punct:]	|标点符号
|[:xdigit:]	|十六进制数
|[:blank:]	|空白字符（未验证）

## 例子
### ?
?不能匹配空字符。也就是说，它占据的位置必须有字符存在。
```
bash-3.2$ touch a.txt b.txt
bash-3.2$ ls
GLOB.md		aasf		b.txt		glob.sh
a.txt		aasf.txt	file		test
bash-3.2$ ls ?.txt
a.txt	b.txt
```

### *
匹配任意长度的字符。
```
bash-3.2$ touch ab.txt a.txt abc.txt
bash-3.2$ ls *.txt
a.txt	ab.txt	abc.txt
```
列出当前目录所有文件
```
ls *
GLOB.md	a.txt	ab.txt	abc.txt	b.txt	glob.sh
```

使用echo命令打印当前目录文件
```
echo *
GLOB.md a.txt ab.txt abc.txt b.txt glob.sh
```
why？通配符会先被shell翻译，然后再传给命令echo。所以，在echo命令执行之前，这个命令被翻译成
```
echo report.txt report1.txt report11.txt report3.txt report5.txt
report09.txt report10.txt report2.txt report4.txt

```

## ** 
- bash version >= 4.0 
> shopt -s globstar  确认globstar 打开，否则`**`会被翻译成`*`使用
### shopt命令
用于显示和设置shell中的行为选项，通过这些选项以增强shell易用性。shopt命令若不带任何参数选项，则可以显示所有可以设置的shell操作选项。
- -s：激活指定的shell行为选项；
- -u：关闭指定的shell行为选项。


列出出当前目录以及**子目录**下面所有文件
```
ls **
GLOB/GLOB(文件匹配模式).md		filesystem/open_functions.py		filesystem/requests_downlarge_file.py
filesystem/open_buffering.py		filesystem/open_large_file.py		filesystem/文件读写详解.md
filesystem/open_encode.py		filesystem/open_mode.py			regex/regex.sh
filesystem/open_function_issatty.py	filesystem/open_newline.py

GLOB:
GLOB(文件匹配模式).md

filesystem:
open_buffering.py		open_functions.py		open_newline.py
open_encode.py			open_large_file.py		requests_downlarge_file.py
open_function_issatty.py	open_mode.py			文件读写详解.md

regex:
regex.sh
```

### [...] 
匹配方括号之中的任意一个字符，比如[aeiou]可以匹配五个元音字母。
```
bash-3.2$ touch  a.txt b.txt
bash-3.2$ ls [ab].txt
a.txt	b.txt
```

方括号匹配任意一个连续子母。
```
bash-3.2$ ouch aac abc acc adc aec
bash-3.2$ echo a[a-d]c
aac abc acc adc
```

### [^...] 和 [!...]
[^...]和[!...]表示匹配不在方括号里面的字符（不包括空字符）。这两种写法是等价的。
```
bash-3.2$ touch aac abc
bash-3.2$ echo a[^a]c
abc
```

### {...} 
表示匹配大括号里面的所有模式，模式之间使用逗号分隔。
```
echo d{a,e,i,u,o}g
dag deg dig dug dog
```

多字符模式
```
bash-3.2$ touch aac abc acc adc aec
bash-3.2$ echo {aac, aec}
{aac, aec}
bash-3.2$ echo {aac,aec}
aac aec
```

## .gitignore
git 的 .gitignore 文件可以使用 glob 模式匹配， 另外还有一些规则：
- 所有空行或者以 # 开头的行都会被 Git 忽略
- 匹配模式可以以 / 开头防止递归
- 匹配模式可以以 / 结尾指定目录
- 要忽略指定模式以外的文件或目录，可以在模式前加上惊叹号 ! 取反

## 参考文档：
- http://www.ruanyifeng.com/blog/2018/09/bash-wildcards.html
- https://www.cnblogs.com/divent/p/5762154.html
- https://medium.com/@leedowthwaite/why-most-people-only-think-they-understand-wildcards-63bb9c2024ab