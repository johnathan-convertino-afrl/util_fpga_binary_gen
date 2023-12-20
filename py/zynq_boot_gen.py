#!/usr/bin/env python3
################################################################################
## @file    zynq_boot_bin.py
## @author  Jay Convertino
## @date    2023.12.19
## @brief   file check will pull two file names from settings file based on the
##          tool pased (ex icarus is pulled from the .scr file). These two files
##          are then checked for valid md5 sums that match.
## @warning THIS IS WRITTEN TO ALWAYS LOOK FOR IN_FILE_NAME/OUT_FILE_NAME
##          PARAMETERS.
##
##  MIT License
##
## Copyright 2023 Jay Convertino
##
## Permission is hereby granted, free of charge, to any person obtaining a copy
## of this software and associated documentation files (the "Software"), to deal
## in the Software without restriction, including without limitation the rights
## to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
## copies of the Software, and to permit persons to whom the Software is 
## furnished to do so, subject to the following conditions:

## The above copyright notice and this permission notice shall be included in 
## all copies or substantial portions of the Software.

## THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
## IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
## FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
## AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
## LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
## FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
## IN THE SOFTWARE. 
################################################################################

import subprocess
import pathlib

################################################################################
## MAIN
################################################################################
# find file, if bit files found.. take the first one and set to file.
files_found = sorted(pathlib.Path().glob("*.bit"))

if len(files_found) == 0:
  print("INFO: No bit file found, zynq_boot_bin generation failed.")
  exit(1)

pathlib.Path(files_found[0]).replace("BOOTFS/system.bit")

try:
  subprocess.run(["vivado", "-mode tcl -nolog -nojournal -source export_xsa.tcl"], cwd=str(pathlib.Path.cwd()))
except subprocess.CalledProcessError as error_code:
  print("vivado error:", error_code.returncode, error_code.output)
  exit(1)

try:
  subprocess.run(["xsct", "zynq_gen_fsbl.tcl"], cwd=str(pathlib.Path.cwd()))
except subprocess.CalledProcessError as error_code:
  print("xsct error:", error_code.returncode, error_code.output)
  exit(1)

pathlib.Path("BOOTFS/vitis/zynq_fsbl/Debug/zynq_fsbl.elf").replace("BOOTFS/fsbl.elf")

try:
  subprocess.run(["bootgen", "-image bootbin.bif -arch zynq -o BOOT.bin"], cwd=str(pathlib.Path.cwd()) + '/' + "BOOTFS")
except subprocess.CalledProcessError as error_code:
  print("bootgen error:", error_code.returncode, error_code.output)
  exit(1)

print("INFO: bootgen complete, file BOOT.bin available at: " + str(pathlib.Path.cwd()) + '/' + "BOOTFS")

