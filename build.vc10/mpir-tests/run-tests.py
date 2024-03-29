#
# Python script for running GMP tests 
#
# Run this from the build.vc9\mpir-tests directory

from __future__ import print_function
import os
import shutil
import string
import copy
import subprocess
import code
import sys
import re

try:
  f = open('..\output_params.bat')
  par = f.readlines()
  f.close()
  m1 = re.match(r'\(set libr\=(.*)\)', par[0])
  m2 = re.match(r'\(set plat\=(.*)\)', par[1])
  m3 = re.match(r'\(set conf\=(.*)\)', par[2])
  if m1 and m2 and m3:
    d = (m1.group(1), m2.group(1), m3.group(1))
  else:
    raise IOError
except Exception:
  print('Cannot determine test configuration from "output_params.bat"')
  sys.exit(-1)

tdir = d[1] + '\\' + d[2] + '\\'
if d[0] == 'dll':
# shutil.copy("..\\dll\\" + tdir + "mpir.dll",  os.getcwd())
  xt = 'Dynamic Link Library'
else:
  xt = 'Static Library'
print('Testing MPIR {:s} in {:s} Configuration'.format(xt, tdir))

dir_list = []
for x in os.walk(os.getcwd()) :
  if x[0] == os.getcwd() :
    dir_list += x[1]
  else :
    break

prj_list = []
for x in dir_list :
  l = os.listdir(os.getcwd() + '\\' + x)
  for f in l :
    y = os.path.splitext(f)
    if y[1] == '.vcxproj' and y[0] != 'add-test-lib' :
      prj_list += [y[0]]
prj_list.sort()

exe_list = []
try :
  l = os.listdir(os.getcwd() + '\\..\\' + tdir)
except :
  print("Tests have not been built for this configuration")
  os._exit(-1)

for f in l :
  x = os.path.splitext(f)
  if x[1] == '.exe' :
    exe_list += [x[0]]
exe_list.sort()
if len(exe_list) == 0 :
  print("No executable test files for this configuration")
  os._exit(-1)

build_fail = 0
run_ok = 0
run_fail = 0
for i in prj_list :
  if i in exe_list :
    ef = '.\\..\\' + tdir + '\\' + i + '.exe'
    prc = subprocess.Popen( ef, stdout = subprocess.PIPE,
      stderr = subprocess.STDOUT, creationflags = 0x08000000 )
    output = prc.communicate()[0]
    if prc.returncode :
      print(i, ': ERROR (', prc.returncode, ' )')
      run_fail += 1
    else :
      print(i, ': success')
      run_ok += 1
    if output :
      print('    ', output.decode(), end = '')
  else :
    print("Build failure for {0}".format(i))
    build_fail += 1
print(build_fail + run_ok + run_fail, "tests:")
if build_fail > 0 :
  print("\t{0} failed to build".format(build_fail))
if run_ok > 0 :
  print("\t{0} ran correctly".format(run_ok))
if run_fail > 0 :
  print("\t{0} failed".format(run_fail)) 
if len(sys.argv) == 1 :
  try :
    input(".. completed - press ENTER")
  except :
    pass
else :
  sys.exit(build_fail + run_fail)
