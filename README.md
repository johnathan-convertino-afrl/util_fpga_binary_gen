# AFRL Util FPGA Binary gen
### Base for system boot file generation.
---

   author: Jay Convertino   
   
   date: 2023.11.29
   
   details: Various generation files for development boot file creation that depend on FPGA bitstream files.
   
   license: MIT   
   
---

### Version
#### Current
  - V0.0.0 - initial release

#### Previous
  - none
### Dependencies
#### Build

### Usage
Uses the python script named parse_and_gen.py to injest and execute commands based on yaml files. These yaml files describe how to build boot bninaries for the target platform. At the moment this targets SDCARDS. Future would add FLASH memory. This script will be copied to the root of your build. The python file will generate the boot files in a folder named BOOTFS. The BOOTFS folder contains all build outputs used in the process of generating its final files.

These systems use uboot for system startup, they also generate any needed first stage boot loads from uboot of their own custom tools.

#### Example
Simply add the below for your development board and the post hooks with automatically be added to your build and executed.
```
depend:
      - AFRL:utility:xilinx_zcu102_boot_gen:1.0.0
```

### Cores
  - AFRL:utility:terasic_hanpilot_boot_gen:1.0.0 : Hanpilot SDCARD boot generator
  - AFRL:utility:zynqmp_boot_gen:1.0.0 : Base files used for ZynqMP devices.
  - AFRL:utility:arria10_boot_gen:1.0.0 : Base files used for Arria10 devices.
  - AFRL:utility:zynq_boot_gen:1.0.0 : Base files used for Zynq7 devices
  - AFRL:utility:digilent_zed_boot_gen:1.0.0 : Zedboard uboot generation target
  - AFRL:utility:intel_a10soc_boot_gen:1.0.0 : a10soc uboot generation target
  - AFRL:utility:xilinx_zc702_boot_gen:1.0.0 : zc702 uboot generation target
  - AFRL:utility:xilinx_zc706_boot_gen:1.0.0 : zc706 uboot generation target
  - AFRL:utility:xilinx_vc707_boot_gen:1.0.0 : vc707 untested generation target
  - AFRL:utility:xilinx_zcu102_boot_gen:1.0.0 : zcu102 uboot generation target
  - AFRL:utility:xilinx_kc705_boot_gen:1.0.0 : kc705 untested generation target

### Folders
  - digilent : Contains yaml file and core for generating boot artifacts targeting digilent development boards.
  - intel : Contains yaml file and core for generating boot artifacts targeting intel development boards.
  - src : Contains common scripts, and cores for various platform boot file generation.
  - terasic : Contains yaml file and core for generating boot artifacts targeting terasic development boards.
  - xilinx : Contains yaml file and core for generating boot artifacts targeting xilinx development boards.

