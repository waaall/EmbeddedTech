#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Windows 构建脚本 - 简化版
所有工具路径手动指定，不进行环境检测，避免路径冲突

=== 快速使用 ===

1. 编辑配置（在脚本末尾）：
   - 修改 MSVC_CONFIG 或 MINGW_CONFIG 中的路径
   - 确保所有路径指向正确的可执行文件

2. 运行构建：
   python3 build_windows.py --config msvc
   python3 build_windows.py --config mingw

3. 自定义构建类型：
   python3 build_windows.py --config msvc --build-type Debug
   python3 build_windows.py --config msvc --jobs 8

=== 设计思想 ===
参考 Qt Creator 的方式，通过 CMake 参数直接指定所有工具：
  -DCMAKE_PREFIX_PATH:PATH=<Qt安装路径>
  -DCMAKE_C_COMPILER:FILEPATH=<C编译器路径>
  -DCMAKE_CXX_COMPILER:FILEPATH=<C++编译器路径>
  -DCMAKE_MAKE_PROGRAM:FILEPATH=<构建工具路径>
  -DQT_QMAKE_EXECUTABLE:FILEPATH=<qmake路径>
"""

import subprocess
import sys
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class ToolchainConfig:
    """工具链配置 - 手动指定所有工具路径"""

    # === 必需路径 ===
    cmake_exe: Path              # CMake 可执行文件
    qt_prefix: Path              # Qt 安装前缀目录（不含 /bin）
    c_compiler: Path             # C 编译器（cl.exe 或 gcc.exe）
    cxx_compiler: Path           # C++ 编译器（cl.exe 或 g++.exe）

    # === 可选路径 ===
    make_program: Optional[Path] = None   # 构建工具（ninja.exe 或 mingw32-make.exe）
    qmake_exe: Optional[Path] = None      # qmake.exe（可选，用于某些 Qt 模块）

    # === 构建选项 ===
    generator: str = "Ninja"              # CMake 生成器
    build_type: str = "Release"           # 构建类型：Release 或 Debug
    build_dir: Path = field(default_factory=lambda: Path("build"))  # 构建目录
    jobs: Optional[int] = None            # 并行任务数（None = 自动检测）

    # === 额外的 CMake 参数 ===
    extra_cmake_args: List[str] = field(default_factory=list)

    def validate(self) -> None:
        """验证所有路径是否存在"""
        paths_to_check = {
            "CMake": self.cmake_exe,
            "Qt 安装目录": self.qt_prefix,
            "C 编译器": self.c_compiler,
            "C++ 编译器": self.cxx_compiler,
        }

        if self.make_program:
            paths_to_check["构建工具"] = self.make_program
        if self.qmake_exe:
            paths_to_check["qmake"] = self.qmake_exe

        errors = []
        for name, path in paths_to_check.items():
            if not path.exists():
                errors.append(f"  - {name}: {path}")

        if errors:
            raise FileNotFoundError(
                "以下路径不存在，请检查配置：\n" + "\n".join(errors)
            )


class WindowsBuilder:
    """Windows 构建器 - 负责执行 CMake 配置和构建"""

    def __init__(self, config: ToolchainConfig):
        self.config = config

    def configure(self) -> None:
        """配置阶段 - 生成构建文件"""
        print(f"[配置] 使用生成器: {self.config.generator}")
        print(f"[配置] 构建类型: {self.config.build_type}")
        print(f"[配置] Qt 路径: {self.config.qt_prefix}")
        print(f"[配置] C++ 编译器: {self.config.cxx_compiler}")

        # 基础 CMake 参数
        args = [
            str(self.config.cmake_exe),
            "-S", ".",  # 源码目录
            "-B", str(self.config.build_dir),  # 构建目录
            "-G", self.config.generator,
            f"-DCMAKE_BUILD_TYPE={self.config.build_type}",
        ]

        # Qt 相关路径
        args.append(f"-DCMAKE_PREFIX_PATH:PATH={self.config.qt_prefix}")
        if self.config.qmake_exe:
            args.append(f"-DQT_QMAKE_EXECUTABLE:FILEPATH={self.config.qmake_exe}")

        # 编译器路径
        args.append(f"-DCMAKE_C_COMPILER:FILEPATH={self.config.c_compiler}")
        args.append(f"-DCMAKE_CXX_COMPILER:FILEPATH={self.config.cxx_compiler}")

        # 构建工具路径
        if self.config.make_program:
            args.append(f"-DCMAKE_MAKE_PROGRAM:FILEPATH={self.config.make_program}")

        # 额外参数
        args.extend(self.config.extra_cmake_args)

        print(f"\n[执行] {' '.join(str(a) for a in args)}\n")
        subprocess.run(args, check=True)
        print("[配置] 完成")

    def build(self) -> None:
        """构建阶段 - 编译项目"""
        print(f"\n[构建] 开始编译...")

        args = [
            str(self.config.cmake_exe),
            "--build", str(self.config.build_dir),
            "--config", self.config.build_type,
        ]

        # 并行任务数
        if self.config.jobs:
            args.extend(["-j", str(self.config.jobs)])

        print(f"[执行] {' '.join(str(a) for a in args)}\n")
        subprocess.run(args, check=True)
        print("\n[构建] 完成")

    def run(self) -> None:
        """完整构建流程：配置 → 构建"""
        self.config.validate()
        self.configure()
        self.build()


# ============================================================================
# 配置模板 - 根据你的实际路径修改
# ============================================================================

# MSVC 工具链配置示例
MSVC_CONFIG = ToolchainConfig(
    # CMake（使用 msys2 中的）
    cmake_exe=Path(r"D:\Develop\msys2\usr\bin\cmake.exe"),

    # Qt 安装目录（MSVC 版本）
    qt_prefix=Path(r"D:\Develop\Qt\6.9.3\msvc2022_64"),

    # MSVC 编译器路径（需要在 Visual Studio 安装目录中找到 cl.exe）
    # 示例路径，你需要根据实际 Visual Studio 安装位置修改
    c_compiler=Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe"),
    cxx_compiler=Path(r"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Tools\MSVC\14.40.33807\bin\Hostx64\x64\cl.exe"),

    # 构建工具（使用 msys2 中的 ninja）
    make_program=Path(r"D:\Develop\msys2\usr\bin\ninja.exe"),

    # qmake 路径（可选）
    qmake_exe=Path(r"D:\Develop\Qt\6.9.3\msvc2022_64\bin\qmake.exe"),

    # 生成器
    generator="Ninja",

    # 额外参数（可选）
    extra_cmake_args=[
        "-DPRODUCTION_OPTIMIZATION=ON",
        # "-DBUILD_GPL3=OFF",
        # "-DBUILD_COMMERCIAL=ON",
    ]
)

# MinGW 工具链配置示例
MINGW_CONFIG = ToolchainConfig(
    # CMake（使用 msys2 中的）
    cmake_exe=Path(r"D:\Develop\msys2\usr\bin\cmake.exe"),

    # Qt 安装目录（MinGW 版本）
    qt_prefix=Path(r"D:\Develop\Qt\6.9.3\mingw_64"),

    # MinGW 编译器路径（使用 msys2 mingw64）
    c_compiler=Path(r"D:\Develop\msys2\mingw64\bin\gcc.exe"),
    cxx_compiler=Path(r"D:\Develop\msys2\mingw64\bin\g++.exe"),

    # 构建工具（可以用 ninja 或 mingw32-make）
    make_program=Path(r"D:\Develop\msys2\usr\bin\ninja.exe"),
    # make_program=Path(r"D:\Develop\msys2\mingw64\bin\mingw32-make.exe"),  # 或者用这个

    # qmake 路径（可选）
    qmake_exe=Path(r"D:\Develop\Qt\6.9.3\mingw_64\bin\qmake.exe"),

    # 生成器
    generator="Ninja",
    # generator="MinGW Makefiles",  # 如果用 mingw32-make

    # 额外参数（可选）
    extra_cmake_args=[
        "-DPRODUCTION_OPTIMIZATION=ON",
    ]
)


# ============================================================================
# 命令行入口
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Windows 构建脚本 - 手动指定工具链路径",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  # 使用 MSVC 工具链构建 Release 版本
  python build_windows.py --config msvc

  # 使用 MinGW 工具链构建 Debug 版本
  python build_windows.py --config mingw --build-type Debug

  # 指定并行任务数
  python build_windows.py --config msvc --jobs 8

注意：
  所有工具路径在脚本中硬编码，请先编辑 MSVC_CONFIG 或 MINGW_CONFIG
        """
    )

    parser.add_argument(
        "--config",
        choices=["msvc", "mingw"],
        required=True,
        help="选择工具链配置（msvc 或 mingw）"
    )

    parser.add_argument(
        "--build-type",
        choices=["Release", "Debug"],
        default="Release",
        help="构建类型（默认：Release）"
    )

    parser.add_argument(
        "--jobs", "-j",
        type=int,
        help="并行任务数（默认：自动检测）"
    )

    parser.add_argument(
        "--build-dir",
        type=Path,
        default=Path("build"),
        help="构建目录（默认：build）"
    )

    args = parser.parse_args()

    # 选择配置
    if args.config == "msvc":
        config = MSVC_CONFIG
    else:
        config = MINGW_CONFIG

    # 覆盖命令行参数
    config.build_type = args.build_type
    if args.jobs:
        config.jobs = args.jobs
    config.build_dir = args.build_dir

    # 执行构建
    try:
        builder = WindowsBuilder(config)
        builder.run()
        print("\n✓ 构建成功！")
    except subprocess.CalledProcessError as e:
        print(f"\n✗ 构建失败，退出码：{e.returncode}", file=sys.stderr)
        sys.exit(1)
    except FileNotFoundError as e:
        print(f"\n✗ 配置错误：{e}", file=sys.stderr)
        print("\n请编辑脚本中的 MSVC_CONFIG 或 MINGW_CONFIG，确保所有路径正确", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
