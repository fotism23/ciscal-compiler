#!/usr/bin/python

from consts import *


class Entry(object):
    def __init__(self, name, entry_type):
        self.type = entry_type
        self.name = name
        self.type_data = None
        self.level = 0


class Function(object):
    def __init__(self, func_type):
        self.func_type = func_type
        self.frame_length = 0
        self.arguments = []
        self.start_quad_id = -1
        self.has_return = False
        self.arg_num = 0
        self.scope = None  # mplampla

    def get_arg_num(self):
        return len(self.arguments)


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
        self.frame_length = 12

        self.caller = None

        # self.parent_entry = None
        self.children_entries = []


class Symbol(object):
    def __init__(self, debug):
        self.level = 1
        self.current_scope = None
        self.global_scope = None
        self.scopes = []
        self.debug = debug

    def error_handler(self, message, caller):
        if self.debug:
            print "Caller: " + caller
        print "Error!!!"
        print message
        exit(0)

    @staticmethod
    def new_entry(name, entry_type):
        return Entry(name, entry_type)

    def push_scope(self, name):
        scope = Scope(self.level, name)
        self.level = self.level + 1
        scope.encl_scope = self.current_scope
        scope.frame_length = 12

        s = self.lookup(name)
        if s is not None and s.type == Lang.TYPE_FUNC:
            s.type_data.scope = scope

        if self.current_scope is not None:
            parent_entry = self.lookup(name)
            scope.parent_entry = parent_entry
        else:
            scope.parent_entry = None
            pass

        if self.current_scope is None:
            self.current_scope = scope
            self.global_scope = self.current_scope
            self.scopes.append(self.current_scope)
        else:
            self.current_scope = scope



        #if len(self.current_scope.children_entries) > 1 and self.current_scope.children_entries[1].type == Lang.TYPE_FUNC:
         #   self.current_scope.children_entries[1].type_data.scope = self.current_scope

    def pop_scope(self):

        if self.current_scope.parent_entry is not None:
            if not self.current_scope.parent_entry.type_data.has_return and self.current_scope.parent_entry.type_data.func_type == Lang.FUNC_TYPE_FUNC:
                self.error_handler("function " + self.current_scope.from_entry.name + " has no return statement", "pop_scope")

        if len(self.scopes) == 0:
            return

        if self.scopes[len(self.scopes) - 1] is not None:
            self.current_scope = self.scopes.pop()

        self.current_scope = self.current_scope.encl_scope
        if self.current_scope is None:
            self.current_scope = self.global_scope



    def add_symbol(self, symbol):
        if symbol.type == Lang.TYPE_FUNC and symbol.type_data.func_type == Lang.FUNC_TYPE_PROG:
            symbol.level = 1
        else:
            if symbol.type == Lang.TYPE_FUNC:
                symbol.level = self.current_scope.nesting_level + 1
            else:
                symbol.level = self.current_scope.nesting_level

        self.current_scope.children_entries.append(symbol)

    '''
        @name new_variable - !!!Not yet implemented at this stage.
        @name - Variable name.
        @return: Null.
    '''
    def new_variable(self, name, temp):
        lookup_entry = self.lookup(name)

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
        symbol.type = par_type
        self.current_scope.parent_entry.type_data.arg_num = self.current_scope.parent_entry.type_data.arg_num + 1
        symbol.type_data.arg_num = self.current_scope.parent_entry.type_data.arg_num
        func = self.current_scope.parent_entry

        symbol.type_data.func = func
        func.type_data.arguments.append(symbol)
        # self.current_scope.type_data.arguments.append(symbol)
        # symbol.type_data.type = par_type
        # symbol.type_data.func = self.current_scope.prev.entries

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
                if str(name) == sym.name:
                    return sym
            current_scope = current_scope.encl_scope
        return None

    def look_for_argument(self, name):
        current_scope = self.current_scope
        while current_scope is not None:
            for sym in current_scope.children_entries:
                if sym.type == Lang.TYPE_FUNC:
                    for arg in sym.type_data.arguments:
                        if arg.name == name:
                            return arg
        return None
