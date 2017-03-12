#!/usr/bin/python

from consts import *
import string
import lexer

class Syntax(object):
    def __init__(self, lex):
        self.program_id = ''
        self.m_lexer = lex
        self.debug = lex.debug
        self.token = Error.TOKEN_NOT_INITIALIZED
        self.program_block = True
        self.in_while = False

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
        return None

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
    def new_variable(self, name):
        pass

    '''
        @name new_function - !!!Not yet implemented at this stage.
        @name - Function name.
        @return: Null.
    '''
    def new_function(self, name):
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
            program_id = self.get_lexer_buffer()

        if self.token == Token.ALPHANUM:
            self.run_lexer()
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
                function_type = 'PROC'
            else:
                function_type = 'FUNC'
            self.run_lexer()
            name = self.id_section()
            self.new_function(name)
            self.function_body(name)

    '''
        @name block - Block Rule.
        @param block_name - Block name.
        @return: Null.
    '''
    def block(self, block_name):
        if self.program_block == True:
            self.program_block = False

            if self.token == Token.LEFTCBRACK:
                self.new_function(block_name)
                self.run_lexer()
                self.declerations()
                self.subprogram()
                self.sequence()
                if self.token == Token.RIGHTCBRACK:
                    self.run_lexer()
                else:
                    self.error_handler("} expected", "block (program)")
            else:
                self.error_handler("{ expected", "block")
        else:
            if self.token == Token.LEFTCBRACK:
                self.run_lexer()
                self.declerations()
                self.subprogram()
                self.sequence()
                if self.token == Token.RIGHTCBRACK:
                    self.run_lexer()
                else:
                    self.error_handler("} expected", "block")
            else:
                self.error_handler("{ expected", "block")

    '''
        @name declerations - Declerations Rule.
        @return: Null.
    '''
    def declerations(self):
        if self.token == KnownState.DECLARE:
            self.run_lexer()
            self.varlist()
            if self.token == KnownState.ENDDECLARE:
                self.run_lexer()
            else:
                self.error_handler("enddeclare expected", "declerations")

    '''
        @name varlist - Varlist Rule.
        @return: Null.
    '''
    def varlist(self):
        if self.token == Token.ALPHANUM:
            self.new_variable(self.get_lexer_buffer())
            self.run_lexer()
            while self.token == Token.COMMA:
                self.run_lexer()
                if self.token == Token.ALPHANUM:
                    self.new_variable(self.get_lexer_buffer())
                    self.run_lexer()
                else:
                    self.error_handler("ID expected", "varlist")

    '''
        @name function_body - Function Body Rule.
        @func_name - Function id.
        @return: Null.
    '''
    def function_body(self, func_name):
        self.formalpars()
        self.block(func_name)

    '''
        @name formalpars - Formalpars Rule.
        @return: Null.
    '''
    def formalpars(self):
        if self.token == Token.LEFTPAR:
            self.run_lexer()
            self.formalpars_list()
            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected", "formalpars")

    '''
        @name formalpars_list - Formalpars List Rule.
        @return: Null.
    '''
    def formalpars_list(self):
        self.formalpar_item()

        while self.token == Token.COMMA:
            self.run_lexer()
            self.formalpar_item()

    '''
        @name formalpar_item - Formalpars Item Rule.
        @return: Null.
    '''
    def formalpar_item(self):
        formalpar_item_type = ''

        if self.token == KnownState.IN or self.token == KnownState.INOUT:
            if self.token == KnownState.IN:
                formalpar_item_type = 'IN'
            else:
                formalpar_item_type = 'INOUT'

            self.run_lexer()
            name = self.id_section()

            item = self.lookup(name)
            if item is not None and item.type == 'FUNC':
                self.error_handler(name + "function already exists.", "formalpar item")
        else:
            self.error_handler("in id or inout id expected", "formalpar item")

    '''
        @name sequence - Sequence Rule.
        @return: Null.
    '''
    def sequence(self):
        self.statement()

        while self.token == Token.SEMICOL:
            self.run_lexer()
            self.statement()

    '''
        @name brackets_sequence - Brackets Sequence Rule.
        @return: Null.
    '''
    def brackets_sequence(self):
        if self.token == Token.LEFTCBRACK:
            self.run_lexer()
            self.sequence()
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
    def brack_or_statement(self):
        if self.token == Token.LEFTCBRACK:
            self.brackets_sequence()
        else:
            self.statement()
            self.run_lexer()
            if self.token != Token.SEMICOL:
                self.error_handler("; expected.", "brack or statement")

    '''
        @name statement - Statement Rule.
        @return: Null.
    '''
    def statement(self):
        if self.token == Token.ALPHANUM:
            self.assignment_statement()
        elif self.token == KnownState.IF:
            self.if_statement()
        elif self.token == KnownState.DO:
            self.while_statement()
        elif self.token == KnownState.EXIT:
            self.exit_statement()
        elif self.token == KnownState.RETURN:
            self.return_statement()
        elif self.token == KnownState.SELECT:
            self.select_statement()
        elif self.token == KnownState.PRINT:
            self.print_statement()
        elif self.token == KnownState.CALL:
            self.call_statement()
        elif self.token == KnownState.WHILE:
            self.while_statement()
        else:
            pass

    '''
        @name assignment_statement - Assignment Statement Rule.
        @return: Null.
    '''
    def assignment_statement(self):
        variable_id = ''
        if self.token == Token.ALPHANUM:
            variable_id = self.get_lexer_buffer()
            statement = self.lookup(variable_id)

            if statement is None:
                self.error_handler(variable_id + " no such variable.", "assignment statement")
            elif (statement.type == 'FUNC') or (statement.type == 'CONST'):
                self.error_handler(variable_id + " is not assignable.", "assignment statement")

            self.run_lexer()

            if self.token == Token.COL:
                self.run_lexer()
                if self.token == Token.EQUALS:
                    self.run_lexer()
                    self.expression()
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
    def if_statement(self):
        if self.token == KnownState.IF:
            self.run_lexer()

            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.condition()
                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                    self.brack_or_statement()
                    self.elsepart()
                else:
                    self.error_handler(") expected", "id statement")
            else:
                self.error_handler("(<parameters>) expected", "id statement")
        else:
            self.error_handler("if expected", "id statement")

    def elsepart(self):
        if self.token == KnownState.ELSE:
            self.run_lexer()
            self.brack_or_statement()
        else:
            pass

    '''
        @name while_statement - While Statement Rule.
        @return: Null.
    '''
    def while_statement(self):
        if self.token == KnownState.WHILE:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.condition()
                if self.token == Token.RIGHTPAR:
                    self.run_lexer()
                    self.in_while = True
                    self.brack_or_statement()
                    self.in_while = False
                else:
                    self.error_handler("expected ).", "while statement")
            else:
                self.error_handler("expected ( after while statement.", "while statement")
        else:
            self.error_handler("expected while statement.", "while statement")

    def do_while_statement(self):
        if self.token == KnownState.DO:
            self.run_lexer()
            self.in_while = True
            self.brack_or_statement()
            self.in_while = False

            if self.token == KnownState.WHILE:
                self.run_lexer()
                if self.token == Token.LEFTPAR:
                    self.run_lexer()
                    self.condition()
                    if self.token == Token.RIGHTPAR:
                        self.run_lexer()
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
                                        self.error_handler("constant value or default statement expected.", "select statement")
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
            if self.in_while == False:
                exit()
            self.run_lexer()
        else:
            self.error_handler("exit statement expected.", "exit statement")

    '''
        @name return_statement - Return Statement Rule.
        @return: Null.
    '''
    def return_statement(self):
        if self.token == KnownState.RETURN:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.expression()
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
        if self.token == KnownState.PRINT:
            self.run_lexer()
            if self.token == Token.LEFTPAR:
                self.run_lexer()
                self.expression()
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
                if item is None or (item is not None and item.type != 'FUNC'):
                    self.error_handler(name + " no such procedure.", "call statement")
                elif item.type != 'PROC':
                    self.error_handler(name + " is not a procedure.", "call statement")
                self.run_lexer()
                self.actualpars(name)
            else:
                self.error_handler("id expected.", "call statement")
        else:
            self.error_handler("call statement expected.", "call statement")

    '''
        @name actualpars - Actualpars Rule.
        @return: Null.
    '''
    def actualpars(self, name):
        if self.token == Token.LEFTPAR:
            self.run_lexer()
            self.actualpars_list(name)
            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected.", "actualpars")
        else:
            self.error_handler("( expected.", "actualpars")

    '''
        @name actualpars_list - Actualpars List Rule.
        @return: Null.
    '''
    def actualpars_list(self, name):
        self.actualpar_item(name)

        while self.token == Token.COMMA:
            self.run_lexer()
            self.actualpar_item(name)
    '''
        @name actualpar_item - Actualpars Item Rule.
        @return: Null.
    '''
    def actualpar_item(self, name):
        if self.token == KnownState.IN:
            self.run_lexer()
            self.expression()
        elif self.token == KnownState.INOUT:
            self.run_lexer()
            if self.token == Token.ALPHANUM:
                name = self.get_lexer_buffer()
                symbol = self.lookup(name)
                if symbol is None:
                    self.error_handler(name + " no such variable.", "actualpar item")
                self.run_lexer()
            else:
                self.error_handler("expected id.", "actualpar item")
        else:
            self.error_handler("IN or INOUT expected.", "actualpar item")

    '''
        @name expression - Expression Rule.
        @return: Null.
    '''
    def expression(self):
        self.optional_sign()
        self.term()

        while self.token == Token.ADDOPERATOR:
            self.run_lexer()
            self.term()

    '''
        @name optional_sign - Optional Sign Rule.
        @return: Null.
    '''
    def optional_sign(self):
        if self.token == Token.ADDOPERATOR:
            self.run_lexer()

    '''
        @name term - Term Rule.
        @return: Null.
    '''
    def term(self):
        self.factor()

        while self.token == Token.MULTOPERATOR:
            self.run_lexer()
            self.factor()

    '''
        @name factor - Factor Rule.
        @return: Null.
    '''
    def factor(self):
        if self.token == Token.NUM:
            if int(self.get_lexer_buffer()) > 32767 or int(self.get_lexer_buffer()) < -32768:
                self.error_handler("number out of range [-32768, 32767].", "factor")
            self.run_lexer()
        elif self.token == Token.LEFTPAR:
            self.run_lexer()
            self.expression()

            if self.token == Token.RIGHTPAR:
                self.run_lexer()
            else:
                self.error_handler(") expected.", "factor")
        else:
            name = self.id_section()

            if self.token == Token.LEFTPAR:
                symbol = self.lookup(name)
                if (symbol is not None and symbol.type != 'FUNC') or symbol is None:
                    self.error_handler(name + " is not a function.", "factor")
                self.actualpars(name)
            else:
                symbol = self.lookup(name)

                if symbol is None:
                    self.error_handler("variable with id " + name + " not found.", "factor")
                elif symbol.type == 'FUNC':
                    pass
                elif symbol.type == 'PROC':
                    self.error_handler(name + "is not a function", "factor")

    '''
        @name condition - Condition Rule.
        @return: Null.
    '''
    def condition(self):
        self.boolterm()
        while self.token == KnownState.OR:
            self.run_lexer()
            self.boolterm()

    '''
        @name boolterm - Boolterm Rule.
        @return: Null.
    '''
    def boolterm(self):
        self.boolfactor()
        while self.token == KnownState.AND:
            self.run_lexer()
            self.boolfactor()

    '''
        @name boolfactor - Boolfactor Rule.
        @return: Null.
    '''
    def boolfactor(self):
        if self.token == KnownState.NOT:
            self.run_lexer()
            if self.token == Token.LEFTSBRACK:
                self.run_lexer()
                self.condition()
                if self.token == Token.RIGHTSBRACK:
                    self.run_lexer()
                else:
                    self.error_handler("] expected.", "boolfactor")
            else:
                self.error_handler("[ expected.", "boolfactor")
        elif self.token == Token.LEFTSBRACK:
            self.run_lexer()
            self.condition()

            if self.token == Token.RIGHTSBRACK:
                self.run_lexer()
            else:
                self.error_handler('] expected.', "boolfactor")
        else:

            self.expression()
            operator = self.relational_operator()
            self.expression()

    '''
        @name relational_operator - Relational Operator Rule.
        @return: Null.
    '''
    def relational_operator(self):
        if self.token >= Token.EQUALS and self.token <= Token.DIFFERENT:
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


