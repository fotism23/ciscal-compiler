#!/usr/bin/python

from consts import *

class Entry(object):
    def __init__(self, name, entry_type):
        self.type = entry_type
        self.name = name
        self.next = None
        self.type_data = None
        self.level = 0
        self.offset = 0

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
    def __init__(self, nesting_level, name):
        self.name = name
        self.entries = []
        self.nesting_level = nesting_level
        self.encl_scope = None
        self.framelength = 0

class Symbol(object):
    def __init__(self, debug):
        self.level = 1
        self.offset = 0
        self.current_scope = None
        self.global_scope = None
        self.debug = debug

    def error_handler(self, message, caller):
        if self.debug == True:
            print "Caller: " + caller
        print message
        exit(0)

    def push_scope(self, name):
        scope = Scope(self.level, name)
        self.level = self.level + 1
        encl_scope = None

        if self.current_scope is not None:
            encl_scope = self.lookup(name)
            scope.encl_scope = encl_scope
        else:
            scope.encl_scope = None

        if self.current_scope is None:
            self.current_scope = scope
            self.global_scope = self.current_scope
        else:
            self.current_scope = scope

    def pop_scope(self):
        pass

    def add_symbol(self, symbol):
        pass

    def new_variable(self, name, temp):
        lookup_entry = self.lookup(name)

        entry_type = -1
        if temp is True:
            entry_type = Lang.TYPE_TEMP
        else:
            entry_type = Lang.TYPE_VAR

        symbol = Entry(name, entry_type)

        symbol.offset = self.current_scope.framelength
        self.current_scope.framelength = self.current_scope.framelength + 4

        if lookup_entry is not None:
            if lookup_entry.level == self.current_scope.nesting_level:
                if lookup_entry.type == Lang.TYPE_ARG:
                    self.error_handler("Error, Argument " + name + " has been declared.", "new variable")
                else:
                    self.error_handler("Error, " + name + " has been declared in this scope", "new Variable")

        self.add_symbol(symbol)

    def new_function(self, name, func_type):
        if self.lookup(name) is not None:
            self.error_handler("Function " + name + " has been declared", "new function")

        symbol = Entry(name, Lang.TYPE_FUNC)
        func = Function(func_type)
        symbol.type_data = func

        self.add_symbol(symbol)

    def add_argument(self, name, par_type):
        symbol = Entry(name, Lang.TYPE_ARG)
        symbol.offset = self.current_scope.framelength
        arg = Argument(par_type)
        symbol.type_data = arg
        symbol.level = self.current_scope.nesting_level
        self.current_scope.framelength = self.current_scope.framelength + 4
        self.add_symbol(symbol)

    def lookup(self, name):
        current_scope = self.current_scope
        while current_scope is not None:
           for sym in current_scope.entries:
               if str(name) is sym.name:
                   return sym
            current_scope = current_scope.encl_scope
        return None

