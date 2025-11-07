#!/usr/bin/env python
"""
Serial Studio 跨平台构建编排工具

=== 使用说明 ===

一. 基础构建(Mac / Linux):
   python build_selector.py

   1. 指定构建类型:
   python build_selector.py --build-type Release
   python build_selector.py --build-type Debug --sanitizer

   2. 指定 Qt 路径:
     python build_selector.py --qt-root ~/Qt/6.9.2/macos
     python build_selector.py --qt-root /opt/Qt/6.9.2/gcc_64

二. windows

在 Windows 上使用 MSVC 构建前，需先设置好 MSVC 环境变量

cmd /k "`"D:\Develop\Microsoft Visual Studio\VS2022Community\VC\Auxiliary\Build\vcvars64.bat`" amd64 && python D:\zx-code\Serial-Studio\scripts\build_selector.py --toolchain msvc"

或者:搜索 “Developer Command Prompt for VS 2022”；打开后进入项目目录执行python


1. Windows 平台(必须指定工具链，并手动指定 qt-cmake / cmake 可执行路径):
   # MSVC(需在 Developer Command Prompt 中运行):
   python build_selector.py --toolchain msvc --qt-cmake "C:/Qt/Tools/CMake_64/bin/qt-cmake.exe" --cmake "C:/Qt/Tools/CMake_64/bin/cmake.exe" --qt-root "C:/Qt/6.9.2/msvc2022_64"

   # MinGW:
   python build_selector.py --toolchain mingw --qt-cmake "C:/Qt/Tools/CMake_64/bin/qt-cmake.exe" --cmake "C:/Qt/Tools/CMake_64/bin/cmake.exe" --qt-root "C:/Qt/6.9.2/mingw_64" --qt-tools-root "C:/Qt/Tools/mingw1120_64"



三. 高级选项:
   # 生产构建 + 打包
   python build_selector.py --production --package

   # 构建后运行
   python build_selector.py --run

   # 自定义生成器和并行任务数
   python build_selector.py --generator Ninja --jobs 8

   # 使用配置文件
   python build_selector.py --config build_config.json

  1. 配置文件示例(build_config.json):
   {
     "qt_root": "/path/to/Qt/6.9.2/gcc_64",
     "build_type": "Release",
     "jobs": 8,
     "production": true
   }

  2. 查看配置摘要(不实际构建):
    python build_selector.py --info

=== 功能特性 ===
- 支持多平台:macOS、Windows(MSVC/MinGW)、Linux
- 支持多生成器:Ninja、Unix Makefiles、MinGW Makefiles、NMake Makefiles
- 灵活配置:CLI 选项、JSON 配置文件、环境变量
- 自动检测:平台、可用生成器、CPU 核心数
- 完整工作流:配置 → 构建 → 打包 → 运行
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence

APP_NAME = "Serial-Studio"


class BuildError(RuntimeError):
    """构建过程中发生错误时抛出的异常"""


@dataclass
class BuildOptions:
    """构建配置选项(聚合所有构建参数)"""

    # 必需参数
    platform: str  # 目标平台:mac, windows, linux

    # 构建配置
    build_type: str = "Release"  # 构建类型:Release 或 Debug
    toolchain: Optional[str] = None  # 工具链:msvc/mingw(仅 Windows)
    generator: Optional[str] = None  # CMake 生成器
    build_dir: Path = Path("build")  # 构建输出目录
    jobs: Optional[int] = None  # 并行构建任务数

    # 行为控制
    configure_only: bool = False  # 仅配置，不构建
    dry_run: bool = False  # 仅打印命令，不执行
    production: bool = True  # 启用生产优化
    sanitizer: bool = False  # 启用内存检查器(仅 Debug)
    gpl_only: bool = False  # 仅构建 GPL 版本
    clean: bool = False  # 构建前清理目录
    run_after_build: bool = False  # 构建后运行应用
    create_package: bool = False  # 构建后创建安装包
    info_only: bool = False  # 仅显示配置信息
    verbose: bool = False  # 详细日志输出

    # 工具路径
    qt_cmake_binary: Optional[str] = None  # qt-cmake 路径
    cmake_binary: Optional[str] = None  # cmake 路径
    qt_root: Optional[Path] = None  # Qt 安装根目录
    qt_tools_root: Optional[Path] = None  # Qt 工具目录(如 MinGW)

    # 额外参数
    extra_cmake_args: List[str] = field(default_factory=list)
    env_overrides: Dict[str, str] = field(default_factory=dict)


def detect_platform() -> str:
    """检测当前操作系统平台"""
    system = sys.platform
    if system.startswith("darwin"):
        return "mac"
    if system.startswith("win"):
        return "windows"
    if system.startswith("linux"):
        return "linux"
    raise BuildError(f"Unsupported host platform: {system}")


def configure_logging(verbose: bool) -> logging.Logger:
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=level, format="[%(levelname)s] %(message)s")
    return logging.getLogger("serial-studio-build")


class CommandRunner:
    """命令执行器:封装子进程调用，支持环境变量合并和 dry-run 模式"""

    def __init__(self, logger: logging.Logger, dry_run: bool, env: Dict[str, str]):
        self._logger = logger
        self._dry_run = dry_run
        self._base_env = env  # 基础环境变量(从父进程继承)

    def run(self, args: Sequence[str], cwd: Path, extra_env: Optional[Dict[str, str]] = None) -> None:
        """
        执行命令

        参数:
            args: 命令及其参数列表
            cwd: 工作目录
            extra_env: 额外的环境变量(将与基础环境合并)
        """
        command_str = " ".join(args)
        self._logger.debug("Executing: %s", command_str)
        if self._dry_run:
            return

        # 合并环境变量:基础环境 + 额外环境(后者优先)
        env = {**self._base_env, **(extra_env or {})}
        try:
            subprocess.run(args, cwd=cwd, env=env, check=True)
        except subprocess.CalledProcessError as exc:
            raise BuildError(f"Command failed ({exc.returncode}): {command_str}") from exc


class ToolchainStrategy:
    """工具链策略基类:定义不同平台和编译器的构建行为"""

    def configure_args(self, options: BuildOptions) -> List[str]:
        """返回 CMake 配置阶段的参数(如生成器、Qt 路径)"""
        raise NotImplementedError

    def configure_env(self, options: BuildOptions) -> Dict[str, str]:
        """返回配置和构建时需要的额外环境变量"""
        return {}

    def build_args(self, options: BuildOptions) -> List[str]:
        """返回 CMake 构建阶段的参数(如 MSVC 的 --config)"""
        return []


def generator_available(name: str) -> bool:
    """检查指定的 CMake 生成器是否可用"""
    if name.startswith("Ninja"):
        return shutil.which("ninja") is not None
    if name == "MinGW Makefiles":
        return shutil.which("mingw32-make") is not None
    if name == "NMake Makefiles":
        return shutil.which("nmake") is not None
    if name.startswith("Visual Studio"):
        # 检查是否在 MSVC 环境中(通过检查 VCINSTALLDIR 环境变量)
        # 或者 vswhere 是否可用(用于检测 Visual Studio 安装)
        return os.environ.get("VCINSTALLDIR") is not None or shutil.which("vswhere") is not None
    return True


def pick_generator(preferred: Iterable[str]) -> Optional[str]:
    """从首选列表中选择第一个可用的生成器"""
    for candidate in preferred:
        if generator_available(candidate):
            return candidate
    return None


def validate_qt_paths(qt_root: Optional[Path], qt_tools_root: Optional[Path]) -> None:
    """验证 Qt 路径是否存在且有效"""
    if qt_root:
        if not qt_root.exists():
            raise BuildError(f"Qt root path does not exist: {qt_root}")
        if not qt_root.is_dir():
            raise BuildError(f"Qt root path is not a directory: {qt_root}")
        # 检查是否包含典型的 Qt 目录结构
        if not (qt_root / "bin").exists() and not (qt_root / "lib").exists():
            raise BuildError(f"Qt root path does not appear to be a valid Qt installation: {qt_root}")

    if qt_tools_root:
        if not qt_tools_root.exists():
            raise BuildError(f"Qt tools root path does not exist: {qt_tools_root}")
        if not qt_tools_root.is_dir():
            raise BuildError(f"Qt tools root path is not a directory: {qt_tools_root}")


def check_msvc_environment() -> bool:
    """检查是否在正确的 MSVC 环境中运行"""
    # MSVC 环境会设置这些环境变量
    msvc_vars = ["VCINSTALLDIR", "VSINSTALLDIR", "VCToolsInstallDir"]
    return any(os.environ.get(var) for var in msvc_vars)


class GenericToolchain(ToolchainStrategy):
    """通用工具链策略(用于 macOS 和 Linux)"""

    def configure_args(self, options: BuildOptions) -> List[str]:
        # 优先选择 Ninja，否则使用 Unix Makefiles
        generator = options.generator or pick_generator(["Ninja", "Unix Makefiles"])
        args: List[str] = []
        if generator:
            args.extend(["-G", generator])
        # 设置 Qt 安装路径，让 CMake 能找到 Qt 模块
        if options.qt_root:
            args.append(f"-DCMAKE_PREFIX_PATH={options.qt_root}")
        return args


class MinGWToolchain(ToolchainStrategy):
    """MinGW 工具链策略(Windows 上的 GCC)"""

    def configure_args(self, options: BuildOptions) -> List[str]:
        # MinGW 优先使用 Ninja，否则使用 MinGW Makefiles
        generator = options.generator or pick_generator(["Ninja", "MinGW Makefiles"])
        if not generator:
            raise BuildError("No suitable CMake generator found for MinGW (install Ninja or mingw32-make).")
        args = ["-G", generator]
        if options.qt_root:
            args.append(f"-DCMAKE_PREFIX_PATH={options.qt_root}")
        return args

    def configure_env(self, options: BuildOptions) -> Dict[str, str]:
        """配置 MinGW 环境变量，将 Qt 和 MinGW 工具路径添加到 PATH

        路径优先级(从高到低):
        1. qt_tools_root/bin - MinGW 编译器(g++, gcc, mingw32-make 等)
        2. qt_root/bin - Qt 的 DLL 和工具
        3. 原始 PATH - 系统环境变量

        这样可以确保使用正确版本的编译器，避免与系统其他编译器冲突
        """
        extra_path: List[str] = []
        # 编译器路径应该有最高优先级，避免使用系统PATH中的其他版本
        if options.qt_tools_root:
            extra_path.append(str(options.qt_tools_root / "bin"))
        # Qt DLL 路径次之
        if options.qt_root:
            extra_path.append(str(options.qt_root / "bin"))
        if not extra_path:
            return {}
        # 使用 os.pathsep 确保跨平台兼容(Windows 用 ;，Unix 用 :)
        joined = os.pathsep.join(extra_path + [os.environ.get("PATH", "")])
        return {"PATH": joined}


class MsvcToolchain(ToolchainStrategy):
    """MSVC 工具链策略(Visual Studio 编译器)"""

    def configure_args(self, options: BuildOptions) -> List[str]:
        # 检查是否在正确的 MSVC 环境中
        if not check_msvc_environment():
            raise BuildError(
                "MSVC toolchain requires running from a Visual Studio Developer Command Prompt.\n"
                "Please run this script from:\n"
                "  - Developer Command Prompt for VS\n"
                "  - Or execute 'vcvarsall.bat' before running this script"
            )

        # MSVC 优先使用 Ninja，否则使用 NMake Makefiles
        preferred = ["Ninja", "Ninja Multi-Config", "NMake Makefiles"]
        generator = options.generator or pick_generator(preferred)
        if not generator:
            raise BuildError("No suitable generator found for MSVC (install Ninja or use Developer Command Prompt for nmake).")
        args = ["-G", generator]
        if options.qt_root:
            args.append(f"-DCMAKE_PREFIX_PATH={options.qt_root}")
        return args

    def configure_env(self, options: BuildOptions) -> Dict[str, str]:
        """对 MSVC 构建进行环境净化，避免被 MSYS2/Git 的 sh.exe、路径转换影响

        处理步骤:
        1. 清除 MSYS2 相关环境变量，防止 CMake 进入 MSYS 模式
        2. 过滤 PATH 中的 msys2/mingw64 路径，避免使用错误的工具(如 sh.exe、link.exe)
        3. 将 Qt 路径添加到 PATH 前端，确保能找到 Qt DLL 和工具
        """
        env: Dict[str, str] = {}
        # 清空会触发 MSYS 路径/行为的变量
        for key in ("MSYSTEM", "CHERE_INVOKING", "MSYS2_PATH_TYPE", "SHELL"):
            if os.environ.get(key):
                env[key] = ""

        # 过滤 PATH 中的 msys2/mingw64/git 的 usr/bin，避免 CMake 进入 MSYS 模式或拿到错误的 link.exe/sh.exe
        try:
            import re as _re
            # 过滤 msys2/mingw64 的路径，但保留 msys2 中的独立工具(如 ninja)
            # 主要过滤 /usr/bin 和 /mingw64/bin，因为这些会导致工具链冲突
            bad = _re.compile(r"(msys2|msys64)[\\/](usr|mingw64)[\\/]bin", _re.IGNORECASE)
            parts = os.environ.get("PATH", "").split(os.pathsep)
            filtered = [p for p in parts if not bad.search(p or "")]

            # 将 Qt 路径添加到前端，确保优先使用 Qt 的 DLL 和工具
            qt_paths: List[str] = []
            if options.qt_root:
                qt_paths.append(str(options.qt_root / "bin"))

            if qt_paths or filtered:
                env["PATH"] = os.pathsep.join(qt_paths + filtered)
        except Exception:
            # 如果过滤失败，至少确保添加 Qt 路径
            if options.qt_root:
                qt_bin = str(options.qt_root / "bin")
                original_path = os.environ.get("PATH", "")
                env["PATH"] = os.pathsep.join([qt_bin, original_path])
        return env

    def build_args(self, options: BuildOptions) -> List[str]:
        # MSVC 多配置生成器需要指定 --config 参数
        return ["--config", options.build_type]


def load_config_file(path: Optional[str]) -> Dict[str, str]:
    """从 JSON 文件加载配置项"""
    if not path:
        return {}
    config_path = Path(path).expanduser()
    if not config_path.exists():
        raise BuildError(f"Config file not found: {config_path}")
    with config_path.open("r", encoding="utf-8") as handle:
        try:
            data = json.load(handle)
        except json.JSONDecodeError as exc:
            raise BuildError(f"Invalid JSON config: {config_path}") from exc
    if not isinstance(data, dict):
        raise BuildError("Config file must contain a JSON object.")
    return {str(k): v for k, v in data.items()}


def parse_env_overrides(values: Sequence[str]) -> Dict[str, str]:
    """解析 KEY=VALUE 格式的环境变量覆盖"""
    overrides: Dict[str, str] = {}
    for item in values:
        if "=" not in item:
            raise BuildError(f"Environment override must be KEY=VALUE, got '{item}'.")
        key, value = item.split("=", 1)
        overrides[key] = value
    return overrides


def resolve_command(preferred: Optional[str], fallback: str, *, require_explicit: bool = False) -> str:
    """解析命令路径:优先使用用户指定的，否则在 PATH 中查找(Windows 可强制显式指定)"""
    if preferred:
        return preferred
    if require_explicit:
        option_hint = "--qt-cmake" if fallback == "qt-cmake" else f"--{fallback}"
        raise BuildError(
            f"Explicit path required for '{fallback}'. Provide it via {option_hint} or JSON config when targeting Windows."
        )
    found = shutil.which(fallback)
    if not found:
        raise BuildError(f"Required command '{fallback}' not found in PATH; specify it explicitly with CLI options.")
    return found


def determine_build_directory(options: BuildOptions, project_root: Path) -> Path:
    """确定构建输出目录:绝对路径直接使用，相对路径则自动构造层级结构"""
    if options.build_dir.is_absolute():
        return options.build_dir
    # 构建目录结构:build/<platform>/<toolchain>/<build_type>
    segments: List[str] = ["build", options.platform]
    if options.toolchain:
        segments.append(options.toolchain)
    segments.append(options.build_type.lower())
    return project_root / Path(*segments)


def select_toolchain(options: BuildOptions) -> ToolchainStrategy:
    """根据平台和工具链选项选择合适的工具链策略"""
    if options.platform == "windows":
        if not options.toolchain:
            raise BuildError("Windows builds require --toolchain (msvc or mingw).")
        if options.toolchain == "msvc":
            return MsvcToolchain()
        if options.toolchain == "mingw":
            return MinGWToolchain()
        raise BuildError(f"Unsupported Windows toolchain: {options.toolchain}")
    if options.toolchain:
        raise BuildError("--toolchain is only valid for Windows builds.")
    return GenericToolchain()


class Builder:
    """构建器类:封装完整的 CMake 构建流程"""

    def __init__(
        self,
        options: BuildOptions,
        project_root: Path,
        logger: logging.Logger,
        runner: CommandRunner,
        toolchain: ToolchainStrategy,
    ):
        self.options = options
        self.project_root = project_root
        self.logger = logger
        self.runner = runner
        self.toolchain = toolchain
        self.build_dir = determine_build_directory(options, project_root)

    def _configure_executable(self) -> str:
        if self.options.qt_cmake_binary:
            return self.options.qt_cmake_binary
        if self.options.platform != "windows":
            try:
                return resolve_command(None, "qt-cmake")
            except BuildError:
                pass
        return resolve_command(
            self.options.cmake_binary,
            "cmake",
            require_explicit=self.options.platform == "windows",
        )

    def info(self) -> None:
        self.logger.info("Build configuration:")
        self.logger.info("  platform      : %s", self.options.platform)
        self.logger.info("  build type    : %s", self.options.build_type)
        if self.options.toolchain:
            self.logger.info("  toolchain     : %s", self.options.toolchain)
        self.logger.info("  build dir     : %s", self.build_dir)
        if self.options.generator:
            self.logger.info("  generator     : %s", self.options.generator)
        if self.options.jobs:
            self.logger.info("  parallel jobs : %s", self.options.jobs)
        if self.options.qt_cmake_binary:
            self.logger.info("  qt-cmake      : %s", self.options.qt_cmake_binary)
        if self.options.cmake_binary:
            self.logger.info("  cmake         : %s", self.options.cmake_binary)
        if self.options.qt_root:
            self.logger.info("  Qt root       : %s", self.options.qt_root)
        if self.options.qt_tools_root:
            self.logger.info("  Qt tools root : %s", self.options.qt_tools_root)
        if self.options.extra_cmake_args:
            self.logger.info("  extra args    : %s", " ".join(self.options.extra_cmake_args))
        if self.options.env_overrides:
            self.logger.info("  env overrides : %s", self.options.env_overrides)

    def clean(self) -> None:
        if not self.build_dir.exists():
            return
        self.logger.info("Removing build directory: %s", self.build_dir)
        shutil.rmtree(self.build_dir)

    def configure(self) -> None:
        """执行 CMake 配置步骤"""
        self.logger.info("Configuring project...")
        self.build_dir.mkdir(parents=True, exist_ok=True)

        cmake_bin = self._configure_executable()

        # 构造 CMake 配置命令
        configure_cmd = [
            cmake_bin,
            "-S",  # 源代码目录
            str(self.project_root),
            "-B",  # 构建输出目录
            str(self.build_dir),
            f"-DCMAKE_BUILD_TYPE={self.options.build_type}",
            f"-DBUILD_GPL3={'ON' if self.options.gpl_only else 'OFF'}",
        ]

        # 添加项目特定的构建选项
        if self.options.production:
            configure_cmd.append("-DPRODUCTION_OPTIMIZATION=ON")
        if self.options.sanitizer:
            configure_cmd.append("-DDEBUG_SANITIZER=ON")

        # 添加工具链特定的配置参数(生成器、Qt 路径等)
        configure_cmd.extend(self.toolchain.configure_args(self.options))

        # 如使用 Ninja，显式指定 Ninja 可执行文件，避免 PATH 冲突
        try:
            if "-G" in configure_cmd:
                _idx = configure_cmd.index("-G")
                _gen = configure_cmd[_idx+1]
                if _gen.startswith("Ninja"):
                    _ninja = shutil.which("ninja")
                    if _ninja:
                        configure_cmd.append(f"-DCMAKE_MAKE_PROGRAM={_ninja}")
        except Exception:
            pass

        # 添加用户指定的额外 CMake 参数
        configure_cmd.extend(self.options.extra_cmake_args)

        # 合并环境变量:用户覆盖 + 工具链特定环境
        env = self.options.env_overrides.copy()
        env.update(self.toolchain.configure_env(self.options))

        self.runner.run(configure_cmd, cwd=self.project_root, extra_env=env)

    def build(self) -> None:
        """执行 CMake 构建步骤"""
        self.logger.info("Building project...")
        cmake_bin = resolve_command(
            self.options.cmake_binary,
            "cmake",
            require_explicit=self.options.platform == "windows",
        )
        build_cmd = [
            cmake_bin,
            "--build",
            str(self.build_dir),
        ]

        # 启用并行构建以加速编译
        if self.options.jobs and self.options.jobs > 1:
            build_cmd.extend(["--parallel", str(self.options.jobs)])

        # 添加工具链特定的构建参数(如 MSVC 的 --config)
        build_cmd.extend(self.toolchain.build_args(self.options))
        self.runner.run(build_cmd, cwd=self.project_root, extra_env=self.options.env_overrides)

    def package(self) -> None:
        """执行 CMake 打包步骤(创建安装包)"""
        self.logger.info("Creating package...")
        cmake_bin = resolve_command(
            self.options.cmake_binary,
            "cmake",
            require_explicit=self.options.platform == "windows",
        )
        package_cmd = [
            cmake_bin,
            "--build",
            str(self.build_dir),
            "--target",
            "package",  # 调用 CPack 生成安装包
        ]
        package_cmd.extend(self.toolchain.build_args(self.options))
        self.runner.run(package_cmd, cwd=self.project_root, extra_env=self.options.env_overrides)

    def run_app(self) -> None:
        """构建完成后启动应用程序"""
        self.logger.info("Launching application...")
        app_path: Path

        # macOS:应用程序打包为 .app bundle
        if self.options.platform == "mac":
            app_dir = self.build_dir / "app" / f"{APP_NAME}.app"
            if not app_dir.exists():
                raise BuildError(f"Application bundle not found: {app_dir}")
            self.runner.run(["open", str(app_dir)], cwd=self.project_root, extra_env=self.options.env_overrides)
            return

        # Windows 和 Linux:直接查找可执行文件
        if self.options.platform == "windows":
            exe_name = f"{APP_NAME}.exe"
            cache = self.build_dir / "CMakeCache.txt"
            is_multi = False
            if cache.exists():
                try:
                    _cache = cache.read_text(encoding="utf-8", errors="ignore")
                    if "CMAKE_CONFIGURATION_TYPES" in _cache:
                        is_multi = True
                except Exception:
                    pass
            if is_multi:
                app_path = self.build_dir / "app" / self.options.build_type / exe_name
            else:
                app_path = self.build_dir / "app" / exe_name
        else:
            app_path = self.build_dir / "app" / APP_NAME

        if not app_path.exists():
            raise BuildError(f"Executable not found: {app_path}")
        self.runner.run([str(app_path)], cwd=self.project_root, extra_env=self.options.env_overrides)


def parse_cli(argv: Optional[Sequence[str]]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Serial Studio build orchestrator",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--config", help="Path to JSON configuration file.")
    parser.add_argument("--platform", choices=["mac", "windows", "linux"], help="Target platform.")
    parser.add_argument("--build-type", choices=["Release", "Debug"], default="Release", help="CMake build type.")
    parser.add_argument("--toolchain", choices=["msvc", "mingw"], help="Windows toolchain.")
    parser.add_argument("--generator", help="Explicit CMake generator.")
    parser.add_argument("--build-dir", help="Output build directory.")
    parser.add_argument("--jobs", type=int, help="Maximum parallel build jobs.")
    parser.add_argument("--clean", action="store_true", help="Delete the build directory before configuring.")
    parser.add_argument("--configure-only", action="store_true", help="Run configure step without building.")
    parser.add_argument("--run", dest="run_app", action="store_true", help="Launch the application after build.")
    parser.add_argument("--package", action="store_true", help="Invoke the CMake 'package' target after build.")
    parser.add_argument("--info", action="store_true", help="Print configuration summary and exit.")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without executing them.")
    parser.add_argument("--production", action="store_true", help="Enable production optimizations.")
    parser.add_argument("--sanitizer", action="store_true", help="Enable sanitizers (Debug builds).")
    parser.add_argument("--commercial", action="store_true", help="Enable commercial build (disables GPL-only flag).")
    parser.add_argument("--verbose", action="store_true", help="Increase logging verbosity.")
    parser.add_argument("--qt-root", help="Path to the Qt installation used for this build.")
    parser.add_argument("--qt-tools-root", help="Path to auxiliary Qt tools (e.g. MinGW toolchain).")
    parser.add_argument(
        "--qt-cmake",
        dest="qt_cmake_binary",
        help="Explicit path to qt-cmake (required on Windows).",
    )
    parser.add_argument(
        "--cmake",
        dest="cmake_binary",
        help="Explicit path to cmake (required on Windows).",
    )
    parser.add_argument(
        "--env",
        action="append",
        default=[],
        help="Environment override in KEY=VALUE form (can be repeated).",
    )
    parser.add_argument(
        "--cmake-arg",
        action="append",
        dest="extra_cmake_args",
        default=[],
        help="Additional argument passed to the CMake configure step (can be repeated).",
    )
    parser.add_argument("remainder", nargs=argparse.REMAINDER, help="Additional arguments after '--' go to CMake.")
    return parser.parse_args(argv)


def merge_cli_with_config(cli: argparse.Namespace) -> BuildOptions:
    config_values = load_config_file(cli.config)

    def from_sources(key: str, default=None):
        if getattr(cli, key, None) is not None:
            return getattr(cli, key)
        return config_values.get(key, default)

    platform_value = from_sources("platform", detect_platform())
    build_dir_value = from_sources("build_dir")

    build_dir_path = Path(build_dir_value) if build_dir_value else Path("build")

    extra_args = list(cli.extra_cmake_args or [])
    if cli.remainder:
        extra = list(cli.remainder)
        if extra and extra[0] == "--":
            extra = extra[1:]
        extra_args.extend(extra)

    env_overrides = parse_env_overrides(cli.env or [])
    for key, value in config_values.get("env_overrides", {}).items():
        env_overrides.setdefault(key, value)

    qt_root_value = from_sources("qt_root")
    qt_tools_value = from_sources("qt_tools_root")

    options = BuildOptions(
        platform=platform_value,
        build_type=from_sources("build_type", cli.build_type),
        toolchain=from_sources("toolchain"),
        generator=from_sources("generator"),
        build_dir=build_dir_path,
        jobs=from_sources("jobs"),
        configure_only=from_sources("configure_only", cli.configure_only),
        dry_run=from_sources("dry_run", cli.dry_run),
        production=from_sources("production", cli.production),
        sanitizer=from_sources("sanitizer", cli.sanitizer),
        gpl_only=not from_sources("commercial", cli.commercial),
        clean=from_sources("clean", cli.clean),
        run_after_build=from_sources("run_app", cli.run_app),
        create_package=from_sources("package", cli.package),
        info_only=from_sources("info", cli.info),
        verbose=from_sources("verbose", cli.verbose),
        qt_cmake_binary=from_sources("qt_cmake_binary"),
        cmake_binary=from_sources("cmake_binary"),
        qt_root=Path(qt_root_value).expanduser() if qt_root_value else None,
        qt_tools_root=Path(qt_tools_value).expanduser() if qt_tools_value else None,
        extra_cmake_args=extra_args,
        env_overrides=env_overrides,
    )

    if options.jobs is None:
        options.jobs = os.cpu_count() or 1

    if options.build_type not in {"Release", "Debug"}:
        options.build_type = options.build_type.capitalize()

    return options


def validate_options(options: BuildOptions) -> None:
    """验证构建选项的一致性和有效性"""
    if options.jobs is not None and options.jobs < 1:
        raise BuildError("--jobs must be a positive integer.")
    if options.platform != "windows" and options.toolchain:
        raise BuildError("--toolchain is only supported on Windows.")
    if options.platform == "windows" and not options.toolchain:
        raise BuildError("Provide --toolchain when targeting Windows (msvc or mingw).")
    if options.platform == "windows":
        missing_paths = []
        if not options.qt_cmake_binary:
            missing_paths.append("--qt-cmake")
        if not options.cmake_binary:
            missing_paths.append("--cmake")
        if missing_paths:
            raise BuildError(
                "Windows builds now require explicit tool paths. Please provide: " + ", ".join(missing_paths)
            )
        for label, path_value in (("qt-cmake", options.qt_cmake_binary), ("cmake", options.cmake_binary)):
            candidate = Path(path_value).expanduser()
            if not candidate.exists():
                raise BuildError(f"Specified {label} executable not found: {path_value}")
    if options.sanitizer and options.build_type != "Debug":
        raise BuildError("Sanitizers can only be enabled for Debug builds.")
    if options.production and options.build_type != "Release":
        raise BuildError("Production optimizations only apply to Release builds.")

    # 验证 Qt 路径是否存在且有效
    validate_qt_paths(options.qt_root, options.qt_tools_root)


def main(argv: Optional[Sequence[str]] = None) -> int:
    """
    主函数:编排完整的构建流程

    返回值:
        0 - 成功
        1 - 构建错误
        130 - 用户中断
    """
    try:
        # 解析命令行参数
        cli_args = parse_cli(argv)
        # 合并 CLI 参数和配置文件选项
        options = merge_cli_with_config(cli_args)
        # 验证选项的一致性
        validate_options(options)

        logger = configure_logging(options.verbose)
        # 脚本位于 scripts/ 目录，项目根目录是其父目录
        here = Path(__file__).resolve().parent
        cwd = Path.cwd()
        if (cwd / "CMakeLists.txt").exists():
            project_root = cwd
        elif (here / "CMakeLists.txt").exists():
            project_root = here
        elif (here.parent / "CMakeLists.txt").exists():
            project_root = here.parent
        else:
            project_root = cwd

        # 初始化命令执行器和工具链
        runner = CommandRunner(logger=logger, dry_run=options.dry_run, env=dict(os.environ))
        toolchain = select_toolchain(options)
        builder = Builder(options=options, project_root=project_root, logger=logger, runner=runner, toolchain=toolchain)

        # 打印构建配置摘要
        builder.info()
        if options.info_only:
            return 0

        # 可选:清理旧的构建目录
        if options.clean:
            builder.clean()

        # 步骤 1:配置项目(生成构建文件)
        builder.configure()
        if options.configure_only:
            return 0

        # 步骤 2:编译项目
        builder.build()

        # 可选:打包安装程序
        if options.create_package:
            builder.package()

        # 可选:启动应用程序
        if options.run_after_build:
            builder.run_app()

        logger.info("Build completed successfully.")
        return 0

    except BuildError as error:
        logging.getLogger("serial-studio-build").error(str(error))
        return 1
    except KeyboardInterrupt:
        logging.getLogger("serial-studio-build").warning("Operation interrupted by user.")
        return 130


if __name__ == "__main__":
    sys.exit(main())
