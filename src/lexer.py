#!/usr/bin/python

from consts import *
import string

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
    elif state is '':
        return

def is_terminal_state():
    return
    

'''
    @name lexer

    @functionality :
'''
def lexer():
    current_state = Token.NF_START
    current_char = ''
    current_char_type = -1
    local_buffer = ''

    while True:
        current_char = get_next_character()

        if is_alpha(current_char):
            current_char_type = Type.ALPHA
        elif is_num(current_char):
            current_char_type = Type.NUM
        elif is_white(current_char):
            current_char_type = Type.WHITE
        elif is_operator(current_char):
            if current_char is '+' | current_char is "-":
                current_char_type = Type.ADDOPERATOR
            else:
                current_char_type = Type.MULTOPERATOR
        else:
            if current_char is '[':
                current_char_type = Type.LEFTSBRACK
            elif current_char is ']':
                current_char_type = Type.RIGHTSBRACK
            elif current_char is '{':
                current_char_type = Type.LEFTCBRACK
            elif current_char is '}':
                current_char_type = Type.RIGHTCBRACK
            elif current_char is '(':
                current_char_type = Type.LEFTPAR
            elif current_char is ')':
                current_char_type = Type.RIGHTPAR
            elif current_char is '<':
                current_char_type = Type.LESSTHAN
            elif current_char is '>':
                current_char_type = Type.GREATERTHAN
            elif current_char is '=':
                current_char_type = Type.EQUALS
            elif current_char is ',':
                current_char_type = Type.EQUALS
            elif current_char is ';':
                current_char_type = Type.SEMICOL
            elif current_char is ':':
                current_char_type = Type.COL
            elif current_char is '':
                current_char_type = Type.EOF
            else:
                current_char_type = Type.ERR_01

        if current_state != Token.NF_COMMENT:
            if current_char is '/':
                current_char = get_next_character()
                if current_char is '*':
                    current_state = Token.NF_COMMENT
                else:
                    put_character_back()
                    current_char = '/'
        else:
            if current_char is '*':
                current_char = get_next_character()
                if current_char is '/':
                    current_state = KnownState.COMMENT
                    return current_state
                else:
                    put_character_back()

        current_state = get_next_state(current_state, current_char_type)

        if current_state != Token.NF_COMMENT:
            if current_state != Token.WHITE:
                local_buffer += current_char
            else:
                current_state = Token.NF_START
                continue

            if is_terminal_state() & current_state != Token.WHITE:
                if current_state == Token.ALPHANUM:
                    put_character_back()
                    local_buffer = local_buffer[:-1]

                    if buffer in Lang.reserved:
                        current_state = Lang.reserved.index(buffer)
                        return current_state

                if current_state == Token.NUM:
                    put_character_back()
                    local_buffer = local_buffer[:-1]

                if current_state == Token.GREATERTHAN | current_state == Token.LESSTHAN:
                    put_character_back()

                local_buffer = local_buffer[:-1]
                return current_state
    return Error.ERROR_NOT_KNOWN_STATE




def init_lexer(input_content, debug):
    global err_message, SOURCE_CONTENT

    if debug == True:
        print input_content

    err_message = "No Error!"
    source_content = input_content
