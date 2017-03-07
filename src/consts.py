#!/usr/bin/python

DEBUG = True

class Type:
    NUM = 0
    ALPHA = 1
    WHITE = 2
    ADDOPERATOR = 3
    MULTOPERATOR = 4
    LESSTHAN = 5
    GREATERTHAN = 6
    EQUALS = 7
    SLASH = 8
    STAR = 9
    LEFTSBRACK = 10
    RIGHTSBRACK = 11
    LEFTCBRACK = 12
    RIGHTCBRACK = 13
    LEFTPAR = 14
    RIGHTPAR = 15
    COMMA = 16
    SEMICOL = 17
    COL = 18
    EOF = 19
    ERR_01 = 20

class Lang:
    reserved = [
    "and",
    "declare",
    "do",
    "else",
    "enddeclare",
    "exit",
    "procedure",
    "function",
    "print",
    "if",
    "in",
    "inout",
    "not",
    "program",
    "or",
    "return",
    "while",
    "call"]

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
    LEFTSBRACK = 20
    RIGHTSBRACK = 21
    LEFTCBRACK = 22
    RIGHTCBRACK = 23
    LEFTPAR = 24
    RIGHTPAR = 25
    COMMA = 26
    SEMICOL = 27
    COL = 28

class Error:
    ERROR_NOT_KNOWN_STATE = -1
    ERROR_NOT_KNOWN_CHARACTER = -2
    TOKEN_NOT_INITIALIZED = -3

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
    COMMENT = 47
    

class State:
    START = 0
    PROGRAM = 1
    BLOCK = 2
    DECLARATION = 3
    VARLIST = 4
    SUBPROGRAMS = 5
    FUNC = 6
    FUNCBODY = 7
    FORMALPARS = 8
    FORMALPARLIST = 9
    FORMALPARITEM = 10
    EQUENCE = 11
    BRACKETS_SEQ = 12
    BRACK_OR_STAT = 13
    STATEMENT = 14
    ASSIGNMENT_STAT = 15
    F_STAT = 16
    ELSEPART = 17
    WHILE_STAT = 18
    SELECT_STAT = 19
    DO_WHILE_STAT = 20
    EXIT_STAT = 21
    RETURN_STAT = 22
    PRINT_STAT = 23
    ALL_STAT = 24
    ACTUALPARS = 25
    ACTUALPARLIST = 26
    CTUALPARITEM = 27
    CONDITION = 28
    BOOLTERM = 29
    BOOLFACTOR = 30
    EXPRESSION = 31
    TERM = 32
    FACTOR = 33
    IDTAIL = 34
    RELATIONAL_OPER = 35
    ADD_OPER = 36
    MUL_OPER = 37
    OPTIONAL_SIGN = 38
