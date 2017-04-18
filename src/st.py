#!/usr/bin/python

class Entry(object):
    def __init__(self, name, entry_type):
        self.type = entry_type
        self.name = name
        self.next = None
        self.type_data = None

class Function(object):
    def __init__(self, func_type):
        self.type = func_type
        self.framelength = 0
        self.arguments = []
        self.start_quad_id = -1

class Argument(object):
    def __init__(self, arg_type):
        self.type = arg_type
        self.offset = 0

class Variable(object):
    def __init__(self):
        self.offset = 0

class Scope:
    def __init__(self, nesting_level):
        self.entries = []
        self.nesting_level = nesting_level
        self.encl_scope = None
    