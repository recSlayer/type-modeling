# -*- coding: utf-8 -*-

from type_checker import *
from tests.fixtures import TestTypes
import unittest


class TestTypeChecking(unittest.TestCase):

    def test_simple_method_call_passes(self):
        self.assertNoCompileErrors(
            MethodCall(
                Variable("p", TestTypes.point),
                "getX"))

    def test_flags_nonexistent_method(self):
        self.assertCompileErrors(
            NoSuchMethod,
            "Point has no method named getZ",
            MethodCall(
                Variable("p", TestTypes.point),
                "getZ"))

    def test_flags_too_many_arguments(self):
        self.assertCompileErrors(
            TypeError,
            "Wrong number of arguments for Point.setX(): expected 0, got 2",
            MethodCall(
                Variable("p", TestTypes.point),
                "getX",
                Literal("0", TestTypes.double),
                Literal("0", TestTypes.double)))

    def test_flags_too_few_arguments(self):
        self.assertCompileErrors(
            TypeError,
            "Wrong number of arguments for Rectangle.setPosition(): expected 2, got 1",
            MethodCall(
                Variable("r", TestTypes.rectangle),
                "setPosition",
                Literal("0", TestTypes.double)))

    def test_flags_wrong_argument_type(self):
        self.assertCompileErrors(
            TypeError,
            "Rectangle.setPosition() expects arguments of type (double, double), but got (double, boolean)",
            MethodCall(
                Variable("rect", TestTypes.rectangle),
                "setPosition",
                Literal("0", TestTypes.double),
                Literal("true", TestTypes.boolean)))

    def test_allows_subtypes_for_arguments(self):
        self.assertNoCompileErrors(
            MethodCall(
                Variable("rect", TestTypes.rectangle),
                "setFillColor",
                Variable("red", TestTypes.color)))

    # ––– Helpers –––

    def assertCompileErrors(self, error, error_message, expr):
        with self.assertRaises(error, msg=error_message):
            expr.check_types()

    def assertNoCompileErrors(self, expr):
        expr.check_types()

if __name__ == '__main__':
    unittest.main()
