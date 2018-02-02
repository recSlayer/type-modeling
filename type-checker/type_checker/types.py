# -*- coding: utf-8 -*-

class JavaType(object):

    def __init__(self, name, *direct_supertypes):
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

JavaType.int    = JavaType("int")
JavaType.double = JavaType("double")

JavaType.object        = JavaType("Object")
JavaType.string        = JavaType("String",       JavaType.object)
JavaType.iterable      = JavaType("Iterable",     JavaType.object)
JavaType.collection    = JavaType("Collection",   JavaType.iterable)
JavaType.random_access = JavaType("RandomAccess", JavaType.object)
JavaType.list          = JavaType("List",         JavaType.collection)
JavaType.array_list    = JavaType("ArrayList",    JavaType.list, JavaType.random_access)
JavaType.linked_list   = JavaType("LinkedList",   JavaType.list)
