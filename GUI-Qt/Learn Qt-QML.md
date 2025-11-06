

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


