# AFRL Util FPGA Binary gen
### Base for system boot file generation.

![image](img/AFRL.png)

---

   author: Jay Convertino   
   
   date: 2023.11.29
   
   details: Various generation files for development boot file creation that depend on FPGA bitstream files.
   
   license: MIT   
   
---

### VERSION
#### Current
  - V0.0.0 - initial release

#### Previous
  - none

### DEPENDENCIES
#### ALL
  - python3
    - PyYAML
    - system_builder
  - fusesoc
  - make
  - genimage
  - mkimage
  - bison
  - flex

#### Xilinx
  - vivado
  - xsct
  - bootgen

#### Intel
  - quartus_cpf

### USAGE
Uses the python script named parse_and_gen.py to injest and execute commands based on yaml files. These yaml files describe how to build boot binaries for the target platform. At the moment this targets SDCARDS. Future would add FLASH memory. This script will be copied to the root of your build. The python file will generate the boot files in a folder named BOOTFS. The BOOTFS folder contains all build outputs used in the process of generating its final files.

These systems use uboot for system startup, they also generate any needed first stage boot loads from uboot of their own custom tools.

The main output of this is uboot. This will also include security features and other applications typically stored on a sdcard in a FAT32 partition.

An older GCC version is downloaded from a zip archive and compiled on the target system. This is done since newer versions of GCC will not compile uboot from 2020 (intel) and 2022 (xilinx).

#### Example
Simply add the below for your development board and the post hooks will automatically be added to your build and executed.

```
depend:
      - AFRL:utility:xilinx_zcu102_boot_gen:1.0.0
```

### CORES
Only include needed is the AFRL:utility:*_boot_gen:X.X.X core. See example above.

- name: AFRL:utility:terasic_hanpilot_boot_gen:1.0.0
  - description: Contains yaml file for build instructions
- name: AFRL:utility:zynqmp_boot_gen:1.0.0
  - description: Generate boot.bin for zynqmp platforms, do not use outside of a specified platform generator.
- name: AFRL:utility:arria10_boot_gen:1.0.0
  - description: Generate boot.bin for arria10 platforms.
- name: AFRL:utility:python_build_tool:1.0.0
  - description: Python build tools for various FPGA related binaries.
- name: AFRL:utility:vexriscv_boot_gen:1.0.0
  - description: Generate boot.bin for Vexriscv platforms.
- name: AFRL:utility:zynq_boot_gen:1.0.0
  - description: Generate boot.bin for zynq platforms.
- name: AFRL:utility:digilent_zed_boot_gen:1.0.0
  - description: Git pull fsbl and uboot, generate elf files, and copy to BOOTFS folder in build.
- name: AFRL:utility:digilent_vexriscv_nexys_boot_gen:1.0.0
  - description: Git pull fsbl and uboot, generate elf files, and copy to BOOTFS folder in build.
- name: AFRL:utility:intel_a10soc_boot_gen:1.0.0
  - description: Contains yaml file for build instructions
- name: AFRL:utility:xilinx_zc702_boot_gen:1.0.0
  - description: Git pull fsbl and uboot, generate elf files, and copy to BOOTFS folder in build.
- name: AFRL:utility:xilinx_zc706_boot_gen:1.0.0
  - description: Git pull fsbl and uboot, generate elf files, and copy to BOOTFS folder in build.
- name: AFRL:utility:xilinx_vc707_boot_gen:1.0.0
  - description: Files to help generate base vc707 board items
- name: AFRL:utility:xilinx_zcu102_boot_gen:1.0.0
  - description: Contains yaml file for build instructions
- name: AFRL:utility:xilinx_kc705_boot_gen:1.0.0
  - description: Files to help generate base kc705 board items

### FOLDERS
  - digilent : Contains yaml file and core for generating boot artifacts targeting digilent development boards.
  - intel : Contains yaml file and core for generating boot artifacts targeting intel development boards.
  - src : Contains common scripts, and cores for various platform boot file generation.
  - terasic : Contains yaml file and core for generating boot artifacts targeting terasic development boards.
  - xilinx : Contains yaml file and core for generating boot artifacts targeting xilinx development boards.
