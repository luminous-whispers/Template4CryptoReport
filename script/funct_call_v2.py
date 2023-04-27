'''
函数调用图快速生成
作者：yjw
最后修改时间：230426

描述：
该程序自动扫描某文件夹（修改 directory 变量值自定义目录），
自动执行包含 main() 函数，并生成函数调用图 call-graph。

注意，
1. 期间输入值需要手动黏贴入stdin
2. 可以从命令行输入目标文件夹路径，建议绝对路径

Debug:
1. 显示Error importing module, skipping:
    模块如果本身需要执行某些代码，应放入“if __name__ == '__main__'”块中，
    否则PyCallGraph库无法解析该文件执行顺序。

2. 跳过某文件:
    检查是否包含main()函数

优化方向：
检验缓冲区是否被耗尽，否则报错上一个程序异常，并清空上一个文件(不输出)
因为某些文件可能不会报错，但输入是错的
'''

import os
import sys
import importlib
# import subprocess 
# # the pycallgraph will not trace to subprocess, ouput graph is uncomplete
from pycallgraph import PyCallGraph
from pycallgraph.output import GraphvizOutput
from pycallgraph.config import Config

def has_main_function(module_name: str, errors: list)->bool:
    # 文件中必须定义main函数
    try:
        # 注意模块文件中执行代码只能放入"if __name__ == "__main__"块中, 否则导入会失败
        module = importlib.import_module(module_name)
        if hasattr(module, "main"):
            return True
        else:
            error = f"\"{module_name}.py\" !! Warning: module has no main funct. Skipping."
            errors.append(error)
            print(error)
            return False
    except Exception:
        error = f"\"{module_name}.py\" !! Error: importing module failed. Skipping."
        errors.append(error)
        print(error) 
        return False

def is_valid_module(file_name: str, errors: list):
    '''
    判定文件有效性：
    1. 是否自递归，是否是python执行文件
    2. 判断模块中，是否有main函数
    3. 询问用户是否需要执行

    errors 用来记录文件错误信息，直接修改外部errors变量
    '''

    if not file_name.endswith(".py") or file_name.startswith("__"):
        # 非python可执行文件，此错误不会出现在errors中
        return False
    this_script = os.path.basename(__file__)# 防止自递归
    if file_name == this_script:
        # 执行自己的错误不会出现在errors中
        return False
        
    print("\n<--- new module --->")
    module_name = file_name[:-3]  # Remove '.py' extension
    if not has_main_function(module_name, errors):
        # 检查是否包含main()函数
        return False

    print(f"- Do you want to run module \"{module_name}.py\", Input yes or no")
    user_input = input().strip()
    no_dict = ['no', 'No', 'n', 'N', 'NO', '否']
    if user_input in no_dict:
        # 用户拒绝，此文件不会出现在errors信息中
        return False

    return True

def generate_callgraph(module_name: str, output_file: str, errors: str):
    # config for graphviz
    config = Config()
    graphviz = GraphvizOutput()
    graphviz.output_file = output_file

    # import module
    module = importlib.import_module(module_name)

    try: 
        with PyCallGraph(output=graphviz, config=config):
            module.main()
    except Exception as exc:
        error = (f'\"{module_name}.py\" !! Error: {exc}. Module shutdown')
        errors.append(error)
        print(error)
    finally: 
        # 清空 stdin 缓冲区，防止下一个程序异常
        sys.stdin.flush()


if __name__ == "__main__":
    if len(sys.argv)>1:
        # 命令行参数输入目标文件夹
        dir = sys.argv[1]
    else:
        # 硬编码目标文件夹，请自行修改
        dir = "D:\yjw\course\密码学\密码学实验\code\c7-RSA"
    os.chdir(dir)

    errors = [] # 记录一些绘制callgraph失败的文件的信息

    for file in os.listdir(dir):
        if is_valid_module(file, errors):
            module_name = file[:-3]  # Remove '.py' extension

            # check if callgraph directory exists, if not, create it
            if not os.path.exists(dir+ "\callgraph"):
                os.mkdir(dir+ "\callgraph")

            # your identity
            print("- Master: yujiawei")
            # executed file name hint
            print(f"- Running and generating call graph for: \"{file}\"")
            print("- If blocked, you need to input")

            # paint callgraph, can also change output_file target here !!
            output_file = dir+ "\callgraph\\" + f"{module_name}_callgraph.png"
            generate_callgraph(module_name, output_file, errors)

    # error log output
    if errors:
        print("<-- 可疑错误-->\n")
        for error in errors:
            print(error)
    else:
        print("<-- 无异常退出 -->\n")
