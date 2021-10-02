# -*- coding: utf-8 -*-


class JavaType(object):
    """ Represents any Java type, including both class types and primitives.

    Attributes:
        is_is_object_type: Indicates whether this type includes objects, and can be instantiated.
    """

    is_object_type = False

    def __init__(self, name, direct_supertypes=[]):
        self.name = name

    def is_subtype_of(self, other):
        """ Return True if and only if this type can be used where the give type is expected.

        Subclasses must override this.
        """
        raise NotImplementedError(type(self).__name__ + " must override is_subtype_of()")

    def is_supertype_of(self, other):
        """ Convenience counterpart to is_subtype_of().
        """
        return other.is_subtype_of(self)

    def method_named(self, method_name):
        raise JavaTypeError("Type {0} does not have methods".format(self.name))


class JavaConstructor(object):
    """ The declaration of a Java constructor.
    """
    def __init__(self, argument_types=[]):
        self.argument_types = argument_types


class JavaMethod(object):
    """ The declaration of a Java method.
    """
    def __init__(self, name, argument_types=[], return_type=None):
        self.name = name
        self.argument_types = argument_types
        self.return_type = return_type


class JavaPrimitiveType(JavaType):
    def is_subtype_of(self, other):
        return self == other


class JavaObjectType(JavaType):
    """
    Describes the API of a Java type whose values are objects, i.e. a class or interface.

    (This type model does not draw a distinction between classes and interfaces,
    and assumes they are all instantiable. Other than instantiability, the
    distinction makes no difference to us here: we are only checking types, not
    compiling or executing code, so none of the methods have implementations.)
    """

    is_object_type = True

    def __init__(self, name, direct_supertypes=[], constructor=JavaConstructor([]), methods=[]):
        super().__init__(name)
        self.name = name
        self.direct_supertypes = direct_supertypes
        self.constructor = constructor
        self.methods = {method.name: method for method in methods}

    def is_subtype_of(self, other):
        """ True if this type can be used where the other type is expected.
        """
        return(
            other == self
            or any(t.is_subtype_of(other) for t in self.direct_supertypes))

    def method_named(self, name):
        """ Returns the JavaMethod with the given name, which may come from a supertype.
        """
        try:
            return self.methods[name]
        except KeyError:
            for supertype in self.direct_supertypes:
                try:
                    return supertype.method_named(name)
                except NoSuchJavaMethod:
                    pass
            raise NoSuchJavaMethod("{0} has no method named {1}".format(self.name, name))


class JavaVoidType(JavaType):
    def __init__(self):
        super().__init__("void")

    def is_subtype_of(self, other):
        return False


class JavaNullType(JavaType):
    """ The type of the value `null` in Java.
    """
    def __init__(self):
        super().__init__("null")

    def is_subtype_of(self, other):
        return other.is_object_type

    def method_named(self, method_name):
        raise NoSuchJavaMethod("Cannot invoke method {0}() on {1}".format(method_name, self.name))


class JavaTypeError(Exception):
    """ Indicates a compile-time type error in an expression.
    """
    pass


class NoSuchJavaMethod(Exception):
    pass


# Our simple language’s built-in types

class JavaBuiltInTypes:
    VOID    = JavaVoidType()

    BOOLEAN = JavaPrimitiveType("boolean")
    INT     = JavaPrimitiveType("int")
    DOUBLE  = JavaPrimitiveType("double")

    NULL    = JavaNullType()

    OBJECT = JavaObjectType(
        "Object",
        methods=[
            JavaMethod("equals", argument_types=[], return_type=BOOLEAN),  # have to resolve circular ref after creating
            JavaMethod("hashCode", return_type=INT),
        ]
    )
    OBJECT.methods["equals"].argument_types = [OBJECT]
