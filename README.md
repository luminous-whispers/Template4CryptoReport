**自制的BUAA-网安-密码学实验模板，附赠一些小脚本**

## How to use

将每个大实验（比如RSA）的各个小实验（如共模攻击）分为单独的模块 src/experiment[lab no].tex。

### Latex文件夹结构

demo

|

\+ - /fonts: 放导入的字体

|

\+ - /pic: 放图片，推荐命名为callback-[lab no].png（调用图）、test-[lab no].png（测试样例）

|

\+ - /script: 小脚本

|

\+ - /src: 放小实验的tex文件、伪代码、思考题

### 注意事项

1. 使用Xelatex编译，路径不要有中文
2. 空行代表分段；不空行tex中换行不会分段，但可以使用\\在pdf中换行。分段可以从首行缩进看出。
3. 如果图片等插入的内容在pdf中没有更新，尝试删除main.aux缓存文件，或重命名插入文件。

> 有bug在issue中提

## Something else

### 相关推荐

1. 截图软件推荐使用snipaste
2. IDE推荐使用VScode，安装Latex WorkShip
3. 鉴于latex编译缓慢，且并不直观。推荐在markdown实时渲染器下编辑大段文字和公式，黏贴入tex文件内即可。
4. 如果借鉴互联网内容，推荐使用markdownload浏览器插件，自动提取文本内容和数学公式

### 小脚本

1. 自动扫描整个文件夹并绘制callgraph调用图，funct_call-v2.py
2. 将python转为pseudocode形式，py2pseudocode.py


## Dev Log

这里小孩子不要研究
1. 可能会默认使用\\(\\)符号来输入行内数学公式。
