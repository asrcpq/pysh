#!/usr/bin/env python3

import traceback
from shell import cmd
from io import BytesIO
import sys, os, platform

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

def pw(s, c):
	return f"[3{c}m{s}[0m"

static = pw(f"{os.getlogin()}@{platform.node()}:", 6)
def prompt(ret):
	result = ""
	if ret != 0:
		result += pw(f"{ret}<", 1)
	result += static
	cwd = os.getcwd()
	result += pw(f"{cwd}", 5)
	if os.access(cwd, os.W_OK):
		result += "\n> "
	else:
		# TODO: wlwrap bug overwrite this color
		result += pw("\n> ", 1)
	return result

ret = 0
sys.path.append(f"{os.getcwd()}/../pywk")
import pywk
while True:
	line = input(prompt(ret))
	ret = proc(line)
