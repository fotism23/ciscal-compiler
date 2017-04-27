#!/usr/bin/python


class Quad(object):
    def __init__(self, operator, x, y, z):
        self.operator = operator
        self.x = x
        self.y = y
        self.z = z
        self.label = None
        self.next = None
        self.prev = None


class BoolAttr(object):
    def __init__(self):
        self.place = ''
        self.true = QuadList("true_list")
        self.false = QuadList("false_list")


class QuadList(object):
    def __init__(self, name):
        self.data = []
        self.name = name
        self.next = None
        self.can_exit = False

    def merge(self, list2):
        self.next = list2


class Intermediate(object):
    def __init__(self, debug, symbol_table):
        self.quad_label = 1
        self.quads = QuadList("main")
        self.quad_list = None
        self.debug = debug
        self.temp_id = 0
        self.symbol_table = symbol_table

    def error_handler(self, message, caller):
        if self.debug:
            print "Caller: " + caller
        print message
        exit(0)

    def next_quad(self):
        return self.quad_label

    def gen_quad(self, operator, x, y, z):
        quad = Quad(operator, x, y, z)
        quad.label = str(self.quad_label)
        self.quad_label = self.quad_label + 1
        self.add_quad(self.quads, quad)
        return quad

    def new_temp(self):
        var_id = 'temp' + str(self.temp_id)
        self.temp_id = self.temp_id + 1
        self.symbol_table.new_variable(var_id, True)
        return var_id

    @staticmethod
    def get_exit_list(m_list):
        while m_list is not None:
            if m_list.can_exit:
                return m_list
            m_list = m_list.next
        return None

    @staticmethod
    def add_quad(quads, quad):
        quads.data.append(quad)

    @staticmethod
    def empty_list(name):
        return QuadList(name)

    @staticmethod
    def empty_quad():
        return Quad(None, None, None, None)

    @staticmethod
    def empty_attr():
        return BoolAttr()

    @staticmethod
    def make_list(x):
        return QuadList(x)

    @staticmethod
    def merge(list1, list2):
        if list1 is None:
            return list2
        elif list2 is None:
            return list1

        while list1.next is not None:
            list1 = list1.next

        list1.next = list2
        return list1

    def back_patch(self, m_list, z):
        temp_list = m_list
        while temp_list is not None:
            quad = self.quads
            while quad is not None:
                if not temp_list.can_exit and quad.name != temp_list.name and quad.z != "_":
                    quad.z = z
                quad = quad.next
            temp_list = temp_list.next

    def generate_file(self):
        with open("icode.ic", "w") as out_file:
            for i in self.quads.data:
                out_file.write(str(i.label) + "\t: " + str(i.operator) + " " + str(i.x) + " " + str(i.y) + " " + str(i.z) + "\n")
            out_file.close()
