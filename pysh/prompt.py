import os, platform

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
