#!/usr/bin/python

from states import *

reserved = {
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
    "call"
}

SOURCE_CONTENT = ''
CURRENT_SOURCE_INDEX = -1
CURRENT_LINE = 0

'''
    @name is_alpha
    @param char : character read from the source code string.

    @return : True if the parameter is Alpha-type character. False if Not.
'''
def is_alpha(char):
    return ((char >= 'A')&(char <= 'Z'))|((char >= 'a')&(char <= 'z'))|(char == '_')

'''
    @name is_num
    @param char : character read from the source code string.

    @return : True if the parameter is Num-type character. False if Not.
'''
def is_num(char):
    return (char >= '0')&(char <= '9')

'''
    @name is_allhanum
    @param char : character read from the source code string.

    @return : True if the parameter is Alphanum-type character. False if Not.
'''
def is_allhanum(char):
    return is_alpha(char)|is_num(char)

'''
    @name is_white
    @param char : character read from the source code string.

    @return : True if the parameter is White-type character. False if Not.
'''
def is_white(char):
    return (char is '\n')|(char is ' ')|(char is '\t')

'''
    @name operator
    @param char : character read from the source code string.
    @return : True if the parameter is operator-type character. False if Not.
'''
def is_operator(char):
    return (char is '+')|(char is '-')|(char is '*')|(char is '/')

'''
    @name get_next_character
    @return: The next character from the source code string.
'''
def get_next_character():
    global SOURCE_CONTENT, CURRENT_LINE, CURRENT_SOURCE_INDEX

    CURRENT_SOURCE_INDEX = CURRENT_SOURCE_INDEX + 1

    if SOURCE_CONTENT[CURRENT_SOURCE_INDEX] is "\n":
        CURRENT_LINE = CURRENT_LINE + 1
    return SOURCE_CONTENT[CURRENT_SOURCE_INDEX]

'''
    @name put_character_back
    @functionality: Undoes the get next character action by moving the cursor to the previous position. 
    @return: Null.
'''
def put_character_back():
    global SOURCE_CONTENT, CURRENT_LINE, CURRENT_SOURCE_INDEX

    CURRENT_SOURCE_INDEX = CURRENT_SOURCE_INDEX - 1
    if SOURCE_CONTENT[CURRENT_SOURCE_INDEX] is "\n":
        CURRENT_LINE = CURRENT_LINE - 1


def get_next_word():
    buffer = ''
    w = get_next_character()

    while(w is not ' ' & w is not '\n'):
        buffer += w
        w = get_next_character()
    return buffer

def get_next_state(state, char_type):
    if state is 'START':
        return char_type
    elif state is ''
    

'''
    @name lexer

    @functionality :
'''
def lexer():
    current_state = START
    current_char = ''
    current_char_type = ''

    while True:
        current_char = get_next_character()

        if is_alpha(current_char):
            current_char_type = 'ALPHA'
        elif is_num(current_char):
            current_char_type = 'NUM'
        elif is_white(current_char):
            current_char_type = 'WHITE'
        elif is_operator(current_char):
            if current_char is '+' | current_char is "-":
                current_char_type = 'ADDOPERATOR'
            else:
                current_char_type = "MULTOPERATOR"
        else:
            if current_char is '[':
                current_char_type = 'LEFTSBRACK'
            elif current_char is ']':
                current_char_type = 'RIGHTSBRACK'
            elif current_char is '{':
                current_char_type = 'LEFTCBRACK'
            elif current_char is '}':
                current_char_type = 'RIGHTCBRACK'
            elif current_char is '(':
                current_char_type = 'LEFTPAR'
            elif current_char is ')':
                current_char_type = 'RIGHTPAR'
            elif current_char is '<':
                current_char_type = 'LESSTHAN'
            elif current_char is '>':
                current_char_type = 'GREATERTHAN'
            elif current_char is '=':
                current_char_type = 'EQUALS'
            elif current_char is ',':
                current_char_type = 'COMMA'
            elif current_char is ';':
                current_char_type = 'SEMICOL'
            elif current_char is ':':
                current_char_type = 'COL'
            elif current_char is '':
                current_char_type = 'EOF'
            else:
                current_char_type = 'ERR_01'

        if current_state is not 'NF_COMMENT':
            if current_char is '/':
                current_char = get_next_character()
                if current_char is '*':
                    current_state = 'NF_COMMENT'
                else:
                    put_character_back()
                    current_char = '/'
        else:
            if current_char is '*':
                current_char = get_next_character()
                if current_char is '/':
                    current_state = "T_COMMENT"
                    return current_state
                else:
                    put_character_back()
        
        current_state = 


def init_lexer(input_content, debug):
    global err_message, SOURCE_CONTENT

    if debug == True:
        print input_content

    err_message = "No Error!"
    source_content = input_content
