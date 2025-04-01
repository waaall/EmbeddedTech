FPGA出现在很多工业领域，因为这样省去了硬件设计中流片这一高昂的成本，所以有必要了解一下。
`iCloud/Documents/my_refs/计算机/FPGA_BOOK`文件夹中有一些书籍之类的供参考学习。

# Reference
## 入门
- [FPGA入门资料Tutorial](https://github.com/LeiWang1999/FPGA)
- [FPGA 学习指南](https://blog.csdn.net/qq_33919450/article/details/130812566)
## fpga开源工具
- [homebrew-oss-fpga](https://github.com/ktemkin/homebrew-oss-fpga)
- [OSS CAD Suite: the one-stop shop for our tools](https://github.com/YosysHQ#oss-cad-suite-the-one-stop-shop-for-our-tools)
- [openlane2](https://openlane2.readthedocs.io/en/latest/getting_started/common/docker_installation/installation_macos.html)

If you want to use our EDA tools, the easiest way is to install the binary release [OSS CAD suite](https://github.com/YosysHQ/oss-cad-suite-build/releases/latest), which contains all required dependencies and related tools. Find the [documentation here](https://yosyshq.readthedocs.io/en/latest/). We also have an [OSS CAD Suite github action](https://github.com/YosysHQ/setup-oss-cad-suite) for using the tools in a github CI workflow.

[Tabby CAD Suite](https://www.yosyshq.com/tabby-cad-datasheet) is a commercial extension of OSS CAD Suite available from [YosysHQ GmbH](https://www.yosyshq.com/about) that additionally includes the Verific frontend for industry-grade SystemVerilog and VHDL support, formal verification with SVA, and formal apps.

### [Projects](https://github.com/YosysHQ#our-projects)

- [Yosys](https://github.com/YosysHQ/yosys): a framework for RTL synthesis tools
- [nextpnr](https://github.com/YosysHQ/nextpnr): place and route for FPGA architectures. Supported architectures: iCE40 ([Project Icestorm](https://github.com/YosysHQ/icestorm)), ECP5 ([Project Trellis](https://github.com/YosysHQ/prjtrellis)), Nexus ([Project Oxide](https://github.com/gatecat/prjoxide)), Gowin ([Project Apicula](https://github.com/YosysHQ/apicula)) and more!

Front-ends for applications built on top of Yosys:

- [sby](https://github.com/YosysHQ/sby): formal property checking
- [mcy](https://github.com/YosysHQ/mcy): mutation coverage
- [eqy](https://github.com/YosysHQ/eqy): equivalence checking

Other notable projects:

- [riscv-formal](https://github.com/YosysHQ/riscv-formal): formally check compliance with the RISC-V specification
- [picorv32](https://github.com/YosysHQ/picorv32): A Size-Optimized RISC-V CPU
- [nerv](https://github.com/YosysHQ/nerv): A very simple educational RISC-V CPU for demonstrating riscv-formal

## 官网
- [Xilinx](https://www.xilinx.com/)
- [Xilinx Wiki](https://xilinx-wiki.atlassian.net/wiki/spaces/A/overview)
- [Xilinx Forums](https://forums.xilinx.com/)
- [Xilinx Open Hardware](http://www.openhw.org/)
- [电子创新网Xilinx社区](http://xilinx.eetrend.com/)
- [Altera](https://www.intel.cn/content/www/cn/zh/products/programmable.html)
- [Digilent 中国](http://www.digilent.com.cn/)
- [米联客](https://www.uisrc.com/portal.php)
- [opencores 开源硬件IP站](https://opencores.org/)
- [FPGA FOR FUN](https://www.fpga4fun.com/CrossClockDomain.html)
- [HDLBits](https://hdlbits.01xz.net/wiki/Main_Page)

## 其他
- [FPGA入门学习流程](https://www.bilibili.com/video/BV1aK4y1E7nc)
- [数字电路]()
- [FPGA的优点简介](https://cloud.tencent.com/developer/article/1467981)
- [macos-fpga](https://longfangsong.github.io/macos-fpga/)

# 小问题

## ECP5、iCE40和Xilinx？
嗯，用户问的是ECP5、iCE40和Xilinx之间的关系。首先，我应该先确认这几个术语各自的背景和所属公司。 ECP5，听起来像是某个FPGA的系列名称。记得ECP是Lattice Semiconductor的一个FPGA系列，可能ECP5是他们的第五代产品。iCE40也是Lattice的，属于低功耗FPGA，常用于消费电子和IoT设备。而Xilinx则是另一家知名的FPGA厂商，现在被AMD收购了，他们主要的产品是Virtex、Spartan、Artix、Kintex等系列。 用户可能是在比较这三个品牌的产品，或者想知道他们之间的区别与联系。需要解释这三者分属不同公司，ECP5和iCE40属于Lattice，Xilinx是自己独立的系列。可能用户在选择FPGA时，想了解不同厂商的产品特性，或者在学习FPGA时遇到这几个名词，需要明确各自的背景。 需要进一步确认ECP5和iCE40确实是Lattice的产品，同时指出Xilinx的FPGA系列，比如Spartan-6、Artix-7，或者更早的型号，与Lattice的产品在应用领域、性能、功耗等方面的差异。用户可能想知道为何会有这些不同的产品线，它们各自的市场定位，或者技术上的区别。 另外，用户可能混淆了这三者之间的关系，比如是否属于同一家公司，或者是否有技术上的继承关系。需要明确说明Lattice和Xilinx是两家不同的公司，各自有不同的产品线。ECP5和iCE40是Lattice的两个不同系列，针对不同的应用场景，而Xilinx的产品则属于另一家，有各自的特点。 还要考虑到用户可能的背景，是否是FPGA初学者，在选择开发板或芯片时遇到这些型号，需要了解它们的区别和适用场景。或者是项目需求中需要比较不同厂商的FPGA，比如成本、功耗、逻辑资源等方面的对比。 可能需要提到ECP5属于中端FPGA，适合通信、工业应用；iCE40是低功耗、小封装，适合嵌入式或便携设备；而Xilinx的产品线更广泛，从低端到高端都有，比如Spartan系列成本较低，Virtex系列性能更高。 同时，还需要提到开源工具链的支持情况，比如iCE40有Yosys和nextpnr等开源工具，而Xilinx主要依赖官方的Vivado，这对开发者来说可能有不同的选择考虑。 最后，总结三者分属不同公司，各自有不同的产品定位和技术特点，应用场景也不同，用户需要根据具体需求选择合适的FPGA型号。

ECP5、iCE40 和 Xilinx 涉及不同类型的 FPGA（现场可编程门阵列）及厂商，它们之间的关系如下：

---
### **1. 厂商归属**

|**名称**|**所属公司**|**厂商定位**|
|---|---|---|
|**ECP5**|Lattice Semiconductor|中低端 FPGA（低功耗、低成本）|
|**iCE40**|Lattice Semiconductor|超低功耗 FPGA（IoT、边缘设备）|
|**Xilinx**|AMD（2020 年被收购）|高端 FPGA（高性能、复杂逻辑）|

### **2. 产品定位对比**

#### **ECP5 系列**
- **特点**：高性价比、支持高速接口（PCIe、DDR3）
- **应用场景**：工业控制、通信基站、视频处理
- **典型型号**：LFE5U-25F-6BG256C

#### **iCE40 系列**
- **特点**：超低功耗（μW 级）、小封装
- **应用场景**：可穿戴设备、IoT、消费电子
- **典型型号**：iCE40UP5K（支持硬件神经网络加速）

#### **Xilinx FPGA**
- **代表系列**：
    - **Spartan**：低成本入门级（如 Spartan-6）
    - **Artix/Kintex**：中高端（通信、医疗成像）
    - **Virtex**：顶级性能（航空航天、数据中心）
- **典型型号**：XC7A35T（Artix-7）、XC7K325T（Kintex-7）

### **3. 技术差异**

| **特性**   | **ECP5**        | **iCE40**    | **Xilinx Artix-7** |
| -------- | --------------- | ------------ | ------------------ |
| **逻辑单元** | 8.5K - 85K LUTs | 1K - 8K LUTs | 16K - 215K LUTs    |
| **功耗**   | 中等（100mW级）      | 极低（μW级）      | 较高（1W以上）           |
| **高速接口** | PCIe Gen2       | 无            | PCIe Gen3/4        |
| **开发工具** | Lattice Diamond | IceStorm（开源） | Vivado（商业）         |
| **价格范围** | $5~$50          | $1~$10       | $20~$5000+         |

### **4. 应用场景选择**
- **选择 ECP5**：需要低成本实现 DDR3 或 PCIe 接口的工业设备。
- **选择 iCE40**：电池供电的便携设备（如智能手表）。
- **选择 Xilinx**：需处理高速数据流（如 5G 通信、AI 加速）。

### **5. 开源生态支持**
- **iCE40**：唯一支持 **全开源工具链**（Yosys + nextpnr）。
- **ECP5**：部分支持开源工具（Project Trellis）。
- **Xilinx**：依赖商业工具（Vivado），但部分型号支持 **Vitis 开源库**。

### **总结**
- **ECP5 和 iCE40** 是 Lattice 的差异化产品，分别面向中低端和超低功耗市场。
- **Xilinx** 提供覆盖全场景的 FPGA，尤其在高端领域占据主导地位。
- 三者无直接技术继承关系，选择取决于项目需求（性能、功耗、成本）。
