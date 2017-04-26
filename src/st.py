#!/usr/bin/python

from consts import *


class Entry(object):
    def __init__(self, name, entry_type):
        self.type = entry_type
        self.name = name
        self.type_data = None
        self.offset = 0
        self.level = 0


class Function(object):
    def __init__(self, func_type):
        self.func_type = func_type
        self.frame_length = 0
        self.arguments = []
        self.start_quad_id = -1
        self.has_return = False
        self.arg_num = len(self.arguments)


class Argument(object):
    def __init__(self, arg_type):
        self.type = arg_type
        self.offset = 0
        self.func = None


class Variable(object):
    def __init__(self):
        self.offset = 0


class Scope:
    def __init__(self, nesting_level, name):
        self.name = name
        self.nesting_level = nesting_level
        self.encl_scope = None
        self.frame_length = 0
        self.caller = None

        self.parent_entry = None
        self.children_entries = []


class Symbol(object):
    def __init__(self, debug):
        self.level = 1
        self.offset = 0
        self.current_scope = None
        self.global_scope = None
        self.debug = debug
        self.quad_label = 0

    def error_handler(self, message, caller):
        if self.debug:
            print "Caller: " + caller
        print message
        exit(0)

    def push_scope(self, name):
        scope = Scope(self.level, name)
        self.level = self.level + 1

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
        # TODO : pop scope
        if self.current_scope.from_entry is not None:
            if not self.current_scope.from_entry.type_data.has_return and self.current_scope.from_entry.type_data.type == Lang.FUNC_TYPE_FUNC:
                self.error_handler("function " + self.current_scope.from_entry.name + " has no return statement", "pop_scope")

        if self.current_scope.prev is not None:
            self.current_scope.prev.next = None
            self.current_scope = self.current_scope.prev
            cur = self.current_scope.entries

            while cur is not None:
                if cur.type == Lang.TYPE_FUNC:
                    arg = cur.type_data.arguments[cur.type_data.arguments.length - 1]
                cur = cur.next


    def add_symbol(self, symbol):
        # TODO : add symbol
        pass

    '''
        @name new_variable - !!!Not yet implemented at this stage.
        @name - Variable name.
        @return: Null.
    '''
    def new_variable(self, name, temp):
        lookup_entry = self.lookup(name)

        entry_type = -1
        if temp:
            entry_type = Lang.TYPE_TEMP
        else:
            entry_type = Lang.TYPE_VAR

        symbol = Entry(name, entry_type)

        symbol.offset = self.current_scope.frame_length
        self.current_scope.frame_length = self.current_scope.frame_length + 4

        if lookup_entry is not None:
            if lookup_entry.level == self.current_scope.nesting_level:
                if lookup_entry.type == Lang.TYPE_ARG:
                    self.error_handler("Error, Argument " + name + " has been declared.", "new variable")
                else:
                    self.error_handler("Error, " + name + " has been declared in this scope", "new Variable")

        self.add_symbol(symbol)

    '''
        @name new_function - !!!Not yet implemented at this stage.
        @name - Function name.
        @return: Null.
    '''
    def new_function(self, name, func_type):
        if self.lookup(name) is not None:
            self.error_handler("Function " + name + " has been declared", "new function")

        symbol = Entry(name, Lang.TYPE_FUNC)
        func = Function(func_type)
        symbol.type_data = func

        self.add_symbol(symbol)

    def add_argument(self, name, par_type):
        symbol = Entry(name, Lang.TYPE_ARG)
        symbol.offset = self.current_scope.frame_length

        symbol.type_data = Argument(par_type)
        #symbol.type_data.type = par_type
        #symbol.type_data.func = self.current_scope.prev.entries

        symbol.level = self.current_scope.nesting_level
        self.current_scope.frame_length = self.current_scope.frame_length + 4
        self.add_symbol(symbol)

    '''
        @name lookup - Checks if symbol_table contains an entry with a name.
        @name name - Entry name.
        @return - Entry if found. None otherwise.
    '''

    def lookup(self, name):
        current_scope = self.current_scope
        while current_scope is not None:
            for sym in current_scope.children_entries:
                if str(name) is sym.name:
                    return sym
            current_scope = current_scope.encl_scope
        return None
