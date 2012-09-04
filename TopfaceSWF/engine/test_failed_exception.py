__author__ = 'ngavrish'

class TestFailedException(Exception):

    def __init__(self,value):
        print "TEST FAILED"
        print value
        self.value = value

    def __str__(self):
        return repr(self.value)

