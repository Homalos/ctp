#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
自动生成C++ DLL入口点代码文件
生成dllmain.cpp、stdafx.cpp、stdafx.h三个文件
生成所有文件到当前目录
python generate_dll_entry.py all

生成到指定目录
python generate_dll_entry.py all ./output

只生成dllmain.cpp
python generate_dll_entry.py dllmain.cpp

预览stdafx.h内容
python generate_dll_entry.py preview stdafx.h
"""

import os
from pathlib import Path
from typing import Dict

class DllEntryGenerator:
    """DLL入口点代码生成器"""
    
    def __init__(self, output_dir_name: str = "."):
        """
        初始化生成器
        """
        self.output_dir = "."

        self.output_dir_name = output_dir_name

        self.files_to_generate = {
            'dllmain.cpp': self.generate_dllmain_cpp,
            'stdafx.cpp': self.generate_stdafx_cpp,
            'stdafx.h': self.generate_stdafx_h
        }

    @staticmethod
    def generate_dllmain_cpp() -> str:
        """生成dllmain.cpp文件内容"""
        content = """// dllmain.cpp : 定义 DLL 应用程序的入口点。
#include "stdafx.h"

BOOL APIENTRY DllMain( HMODULE hModule,
                       DWORD  ul_reason_for_call,
                       LPVOID lpReserved
                     )
{
\tswitch (ul_reason_for_call)
\t{
\tcase DLL_PROCESS_ATTACH:
\tcase DLL_THREAD_ATTACH:
\tcase DLL_THREAD_DETACH:
\tcase DLL_PROCESS_DETACH:
\t\tbreak;
\t}
\treturn TRUE;
}

"""
        return content

    @staticmethod
    def generate_stdafx_cpp() -> str:
        """生成stdafx.cpp文件内容"""
        content = """#include "stdafx.h"

"""
        return content

    @staticmethod
    def generate_stdafx_h() -> str:
        """生成stdafx.h文件内容"""
        content = """// stdafx.h: 标准系统包含文件的包含文件，
// 或是经常使用但不常更改的
// 特定于项目的包含文件
//

#pragma once

#include "targetver.h"

#define WIN32_LEAN_AND_MEAN             // 从 Windows 头文件中排除极少使用的内容
// Windows 头文件
#include <windows.h>



// 在此处引用程序需要的其他标头

"""
        return content

    def create_output_dir(self):
        """创建输出目录（如果不存在）"""

        # 获取当前文件的Path对象
        current_file = Path(__file__).resolve()

        # 获取当前文件所在的目录父目录 /ctp/api/src
        parent_path: Path = current_file.parent.parent

        output_path: Path = Path(parent_path / "src" / self.output_dir_name)

        self.output_dir = os.fspath(output_path)
        print(f"输出目录路径: {self.output_dir}")

        if not output_path.exists():
            try:
                output_path.mkdir(parents=True, exist_ok=True)
                print(f"目录已创建: {output_path}")
                return True
            except PermissionError:
                print(f"权限不足，无法创建目录: {output_path}")
                return False
            except OSError as e:
                print(f"创建目录时出错: {e}")
                return False
        else:
            return True

    def write_file(self, filename: str, content: str) -> bool:
        """
        写入文件
        
        Args:
            filename: 文件名
            content: 文件内容
            
        Returns:
            bool: 是否成功写入
        """
        filepath = os.path.join(self.output_dir, filename)
        try:
            with open(filepath, 'w', encoding='gb2312') as f:
                f.write(content)
            
            # 统计文件信息
            lines = content.count('\n')
            size = len(content.encode('gb2312'))
            print(f"✓ 成功生成 {filename}")
            print(f"  - 文件大小: {size} 字节")
            print(f"  - 行数: {lines} 行")
            print(f"  - 路径: {filepath}")
            
            return True
        except Exception as e:
            print(f"✗ 写入文件 {filename} 失败: {e}")
            return False
    
    def generate_all(self) -> Dict[str, bool]:
        """
        生成所有文件
        
        Returns:
            Dict[str, bool]: 每个文件的生成结果
        """
        results = {}
        
        print("=" * 60)
        print("C++ DLL入口点代码生成器")
        print("=" * 60)
        
        # 创建输出目录
        if not self.create_output_dir():
            print("无法创建输出目录，终止生成")
            return results
        
        print(f"\n开始生成文件到目录: {self.output_dir}")
        print("-" * 40)
        
        # 生成每个文件
        for filename, generator_func in self.files_to_generate.items():
            print(f"\n正在生成 {filename}...")
            
            try:
                content = generator_func()
                success = self.write_file(filename, content)
                results[filename] = success
                
            except Exception as e:
                print(f"✗ 生成 {filename} 时发生错误: {e}")
                results[filename] = False
        
        # 输出总结
        print("\n" + "=" * 60)
        print("生成结果总结:")
        print("=" * 60)
        
        success_count = sum(1 for success in results.values() if success)
        total_count = len(results)
        
        for filename, success in results.items():
            status = "✓ 成功" if success else "✗ 失败"
            print(f"{filename:15} - {status}")
        
        print(f"\n总计: {success_count}/{total_count} 个文件生成成功")
        
        if success_count == total_count:
            print("所有文件生成完成！")
        else:
            print("部分文件生成失败，请检查错误信息")
        
        print("=" * 60)
        
        return results



def main():
    """主函数"""
    generator = DllEntryGenerator("ctpmd")
    generator.generate_all()

    generator = DllEntryGenerator("ctptd")
    generator.generate_all()


if __name__ == "__main__":
    main()
