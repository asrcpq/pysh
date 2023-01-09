#!/usr/bin/env python3

import traceback
import sys, os, pathlib
from pysh.shell import cmd
from pysh.prompt import prompt
from pysh import bi

def get_bins():
	result = []
	for path in os.environ["PATH"].split(":"):
		try:
			for b in os.listdir(path):
				result.append(b)
		except:
			print(traceback.format_exc())
	return result

bins = set(get_bins())
print("load", len(bins), "binaries")
pyreserve = set(["import"])
bins -= pyreserve
shident = ["cd"]

def proc(line):
	tok1 = line.split()
	if not tok1:
		return 127
	tok1 = tok1[0]
	if tok1 in shident or tok1 in bins:
		return cmd(line)
	else:
		try:
			line = pywk.convert(line)
			exec(line)
			return 0
		except:
			print(traceback.format_exc())
			return 127

ret = 0
srcdir = pathlib.Path(sys.argv[0]).parent
sys.path.append(f"{srcdir}/../pywk")
import pywk
sys.path.append(f"{srcdir}/../pyrl")
import pyrl
while True:
	offset = prompt(ret)
	line = pyrl.readline(offset)
	ret = proc(line)
