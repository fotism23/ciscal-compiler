#!/usr/bin/python
from src.consts import Lang


class Code(object):
    def __init__(self, instruction, index):
        self.index = index
        self.instruction = instruction


class Final(object):
    def __init__(self, debug, program_name, symbol_table):
        self.debug = debug
        self.program_name = program_name
        self.code_list = []
        self.lines_generated = 0
        self.current_nesting_level = 0
        self.current_index = 0
        self.symbol_table = symbol_table
        self.arguments = 1

    def error_handler(self, message, caller):
        if self.debug:
            print "Caller: " + caller
        print "Error!!!"
        print message
        exit(0)

    def generate_out_file(self, file_path):
        with open(file_path, "w") as out_file:
            if len(self.code_list) == 0:
                self.error_handler("Code Generator is Empty. Aborting.", "generate_out_file")
            while len(self.code_list) != 0:
                cur_code = self.code_list.pop(0)
                out_file.write(str(cur_code.instruction) + "\n")
        out_file.close()
        print "Final Code generated. Lines : " + str(self.lines_generated)

    def add_machine_code(self, instruction):
        code_obj = Code(instruction, self.current_index)
        self.current_index = self.current_index + 1
        self.code_list.append(code_obj)
        self.lines_generated = self.lines_generated + 1

    def generate_final(self, intermediate):
        print "Generating Final Code"
        quad_lists = intermediate.list_of_quads
        for quad_list in quad_lists:
            for quad in quad_list.data:
                self.add_machine_code(str(quad.label) + ":")

                if quad.operator == "begin_block":
                    temp = self.symbol_table.lookup(quad.x)
                    if temp is None:
                        self.error_handler("quad with label \"" + quad.label + "\" not found", "generate_final")
                    self.current_nesting_level = temp.level
                    if temp.type_data.func_type != Lang.FUNC_TYPE_PROG:
                        self.add_machine_code("sw $ra,($sp)")
                elif quad.operator == "end_block":
                    temp = self.symbol_table.lookup(quad.x)
                    if temp is None:
                        self.error_handler("quad with label \"" + quad.label + "\" not found", "generate_final")
                    if temp.type_data.func_type != Lang.FUNC_TYPE_PROG:
                        self.add_machine_code("lw $ra,($sp)")
                        self.add_machine_code("jr $ra")
                elif quad.operator == "print":
                    self.add_machine_code("li $vo, 1")
                    self.add_machine_code("li $a0, " + quad.z)
                elif quad.operator == ":=":
                    self.loadvr(quad.x, 1)
                    self.storerv(1, quad.z)
                elif quad.operator == "*":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("mul $t1,$t2,$t3")
                    self.storerv(1, quad.z)
                elif quad.operator == "/":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("div $t1,$t2,$t3")
                    self.storerv(1, quad.z)
                elif quad.operator == "+":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("add $t1,$t2,$t3")
                    self.storerv(1, quad.z)
                elif quad.operator == "-":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("sub $t1,$t2,$t3")
                    self.storerv(1, quad.z)
                elif quad.operator == "=":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("beq $t1,$t2," + quad.z)
                elif quad.operator == "<":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("blt $t1,$t2," + quad.z)
                elif quad.operator == ">":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("bgt $t1,$t2," + quad.z)
                elif quad.operator == "<=":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("ble $t1,$t2," + quad.z)
                elif quad.operator == ">=":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("bge $t1,$t2," + quad.z)
                elif quad.operator == "<>":
                    self.loadvr(quad.x, 1)
                    self.loadvr(quad.y, 2)
                    self.add_machine_code("bne $t1,$t2," + quad.z)
                elif quad.operator == "call":
                    func_symbol = self.symbol_table.lookup(quad.x)
                    self.arguments = self.arguments - func_symbol.type_data.get_arg_num()
                    if func_symbol.level == self.current_nesting_level:
                        self.add_machine_code("lw $t0,-4($sp)")
                        self.add_machine_code("sw $t0,04($fp)")
                    else:
                        self.add_machine_code("sw $sp,04($fp)")
                    self.add_machine_code("add $sp,$sp," + str(func_symbol.type_data.frame_length))
                    self.add_machine_code("jal " + quad.x)
                    self.add_machine_code("add $sp,$sp,-" + str(func_symbol.type_data.frame_length))
                elif quad.operator == "par":
                    p = self.symbol_table.lookup(quad.y)
                    if quad.x == "CV":
                        self.loadvr(quad.y, 0)
                        self.add_machine_code("sw $t0, -(12+4*" + str(self.arguments) + ")($fp)")
                        self.arguments = self.arguments + 1
                    elif quad.x == "REF":
                        if self.current_nesting_level == p.offset:
                            if p.type == Lang.TYPE_ARG and p.type_data.arg_type == Lang.PARAMETER_TYPE_IN:
                                self.add_machine_code("add $t0,$sp,-" + p.offset)
                                self.add_machine_code("sw $t0, -(12+4*" + str(self.arguments) + ")($fp)")
                                self.arguments = self.arguments + 1
                            else:
                                self.add_machine_code("lw $t0,-" + p.offset + "($sp)")
                                self.add_machine_code("sw $t0, -(12+4*" + str(self.arguments) + ")($fp)")
                                self.arguments = self.arguments + 1
                        else:
                            if p.type == Lang.TYPE_ARG and p.type_data.arg_type == Lang.PARAMETER_TYPE_IN:
                                self.gnlvcode(quad.y)
                                self.add_machine_code("sw $t0, -(12+4*" + str(self.arguments) + ")($fp)")
                                self.arguments = self.arguments + 1
                            else:
                                self.gnlvcode(quad.y)
                                self.add_machine_code("lw $t0,($t0)")
                                self.add_machine_code("sw $t0, -(12+4*" + str(self.arguments) + ")($fp)")
                                self.arguments = self.arguments + 1
                    else:
                        self.add_machine_code("$t0, $sp, -" + str(p.offset))
                        self.add_machine_code("$t0,-8($fp)")
                elif quad.operator == "halt":
                    pass
                elif quad.operator == "retv":
                    self.loadvr(quad.x, 1)
                    self.add_machine_code("lw $t0,-8($sp)")
                    self.add_machine_code("sw $t1,($t0)")

    def gnlvcode(self, name):
        p = self.symbol_table.lookup(name)
        self.add_machine_code("lw $t0,-4($sp)")

        for i in range(p.level, self.current_nesting_level - 1, 1):
            self.add_machine_code("lw $t0,-4($t0)")

        self.add_machine_code("add $t0,$t0,-" + str(p.offset))

    def loadvr(self, value, reg):
        reg = str(reg)
        if not str.isalpha(value) and value != '$':
            self.add_machine_code("li $t" + reg + "," + value)
        else:
            p = self.symbol_table.lookup(value)
            if p is None:
                p = self.symbol_table.look_for_argument(value)

            if p.level == 1:
                self.add_machine_code("lw $t" + reg + ",-" + str(p.offset) + "($s0)")
            else:
                if p.level == self.current_nesting_level:
                    if p.type == Lang.TYPE_ARG and p.type_data.type == Lang.PARAMETER_TYPE_IN:
                        self.add_machine_code("lw $t0, -" + p.offset + "($sp)")
                        self.add_machine_code("lw $t" + reg + ",($t0)")
                    else:
                        self.add_machine_code("lw $t" + reg + ",-" + str(p.offset) + "($sp)")
                    return
                elif p.level < self.current_nesting_level:
                    self.gnlvcode(p.name)
                    if p.type == Lang.TYPE_ARG and p.type_data.type == Lang.PARAMETER_TYPE_INOUT:
                        self.add_machine_code("lw $t0,($t0)")
                        self.add_machine_code("lw $t" + reg + ",($t0)")
                    else:
                        self.add_machine_code("lw $t" + reg + ",($t0)")
                    return

    def storerv(self, reg, value):
        reg = str(reg)
        p = self.symbol_table.lookup(value)
        if p is None:
            p = self.symbol_table.look_for_argument(value)

        if p.level == 1:
            self.add_machine_code("sw %t" + reg + ",-" + str(p.offset) + "($s0)")
        else:
            if p.level == self.current_nesting_level:
                if p.type == Lang.TYPE_ARG and p.type_data.type == Lang.PARAMETER_TYPE_INOUT:
                    self.add_machine_code("lw $t0,-" + p.offset + "($sp)")
                    self.add_machine_code("sw $t" + reg + ",($t0)")
                else:
                    self.add_machine_code("sw $t" + reg + ",-" + str(p.offset) + "($sp)")
                return
            elif p.level < self.current_nesting_level or p.type == Lang.TYPE_TEMP:
                self.gnlvcode(p.name)
                if p.type == Lang.TYPE_TEMP or (p.type == Lang.TYPE_ARG and p.type_data.type == Lang.PARAMETER_TYPE_INOUT):
                    self.add_machine_code("lw $t0,($t0)")
                    self.add_machine_code("sw $t" + reg + ",($t0)")
                else:
                    self.add_machine_code("sw $t" + reg + ",($t0)")
                return
