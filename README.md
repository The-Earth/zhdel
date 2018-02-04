# zhdel
zhdel.miraheze.org 是一个收集即将被删除的中文维基百科条目的维基站点，具体请见该站首页。该站上运行的自动收集机器人使用本仓库代码。

注：代码很蠢。

## zhdel.py
主脚本。搜索含有删除模板的中文维基百科条目，并搬运。

## clean.py
清理程序。删除最终在中文维基百科上得到保留的条目。

## getwhole.py
出了毛病不得不调试时，用它获取当前zhdel上所有页面的列表。

## 日志文件
这堆东西还依赖于一个同目录下的日志文件。

## 依赖于
- Python 3.x
- [mwclient](https://github.com/mwclient/mwclient) `pip install mwclient`
