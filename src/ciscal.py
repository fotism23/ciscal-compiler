#!/usr/bin/python

import getopt, sys, lexer

err_message = 'test'
input_file_path = ''
output_file_path = ''
source_content = ''


'''
    @name read_input_file

    @functionality : Reads the source file and passes the content into source_content global variable.
    
    @return : Null
'''
def read_input_file():
    global input_file_path, source_content

    with open(input_file_path, "r") as infile:
        source_content = infile.read()

def print_err_message():
    global err_message
    
    print err_message
    sys.exit()

def generate_output_file():
    global output_file_path


def get_program_parameters(argv):
    global input_file_path
    global output_file_path
    
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print 'ciscal.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'ciscal.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file_path = arg
        elif opt in ("-o", "--ofile"):
            output_file_path = arg
    print 'Input file is ', input_file_path
    print 'Output file is ', output_file_path

def main(argv):
    get_program_parameters(argv)
    read_input_file()

    good = lexer.check_grammar(source_content)

    if good == False:
        print_err_message()

if __name__ == "__main__":
    main(sys.argv[1:])
