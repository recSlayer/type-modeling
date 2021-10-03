# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestNull(TypeTest):

    def test_00_object_params_accept_null(self):
        """
        Equivalent Java:

            Rectangle rect;

            rect.setFillColor(null);
        """
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaNullLiteral()))

    def test_01_cannot_call_method_on_null(self):
        """
        Equivalent Java:

            null.hashCode();
        """
        self.assertCompileError(
            NoSuchJavaMethod,  # Think: why shouldn’t this be NullPointerException?
            "Cannot invoke method hashCode() on null",
            JavaMethodCall(
                JavaNullLiteral(),
                "hashCode"))

    def test_02_cannot_instantiate_null(self):
        """
        Equivalent Java:

            new null();
        """
        self.assertCompileError(
            JavaIllegalInstantiationError,
            "Type null is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.NULL))

    def test_03_cannot_pass_null_for_primitive(self):
        """
        Equivalent Java:

            new Point(0.0, null);
        """
        self.assertCompileError(
            JavaTypeMismatchError,
            "Point constructor expects arguments of type (double, double), but got (double, null)",
            JavaConstructorCall(
                Graphics.point,
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaNullLiteral()))

    def test_04_passes_deep_expression(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(null, null);
        """
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaNullLiteral(),
                    JavaNullLiteral())))

    def test_05_catch_wrong_type_in_deep_expression(self):
        """
        Equivalent Java:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Size(null, 0),   // error here
                    window.getSize());
        """
        self.assertCompileError(
            JavaTypeMismatchError,
            "Size constructor expects arguments of type (double, double), but got (null, double)",
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaConstructorCall(
                        Graphics.size,
                        JavaNullLiteral(),
                        JavaLiteral("0", JavaBuiltInTypes.DOUBLE)),
                    JavaMethodCall(
                        JavaVariable("window", Graphics.window),
                        "getSize"))))


if __name__ == '__main__':
    unittest.main()
