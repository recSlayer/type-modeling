# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestTypeChecking(TypeTest):

    def test_variables_never_have_type_errors(self):
        self.assertNoCompileErrors(
            JavaVariable("p", Graphics.point))

    def test_literals_never_have_type_errors(self):
        self.assertNoCompileErrors(
            JavaLiteral("3.72", JavaBuiltInTypes.DOUBLE))

    def test_simple_method_call_passes(self):
        """
        Equivalent Java:

            Point p;

            p.getX()
        """
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getX"))

    def test_flags_nonexistent_method(self):
        """
        Equivalent Java:

            Point p;

            p.getZ()
        """
        self.assertCompileError(
            NoSuchJavaMethod,
            "Point has no method named getZ",
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getZ"))

    def test_flags_too_many_arguments(self):
        """
        Equivalent Java:

            Point p;

            p.getX(0.0, 1.0)
        """
        self.assertCompileError(
            JavaTypeError,
            "Wrong number of arguments for Point.getX(): expected 0, got 2",
            JavaMethodCall(
                JavaVariable("p", Graphics.point),
                "getX",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaLiteral("1.0", JavaBuiltInTypes.DOUBLE)))

    def test_flags_too_few_arguments(self):
        """
        Equivalent Java:

            Rectangle r;

            r.setPosition(0.0)
        """
        self.assertCompileError(
            JavaTypeError,
            "Wrong number of arguments for Rectangle.setPosition(): expected 2, got 1",
            JavaMethodCall(
                JavaVariable("r", Graphics.rectangle),
                "setPosition",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE)))

    def test_flags_wrong_argument_type(self):
        """
        Equivalent Java:

            Rectangle r;

            r.setPosition(0.0, true)
        """
        self.assertCompileError(
            JavaTypeError,
            "Rectangle.setPosition() expects arguments of type (double, double), but got (double, boolean)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setPosition",
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaLiteral("true", JavaBuiltInTypes.BOOLEAN)))

    def test_allows_subtypes_for_arguments(self):
        """
        Equivalent Java:

            Rectangle rect;
            Color red;

            rect.setFillColor(red)
        """
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaVariable("red", Graphics.color)))

    def test_flags_wrong_number_of_constructor_arguments(self):
        """
        Equivalent Java:

            Point p;

            new Rectangle(p)
        """
        self.assertCompileError(
            JavaTypeError,
            "Wrong number of arguments for Rectangle constructor: expected 2, got 1",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point)))

    def test_flags_wrong_constructor_argument_type(self):
        """
        Equivalent Java:

            Point p;

            new Rectangle(p, true)
        """
        self.assertCompileError(
            JavaTypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Point, boolean)",
            JavaConstructorCall(
                Graphics.rectangle,
                JavaVariable("p", Graphics.point),
                JavaLiteral("true", JavaBuiltInTypes.BOOLEAN)))

    def test_cannot_call_methods_on_primitives(self):
        """
        Equivalent Java:

            int x;

            x.hashCode()
        """
        self.assertCompileError(
            JavaTypeError,
            "Type int does not have methods",
            JavaMethodCall(
                JavaVariable("x", JavaBuiltInTypes.INT),
                "hashCode"))

        """
        Equivalent Java:

            new int()
        """
    def test_cannot_instantiate_primitives(self):
        self.assertCompileError(
            JavaTypeError,
            "Type int is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.INT))

    def test_does_not_allow_void_passed_as_argument(self):
        """
        Equivalent Java:

            Rectangle rect;
            Color red;

            rect.setFillColor(              // error here
                rect.setStrokeColor(red));  // returns void
        """
        self.assertCompileError(
            JavaTypeError,
            "Rectangle.setFillColor() expects arguments of type (Paint), but got (void)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaMethodCall(
                    JavaVariable("rect", Graphics.rectangle),
                    "setStrokeColor",
                    JavaVariable("red", Graphics.color))))

    def test_children_get_type_checked_first(self):
        """
        Equivalent Java:

            Rectangle rect;
            Color red;

            rect.setFillColor(         // Should not report this “expected Paint, got Point” error...
                new Point(red, red));  // ...because it detects this type error first
        """
        self.assertCompileError(
            JavaTypeError,
            "Point constructor expects arguments of type (double, double), but got (Color, Color)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaConstructorCall(
                    Graphics.point,
                    JavaVariable("red", Graphics.color),
                    JavaVariable("red", Graphics.color))))

    def test_passes_deep_expression(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Point(0, 0),
                    window.getSize());
        """
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaConstructorCall(Graphics.point,
                                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE)),
                    JavaMethodCall(
                        JavaVariable("window", Graphics.window),
                        "getSize"))))

    def test_catches_wrong_name_in_deep_expression(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Point(0, 0),
                    window.getFunky());  // error here
        """
        self.assertCompileError(
            NoSuchJavaMethod,
            "Window has no method named getFunky",
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaConstructorCall(
                        Graphics.point,
                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE)),
                    JavaMethodCall(
                        JavaVariable("window", Graphics.window),
                        "getFunky"))))

    def test_catches_wrong_type_in_deep_expression(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Size(0, 0),   // error here
                    window.getSize());
        """
        self.assertCompileError(
            JavaTypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (Size, Size)",
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaConstructorCall(
                        Graphics.size,
                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                        JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE)),
                    JavaMethodCall(
                        JavaVariable("window", Graphics.window),
                        "getSize"))))

    def test_catches_type_error_in_method_call_receiver(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            new Rectangle(1, 2)  // error here
                .getSize().getWidth();
        """
        self.assertCompileError(
            JavaTypeError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (double, double)",
            JavaMethodCall(
                JavaMethodCall(
                    JavaConstructorCall(
                        Graphics.rectangle,
                        JavaLiteral("1", JavaBuiltInTypes.DOUBLE),
                        JavaLiteral("2", JavaBuiltInTypes.DOUBLE)),
                    "getSize"),
                "getWidth"))


if __name__ == '__main__':
    unittest.main()
