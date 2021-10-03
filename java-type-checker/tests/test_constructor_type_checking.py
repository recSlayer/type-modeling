# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest


class TestConstructorTypeChecking(TypeTest):
    def test_00_flags_wrong_number_of_constructor_arguments(self):
        # Equivalent Java:
        #
        #     Point p;
        #
        #     new Rectangle(p)
        #
        self.assertCompileError(
            JavaArgumentCountError,
            "Wrong number of arguments for Rectangle constructor: expected 2, got 1",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point)))

    def test_01_flags_wrong_constructor_argument_type(self):
        #
        # Equivalent Java:
        #
        #     Point p;
        #
        #     new Rectangle(p, true)
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Point, boolean)",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point),
                JavaLiteral("true", JavaBuiltInTypes.BOOLEAN)))

    def test_02_cannot_instantiate_primitives(self):
        # Equivalent Java:
        #
        #     new int()
        #
        self.assertCompileError(
            JavaIllegalInstantiationError,
            "Type int is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.INT))

