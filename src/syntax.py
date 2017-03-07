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
            if self.token == Toke.COMMENT:
                break

        if self.token <= Error.ERROR_NOT_KNOWN_STATE:
            print 'LEXER ERROR'
            exit()

    def error_handler(self, message):
        print ("Syntax Error line %d : %d", m_lexer.current_line, message)
    
    def run_syntax(self):
        self.run_lexer()
        program_section()
    
    def program_section(self):
        if self.token == KnownState.PROGRAM:
            self.run_lexer()
        else:
            error_handler("program expected")
        
    def program_id_section(self):
        if self.token == Token.ALPHANUM and self.program_block:
            program_id = m_lexer.local_buffer
        
        if self.token == Token.ALPHANUM:
            self.run_lexer()
        else:
            error_handler("program id expected")

    def subprogram(self):
        function_type = ''
        if token == Token.PROCEDURE or token == Token.FUNCTION:
            if (token == Token.PROCEDURE):
                function_type = 'PROC'
            else:
                function_type = 'FUNC'
            run_lexer()
            
