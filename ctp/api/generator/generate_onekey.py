#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@ProjectName: ctp
@FileName   : generate_onekey.py
@Date       : 2025/9/1 15:20
@Author     : Donny
@Email      : donnymoving@gmail.com
@Software   : PyCharm
@Description: 一键生成 MD和TD cpp、h文件
"""
import subprocess
import sys


if __name__ == '__main__':
    # 1. 第一步：生成API函数常量文件，请在 generator_function_const.py 中运行 main 函数
    result = subprocess.run([sys.executable, 'generator_function_const.py'])
    if result.returncode != 0:
        print("生成API函数常量文件失败")
        exit(1)

    # 2. 第二步：生成DLL入口文件
    result = subprocess.run([sys.executable, 'generate_dll_entry.py'])
    if result.returncode != 0:
        print("生成DLL入口文件失败")
        exit(1)

    # 3. 第三步：生成API DataType文件
    result = subprocess.run([sys.executable, 'generate_data_type.py'])
    if result.returncode != 0:
        print("生成API DataType文件失败")
        exit(1)

    # 4. 第四步：生成API结构体文件
    result = subprocess.run([sys.executable, 'generate_struct.py'])
    if result.returncode != 0:
        print("生成API结构体文件失败")
        exit(1)

    # 5. 第五步：生成API函数文件
    result = subprocess.run([sys.executable, 'generate_api_functions.py'])
    if result.returncode != 0:
        print("生成API函数文件失败")
        exit(1)

    # 6. 第六步：生成API cpp、h文件
    result = subprocess.run([sys.executable, 'generate_cpp.py'])
    if result.returncode != 0:
        print("生成API cpp、h文件失败")
        exit(1)
