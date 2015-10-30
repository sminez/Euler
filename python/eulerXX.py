#! /usr/bin/ python3.4
'''PROBLEM DESCRIPTION FROM EULER.net'''
import time


def eulerXX():
    start = time.time()
    # -- ACTUAL CODE GOES HERE!
    finish = time.time() - start
    print("Solution found in " + str("{0:.5f}".format(finish)) + " seconds.")

if __name__=='__main__':
    eulerXX()
