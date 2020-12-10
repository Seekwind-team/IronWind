import importlib
from helper import logger

tests = ["updateProfile", "updateCompany"]



for test in tests:
	testfile = importlib.__import__("int-test_" + test)
	testfile.test(logger)