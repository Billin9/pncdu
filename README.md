# pncdu
基于 ncdu 实现的一个命令行工具，用来定位文件系统中占用了较大空间的文件、目录


# 依赖的工具和库
- ncdu
- docopt


# 使用方法

```bash
Usage:
  ./pncdu.py [--debug] [PATH]

Arguments:
  PATH    Scan files in the given path (the current directory by default).

Options:
  -h --help              show this help message and exit
  -v --version           show version and exit
  --debug                show all arguments
 ```
