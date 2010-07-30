#!/usr/bin/env python
import sys, os, unittest, glob

retcode = os.system("(cd ..; python setup.py build)")
if retcode != 0: sys.exit(retcode)
lib_dir = glob.glob(os.path.join("../build/lib*"))[0]
sys.path.insert(0, lib_dir)

#if not os.path.isdir("output"):
#    os.mkdir("output")

from io import *
from rundata import *
unittest.main()


