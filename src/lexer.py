#!/usr/bin/python

from consts import *
import string


class Lexer(object):
    def __init__(self):
        self.source_content = ''
        self.source_content_index = -1
        self.current_line = 0
        self.err_message = ''
        self.local_buffer = ''

    '''
        @name init_lexer
        @param input_content: Source code input in string representation.
        @param debug: Enable Debuging Boolean (Developers only).
        @return: Null.
    '''
    def init_lexer(self, input_content):
        if DEBUG == True:
            print input_content

        self.err_message = "No Error!"
        self.source_content = input_content

    '''
        @name is_alpha
        @param char : character read from the source code string.
        @return : True if the parameter is Alpha-type character. False if Not.
    '''
    def is_alpha(self, char):
        return ((char >= 'A') and (char <= 'Z')) or ((char >= 'a') and (char <= 'z')) or (char == '_')

    '''
        @name is_num
        @param char : character read from the source code string.
        @return : True if the parameter is Num-type character. False if Not.
    '''
    def is_num(self, char):
        return (char >= '0') and (char <= '9')


    '''
        @name is_allhanum
        @param char : character read from the source code string.
        @return : True if the parameter is Alphanum-type character. False if Not.
    '''
    def is_allhanum(self, char):
        return self.is_alpha(char) or self.is_num(char)


    '''
        @name is_white
        @param char : character read from the source code string.
        @return : True if the parameter is White-type character. False if Not.
    '''
    def is_white(self, char):
        return (char is '\n') or (char is ' ') or (char is '\t')


    '''
        @name operator
        @param char : character read from the source code string.
        @return : True if the parameter is operator-type character. False if Not.
    '''
    def is_operator(self, char):
        return (char is '+') or (char is '-') or (char is '*') or (char is '/')


    '''
        @name get_next_character
        @return: The next character from the source code string.
    '''
    def get_next_character(self):
        self.source_content_index = self.source_content_index + 1

        if self.source_content_index >= len(self.source_content) - 1:
            return chr(0)

        if self.source_content[self.source_content_index] is "\n":
            self.current_line = self.current_line + 1
        return self.source_content[self.source_content_index]


    '''
        @name put_character_back
        @functionality: Undoes the get next character action by moving the cursor to the previous position. 
        @return: Null.
    '''
    def put_character_back(self):
        self.source_content_index = self.source_content_index - 1
        if self.source_content[self.source_content_index] is "\n":
            self.current_line = self.current_line - 1


    '''
        @name get_next_state
        @param state: Current state.
        @param char_type: current character type.
        @return: Null.
    '''
    def get_next_state(self, state, char_type):
        if state is 'START':
            return char_type
        elif state is '':
            return


    '''
        @name is_terminal_state
        @param state: state to check if is terminal.
        @return: True if state is terminal. False if Not.
    '''
    def is_terminal_state(self, state):
        if ((state >= Token.ALPHANUM) and (state <= KnownState.COMMENT)) or (state is Error.ERROR_NOT_KNOWN_STATE):
            return True
        return False


    '''
        @name identify_character_type
        @param current_char - Character to be identified.
        @return Character type id. Error if character is not recognizable.
    '''
    def identify_character_type(self, current_char):
        if self.is_alpha(current_char):
            return Type.ALPHA
        elif self.is_num(current_char):
            return Type.NUM
        elif self.is_white(current_char):
            return Type.WHITE
        elif self.is_operator(current_char):
            if current_char is '+' | current_char is "-":
                return Type.ADDOPERATOR
            else:
                return Type.MULTOPERATOR
        elif current_char is '[':
            return Type.LEFTSBRACK
        elif current_char is ']':
            return Type.RIGHTSBRACK
        elif current_char is '{':
            return Type.LEFTCBRACK
        elif current_char is '}':
            return Type.RIGHTCBRACK
        elif current_char is '(':
            return Type.LEFTPAR
        elif current_char is ')':
            return Type.RIGHTPAR
        elif current_char is '<':
            return Type.LESSTHAN
        elif current_char is '>':
            return Type.GREATERTHAN
        elif current_char is '=':
            return Type.EQUALS
        elif current_char is ',':
            return Type.EQUALS
        elif current_char is ';':
            return Type.SEMICOL
        elif current_char is ':':
            return Type.COL
        elif current_char is chr(0):
            return Type.EOF

        return Error.ERROR_NOT_KNOWN_CHARACTER


    '''
        @name lexer

        @functionality :
    '''
    def lexer(self):
        current_state = Token.NT_START
        current_char = ''
        current_char_type = -1
        local_buffer = ''

        while True:
            current_char = self.get_next_character()

            current_char_type = self.identify_character_type(current_char)

            if current_state != Token.NT_COMMENT:
                if current_char is '/':
                    current_char = self.get_next_character()
                    if current_char is '*':
                        current_state = Token.NT_COMMENT
                    else:
                        self.put_character_back()
                        current_char = '/'
            else:
                if current_char is '*':
                    current_char = self.get_next_character()
                    if current_char is '/':
                        current_state = KnownState.COMMENT
                        return current_state
                    else:
                        self.put_character_back()

            current_state = self.get_next_state(current_state, current_char_type)

            if current_state != Token.NT_COMMENT:
                if current_state != Token.WHITE:
                    self.local_buffer += current_char
                else:
                    current_state = Token.NT_START
                    continue

                if self.is_terminal_state(current_state) and current_state != Token.WHITE:
                    if current_state == Token.ALPHANUM:
                        self.put_character_back()
                        self.local_buffer = self.local_buffer[:-1]

                        if buffer in Lang.reserved:
                            current_state = Lang.reserved.index(buffer)
                            return current_state

                    if current_state == Token.NUM:
                        self.put_character_back()
                        self.local_buffer = self.local_buffer[:-1]

                    if current_state == Token.GREATERTHAN or current_state == Token.LESSTHAN:
                        self.put_character_back()

                    self.local_buffer = self.local_buffer[:-1]
                    return current_state
        return Error.ERROR_NOT_KNOWN_STATE

