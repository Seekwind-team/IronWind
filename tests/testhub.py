import importlib
import sys
import os
import re
from glob import glob
from datetime import datetime
from helper import Logger

cmd_args = sys.argv

tests = []
logfile_name = ""

if len(cmd_args) > 1:

	if '-l' in cmd_args:
		index = cmd_args.index('-l')
		cmd_args.pop(index)
		logfile_name = os.path.dirname(__file__) +  "\\logs\\" + sys.argv[-1] + ".txt"
		cmd_args.pop(-1)

	tests = cmd_args[1:]

if not tests:
	testfiles = glob(os.path.dirname(__file__) + "\\int-test*")
	for file in testfiles:
		tests.append(re.search("int-test_.*\.py", file).group(0)[:-3])


if not logfile_name:
	logfile_name = os.path.dirname(__file__) + "\\logs\\testlog-" + datetime.now().strftime("%Y-%M-%d_%H-%M-%S") +".txt"


logger = Logger(logfile_name)

for test in tests:
	testfile = importlib.__import__(test)
	testfile.test(logger)