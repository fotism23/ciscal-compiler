#!/usr/bin/python

import getopt
import sys

import intermediate
import lexer
import st
import syntax

err_message = 'test'
input_file_path = ''
output_file_path = ''
source_content = ''
output_content = ''
debug = False

'''
    @name read_input_file
    @functionality: Reads the source file and passes the content into source_content global variable.
    @return: Null
'''


def read_input_file():
    global input_file_path, source_content
    with open(input_file_path, "r") as infile:
        source_content = infile.read().encode("utf8")


def print_err_message():
    global err_message

    print err_message
    sys.exit()


'''
    @name generate_output_file - Generates the output file. 
    @return: Null 
'''


def generate_output_file():
    global output_file_path, output_content


'''
    @name usage - Prints usage to the console.
    @return: Null
'''


def usage():
    print '\nCiscal compiler\n'
    print 'Ciscal compiler in Python language was developed'
    print 'as project assignment for the undergraduate course Compilers'
    print 'of the department of Computer Science & Engineering\nat the University of Ioannina.\n'
    print '(C) Copyright 2017. All rights reserved. Fotios Mitropoulos.'
    print 'Email: cse32486@cs.uoi.gr\n'
    print 'Usage: ciscal.py [options] -i <inputfile> -o <outputfile>'
    print 'Options: -d : Enable Debugging.'
    print '         -h : Show usage.'


def get_program_parameters(argv):
    global input_file_path, output_file_path, debug

    try:
        opts, args = getopt.getopt(argv, "hdi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'ciscal.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            usage()
            sys.exit()
        elif opt == '-d':
            debug = True
        elif opt in ("-i", "--ifile"):
            input_file_path = arg
        elif opt in ("-o", "--ofile"):
            output_file_path = arg

    if debug:
        print 'Input file is ', input_file_path
        print 'Output file is ', output_file_path


def main(argv):
    get_program_parameters(argv)
    read_input_file()

    m_lexer = lexer.Lexer(debug)
    m_lexer.init_lexer(source_content)

    m_symbol = st.Symbol(debug)
    m_inter = intermediate.Intermediate(debug, m_symbol)

    m_syntax = syntax.Syntax(m_lexer, m_symbol, m_inter)
    m_syntax.run_syntax()


if __name__ == "__main__":
    main(sys.argv[1:])
