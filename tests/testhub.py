import importlib
import sys
import os
from helper import Logger

tests = ["updateProfile", "updateCompany"]

try:
    logfile_name = "\\logs\\" + sys.argv[1] + ".txt"
except:
	logfile_name = (os.path.dirname(__file__) + "\\logs\\testlog-" + datetime.now().strftime("%Y-%M-%d_%H-%M-%S") +".txt")

logger = Logger(logfile_name)

for test in tests:
	testfile = importlib.__import__("int-test_" + test)
	testfile.test(logger)