
- [Serial-Studio](https://github.com/Serial-Studio/Serial-Studio)

# Mac serial studio build
```

## Command: Locate qt-cmake

```bash
$ which qt-cmake || true
  /opt/homebrew/bin/qt-cmake
```

## Command: Query logical CPU count via sysctl

```bash
$ sysctl -n hw.logicalcpu
  sysctl: sysctl fmt -1 1024 1: Operation not permitted
```

## Command: Query logical CPU count via getconf

```bash
$ getconf _NPROCESSORS_ONLN
  11
```

## Command: Configure Release build with qt-cmake

```bash
$ qt-cmake -S . -B build-release -DCMAKE_BUILD_TYPE=Release -DPRODUCTION_OPTIMIZATION=ON
  CMake Warning at /opt/homebrew/opt/cmake/share/cmake/Modules/Platform/Darwin-Initialize.cmake:262
  (message):
    Ignoring CMAKE_OSX_SYSROOT value:

     /Applications/Xcode.app/Contents/Developer/Platforms/MacOSX.platform/Developer/SDKs/
  MacOSX26.sdk

    because the directory does not exist.
  Call Stack (most recent call first):
    /opt/homebrew/opt/cmake/share/cmake/Modules/CMakeSystemSpecificInitialize.cmake:35 (include)
    CMakeLists.txt:28 (project)


  -- The CXX compiler identification is AppleClang 17.0.0.17000404
  -- Detecting CXX compiler ABI info
  -- Detecting CXX compiler ABI info - done
  -- Check for working CXX compiler: /usr/bin/c++ - skipped
  -- Detecting CXX compile features
  -- Detecting CXX compile features - done
  -- Performing Test CMAKE_HAVE_LIBC_PTHREAD
  -- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Success
  -- Found Threads: TRUE
  -- Performing Test HAVE_STDATOMIC
  -- Performing Test HAVE_STDATOMIC - Success
  -- Found WrapAtomic: TRUE
  -- BUILD_GPL3=ON — enforcing BUILD_COMMERCIAL=OFF for license compliance
  -- CMAKE_SYSTEM_PROCESSOR: arm64
  Enabling production optimization flags...
  CMake Deprecation Warning at lib/KissFFT/CMakeLists.txt:35 (cmake_minimum_required):
    Compatibility with CMake < 3.10 will be removed from a future version of
    CMake.

    Update the VERSION argument <min> value.  Or, use the <min>...<max> syntax
    to tell CMake that the project requires at least <min> but has been updated
    to work with policies introduced by <max> or earlier.


  -- The C compiler identification is AppleClang 17.0.0.17000404
  -- Detecting C compiler ABI info
  -- Detecting C compiler ABI info - done
  -- Check for working C compiler: /usr/bin/cc - skipped
  -- Detecting C compile features
  -- Detecting C compile features - done
  -- Building KissFFT with datatype: float
  -- Building static library
  -- PKGINCLUDEDIR is include/kissfft
  -- Found OpenGL: /Library/Developer/CommandLineTools/SDKs/MacOSX.sdk/System/Library/Frameworks/
  OpenGL.framework
  -- Found WrapOpenGL: TRUE
  -- Could NOT find WrapVulkanHeaders (missing: Vulkan_INCLUDE_DIR)
  -- Could NOT find WrapVulkanHeaders (missing: Vulkan_INCLUDE_DIR)
  -- Could NOT find WrapVulkanHeaders (missing: Vulkan_INCLUDE_DIR)
  -- Could NOT find WrapVulkanHeaders (missing: Vulkan_INCLUDE_DIR)
  -- Could NOT find WrapVulkanHeaders (missing: Vulkan_INCLUDE_DIR)
  -- LIB Compile Options: -Wall;-Wextra;-Wno-unused-function;-Wno-cast-align;-O2;-ftree-
  vectorize;-funroll-loops;-fomit-frame-pointer;-fno-fast-math;-fno-unsafe-math-
  optimizations;-flto;-finline-functions;-ffunction-sections;-fdata-sections
  -- APP Compile Options: -Wall;-Wextra;-Wno-unused-function;-Wno-cast-align;-O2;-ftree-
  vectorize;-funroll-loops;-fomit-frame-pointer;-fno-fast-math;-fno-unsafe-math-
  optimizations;-flto;-finline-functions;-ffunction-sections;-fdata-sections
  -- Configuring done (8.3s)
  -- Generating done (1.7s)
  -- Build files have been written to: /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/build-
  release
```

## Command: Build Release target (output truncated to 10,240 characters by tool)

```bash
$ cmake --build build-release --parallel 11
  [  0%] Building C object lib/KissFFT/CMakeFiles/kissfft.dir/kiss_fft.c.o
  [  0%] Built target QSimpleUpdater_autogen_timestamp_deps
  [  2%] Building C object lib/KissFFT/CMakeFiles/kissfft.dir/kiss_fftr.c.o
  [  2%] Copying Serial-Studio-GPL3 qml resources into build dir
  [  2%] Copying Serial-Studio-GPL3 qml sources into build dir
  [  2%] Building C object lib/KissFFT/CMakeFiles/kissfft.dir/kfc.c.o
  [  3%] Building C object lib/KissFFT/CMakeFiles/kissfft.dir/kiss_fftnd.c.o
  [  3%] Built target QCodeEditor_autogen_timestamp_deps
  [  3%] Building C object lib/KissFFT/CMakeFiles/kissfft.dir/kiss_fftndr.c.o
  [  3%] Running qmlimportscanner for Serial-Studio-GPL3
  [  3%] Automatic MOC and UIC for target QSimpleUpdater
  [  3%] Built target Serial-Studio-GPL3_copy_res
  [  4%] Automatic MOC for target QCodeEditor
  [  4%] Built target Serial-Studio-GPL3_copy_qml
  /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/lib/KissFFT/kiss_fftr.c:49:18: warning: cast
  from 'char *' to 'kiss_fft_cpx *' increases required alignment from 1 to 4 [-Wcast-align]
     49 |     st->tmpbuf = (kiss_fft_cpx /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/
  lib/KissFFT/kiss_fftnd.c:50:10: warning: cast from 'char *' to 'kiss_fftnd_cfg' (aka 'struct
  kiss_fftnd_state *') increases required alignment from 1 to 8 [-Wcast-align]
  *) (   50 |     st = (ki(s(sc_har *) stfftnd_cfg)- pt>subsr;tate) + subsiz
  e      |          ^~~~~~~~~~~~~~~~~~~~
  );
  /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/lib/KissFFT/kiss_fftnd.c:55:18: warning: cast
  from 'char *' to 'kiss_fft_cfg *' (aka 'struct kiss_fft_state **') increases required alignment
  from 1 to 8 [-Wcast-align]
     55 |     st->states = (kiss_fft_cfg *)ptr;
        |                  ^~~~~~~~~~~~~~~~~~~
  /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/lib/KissFFT/kiss_fftnd.c:58:16: warning: cast
  from 'char *' to 'int *' increases required alignment from 1 to 4 [-Wcast-align]
     58 |     st->dims = (int*)ptr;
        |                ^~~~~~~~~
  /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/lib/KissFFT/kiss_fftnd.c:61:18: warning: cast
  from 'char *' to 'kiss_fft_cpx *' increases required alignment from 1 to 4 [-Wcast-align]
     61 |     st->tmpbuf = (kiss_fft_cpx*)ptr;
        |                  ^~~~~~~~~~~~~~~~~~
  /Users/zhengxu/Desktop/some_code/Local-Serial-Studio/lib/KissFFT/kiss_fftndr.c:59:10: warning:
  cast from 'char *' to 'kiss_fftndr_cfg' (aka 'struct kiss_fftndr_state *') increases required
  alignment from 1 to 8 [-Wcast-align]
     59 |     st = (kiss_fftndr_cfg) ptr;
        |          ^~~~~~~~~~~~~~~~~~~~~
  4 warnings generated.
  1 warning generated.
  1 warning generated.
  [  4%] Linking C static library libkissfft-float.a
  [  4%] Built target Serial-Studio-GPL3_qmlimportscan
  [  4%] Built target kissfft
  [  4%] Built target QSimpleUpdater_autogen
  [  4%] Generating qrc_qsimpleupdater.cpp
  [  4%] Building CXX object lib/QSimpleUpdater/CMakeFiles/QSimpleUpdater.dir/
  qrc_qsimpleupdater.cpp.o
  [  5%] Building CXX object lib/QSimpleUpdater/CMakeFiles/QSimpleUpdater.dir/
  QSimpleUpdater_autogen/mocs_compilation.cpp.o
  [  5%] Building CXX object lib/QSimpleUpdater/CMakeFiles/QSimpleUpdater.dir/src/Updater.cpp.o
  [  6%] Building CXX object lib/QSimpleUpdater/CMakeFiles/QSimpleUpdater.dir/src/Downloader.cpp.o
  [  6%] Building CXX object lib/QSimpleUpdater/CMakeFiles/QSimpleUpdater.dir/src/
  QSimpleUpdater.cpp.o
  [  7%] Linking CXX static library libQSimpleUpdater.a
  ...

  (Output truncated after the portion returned by the tooling.)
```

## Command: Inspect Release app bundle directory

```bash
$ ls build-release/app
  cmake_install.cmake
  CMakeFiles
  gui
  Makefile
  meta_types
  qmltypes
  qrc_rcc.cpp
  qrc_translations.cpp
  rcc
  Serial-Studio-GPL3_autogen
  serial-studio-gpl3_qmltyperegistrations.cpp
  Serial-Studio-GPL3.app
  translations
```

## Command: Inspect Release executable location

```bash
$ ls build-release/app/Serial-Studio-GPL3.app/Contents/MacOS
  Serial-Studio-GPL3