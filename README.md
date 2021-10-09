# PyChakura

命令行python程序执行工具。python程序的输出会在界面中显示出来，界面包含如下功能：

- 关键字搜索、高亮；
- 可以输入python脚本与python解释器进行交互，便于debug；

如果你要执行python2.7的脚本，请使用[PyChakura2.7](https://github.com/Tac213/PyChakura27) 。

## 使用方法

创建1个python启动脚本，比如`launch.py`，示例如下：

```python
# -*- coding: utf-8 -*-
# launch script

import sys


def main():
    """
    PyChakura以这个函数为入口函数执行你的python脚本
    Returns:
        None
    """
    # sys.argv可以正常获取
    print(sys.argv)
    # execute your script

```

接着，在你的**脚本工作目录**执行一下命令即可：

```
py -3 %PY_CHAKURA_DIR%/py_chakura.py -m %LAUNCH_SCRIPT_DIR%/launch.py -p "-a 123 -b 456 789", --window_name Customize
```

参数解释：

- `-m`(`--main`): 启动脚本路径，如果启动脚本位于你的脚本工作目录则可以省略`%LAUCH_SCRIPT_DIR`
- `-p`(`--args`): 脚本执行参数， 会体现在`sys.argv`中
- `--window_name`: 自定义窗口名

note: 点击`键(1左边、esc下边)可以进入控制台，查看PyChakura的log。
