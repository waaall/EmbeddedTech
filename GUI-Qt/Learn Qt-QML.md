

## 安装

需要先注册一个Qt账号。

- Creator的安装包镜像：[ustc official_releases](https://mirrors.ustc.edu.cn/qtproject/official_releases/qtcreator/)
### mac

```bash
brew install qt

# qt-creator 不是必要的
# brew install --cask qt-creator
```

### windows

- [ustc qt mirrors](https://mirrors.ustc.edu.cn/help/qtproject.html)

1. 安装国内源下载器
```powershell
# 上文网址下载qt-online-installer-windows-x64-online.exe，然后terminal执行
.\qt-online-installer-windows-x64-online.exe --mirror https://mirrors.ustc.edu.cn/qtproject
```

2. 选择 `Qt 6.x` + `MSVC 2022 64bit` + `MinGW 64bit` + `Qt-Creator`

3. 微软官网安装
	- Microsoft Visual Studio 2022 Build Tools 或者 community
	- 勾选“使用C++的桌面开发”工作负载（含 MSVC 编译器、Windows SDK、CMake、Ninja 可选）

### Ubuntu


## 编译

> codex resume 019a5c56-6ac9-7162-9d45-80ed614f50c2

Qt的编译选项有两套：MSVC 和 MinGW；默认是MinGW64，在安装了MSVC版本的Qt后，软件中其实有两套独立的Qt二进制程序，具体可以见下文编译示例。

- [MSVC 和 MinGW的区别](https://www.cnblogs.com/linuxAndMcu/p/19050227)

### 工具链选择要点

- **ABI 兼容性**：MSVC 生成的二进制需要和 Visual Studio/WinSDK 配套，方便和第三方 Windows 原生库联动；MinGW 采用 GCC ABI，与 Linux 交叉编译经验更接近，但与 MSVC 产物不能混用。
- **调试体验**：MSVC 可以直接使用 Visual Studio 调试器、WinDbg，并有 PDB 符号；MinGW 主要依赖 gdb，调试 UI 稍弱，但与开源工具链生态一致。
- **运行时依赖**：MSVC 附带 `vcruntime`/`msvcp` 系列 DLL（需打包 redistributable），MinGW 则需要一并分发 libstdc++、libgcc 等 DLL。
- **性能差异**：一般差距不大，但 MSVC 对 Windows API、最新指令集支持更及时，而 MinGW 社区更新包则稍慢；如果目标是跨平台 CLI 工具，MinGW 更通用，桌面 GUI 则推荐 MSVC。

### Qt-cmake & MinGW cmake & MSVC cmake

- 配置阶段建议用 `qt-cmake`，因为它是 Qt 官方提供的 CMake 包装器，会在调用真正的 `cmake` 之前自动加上 Qt 安装目录的 `CMAKE_PREFIX_PATH`、`QT_HOST_PATH`、`Qt6_DIR` 等变量。这样即使系统 PATH 里没有 Qt，也能正确找到 `Qt6Config.cmake`、QML 模块等。
- 一旦配置完成，这些路径已经写进 `build-xxx/CMakeCache.txt`，后续的编译/打包只需 `cmake --build`：它会读取缓存并调用生成器（Ninja、Make、MSBuild 等）。用 `qt-cmake --build` 也行，只是它又转手调用 `cmake --build`，效果完全一样。
- 如果从头到尾都用 `cmake`，那配置时你得手动加上类似 `-DCMAKE_PREFIX_PATH=C:\Qt\6.6.3\msvc2019_64` 的参数，否则 CMake 会找不到 Qt；用 `qt-cmake` 就不用自己管理这些变量。
- **MSVC/MinGW CMake 区别**：MSVC 套件附带 `cmake.exe`、`ninja.exe`、`nmake.exe` 等，路径通常在 VS 的 `CommonExtensions/Microsoft/CMake/CMake/bin`；MinGW/MSYS2 提供 GNU 版本的 `cmake`、`mingw32-make`，两者可以共存但注意 PATH 优先级（见下文示例）。

### 常见构建组合

- **Qt Creator + kit**：GUI 里选择 kit（例：`Desktop Qt 6.6.3 MSVC2019 64bit`），Creator 会自动选择 `qt-cmake` 和合适的生成器。
- **命令行 + MSVC**：在 `x64 Native Tools Command Prompt` 或手动执行 `vcvars64.bat` 之后调用 `qt-cmake -G Ninja`，再 `cmake --build`。
- **命令行 + MinGW**：在 MSYS2/MinGW64 shell 中调用 `qt-cmake -G "MinGW Makefiles"` 或 `-G Ninja`，构建产物完全独立于 MSVC。
- **交叉编译**：`qt-cmake` 会根据 kit 自动下发 `-DQT_HOST_PATH`，适合为嵌入式 Linux、Android、iOS 构建；若直接 `cmake` 则需要在 toolchain file 里手动维护这些变量。

### ninja & make & nmake

- `ninja`：推荐的跨平台生成器，专注增量构建；Qt Creator 默认在 MSVC 和 MinGW kit 上都使用 Ninja。命令行参数 `-G Ninja`。
- `nmake`：MSVC 自带的 make，适合老项目或 VS 解决方案；想用 `nmake` 需要搭配 `-G "NMake Makefiles"`, 但缺点是并发能力一般。
- `mingw32-make`：MinGW 的 `make` 变体。若你在 MSYS2/MinGW shell 里执行 `cmake -G "MinGW Makefiles"`，`cmake --build` 会自动调用它。
- `jom`：Qt 提供的多线程 `nmake` 替代品（Windows-only），对于 Qt Widgets 大项目速度接近 Ninja。
- 选择策略：优先 `ninja` → `jom` → `nmake/mingw32-make`。无论哪种，保持“配置阶段和构建阶段使用同一生成器”这一原则，否则需要删掉 build 目录后重新配置。

### 编译示例

- msys2 cmake & make & ninja地址（加入环境变量高优先级）     `D:\Develop\msys2\usr\bin`
- mingw64 编译器 & mingw32-make地址（加入环境变量高优先级）   `D:\Develop\msys2\mingw64\bin`
- msvc编译器地址（加入环境变量低优先级）   `D:\Develop\Qt\6.9.3\msvc2022_64\bin`
- msvc cmake 地址（加入环境变量低优先级） `D:\Develop\Microsoft Visual Studio\VS2022Community\Common7\IDE\CommonExtensions\Microsoft\CMake\CMake\bin`
- msvc-Qt地址（加入环境变量低优先级）     `D:\Develop\Qt\6.9.3\msvc2022_64\bin`
- mingw_64-Qt地址（未加入环境变量）      `D:\Develop\Qt\6.9.3\mingw_64\bin`

> 提示：把 MSYS2 的路径放在高优先级，确保默认使用 GNU 工具链；同时保留 MSVC/Qt 目录在 PATH 末尾以便手动切换。若需要切换到 MSVC，只要先运行 `vcvars64.bat` or `VsDevCmd.bat`，即可把 CL/Ninja/Qt msvc kit 推到 PATH 前面。

针对“默认使用 Qt + cmake + ninja + MSVC 编译是否可行、如何操作”的问题，可以按以下流程执行：

### Qt + CMake + Ninja + MSVC（命令行流程）

1. **准备环境**
   - 打开 `x64 Native Tools Command Prompt for VS 2022`，或在任意终端里先执行  
     `"%ProgramFiles%\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat"`.
   - 确认 `where cl`, `where ninja`, `where qt-cmake` 均指向 MSVC kit（`C:\Qt\6.x\msvc2022_64`）。
2. **配置（一次性）**
   ```powershell
   set BUILD_DIR=build-msvc-ninja
   qt-cmake -S . -B %BUILD_DIR% -G Ninja ^
     -DCMAKE_BUILD_TYPE=Release ^
     -DCMAKE_INSTALL_PREFIX=%cd%\install-msvc
   ```
   - 这里 `-G Ninja` 强制使用 Ninja；MSVC 的 `cl.exe` 会被 CMake 自动检测。
3. **编译**
   ```powershell
   cmake --build %BUILD_DIR% --config Release --parallel
   ```
   - `--config` 对 Ninja 可省略，但保留可与多配置生成器保持一致。
4. **安装或打包**
   ```powershell
   cmake --install %BUILD_DIR% --config Release
   windeployqt install-msvc\MyApp.exe
   ```
   - `windeployqt` 建议使用同一 kit 下的版本，可自动复制 MSVC Qt 依赖。

### 其他常见命令片段

- **切换到 MinGW 工具链**：`qt-cmake -S . -B build-mingw -G Ninja -DCMAKE_BUILD_TYPE=Debug -- -DCMAKE_C_COMPILER=clang.exe`
- **清理/重新配置**：删除 `build-*` 目录后再运行 `qt-cmake`; 或用 `cmake --fresh -S . -B build-new`.
- **验证 kit**：`cmake --build build-msvc-ninja --target Qt6::qdbus` 若失败，说明路径没指向对应 kit，需要检查 `Qt6_DIR`.



## 基础设计

- [随笔分类 - Qt](https://www.cnblogs.com/linuxAndMcu/category/2426921.html?page=8)



## 性能优化

### cpu占用率高

- [Qt 性能优化之一 CPU占用率高的原因](https://www.cnblogs.com/linuxAndMcu/p/17145325.html "发布于 2023-02-22 17:47")
