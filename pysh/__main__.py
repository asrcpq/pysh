#!/usr/bin/env python3

import traceback
import subprocess
from io import BytesIO
import os, string, platform

def cd(path):
	try:
		os.chdir(path)
	except:
		print(traceback.format_exc())
		return

vborder = set(
	string.ascii_lowercase +
	string.ascii_uppercase +
	string.digits +
	"_"
)
nul = '\x00'
def escape(w):
	result = ""
	vstack = ""
	state = 0
	for ch in w + chr(0):
		if ch == "$":
			state = 1
			continue
		if state == 1:
			if ch in vborder:
				vstack += ch
			else:
				result += os.environ.get(vstack, "")
				if ch != nul:
					result += ch
				vstack = ""
				state = 0
			continue
		if ch != nul:
			result += ch
	return result

def builtin(split):
	if split[0] == "echo":
		print(" ".join(split[1:]))
		return 0
	if split[0] == "cd":
		cd(split[1])
		return 0
	return 127

def system(split):
	try:
		p = subprocess.run(split)
		return p.returncode
	except:
		print(traceback.format_exc())
		return 127

builtins = set(["cd", "echo"])
def cmd(line):
	split = line.split()
	split = [escape(w) for w in split]
	# print(split)
	if split[0] in builtins:
		return builtin(split)
	return system(split)

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
while True:
	line = input(prompt(ret))
	ret = proc(line)
