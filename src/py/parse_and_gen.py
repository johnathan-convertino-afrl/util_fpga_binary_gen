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

if __name__=="__main__":
   main()
