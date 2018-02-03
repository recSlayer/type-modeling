# -*- coding: utf-8 -*-

from type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestTypeChecking(TypeTest):

    def test_simple_method_call_passes(self):
        self.assertNoCompileErrors(
            MethodCall(
                Variable("p", Graphics.point),
                "getX"))

    def test_flags_nonexistent_method(self):
        self.assertCompileError(
            NoSuchMethod,
            "Point has no method named getZ",
            MethodCall(
                Variable("p", Graphics.point),
                "getZ"))

    def test_flags_too_many_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Point.getX(): expected 0, got 2",
            MethodCall(
                Variable("p", Graphics.point),
                "getX",
                Literal("0", JavaType.double),
                Literal("0", JavaType.double)))

    def test_flags_too_few_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Rectangle.setPosition(): expected 2, got 1",
            MethodCall(
                Variable("r", Graphics.rectangle),
                "setPosition",
                Literal("0", JavaType.double)))

    def test_flags_wrong_argument_type(self):
        self.assertCompileError(
            TypeError,
            "Rectangle.setPosition() expects arguments of type (double, double), but got (double, boolean)",
            MethodCall(
                Variable("rect", Graphics.rectangle),
                "setPosition",
                Literal("0", JavaType.double),
                Literal("true", JavaType.boolean)))

    def test_allows_subtypes_for_arguments(self):
        self.assertNoCompileErrors(
            MethodCall(
                Variable("rect", Graphics.rectangle),
                "setFillColor",
                Variable("red", Graphics.color)))

    def test_flags_wrong_number_of_constructor_arguments(self):
        self.assertCompileError(
            TypeError,
            "Wrong number of arguments for Rectangle constructor: expected 2, got 1",
            ConstructorCall(
                Graphics.rectangle,
                Variable("p", Graphics.point)))

    def test_flags_wrong_constructor_argument_type(self):
        self.assertCompileError(
            TypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Point, boolean)",
            ConstructorCall(
                Graphics.rectangle,
                Variable("p", Graphics.point),
                Literal("true", JavaType.boolean)))

    def test_cannot_call_methods_on_primitives(self):
        self.assertCompileError(
            TypeError,
            "Type int does not have methods",
            MethodCall(
                Variable("x", JavaType.int),
                "hashCode"))

    def test_cannot_instantiate_primitives(self):
        self.assertCompileError(
            TypeError,
            "Type int is not instantiable",
            ConstructorCall(
                JavaType.int))

    def test_does_not_allow_void_passed_as_argument(self):
        """
        The equivalent Java here is:

            Rectangle rect;
            Color red;

            rect.setFillColor(              // error here
                rect.setStrokeColor(red));  // returns void
        """
        self.assertCompileError(
            TypeError,
            "Rectangle.setFillColor() expects arguments of type (Paint), but got (void)",
            MethodCall(
                Variable("rect", Graphics.rectangle),
                "setFillColor",
                MethodCall(
                    Variable("rect", Graphics.rectangle),
                    "setStrokeColor",
                    Variable("red", Graphics.color))))

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
                Variable("group", Graphics.graphics_group),
                "add",
                ConstructorCall(
                    Graphics.rectangle,
                    ConstructorCall(Graphics.point,
                        Literal("0", JavaType.double),
                        Literal("0", JavaType.double)),
                    MethodCall(
                        Variable("window", Graphics.window),
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
                Variable("group", Graphics.graphics_group),
                "add",
                ConstructorCall(
                    Graphics.rectangle,
                    ConstructorCall(Graphics.point,
                        Literal("0", JavaType.double),
                        Literal("0", JavaType.double)),
                    MethodCall(
                        Variable("window", Graphics.window),
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
                Variable("group", Graphics.graphics_group),
                "add",
                ConstructorCall(
                    Graphics.rectangle,
                    ConstructorCall(Graphics.size,
                        Literal("0", JavaType.double),
                        Literal("0", JavaType.double)),
                    MethodCall(
                        Variable("window", Graphics.window),
                        "getSize"))))


if __name__ == '__main__':
    unittest.main()
