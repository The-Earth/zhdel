# zhdel
zhdel.miraheze.org 是一个收集即将被删除的中文维基百科条目的维基站点，具体请见该站首页。该站上运行的自动收集机器人使用本仓库代码。自用代码，要拿去用的话，别忘了填上必要的信息，具体参见mwclient的文档。

注：代码很蠢。

## zhdel.py
主脚本。搜索含有删除模板的中文维基百科条目，并搬运。`logdir`设置日志文件路径，`skip`设置暂时忽略的标题（可能会出现无法解决的问题导致中断，忽略问题条目以暂时避开）。

## clean.py
清理程序。删除最终在中文维基百科上得到保留的条目。`logdir`与`skip`设置于主脚本相同。

## query.py
查询脚本。将已删百科内容搬运到中文维基百科的用户子页面，实现已删除内容查询。其实直接在已删百科上就可以看源代码，只是模板无法显示。目前若操作者不是中文维基百科巡查员，会被16号过滤器挡住而无法编辑。

## 日志文件
这堆东西还依赖于一个同目录下的日志文件。

## 依赖于
- Python 3.x
- [mwclient](https://github.com/mwclient/mwclient) `pip install mwclient`
