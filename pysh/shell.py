# cmd
# - escape
# - builtin
#   * cd
# - system

import os, subprocess
import traceback
import string

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
