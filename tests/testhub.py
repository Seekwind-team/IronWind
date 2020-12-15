import importlib
import sys
import os
import re
from glob import glob
from helper import Logger

cmd_args = sys.argv



tests = []
logfile_name = None

if len(cmd_args) > 1:

	if '-l' in cmd_args:
		index = cmd_args.index('-l')
		cmd_args.pop(index)
		logfile_name = os.path.dirname(os.path.abspath(__file__)) +  "\\logs\\" + sys.argv[-1] + ".txt"
		cmd_args.pop(-1)

	tmp_tests = cmd_args[1:]
	for test in tmp_tests:
		tests.append("int-test_"  + test)


if not tests:
	testfiles = glob(os.path.dirname(os.path.abspath(__file__)) + "\\int-test_*")
	for file in testfiles:
		tests.append(re.search("int-test_.*\.py", file).group(0)[:-3])


logger = Logger(logfile_name)

def test():
	for test in tests:
		testfile = importlib.__import__(test)
		testfile.test(logger)