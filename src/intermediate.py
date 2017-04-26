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
        self.true = QuadList("truelist")
        self.false = QuadList("falselist")


class QuadList(object):
    def __init__(self, name):
        self.next = None
        self.name = name


class Intermediate(object):
    def __init__(self, debug, symbol_table):
        self.quad_label = 1
        self.quads = []
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
        self.add_quad(self.quads, quad)
        return quad

    def new_temp(self):
        var_id = 'temp' + str(self.temp_id)
        self.temp_id = self.temp_id + 1
        self.symbol_table.new_variable(var_id, True)
        return var_id

    @staticmethod
    def add_quad(quads, quad):
        quads.append(quad)

    @staticmethod
    def empty_list():
        return QuadList(None)

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

        list_iterator = list1

        while list_iterator.next is not None:
            list_iterator = list_iterator.next

        list_iterator.next = list2
        return list1

    def backpatch(self, m_list, z):
        temp_list = m_list
        while temp_list is not None:
            quad = self.quads
            while quad is not None:
                quad = quad.next
            temp_list = temp_list.next
