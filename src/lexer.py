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
source_content = ''
current_source_index = -1
current_line = 0

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
	return isAlpha(char)|isNum(char)

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

    @return : The next character from the source code string.
'''
def get_next_character():
    global source_content
    global line
    global current_source_index

    current_source_index = current_source_index+1

    if (source_content[current_source_index] is "\n"):
        line = line + 1
    return source_content[current_source_index]

'''
    @name main_loop

    @functionality : 
'''
def main_loop():
    current_state = START
    current_char = ''
    current_char_type = ''

    while(True):
        if is_alpha(current_char): current_char_type = 'ALPHA'
        elif is_num(current_char): current_char_type = 'NUM'
        elif is_white(current_char): current_char_type = 'WHITE'
        elif is_operator(current_char):
            if (current_char is '+' | current_char is "-"):
                current_char_type = 'ADDOPERATOR'
            else:
                current_char_type = "MULTOPERATOR"

'''
    @name check_grammar
    @param input_content : a string representation of the input source code.
    
    @functionality : 

    @return : True if the source file meets the grammar specifications. False if Not.
'''
def check_grammar(input_content):
    global err_message
    global source_content

    err_message = "No Error!"
    source_content = input_content
    print input_content
    return False

