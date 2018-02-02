# -*- coding: utf-8 -*-

class JavaType(object):

    def __init__(self, name, direct_supertypes = []):
        self.name = name
        self.direct_supertypes = direct_supertypes

    def is_subtype_of(self, other):
        """ True if this type is a direct _or_ indirect subtype of the given other type. """
        return(
            other == self
            or any(t.is_subtype_of(other) for t in self.direct_supertypes))

    def is_supertype_of(self, other):
        """ Convenience counterpart to is_subtype_of. """
        return other.is_subtype_of(self)

class JavaClassOrInterface(JavaType):

    def __init__(self, name, direct_supertypes = [], constructors = [], methods = []):
        super().__init__(name, direct_supertypes)
        self.name = name
        self.methods = { method.name: method for method in methods }

    def method_named(self, name):
        """ Returns the JavaMethod with the given name, which may come from a supertype. """
        try:
            return self.methods[name]
        except KeyError:
            for type in self.direct_supertypes:
                try:
                    return type.method_named(name)
                except NoSuchMethod:
                    pass
            raise NoSuchMethod(name)

class NoSuchMethod(Exception):
    pass

class JavaConstructor(object):
    def __init__(self, argumentTypes=[]):
        self.argumentTypes = argumentTypes

class JavaMethod(object):
    def __init__(self, name, argumentTypes=[], returnType=None):
        self.name = name
        self.argumentTypes = argumentTypes
        self.returnType = returnType
