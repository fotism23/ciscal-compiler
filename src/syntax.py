#!/usr/bin/python

from consts import *
import string
import lexer

class Syntax(object):
    def __init__(self, lex):
        self.program_id = ''
        self.m_lexer = lex
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
    def error_handler(self, message):
        print ("Syntax Error line %d : %d ", self.m_lexer.get_current_line(), message)
        exit(0)

    '''
        @name run_syntax - Runs the the syntax.
        @return: Null.
    '''
    def run_syntax(self):
        self.run_lexer()
        self.program()


    '''
        Syntax rules functions.
        Runs lexer and proccess the returned token.
        If the token doesn't match the rules an error is thrown.
    '''

    '''
        @name program - Program Rule.
        @return: Null.
    '''
    def program(self):
        if self.token == KnownState.PROGRAM:
            self.run_lexer()
            name = self.program_id_section()
            self.block(name)
        else:
            self.error_handler("program expected")

    '''
        @name program_id_section - Program ID Rule.
        @return: Null.
    '''
    def program_id_section(self):
        if self.token == Token.ALPHANUM and self.program_block:
            program_id = self.get_lexer_buffer()

        if self.token == Token.ALPHANUM:
            self.run_lexer()
        else:
            self.error_handler("program id expected")

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
            name = self.program_id_section()
            self.new_function(name)
            self.function_body(name)

    '''
        @name block - Block Rule.
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
                    self.error_handler("} expected")
            else:
                self.error_handler("{ expected")
        else:
            if self.token == Token.LEFTCBRACK:
                self.run_lexer()
                self.declerations()
                self.subprogram()
                self.sequence()
                if self.token == Token.RIGHTCBRACK:
                    self.run_lexer()
                else:
                    self.error_handler("} expected")
            else:
                self.error_handler("{ expected")

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
                self.error_handler("enddeclare expected")

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
                    self.error_handler("ID expected")

    def new_variable(self, name):
        pass

    '''
        @name function_body - Function Body Rule.
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
                self.error_handler(") expected")

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
            name = self.program_id_section()

            item = self.lookup(name)
            if item is not None and item.type == 'FUNC':
                self.error_handler(name + " function already exists.")
        else:
            self.error_handler("in id or inout id expected")

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
                self.error_handler("} expected")
        else:
            self.error_handler("{ expexted")


    def brack_or_statement(self):
        if self.token == Token.LEFTCBRACK:
            self.brackets_sequence()
        else:
            self.statement()

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
                self.error_handler(variable_id + " no such variable.")
            elif (statement.type == 'FUNC') or (statement.type == 'CONST'):
                self.error_handler(variable_id + " is not assignable.")

            self.run_lexer()

            if self.token == Token.COL:
                self.run_lexer()
                if self.token == Token.EQUALS:
                    self.run_lexer()
                    self.expression()
                else:
                    self.error_handler("assignment operator ( = ) expected")
            else:
                self.error_handler("assignment operator ( := ) expected")
        else:
            self.error_handler("expected variable id before assiignment")

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
                    self.error_handler(") expected")
            else:
                self.error_handler("(<parameters>) expected")
        else:
            self.error_handler("if expected")

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
        self.run_lexer()

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
                    self.error_handler("expected ).")
            else:
                self.error_handler("expected ( after while statement.")
        else:
            self.error_handler("expected while statement.")


    '''
        @name exit_statement - Exit Statement Rule.
        @return: Null.
    '''
    def exit_statement(self):
        pass

    def return_statement(self):
        pass

    def select_statement(self):
        pass

    def print_statement(self):
        pass

    def call_statement(self):
        pass

    def expression(self):
        pass

class Statement(object):
    def __init__(self, m_type, m_statement_id):
        self.type = m_type
        self.statement_id = m_statement_id


