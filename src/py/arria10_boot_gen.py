#!/usr/bin/env python3
################################################################################
## @file    arria10_boot_gen.py
## @author  Jay Convertino
## @date    2024.01.17
## @brief
##
##  MIT License
##
## Copyright 2024 Jay Convertino
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
files_found = sorted(pathlib.Path().glob("output_files/*.sof"))

if len(files_found) == 0:
  print("ERROR: No sof file found, generation failed.")
  exit(1)

try:
  subprocess.run(["quartus_cpf", "-c", "--hps", "-o", "bitstream_compression=on", files_found[0], "output_files/ghrd_10as066n2.rbf"], cwd=str(pathlib.Path.cwd()))
except subprocess.CalledProcessError as error_code:
  print("Quartus cpf error:", error_code.returncode, error_code.output)
  exit(1)

try:
  subprocess.run(["mkimage", "-C", "none", "-A", "arm", "-T", "script", "-d", "BOOT.cmd", "BOOT.scr"], cwd=str(pathlib.Path.cwd()) + '/' + "BOOTFS")
except subprocess.CalledProcessError as error_code:
  print("mkimage error:", error_code.returncode, error_code.output)
  exit(1)

print("INFO: pre-boot gen complete, rbf files in: " + str(pathlib.Path.cwd()) + '/' + "output_files")

