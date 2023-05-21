'''
函数调用图快速生成
作者：yjw
最后修改时间：230521

描述：
该程序自动扫描某文件夹（修改 directory 变量值自定义目录），
自动执行包含 main() 函数，并生成函数调用图 call-graph。
同一程序支持绘制多次

注意，
1. 期间输入值需要手动黏贴入stdin，输入结束后需要Ctrl+Z结束输入
2. 支持命令行调用, 可从命令行直接指定路径

Debug:
1. 显示Error importing module, skipping:
    模块如果本身需要执行某些代码，应放入“if __name__ == '__main__'”块中，
    否则PyCallGraph库无法解析该文件执行顺序。

2. 跳过某文件:
    检查是否包含main()函数

优化方向：
扫描子文件夹
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

    print(f"- Do you want to run module \"{module_name}.py\"? Input y/n.")
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
        # 清空 stdin(python) 缓冲区，防止下一个程序异常
        sys.stdin.flush()
        # 清空命令行缓冲区
        while True:
            remaining = sys.stdin.read(1)
            if not remaining:
                break


if __name__ == "__main__":

    if len(sys.argv)>1:
        # 命令行参数输入目标文件夹
        dir = sys.argv[1]
    else:
        # 硬编码目标文件夹，请自行修改
        dir = "D:\yjw\course\Cryptography\CryptoLab\code\c10-Signature"

    # 修改工作目录，此后使用相对路径
    os.chdir(dir) 

    # 记录一些异常文件信息
    errors = []

    # 检查输出文件路径是否存在，不存在则创建
    if not os.path.exists(".\callgraph"):
        os.mkdir(".\callgraph")
    output_dir = ".\callgraph\\"

    for file in os.listdir("."): 
        if is_valid_module(file, errors):

            module_name = file[:-3]  # Remove '.py' extension

            # your identity
            # print("- Master: yujiawei")
            cnt = 1
            # 支持执行多次
            while True:
                # executed file name hint
                print(f"- Running and generating Call-Graph for: \"{file}\"")
                print("- Waiting for Input or EOF")

                # paint callgraph!!
                output_file = output_dir + f"{module_name}_callgraph{cnt}.png"
                generate_callgraph(module_name, output_file, errors)

                print(f"- Run \"{module_name}.py\" again?")
                user_input = input().strip()
                yes_dict = ['y', 'Y', 'yes', '1', 'Yes', '是', '好']
                if user_input not in yes_dict:
                    break
                cnt += 1

    # error log output
    if errors:
        print("\n<-- 可疑错误 -->\n")
        for error in errors:
            print(error)
    else:
        print("\n<-- 无异常退出 -->\n")
