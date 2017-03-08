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
    

    def run_lexer(self):
        while True:
            self.token = self.m_lexer.lexer()
            if self.token != KnownState.COMMENT:
                break

        if self.token <= Error.ERROR_NOT_KNOWN_STATE:
            print 'LEXER ERROR'
            exit()

    def error_handler(self, message):
        print ("Syntax Error line %d : %d", self.m_lexer.current_line, message)

    def run_syntax(self):
        self.run_lexer()
        self.program_section()

    def program_section(self):
        if self.token == KnownState.PROGRAM:
            self.run_lexer()
            name = self.program_id_section()
            self.block_section(name)
        else:
            self.error_handler("program expected")

    def program_id_section(self):
        if self.token == Token.ALPHANUM and self.program_block:
            program_id = self.m_lexer.local_buffer

        if self.token == Token.ALPHANUM:
            self.run_lexer()
        else:
            self.error_handler("program id expected")

    def subprogram_section(self):
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

    def block_section(self, block_name):
        if self.program_block == True:
            self.program_block = False

            if self.token == Token.LEFTCBRACK:
                self.new_function(block_name)
                self.run_lexer()
                self.declerations_section()
                self.subprogram_section()
                self.sequence()

                if self.token == Token.RIGHTCBRACK:
                    self.run_lexer()
                else:
                    self.error_handler(" } expected")
            else:
                self.error_handler(" { expected")
        else:
            if self.token == Token.LEFTCBRACK:
                self.run_lexer()
                self.declerations_section()
                self.subprogram_section()
                self.sequence()
                if self.token == Token.RIGHTCBRACK:
                    self.run_lexer()
                else:
                    self.error_handler(" } expected")
            else:
                self.error_handler(" { expected")

    def declerations_section(self):
        if self.token == KnownState.DECLARE:
            self.run_lexer()
            self.varlist()
            if self.token == KnownState.ENDDECLARE:
                self.run_lexer()
            else:
                self.error_handler(" enddeclare expected")

    def varlist(self):
        if self.token == Token.ALPHANUM:
            self.new_variable(self.m_lexer.local_buffer)
            self.run_lexer()

            while self.token == Token.COMMA:
                self.run_lexer()

                if self.token == Token.ALPHANUM:
                    self.new_variable(self.m_lexer.local_buffer)
                    self.run_lexer()
                else:
                    self.error_handler("ID expected")

    def sequence(self):
        pass

    def new_variable(self, name):
        pass
