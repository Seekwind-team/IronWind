from importlib import __import__
from glob import glob
import os
import re
from pprint import pprint as print

def create_test(module_name):
    def func():
        __import__("int-test_" + module_name).test()
    func.__name__ = "test" + module_name
    return func

testfiles = glob(os.path.dirname(os.path.abspath(__file__)) + r"\int-test_*")
thisfile = glob(os.path.dirname(os.path.abspath(__file__)) + r"\int-test_all.py")[0]
testfiles.remove(thisfile)

modules = []

for file in testfiles:
	modules.append(re.search(r"int-test_.*.py", file).group(0)[9:-3])

for module in modules:
    globals()['test_' + module] = create_test(module)