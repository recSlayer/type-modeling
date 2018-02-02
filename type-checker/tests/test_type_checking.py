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
        self.assertCompileError(
            NoSuchMethod,
            "Point has no method named getZ",
            MethodCall(
                Variable("p", TestTypes.point),
                "getZ"))

    def test_flags_too_many_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Point.setX(): expected 0, got 2",
            MethodCall(
                Variable("p", TestTypes.point),
                "getX",
                Literal("0", TestTypes.double),
                Literal("0", TestTypes.double)))

    def test_flags_too_few_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Rectangle.setPosition(): expected 2, got 1",
            MethodCall(
                Variable("r", TestTypes.rectangle),
                "setPosition",
                Literal("0", TestTypes.double)))

    def test_flags_wrong_argument_type(self):
        self.assertCompileError(
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

    def test_flags_wrong_number_of_constructor_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Rectangle constructor: expected 2, got 1",
            ConstructorCall(
                TestTypes.rectangle,
                Variable("p", TestTypes.point)))

    def test_flags_wrong_constructor_argument_type(self):
        self.assertCompileError(
            TypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Point, boolean)",
            ConstructorCall(
                TestTypes.rectangle,
                Variable("p", TestTypes.point),
                Literal("true", TestTypes.boolean)))

    def test_passes_deep_expression(self):
        """
        The equivalent Java here is:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Point(0, 0),
                    window.getSize());
        """
        self.assertNoCompileErrors(
            MethodCall(
                Variable("group", TestTypes.graphics_group),
                "add",
                ConstructorCall(
                    TestTypes.rectangle,
                    ConstructorCall(TestTypes.point,
                        Literal("0", TestTypes.double),
                        Literal("0", TestTypes.double)),
                    MethodCall(
                        Variable("window", TestTypes.window),
                        "getSize"))))

    def test_catch_wrong_name_in_deep_expression(self):
        """
        The equivalent Java here is:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Point(0, 0),
                    window.getFunky());  // error here
        """
        self.assertCompileError(
            NoSuchMethod,
            "Window has no method named getFunky",
            MethodCall(
                Variable("group", TestTypes.graphics_group),
                "add",
                ConstructorCall(
                    TestTypes.rectangle,
                    ConstructorCall(TestTypes.point,
                        Literal("0", TestTypes.double),
                        Literal("0", TestTypes.double)),
                    MethodCall(
                        Variable("window", TestTypes.window),
                        "getFunky"))))

    def test_catch_wrong_type_in_deep_expression(self):
        """
        The equivalent Java here is:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Size(0, 0),   // error here
                    window.getSize());
        """
        self.assertCompileError(
            TypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Size, Size)",
            MethodCall(
                Variable("group", TestTypes.graphics_group),
                "add",
                ConstructorCall(
                    TestTypes.rectangle,
                    ConstructorCall(TestTypes.size,
                        Literal("0", TestTypes.double),
                        Literal("0", TestTypes.double)),
                    MethodCall(
                        Variable("window", TestTypes.window),
                        "getSize"))))

    # ––– Helpers –––

    def assertCompileError(self, error, error_message, expr):
        with self.assertRaises(error, msg=error_message):
            expr.check_types()

    def assertNoCompileErrors(self, expr):
        expr.check_types()

if __name__ == '__main__':
    unittest.main()
