#!/usr/bin/python

from consts import *


class Syntax(object):
    def __init__(self, lex, symbol_table, inter):
        self.program_id = ''
        self.m_lexer = lex
        self.debug = lex.debug
        self.token = Error.TOKEN_NOT_INITIALIZED
        self.program_block = True
        self.in_while = False
        self.symbol_table = symbol_table
        self.intermediate = inter
        self.start_quad = 0

    '''
        @name run_lexer - Runs lexer and saves the returned state in public token variable.
        @return: Null.
    '''

    def run_lexer(self):
        while True:
            self.token = self.m_lexer.lexer()
            if self.debug:
                print ''
                print "Token : " + str(self.token)
                print "Buffer: " + self.get_lexer_buffer()
            if self.token != KnownState.COMMENT:
                break

        if self.token <= Error.ERROR_NOT_KNOWN_STATE:
            print 'LEXER ERROR'
            exit()

    def get_lexer_buffer(self):
        return self.m_lexer.get_buffer()

    def get_lexer_line(self):
        return self.m_lexer.get_current_line()

    def lookup(self, lookup_id):
        return self.symbol_table.lookup(lookup_id)

    '''
        @name error_handler - Prints the error to the console and exits.
        @param message : Error message from the module that found error.
        @return: Null.
    '''

    def error_handler(self, message, caller):
        if self.debug == True:
            print "Caller: " + caller
        print "Syntax Error line " + str(self.m_lexer.get_current_line()) + " : " + message
        exit(0)

    '''
        @name run_syntax - Runs the the syntax.
        @return: Null.
    '''

    def run_syntax(self):
        self.run_lexer()
        self.program()

    '''
        @name new_variable - !!!Not yet implemented at this stage.
        @name - Variable name.
        @return: Null.
    '''

    def new_variable(self, name, temp):
        self.symbol_table.new_variable(name, temp)

    '''
        @name new_function - !!!Not yet implemented at this stage.
        @name - Function name.
        @return: Null.
    '''

    def new_function(self, name, func_type):
        self.symbol_table.new_function(name, func_type)
        pass

    '''
        Syntax rules functions Start.
        Runs lexer and proccess the returned token following ciscla's Grammar.
        If the token doesn't match the rules an error is thrown.
    '''

    '''
        @name program - Program Rule.
        @return: Null.
    '''

    def program(self):
        if self.token == KnownState.PROGRAM:
            self.run_lexer()
            name = self.id_section()
            self.block(name)
        else:
            self.error_handler("program expected", "program")

    '''
        @name id_section - Program ID Rule.
        @return: Null.
    '''

    def id_section(self):
        if self.token == Token.ALPHANUM and self.program_block:
            self.program_id = self.get_lexer_buffer()
            self.run_lexer()
            return self.program_id
        elif self.token == Token.ALPHANUM and not self.program_block:
            name = self.get_lexer_buffer()
            self.run_lexer()
            return name
        else:
            self.error_handler("id expected", "id_section")

    '''
        @name subprogram - Subprograms Rule.
        @return: Null.
    '''

    def subprogram(self):
        function_type = ''
        if self.token == KnownState.PROCEDURE or self.token == KnownState.FUNCTION:
            if self.token == KnownState.PROCEDURE:
                function_type = Lang.FUNC_TYPE_PROC
            else:
                function_type = Lang.FUNC_TYPE_FUNC
            self.run_lexer()
            name = self.id_section()
            self.new_function(name, function_type)
            self.function_body(name)

    '''
        @name block - Block Rule.
        @param block_name - Block name.
        @return: Null.
    '''

    def block(self, block_name):
        sym_list = self.intermediate.empty_list()

        if self.program_block:
            self.program_block = False

            if self.token == Token.LEFTCBRACK:
                self.symbol_table.push_scope(block_name)
                self.new_function(block_name, Lang.FUNC_TYPE_PROG)
                self.run_lexer()
                self.declarations()
                self.subprogram()

                temp = self.symbol_table.lookup(block_name)
                temp.type_data.start_quad_id = self.symbol_table.quad_label

                self.start_quad = self.symbol_table.quad_label
                self.intermediate.gen_quad("begin_block", self.program_id, "_", "_")

                self.sequence(sym_list)

                if self.token == Token.RIGHTCBRACK:
                    self.symbol_table.pop_scope()
                    self.run_lexer()
                else:
                    self.error_handler("} expected", "block (program)")
            else:
                self.error_handler("{ expected", "block")
            self.intermediate.backpatch(sym_list.next, str(self.intermediate.next_quad()))
            self.intermediate.gen_quad("halt", "_", "_", "_")
            self.intermediate.gen_quad("end_block", self.program_id, "_", "_")
        else:
            if self.token == Token.LEFTCBRACK:
                self.run_lexer()
                self.declarations()
                self.subprogram()

                temp = self.symbol_table.lookup(block_name)
                temp.type_data.start_quad_id = self.symbol_table.quad_label

                self.intermediate.gen_quad("begin_block", self.program_id, "_", "_")

                self.sequence(sym_list)

                if self.token == Token.RIGHTCBRACK:
                    self.symbol_table.pop_scope()
                    self.run_lexer()
                else:
                    self.error_handler("} expected", "block")
            else:
                self.error_handler("{ expected", "block")

            self.intermediate.backpatch(sym_list.next, str(self.intermediate.next_quad()))
            self.intermediate.gen_quad("end_block", self.program_id, "_", "_")

    '''
        @name declarations - Declarations Rule.
        @return: Null.
    '''

    def declarations(self):
        if self.token == KnownState.DECLARE:
            self.run_lexer()
            self.var_list()
            if self.token == KnownState.ENDDECLARE:
                self.run_lexer()
            else:
                self.error_handler("enddeclare expected", "declarations")

    '''
        @name var_list - VarList Rule.
        @return: Null.
    '''

    def var_list(self):
        if self.token == Token.ALPHANUM:
            self.new_variable(self.get_lexer_buffer(), False)
            self.run_lexer()
            while self.token == Token.COMMA:
                self.run_lexer()
                if self.token == Token.ALPHANUM:
                    self.new_variable(self.get_lexer_buffer(), False)
                    self.run_lexer()
                else:
                    self.error_handler("ID expected", "varlist")

    '''
        @name function_body - Function Body Rule.
        @func_name - Function id.
        @return: Null.
    '''

    def function_body(self, func_name):
        self.formal_pars()
        self.block(func_name)

    '''
        @name formal_pars - FormalPars Rule.
        @return: Null.
    '''

    def formal_pars(self):
        if self.token == Token.LEFTPAR:
            self.run_lexer()
            self.formal_pars_list()
            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected", "formal_pars")

    '''
        @name formal_pars_list - FormalPars List Rule.
        @return: Null.
    '''

    def formal_pars_list(self):
        self.formal_par_item()

        while self.token == Token.COMMA:
            self.run_lexer()
            self.formal_par_item()

    '''
        @name formal_par_item - FormalPars Item Rule.
        @return: Null.
    '''

    def formal_par_item(self):
        formal_par_item_type = -1

        if self.token == KnownState.IN or self.token == KnownState.INOUT:
            if self.token == KnownState.IN:
                formal_par_item_type = Lang.PARAMETER_TYPE_IN
            else:
                formal_par_item_type = Lang.PARAMETER_TYPE_INOUT

            self.run_lexer()
            name = self.id_section()

            item = self.lookup(name)
            if item is not None and item.type == Lang.TYPE_FUNC:
                self.error_handler(name + "function already exists.", "formalpar item")
            self.symbol_table.add_argument(name, formal_par_item_type)

        else:
            self.error_handler("in id or inout id expected", "formalpar item")


    '''
        @name sequence - Sequence Rule.
        @return: Null.
    '''

    def sequence(self, sym_list):
        temp_list = self.intermediate.empty_list()

        self.statement(temp_list)

        temp = temp_list.next
        while self.token == Token.SEMICOL:
            self.run_lexer()
            self.statement(temp_list)
            temp = self.intermediate.merge(temp, temp_list.next)
        sym_list.next = temp

    '''
        @name brackets_sequence - Brackets Sequence Rule.
        @return: Null.
    '''

    def brackets_sequence(self, sym_list):
        if self.token == Token.LEFTCBRACK:
            self.run_lexer()
            self.sequence(sym_list)
            if self.token == Token.RIGHTCBRACK:
                self.run_lexer()
            else:
                self.error_handler("} expected", "brackets sequence")
        else:
            self.error_handler("{ expexted", "brackets sequence")

    '''
        @name brack_or_statement - Brack or Statement Rule.
        @return: Null.
    '''

    def brack_or_statement(self, sym_list):
        if self.token == Token.LEFTCBRACK:
            self.brackets_sequence(sym_list)
        else:
            self.statement(sym_list)
            self.run_lexer()
            if self.token != Token.SEMICOL:
                self.error_handler("; expected.", "brack or statement")

    '''
        @name statement - Statement Rule.
        @return: Null.
    '''

    def statement(self, sym_list):

        if self.token == Token.ALPHANUM:
            self.assignment_statement(sym_list)
        elif self.token == KnownState.IF:
            self.if_statement(sym_list)
            self.intermediate.backpatch(sym_list, str(self.intermediate.next_quad()))
        elif self.token == KnownState.DO:
            self.while_statement(sym_list)
            sym_list.next = None
        elif self.token == KnownState.EXIT:
            self.exit_statement()
        elif self.token == KnownState.RETURN:
            self.return_statement(sym_list)
        elif self.token == KnownState.SELECT:
            self.select_statement()
        elif self.token == KnownState.PRINT:
            self.print_statement()
        elif self.token == KnownState.CALL:
            self.call_statement()
        elif self.token == KnownState.WHILE:
            self.while_statement(sym_list)
        else:
            pass

    '''
        @name assignment_statement - Assignment Statement Rule.
        @return: Null.
    '''

    def assignment_statement(self, sym_list):
        variable_id = ''
        attr = self.intermediate.empty_attr()
        if self.token == Token.ALPHANUM:
            variable_id = self.get_lexer_buffer()
            statement = self.lookup(variable_id)

            if statement is None:
                self.error_handler(variable_id + " no such variable.", "assignment statement")
            elif (statement.type == Lang.TYPE_FUNC) or (statement.type == Lang.TYPE_CONST):
                self.error_handler(variable_id + " is not assignable.", "assignment statement")

            self.run_lexer()

            if self.token == Token.COL:
                self.run_lexer()
                if self.token == Token.EQUALS:
                    self.run_lexer()
                    self.expression(attr)
                    self.intermediate.gen_quad(":=", attr.place, "_", variable_id)
                    sym_list.next = None
                else:
                    self.error_handler("assignment operator ( = ) expected", "assignment statement")
            else:
                self.error_handler("assignment operator ( := ) expected", "assignment statement")
        else:
            self.error_handler("expected variable id before assiignment", "assignment statement")

    '''
        @name if_statement - If Assignment Statement Rule.
        @return: Null.
    '''

    def if_statement(self, sym_list):
        s1 = self.intermediate.empty_list()
        tail = self.intermediate.empty_list()
        attr = self.intermediate.empty_attr()
        if self.token == KnownState.IF:
            self.run_lexer()

            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.condition()
                q1 = self.intermediate.next_quad()

                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                    self.brack_or_statement(s1)
                    m_list = self.intermediate.makeList(str(self.intermediate.next_quad()))
                    self.intermediate.gen_quad("jump", "_", "_", "_")
                    q2 = self.intermediate.next_quad()
                    self.elsepart(tail)

                    # TODO : complete backpatch

                    self.intermediate.backpatch(attr.true, str(q1))
                    self.intermediate.backpatch(attr.false, str(q2))
                    sym_list.next = self.intermediate.merge(s1.next, m_list)
                    sym_list.next = self.intermediate.merge(sym_list, tail.next)

                else:
                    self.error_handler(") expected", "id statement")
            else:
                self.error_handler("(<parameters>) expected", "id statement")
        else:
            self.error_handler("if expected", "id statement")

    def elsepart(self, tail):
        s2 = self.intermediate.empty_list()
        if self.token == KnownState.ELSE:
            self.run_lexer()
            self.brack_or_statement(s2)
            tail.next = s2.next
        else:
            tail.next = None

    '''
        @name while_statement - While Statement Rule.
        @return: Null.
    '''

    def while_statement(self, sym_list):
        attr = self.intermediate.empty_attr()
        s1 = self.intermediate.empty_list()
        exitlist = None

        if self.token == KnownState.WHILE:

            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.condition(attr)
                self.intermediate.backpatch(attr.true, str(self.intermediate.next_quad()))
                p2 = self.intermediate.next_quad()
                self.intermediate.backpatch(attr.false, str(self.intermediate.next_quad()))

                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                    sym_list.next = s1.next
                    self.in_while = True
                    self.brack_or_statement(sym_list)
                    self.in_while = False
                else:
                    self.error_handler("expected ).", "while statement")
            else:
                self.error_handler("expected ( after while statement.", "while statement")
        else:
            self.error_handler("expected while statement.", "while statement")

    def do_while_statement(self, sym_list):
        attr = self.intermediate.empty_attr()
        s1 = self.intermediate.empty_list()
        exitlist = None

        if self.token == KnownState.DO:
            p1 = self.intermediate.next_quad()
            self.run_lexer()
            self.in_while = True
            self.brack_or_statement(s1)
            self.in_while = False

            if self.token == KnownState.WHILE:
                self.run_lexer()
                if self.token == Token.LEFTPAR:
                    self.run_lexer()
                    self.condition(attr)
                    self.intermediate.backpatch(attr.true, str(p1))
                    p2 = self.intermediate.next_quad()
                    self.intermediate.backpatch(attr.true, str(p2))
                    if self.token == Token.RIGHTPAR:
                        self.run_lexer()
                        sym_list.next = s1.next
                    else:
                        self.error_handler("expected ).", "do while statement")
                else:
                    self.error_handler("expected ( after while statement.", "do while statement")
            else:
                self.error_handler("expected while statement.", "do while statement")
        else:
            self.error_handler("expected do.", "do while statement")

    def select_statement(self):
        if self.token == KnownState.SELECT:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                if self.token == Token.ALPHANUM:
                    name = self.get_lexer_buffer()
                    var = self.lookup(name)
                    if var is None:
                        self.error_handler("variable with id " + name + " not found.", "select statement")
                    else:
                        self.run_lexer()
                        if self.token == Token.RIGHTPAR:
                            self.run_lexer()
                            while True:
                                if self.token == KnownState.DEFAULT:
                                    self.run_lexer()
                                    if self.token == Token.COL:
                                        break
                                    else:
                                        self.error_handler(": expected.", "select statement")
                                else:
                                    if self.token == Token.NUM:
                                        self.run_lexer()
                                        if self.token == Token.COL:
                                            self.run_lexer()
                                            self.brack_or_statement()
                                        else:
                                            self.error_handler(": expected.", "select statement")
                                    else:
                                        self.error_handler("constant value or default statement expected.",
                                                           "select statement")
                                self.run_lexer()
                            self.brack_or_statement()
                        else:
                            self.error_handler(") expected.", "select statement")
                else:
                    self.error_handler("variable id expected.", "select statement")
            else:
                self.error_handler("( expected.", "select statement")
        else:
            self.error_handler("select statement.", "select statement")

    '''
        @name exit_statement - Exit Statement Rule.
        @return: Null.
    '''

    def exit_statement(self):
        if self.token == KnownState.EXIT:
            if not self.in_while:
                exit()
            self.run_lexer()
        else:
            self.error_handler("exit statement expected.", "exit statement")

    '''
        @name return_statement - Return Statement Rule.
        @return: Null.
    '''

    def return_statement(self, attr):
        if self.symbol_table.current_scope.encl_scope is None or self.symbol_table.caller.type is Lang.TYPE_FUNC:
            self.error_handler("return statement out of function", "return_statement")
        else:
            self.symbol_table.current_scope.caller.data_type.has_return = True

        if self.token == KnownState.RETURN:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.expression(attr)
                self.intermediate.gen_quad("retv", attr.place, "_", "_")
                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                else:
                    self.error_handler(") expected.", "return statement")
            else:
                self.error_handler("( expected after return statement.", "return statement")
        else:
            self.error_handler("return statement expected.", "return statement")

    '''
        @name print_statement - Print Statement Rule.
        @return: Null.
    '''

    def print_statement(self):
        attr = self.intermediate.empty_attr()
        if self.token == KnownState.PRINT:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.expression(attr)
                self.intermediate.gen_quad("print", attr.place, "_", "_")
                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                else:
                    self.error_handler(") expected.", "print statement")
            else:
                self.error_handler("( expected.", "print statement")
        else:
            self.error_handler("print statement expected.", "print statement")

    '''
        @name call_statement - Call Statement Rule.
        @return: Null.
    '''

    def call_statement(self):
        if self.token == KnownState.CALL:
            self.run_lexer()
            if self.token == Token.ALPHANUM:
                name = self.get_lexer_buffer()
                item = self.lookup(name)
                if item is None or (item is not None and item.type != Lang.TYPE_FUNC):
                    self.error_handler(name + " no such procedure.", "call statement")
                if item.type != Lang.FUNC_TYPE_PROG:
                    self.error_handler(name + " is not a procedure.", "call statement")
                self.run_lexer()
                self.actual_pars(name)
                self.intermediate.gen_quad("call", "_", "_", name)
            else:
                self.error_handler("id expected.", "call statement")
        else:
            self.error_handler("call statement expected.", "call statement")

    '''
        @name actual_pars - ActualPars Rule.
        @return: Null.
    '''

    def actual_pars(self, name):
        if self.token == Token.LEFTPAR:
            self.run_lexer()
            self.actual_pars_list(name)
            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected.", "actual_pars")
        else:
            self.error_handler("( expected.", "actual_pars")

    '''
        @name actual_pars_list - ActualPars List Rule.
        @return: Null.
    '''

    def actual_pars_list(self, name):
        temp = self.lookup(name)
        m_from = int(self.intermediate.next_quad()) - 1
        item = self.intermediate.Quad(None)
        item_count = 1
        item_list = self.intermediate.QuadList(None)
        quad = None
        tail = self.intermediate.Quad(None)

        self.actual_par_item(name, item_count, item)
        self.intermediate.addquad(item, item_list, tail)

        while self.token == Token.COMMA:
            self.run_lexer()
            item_count = item_count + 1
            self.actual_par_item(name, item_count, item)
            quad = item
            self.intermediate.addquad(item, item_list, tail)

        quad = tail
        while quad is not None:
            self.intermediate.addquad(quad, self.intermediate.quads, tail)

        if item_count != temp.type_data.arg_num:
            self.error_handler("wrong number of arguments", "actual_pars_list")

    '''
        @name actual_par_item - ActualPars Item Rule.
        @return: Null.
    '''

    def actual_par_item(self, name, item_count, item):
        attr = self.intermediate.empty_attr()
        temp = self.lookup(name)
        args = self.intermediate.Entry(name, temp.type_data.func_type)

        if item_count > temp.type_data.arg_num:
            self.error_handler("wrong number of arguments", "actual_par_item")

        for i in range(0, item_count - 1):
            args = args.next

        if self.token == KnownState.IN:
            self.run_lexer()
            self.expression(attr)
            item = self.intermediate.newquad("par", "CV", attr.place, "_")
        elif self.token == KnownState.INOUT:
            self.run_lexer()
            if self.token == Token.ALPHANUM:
                name = self.get_lexer_buffer()
                symbol = self.lookup(name)
                if symbol is None:
                    self.error_handler(name + " no such variable.", "actual_par item")

                item = self.intermediate.newquad("par", "REF", self.get_lexer_buffer(), "_")
                self.run_lexer()
            else:
                self.error_handler("expected id.", "actual_par item")
        else:
            self.error_handler("IN or INOUT expected.", "actual_par item")

    '''
        @name expression - Expression Rule.
        @return: Null.
    '''

    def expression(self, attr):
        attr1 = self.intermediate.empty_attr()
        attr2 = self.intermediate.empty_attr()

        self.optional_sign(attr1)

        while self.token == Token.ADDOPERATOR:
            op = self.get_lexer_buffer()
            op = op[:-1]
            self.run_lexer()
            self.term(attr2)
            temp = self.intermediate.new_temp()
            self.intermediate.gen_quad(op, attr1.place, attr2.place, temp)
            attr1.place = temp
        attr.place = attr1.place

    '''
        @name optional_sign - Optional Sign Rule.
        @return: Null.
    '''

    def optional_sign(self, attr1):
        if self.token == Token.ADDOPERATOR:
            op = self.get_lexer_buffer()
            self.run_lexer()
            self.term(attr1)
            temp = self.intermediate.new_temp()
            self.intermediate.gen_quad(op, "0", attr1.place, temp)
            attr1.place = temp
        else:
            self.term(attr1)

    '''
        @name term - Term Rule.
        @return: Null.
    '''

    def term(self, attr):
        attr1 = self.intermediate.empty_attr()
        attr2 = self.intermediate.empty_attr()

        self.factor(attr1)

        while self.token == Token.MULTOPERATOR:
            op = self.get_lexer_buffer()
            self.run_lexer()
            self.factor(attr2)
            temp = self.intermediate.new_temp()
            self.intermediate.gen_quad(op, attr1.place, attr2.place, temp)
            attr1.place = temp
        attr.place = attr1.place

    '''
        @name factor - Factor Rule.
        @return: Null.
    '''

    def factor(self, attr):
        attr1 = self.intermediate.empty_attr()
        if self.token == Token.NUM:
            if int(self.get_lexer_buffer()) > 32767 or int(self.get_lexer_buffer()) < -32768:
                self.error_handler("number out of range [-32768, 32767].", "factor")
            attr.place = self.get_lexer_buffer()
            self.run_lexer()
        elif self.token == Token.LEFTPAR:
            self.run_lexer()
            self.expression(attr1)

            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected.", "factor")
            attr.place = attr1.place
        else:
            name = self.id_section()
            temp = None
            if self.token == Token.LEFTPAR:
                symbol = self.lookup(name)
                if (symbol is not None and symbol.type != Lang.TYPE_FUNC) or symbol is None:
                    self.error_handler(name + " is not a function.", "factor")
                self.actual_pars(name)
                temp = self.intermediate.new_temp()
                self.intermediate.gen_quad("par", "RET", temp, "_")
                self.intermediate.gen_quad("call", "_", "_", temp)
                attr.place = temp
            else:
                symbol = self.lookup(name)

                if symbol is None:
                    self.error_handler("variable with id " + str(name) + " not found.", "factor")
                elif symbol.type == Lang.TYPE_FUNC:
                    temp = self.intermediate.new_temp()
                    self.intermediate.gen_quad("par", "RET", temp, "_")
                    self.intermediate.gen_quad("call", "_", "_", temp)
                    attr.place = temp
                elif symbol.type == 'PROC':
                    self.error_handler(name + "is not a function", "factor")
                else:
                    attr.place = temp

    '''
        @name condition - Condition Rule.
        @return: Null.
    '''

    def condition(self, attr):
        attr1 = self.intermediate.empty_attr()
        attr2 = self.intermediate.empty_attr()
        self.bool_term(attr1)
        attr.true = attr1.true
        attr.false = attr1.false
        while self.token == KnownState.OR:
            self.run_lexer()
            quad = self.intermediate.next_quad()
            self.bool_term(attr2)
            self.intermediate.backpatch(attr.false, str(quad))
            attr.true = self.intermediate.merge(attr.true, attr2.true)
            attr.false = attr2.false

    '''
        @name boolterm - Boolterm Rule.
        @return: Null.
    '''

    def bool_term(self, attr):
        attr1 = self.intermediate.empty_attr()
        attr2 = self.intermediate.empty_attr()
        self.bool_factor(attr1)
        attr.true = attr1.true
        attr.false = attr1.false
        while self.token == KnownState.AND:
            self.run_lexer()
            quad = self.intermediate.next_quad()
            self.bool_factor(attr2)
            self.intermediate.backpatch(attr.true, str(quad))
            attr.false = self.intermediate.merge(attr.false, attr2.false)
            attr.false = attr2.true

    '''
        @name bool_factor - BoolFactor Rule.
        @return: Null.
    '''

    def bool_factor(self, attr):
        attr1 = self.intermediate.empty_attr()
        attr2 = self.intermediate.empty_attr()
        m_attr = self.intermediate.empty_attr()
        if self.token == KnownState.NOT:
            self.run_lexer()
            if self.token == Token.LEFTSBRACK:
                self.run_lexer()
                self.condition(m_attr)
                if self.token == Token.RIGHTSBRACK:
                    self.run_lexer()
                    '''todo check'''
                    attr.false = m_attr.false
                    attr.true = m_attr.true
                else:
                    self.error_handler("] expected.", "bool_factor")
            else:
                self.error_handler("[ expected.", "bool_factor")
        elif self.token == Token.LEFTSBRACK:
            self.run_lexer()
            self.condition(m_attr)

            if self.token == Token.RIGHTSBRACK:
                self.run_lexer()
                attr.false = m_attr.false
                attr.true = m_attr.true
            else:
                self.error_handler('] expected.', "bool_factor")
        else:
            self.expression(attr1)
            operator = self.relational_operator()
            self.expression(attr2)
            attr.true = self.intermediate.make_list(str(self.intermediate.next_quad()))
            self.intermediate.gen_quad(operator, attr1.place, attr2.place, "_")
            attr.false = self.intermediate.make_list(str(self.intermediate.next_quad()))
            self.intermediate.gen_quad("jump", "_", "_", "_")

    '''
        @name relational_operator - Relational Operator Rule.
        @return: Null.
    '''

    def relational_operator(self):
        if Token.EQUALS <= self.token <= Token.DIFFERENT:
            operator = self.get_lexer_buffer()
            self.run_lexer()
            return operator
        else:
            self.error_handler("relational operator expected.", "relational operator")

    '''
        Syntax rules functions End.
    '''


class Statement(object):
    def __init__(self, m_type, m_statement_id):
        self.type = m_type
        self.statement_id = m_statement_id
