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

class QuadList(object):
    def __init__(self, name):
        self.next = None
        self.name = name


class Intermidiate(object):
    def __init__(self, debug):
        self.quad_label = 1
        self.quads = None
        self.quad_list = None
        self.debug = debug

    def error_handler(self, message, caller):
        if self.debug == True:
            print "Caller: " + caller
        print message
        exit(0)

    def nextquad(self):
        return self.quad_label

    def genquad(self, operator, x, y, z):
        quad = Quad(operator, x, y, z)
        self.add_quad(quad)
        return quad

    def newtemp(self):
        pass

    def add_quad(self, quad):
        if self.quads is None:
            self.quads = quad
        else:
            self.quads.prev = quad
            quad.next = self.quads
            self.quads = quad

    def emptylist(self):
        pass

    def makelist(self, x):
        return QuadList(x)

    def merge(self, list1, list2):
        if list1 is None:
            return list2
        elif list2 is None:
            return list1

        list_iterator = list1

        while list_iterator.next is not None:
            list_iterator = list_iterator.next

        list_iterator.next = list2
        return list1

    def backpatch(self, m_list, z):
        temp_list = m_list
        while temp_list is not None:
            quad = self.quads
            while quad is not None:
                quad = quad.next
            temp_list = temp_list.next
