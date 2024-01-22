#!/usr/bin/env python3
################################################################################
# @file   parse_and_gen.py
# @author Jay Convertino(johnathan.convertino.1@us.af.mil)
# @date   24.01.17
# @brief  parse yaml file to execute built in tools
#
# @license MIT
# Copyright 2024 Jay Convertino
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.
################################################################################

import yaml
import git
import subprocess
import os
import pathlib
import shutil
import sys

def main():
  ## only want one argument
  if len(sys.argv) != 2:
    raise Exception("ERROR: parse_and_arg takes one argument, yaml file to open.")

  stream = open(sys.argv[1], 'r')

  loaded = yaml.safe_load(stream)

  for key, value in loaded.items():
    print("INFO: GENERATING", key)
    print("INFO: TOOL", value['tool'])

    if value['tool'] == 'git_pull':
      git_pull(value)
    elif value['tool'] == 'make':
      make(value)
    elif value['tool'] == 'copy':
      copy(value)
    elif value['tool'] == 'bash':
      bash(value)
    elif value['tool'] == 'quartus_cpf':
      quartus_cpf(value)
    elif value['tool'] == 'mkimage_for_boot_script':
      mkimage_for_boot_script(value)
    elif value['tool'] == 'vivado_xsa_gen':
      vivado_xsa_gen(value)
    elif value['tool'] == 'find_and_move':
      find_and_move(value)
    elif value['tool'] == 'xsct_tcl_run':
      xsct_tcl_run(value)
    elif value['tool'] == 'xiilinx_bootgen':
      xilinx_bootgen(value)
    else:
      print("ERROR: NO VALID TOOL")

def git_pull(value):
  #get dirrrs
  repo_url = value['repo_url']
  tag      = value['tag']
  repo_dir = value['repo_dir']

  if os.path.exists(os.getcwd() + '/' + repo_dir):
    print("INFO: GIT library exists in path, no pull, no checkout.")
    return

  try:
    repo_data = git.Repo.clone_from(repo_url, os.getcwd() + '/' + repo_dir)
  except Exception as e:
    print(e)
    return

  try:
    if tag is not None:
      repo_data.git.checkout(tag)
  except Exception as e:
    print(e)
    return

def make(value):
  src_dir   = value['src_dir']
  make_args = value['make_args']

  make_make_args = ["make"] + make_args

  log = open(os.getcwd() + '/' + pathlib.Path(src_dir).name + "_build.log", "w")

  try:
    subprocess.run(make_make_args, stdout=log, stderr=log, cwd=os.getcwd() + '/' + src_dir)
  except subprocess.CalledProcessError as error_code:
    print("ERROR: Make,", error_code.returncode, error_code.output)
    return

  log.close()

def copy(value):
  src_dir = value['src_dir']
  dest_dir = value['dest_dir']

  try:
    shutil.copyfile(os.getcwd() + '/' + src_dir, os.getcwd() + '/' + dest_dir)
  except Exception as e:
    print(e)
    return

def bash(value):
  command   = value['command']
  arguments = value['arguments']

  executioner = command + arguments

  log = open(os.getcwd() + '/' + pathlib.Path(command[0]).name + "_exec.log", "w")

  try:
    subprocess.run(executioner, stdout=log, stderr=log, cwd=os.getcwd())
  except subprocess.CalledProcessError as error_code:
    print("ERROR: Bash,", error_code.returncode, error_code.output)
    return

  log.close()

def quartus_cpf(value):
  sof_file = value['sof_file']
  rbf_name = value['rbf_name']

  files_found = sorted(pathlib.Path().glob("output_files/*.sof"))

  if len(files_found) == 0:
    print("ERROR: No sof file found, generation failed.")
    return

  try:
    subprocess.run(["quartus_cpf", "-c", "--hps", "-o", "bitstream_compression=on", files_found[0], rbf_name], cwd=str(pathlib.Path.cwd()))
  except subprocess.CalledProcessError as error_code:
    print("Quartus cpf error:", error_code.returncode, error_code.output)
    return

def mkimage_for_boot_script(value):
  arch       = value['arch']
  src_file   = value['src_file']
  dest_file  = value['dest_file']

  try:
    subprocess.run(["mkimage", "-C", "none", "-A", arch, "-T", "script", "-d", src_file, dest_file], cwd=str(pathlib.Path.cwd()))
  except subprocess.CalledProcessError as error_code:
    print("mkimage error:", error_code.returncode, error_code.output)
    return

def vivado_xsa_gen(value):
  xsa_tcl_file = value['xsa_tcl_file']

  try:
    subprocess.run(["vivado", "-mode", "tcl", "-nolog", "-nojournal", "-source", xsa_tcl_file], cwd=str(pathlib.Path.cwd()))
  except subprocess.CalledProcessError as error_code:
    print("vivado error:", error_code.returncode, error_code.output)
    return


def find_and_move(value):
  src_file   = value['src_file']
  dest_file  = value['dest_file']

  files_found = sorted(pathlib.Path().glob(src_file))

  if len(files_found) == 0:
    print("ERROR: src_file not found.")
    return

  pathlib.Path(files_found[0]).replace(dest_file)

def xsct_tcl_run(value):
  tcl_file  = value['tcl_file']

  try:
    subprocess.run(["xsct", tcl_file], cwd=str(pathlib.Path.cwd()))
  except subprocess.CalledProcessError as error_code:
    print("ERROR:", error_code.returncode, error_code.output)
    exit(1)

def xilinx_bootgen(value):
  arch       = value['arch']
  src_file   = value['src_file']
  dest_file  = value['dest_file']
  exec_dir   = value['exec_dir']

  try:
    subprocess.run(["bootgen", "-image", src_file, "-arch", arch, "-o", dest_file], cwd=str(pathlib.Path.cwd()) + "/" + exec_dir)
  except subprocess.CalledProcessError as error_code:
    print("ERROR:", error_code.returncode, error_code.output)
    return

if __name__=="__main__":
  main()
