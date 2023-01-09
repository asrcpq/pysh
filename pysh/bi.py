# python builtins
from biutils import cmdp

def pipechain(s):
	import sys
	from subprocess import Popen, PIPE
	p = Popen(cmdp(s[0]), stdout = PIPE)
	prev_out = p.stdout
	for ss in s[1:]:
		ss = cmdp(ss)
		p = Popen(ss, stdin = prev_out, stdout = PIPE)
		prev_out = p.stdout
	for c in iter(lambda: prev_out.read(1), b""):
		sys.stdout.buffer.write(c)
