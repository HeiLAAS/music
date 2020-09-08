# music 点歌插件

这是一个适用于Hoshino v2的点歌插件

## 说明

音乐分享的支持来自Mirai，请选择合适的插件获得最好的使用体验，如`go-cqhttp`或`cqhttp-mirai`。

如遇使用问题欢迎提交Issue。

*2020/9/7* 已支持单独搜索网易和QQ，使用点歌命令时标注歌曲来源。

*2020/9/7* 修复了查询失败时的处理机制，使用新版`go-cqhttp`时分享QQ音乐能够显示歌手。

## 安装

输入以下命令安装所需依赖:

```shell
python3.8 -m pip install httpx pycryptodomex
```

**Windows用户请看 [Installation — PyCryptodome 3.9.8 documentation](https://pycryptodome.readthedocs.io/en/latest/src/installation.html#windows-from-sources-python-3-5-and-newer)**

下载或克隆本项目，将`music`文件夹放入`modules`文件夹中，并在`config/__bot__.py`的模块列表里加入`music`。

重启HoshinoBot

## 用法

输入以下命令使用：

- \[点歌 好日子\] 点一首歌。
- \[搜网易 好日子\] 从网易云音乐点一首歌。
- \[搜QQ 好日子\] 从QQ音乐点一首歌。
- \[选择 0\] 从点歌结果中选择一首。

## 本体

本插件来自[laipz8200的魔改版HoshinoBot](https://github.com/laipz8200/HoshinoBot)。