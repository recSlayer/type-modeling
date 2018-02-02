# -*- coding: utf-8 -*-


class Expression(object):
    def static_type(self):
        raise NotImplementedError(type(self).__name__ + " must implement static_type()")

    def check_types(self):
        pass  # no checks by default


class Variable(Expression):
    def __init__(self, name, type):
        self.name = name
        self.type = type

    def static_type(self):
        return self.type

class Literal(Expression):
    def __init__(self, value, type):
        self.value = value
        self.type = type

    def static_type(self):
        return self.type


class MethodCall(Expression):
    def __init__(self, receiver, name, *args):
        self.receiver = receiver
        self.name = name
        self.args = args

    def check_types(self):
        receiver_type = self.receiver.static_type()
        method = receiver_type.method_named(self.name)
        actual_types = [arg.static_type() for arg in self.args]

        if len(method.argument_types) != len(actual_types):
            raise TypeError(
                "Wrong number of arguments for {0}.{1}: expected {2}, got {3}".format(
                    receiver_type.name,
                    self.name,
                    len(method.argument_types),
                    len(actual_types)))

        for(expected_type, actual_type) in zip(method.argument_types, actual_types):
            if not actual_type.is_subtype_of(expected_type):
                raise TypeError(
                    "{0}.{1}() expects arguments of type {2}, but got {3}".format(
                        receiver_type.name,
                        self.name,
                        names(method.argument_types),
                        names(actual_types)))


class TypeError(Exception):
    pass

def names(named_things):
    """ Helper for formatting pretty error messages """
    return "(" + ", ".join([e.name for e in named_things]) + ")"
