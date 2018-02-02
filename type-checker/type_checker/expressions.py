# -*- coding: utf-8 -*-


def check_arg_types(call_name, callable, args):
    for arg in args:
        arg.check_types()

    expected_types = callable.argument_types
    actual_types = [arg.static_type() for arg in args]

    if len(expected_types) != len(actual_types):
        raise TypeError(
            "Wrong number of arguments for {0}: expected {1}, got {2}".format(
                call_name,
                len(expected_types),
                len(actual_types)))

    for(expected_type, actual_type) in zip(expected_types, actual_types):
        if not actual_type.is_subtype_of(expected_type):
            raise TypeError(
                "{0} expects arguments of type {1}, but got {2}".format(
                    call_name,
                    names(expected_types),
                    names(actual_types)))


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
        check_arg_types(
            receiver_type.name + "." + self.name,
            callable=receiver_type.method_named(self.name),
            args=self.args)

    def static_type(self):
        return self.receiver.static_type().method_named(self.name).return_type


class ConstructorCall(Expression):
    def __init__(self, instantiated_type, *args):
        self.instantiated_type = instantiated_type
        self.args = args

    def check_types(self):
        check_arg_types(
            self.instantiated_type.name + " constructor",
            callable=self.instantiated_type.constructor,
            args=self.args)

    def static_type(self):
        return self.instantiated_type



class TypeError(Exception):
    pass

def names(named_things):
    """ Helper for formatting pretty error messages """
    return "(" + ", ".join([e.name for e in named_things]) + ")"
