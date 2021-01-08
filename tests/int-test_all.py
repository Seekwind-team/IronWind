from importlib import __import__


def test_changeEmail():
    __import__("int-test_changeEmail").test()

def test_changePassword():
    __import__("int-test_changePassword").test()

def test_createUser():
    __import__("int-test_createUser").test()

def test_updateCompany():
   __import__("int-test_updateCompany").test()

def test_updateProfile():
   __import__("int-test_updateProfile").test()