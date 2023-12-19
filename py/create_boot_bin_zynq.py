#!/usr/bin/env python3
################################################################################
## @file    file_check.py
## @author  Jay Convertino
## @date    2023.02.25
## @brief   file check will pull two file names from settings file based on the
##          tool pased (ex icarus is pulled from the .scr file). These two files
##          are then checked for valid md5 sums that match.
## @warning THIS IS WRITTEN TO ALWAYS LOOK FOR IN_FILE_NAME/OUT_FILE_NAME
##          PARAMETERS.
##
##  MIT License
##
## Copyright 2022 Jay Convertino
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

import sys
import glob
import hashlib

################################################################################
## FUNCTIONS
################################################################################
## icarus_file_find will search for a scr file and pull out in_file_name/out_file_name
def icarus_file_find():
  files = []
  scr_list = glob.glob('*.scr')

  ## did we find it? or did we find too many
  if len(scr_list) != 1:
    raise Exception("ERROR: More than one scr file, or scr file does not exist. NUM: %d", len(scr_list))
  
  ## open the first, and what should be only file in the list
  with open(scr_list[0], "r") as fp:
    ## read each line a find the file_name parameter. 
    for line in fp:
      ## find in_file_name/out_file_name, then split on the = sign, remove quotes, and remove the null terminator.
      if line.find("FILE_NAME") != -1:
        split_line = line.split("=")
        line = split_line[-1].replace('"', '')
        files.append(line.rstrip())
  
  ## should not have more than or less than 2 files
  if len(files) != 2:
    raise Exception("ERROR: could not find two files for comparison.", files)
  
  return files

################################################################################
## MAIN
################################################################################
## Empty lists
files = []
md5sum = []

## only want one argument
if len(sys.argv) != 2:
  raise Exception("ERROR: file_check only takes one argument.")

## check arguments for type of simulator so we can extract file names using the correct method.
if sys.argv[1].lower() == "icarus":
  files = icarus_file_find()
else:
  raise Exception("ERROR: file_check argument needs to be a defined simulator.")

## open each file, and read it in chunks to generate md5 sum
for file in files:
  with open(file, "rb") as fp:
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: fp.read(1024), b""):
      hash_md5.update(chunk)
    
    md5sum.append(hash_md5.hexdigest())

## compare all md5sums to the first to make sure they are all equal, if not raise error.
if all(element == md5sum[0] for element in md5sum):
  print("FILES MATCH WITH A MD5SUM OF:", md5sum[0])
else:
  raise Exception("ERROR: MD5SUM OF A FILE FAILED TO MATCH:", files, md5sum)
