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
import subprocess
import os
import pathlib
import shutil
import sys
import tarfile
import argparse
import logging
import time

logger = logging.getLogger()

# check for git
try:
  import git
except ImportError:
  print("REQUIREMENT MISSING: gitpython, pip install gitpython")
  exit(0)

# check for system builder
try:
  from system.builder import *
except ImportError:
  print("REQUIREMENT MISSING: system_builder, pip install system_builder")
  exit(0)


def main():
  args = parse_args(sys.argv[1:])

  yaml_data = open_yaml(args.yaml_file)

  if yaml_data == None:
    print("ERROR: no yaml file data.")
    exit(~0)

  logger_setup(args.debug)

  for key, value in yaml_data.items():
    print("INFO: GENERATING", key)
    print("INFO: TOOL", value['tool'])

    if value['tool'] == 'git_pull':
      try:
        git_pull(value)
      except Exception as e:
        logger.error(str(e))
        print(f"ERROR: {value['tool']} failed. See log for error.")
        exit(~0)
    elif value['tool'] == 'copy':
      try:
        copy(value)
      except Exception as e:
        logger.error(str(e))
        print(f"ERROR: {value['tool']} failed. See log for error.")
        exit(~0)
    elif value['tool'] == 'find_and_move':
      try:
        find_and_move(value)
      except Exception as e:
        logger.error(str(e))
        print(f"ERROR: {value['tool']} failed. See log for error.")
        exit(~0)
    elif value['tool'] == 'builder':
      try:
        value.pop('tool')
        run_builder(value)
      except Exception as e:
        logger.error(str(e))
        print(f"ERROR: {value['tool']} failed. See log for error.")
        exit(~0)
    elif value['tool'] == 'untar':
      try:
        untar(value)
      except Exception as e:
        logger.error(str(e))
        print(f"ERROR: {value['tool']} failed. See log for error.")
        exit(~0)
    else:
      print("ERROR: NO VALID TOOL")

    print("INFO: TOOL COMPLETED");

def git_pull(value):
  #get dirrrs
  repo_url = value['repo_url']
  tag      = value['tag']
  repo_dir = value['repo_dir']

  if not os.path.exists(os.getcwd() + '/' + repo_dir):
    logger.info(f"Pulling GIT repo from {repo_url}")

    try:
      repo_data = git.Repo.clone_from(repo_url, os.getcwd() + '/' + repo_dir)
    except Exception as e: raise
  else:
    logger.info(f"GIT repo exists, opening for checkout.")
    repo_data = git.Repo(os.getcwd() + '/' + repo_dir)

  try:
    if tag is not None:
      repo_data.git.checkout(tag)
  except Exception as e: raise

def copy(value):
  src_dir = value['src_dir']
  dest_dir = value['dest_dir']

  try:
    shutil.copyfile(os.getcwd() + '/' + src_dir, os.getcwd() + '/' + dest_dir)
  except Exception as e: raise

def find_and_move(value):
  src_file   = value['src_file']
  dest_file  = value['dest_file']

  files_found = sorted(pathlib.Path().glob(src_file))

  if len(files_found) == 0: raise

  logger.info(f"Moving {src_file} to {dest_file}")

  pathlib.Path(files_found[0]).replace(dest_file)

def untar(value):
  src_file   = value['src_file']
  dest_dir   = value['dest_dir']

  comp_file = None

  # open file
  try:
    comp_file = tarfile.open(src_file)
  except Exception as e: raise

  # extracting file
  try:
    comp_file.extractall(dest_dir)
  except Exception as e: raise

  logger.info(f"Extracting {src_file} to {dest_dir}")

  comp_file.close()


def run_builder(yaml_data):
  cmd_compiler = commandCompiler(yaml_commands = "commands.yml")

  cmd_compiler.setProjectsWithYamlData(yaml_data)

  try:
    cmd_compiler.create()
  except Exception as e:
    time.sleep(1)
    print(str(e))
    print("\n" + f"ERROR: build system failure, for details, see log file log/{os.path.basename(logger.handlers[0].baseFilename)}")
    exit(~0)

  projects = cmd_compiler.getResult()

  cmd_exec = commandExecutor(projects, progressbar = False)

  try:
    cmd_exec.runProject()
  except KeyboardInterrupt:
    cmd_exec.stop()
    time.sleep(1)
    print("\n" + f"Build interrupted with CTRL+C.")
    exit(~0)
  except Exception as e:
    time.sleep(1)
    print(str(e))
    print("\n" + f"ERROR: build system failure, for details, see log file log/{os.path.basename(logger.handlers[0].baseFilename)}")
    exit(~0)

# setup logger for log file
def logger_setup(debug):
  log_name = time.strftime("log/" + "%y%m%d", time.localtime()) + '_' +  str(int(time.mktime(time.localtime()))) + '.log'

  os.makedirs(os.getcwd() + "/log", exist_ok=True)

  if debug:
    logger.setLevel(logging.DEBUG)
  else:
    logger.setLevel(logging.INFO)

  log_file = logging.FileHandler(filename = log_name, mode = 'w', delay=True)

  if debug:
    log_file.setLevel(logging.DEBUG)
  else:
    log_file.setLevel(logging.INFO)

  format_file = logging.Formatter(fmt = '%(asctime)-12s : %(levelname)-8s : %(message)s', datefmt='%y.%m.%d %H:%M')
  log_file.setFormatter(format_file)

  logger.addHandler(log_file)

# parse args for tuning build
def parse_args(argv):
  parser = argparse.ArgumentParser(description='Automate generation using yaml target list.')

  parser.add_argument('yaml_file',                                                                                    help='Yaml file used to describe build')
  parser.add_argument('--debug',      action='store_true',  default=False,        dest='debug',       required=False, help='Turn on debug logging messages')

  return parser.parse_args()

def open_yaml(file_name):
  try:
    stream = open(file_name, 'r')
  except:
    print(file_name + " not available.")
    return None

  try:
    yaml_data = yaml.safe_load(stream)
  except yaml.YAMLError as e:
    logger.error("yaml issue")
    for line in str(e).split("\n"):
      logger.error(line)
    print("ERROR: check log for yaml parse error.")
    stream.close()
    return None

  stream.close()
  return yaml_data

if __name__=="__main__":
  main()
