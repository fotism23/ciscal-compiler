#!/usr/bin/python

'''
    List of Language's reserved words.
'''
class Lang:
    reserved = [
    'and',
    'declare',
    'do',
    'else',
    'enddeclare',
    'exit',
    'procedure',
    'function',
    'print',
    'if',
    'in',
    'inout',
    'not',
    'program',
    'or',
    'return',
    'while',
    'call']

    TYPE_ARG = 0
    TYPE_TEMP = 1
    TYPE_VAR = 2
    TYPE_FUNC = 3
    TYPE_PROG = 4

class Token:
    NT_START = 0
    NT_ALPHA = 1
    NT_NUM = 2
    NT_LESSTHAN = 3
    NT_GREATERTHAN = 4
    NT_COMMENT = 5
    ALPHANUM = 6
    NUM = 7
    CHAR = 8
    WHITE = 9
    ADDOPERATOR = 10
    MULTOPERATOR = 11
    EQUALS = 12
    LESSTHAN = 13
    GREATERTHAN = 14
    LESSTHANEQUAL = 15
    GREATERTHANEQUAL = 16
    DIFFERENT = 17
    SLASH = 18
    STAR = 19
    LEFTCBRACK = 20
    RIGHTCBRACK = 21
    LEFTSBRACK = 22
    RIGHTSBRACK = 23
    LEFTPAR = 24
    RIGHTPAR = 25
    COMMA = 26
    SEMICOL = 27
    COL = 28

class KnownState:
    AND = 29
    DECLARE = 30
    DO = 31
    ELSE = 32
    ENDDECLARE = 33
    EXIT = 34
    PROCEDURE = 35
    FUNCTION = 36
    PRINT = 37
    IF = 38
    IN = 39
    INOUT = 40
    NOT = 41
    PROGRAM = 42
    OR = 43
    RETURN = 44
    WHILE = 45
    CALL = 46
    EOF = 47
    COMMENT = 48
    SELECT = 49
    DEFAULT = 50

class Error:
    ERROR_NOT_KNOWN_STATE = -1
    ERROR_NOT_KNOWN_CHARACTER = -2
    TOKEN_NOT_INITIALIZED = -3
