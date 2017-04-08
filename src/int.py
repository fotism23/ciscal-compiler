#!/usr/bin/python

from consts import *
import string

class Quad(object):
    def __init__(self, operator, x, y, z, label):
        self.operator = operator
        self.x = x
        self.y = y
        self.z = z
        self.label = label
        self.next = None
        self.prev = None

class Intermidiate(object):
    def __init__(self):
        self.quad_label = 1

    def nextquad(self):
        return self.quad_label

    def genquad(self, operator, x, y, z):
        quad = Quad(operator, x, y, z)
        self.add_quad(quad)
        return quad

    def newtemp(self):
        pass

    def add_quad(self, quad):
        pass

    def emptylist(self):
        pass

    def makelist(self, x):
        pass

    def merge(self, list1, list2):
        pass

    def backpatch(self, list, z):
        pass
