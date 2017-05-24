#!/usr/bin/python
from src.consts import Lang


class Quad(object):
    def __init__(self, operator, x, y, z):
        self.operator = operator
        self.x = x
        self.y = y
        self.z = z
        self.label = None


class BoolAttr(object):
    def __init__(self):
        self.place = ''
        self.true = QuadList("true_list")
        self.false = QuadList("false_list")


class QuadList(object):
    def __init__(self, name):
        self.data = []
        self.name = name
        self.can_exit = False
        self.index = -1

    def merge(self, list2):
        self.data.extend(list2.data)

    def add_quad(self, quad):
        self.data.append(quad)


class Intermediate(object):
    def __init__(self, debug, symbol_table):
        self.quad_label = 1
        self.list_of_quads = [QuadList("main")]
        self.current_quad_list_index = 0

        self.debug = debug
        self.temp_id = 0
        self.symbol_table = symbol_table

    def error_handler(self, message, caller):
        if self.debug:
            print "Caller: " + caller
        print "Error!!!"
        print message
        exit(0)

    def next_quad(self):
        return self.quad_label

    def get_next_list(self, m_list):
        if m_list.index >= len(self.list_of_quads) - 1:
            return None
        return self.list_of_quads[m_list.index + 1]

    def set_next_list(self, s_list, m_list):
        self.list_of_quads.insert(s_list.index - 1, m_list)
        for i in range(0, len(self.list_of_quads), 1):
            if m_list is not None:
                self.list_of_quads[i].index = i

    def gen_quad(self, operator, x, y, z):
        quad = Quad(operator, x, y, z)
        quad.label = str(self.quad_label)
        self.quad_label = self.quad_label + 1
        if operator == "begin_block":
            self.list_of_quads[self.current_quad_list_index] = self.make_list(x, quad)
        else:
            self.list_of_quads[self.current_quad_list_index].add_quad(quad)
        # self.list_of_quads(0).add_quad(self.list_of_quads(0), quad)  # todo fix
        # if self.quad_list is None:
        #    self.list_of_quads.append(self.quads)
        return quad

    def new_temp(self):
        var_id = 'temp' + str(self.temp_id)
        self.temp_id = self.temp_id + 1
        self.symbol_table.new_variable(var_id, True)
        return var_id

    def get_exit_list(self, m_list):
        # while m_list is not None:
        i = m_list.index
        for index in range(i, len(self.list_of_quads)):
            m_list = self.list_of_quads[i]
            if m_list.can_exit:
                return m_list
        return None

    @staticmethod
    def empty_list(name):
        return QuadList(name)

    @staticmethod
    def empty_quad():
        return Quad(None, None, None, None)

    @staticmethod
    def empty_attr():
        return BoolAttr()

    def make_list(self, name, element):
        quad_list = self.empty_list(name)
        quad_list.data.append(element)
        quad_list.index = self.current_quad_list_index
        self.list_of_quads.append(quad_list)
        return quad_list

    def go_to_next(self):
        self.current_quad_list_index = self.current_quad_list_index + 1

    @staticmethod
    def merge(list1, list2):
        if list1 is None:
            return list2
        elif list2 is None:
            return list1

        # while list1.next is not None:
        #    list1 = list1.next

        list1.data.extend(list2.data)
        return list1

    def back_patch(self, m_list, z):
        i = m_list.index
        for index in range(i, len(self.list_of_quads)):
            m_list = self.list_of_quads[i]
            for quad in m_list.data:
                if not m_list.can_exit and self.list_of_quads[self.current_quad_list_index].name != m_list.name and quad.z != "_":
                    quad.z = z

    def generate_int_file(self, name):
        print "Generating Intermediate Code."
        with open(name + ".int", "w") as out_file:
            for quad_list in self.list_of_quads:
                for i in quad_list.data:
                    out_file.write("L_" + str(i.label) + ": " + str(i.operator) + " " + str(i.x) + " " + str(i.y) + " " + str(i.z) + "\n")
            out_file.close()
            print "Intermediate code generated.\n"

    def generate_c_code(self, name):
        print "Generating C code."
        with open(name + ".c", "w") as out_file:
            out_file.write("int main() {\n")
            for global_entry in self.symbol_table.global_scope.children_entries:
                if global_entry.type == Lang.TYPE_VAR:
                    out_file.write("\tint " + global_entry.name + ";\n")
            out_file.write("\n")

            for quad_list in self.list_of_quads:
                for i in quad_list.data:
                    if i.operator == ":=":
                        out_file.write("\tL_" + str(i.label) + ": " + str(i.z) + "=" + i.x + ";\n")
                    elif i.operator == "=":
                        out_file.write("\tL_" + str(i.label) + ": if(" + str(i.x) + "==" + str(i.y) + ") goto L_" + str(i.z) + ";\n")
                    elif i.operator == "jump":
                        out_file.write("\tL_" + str(i.label) + ": goto L_" + str(i.z) + ";\n")
                    elif i.operator == "<" or i.operator == ">":
                        out_file.write("\tL_" + str(i.label) + ": if(" + str(i.x) + str(i.operator) + str(i.y) + ") goto L_" + str(i.z) + ";\n")
                    elif i.operator == "print":
                        out_file.write("\tL_" + str(i.label) + ": printf(\"%d\", " + str(i.x) + ");\n")
                    elif i.operator == "+":
                        out_file.write("\tL_" + str(i.label) + ": " + str(i.z) + "=" + str(i.x) + str(i.operator) + str(i.y) + ";\n")

            out_file.write("}")
            out_file.close()
            print "C code generated.\n"
