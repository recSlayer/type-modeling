# -*- coding: utf-8 -*-

from type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestNull(TypeTest):

    def test_object_params_accept_null(self):
        self.assertNoCompileErrors(
            MethodCall(
                Variable("rect", Graphics.rectangle),
                "setFillColor",
                NullExpr()))

    def test_cannot_call_method_on_null(self):
        self.assertCompileError(
            NoSuchMethod,  # Think: why shouldn’t this be NullPointerException?
            "null or whatever",
            MethodCall(
                NullExpr(),
                "hashCode"))

    def test_cannot_pass_null_for_primitive(self):
        self.assertCompileError(
            TypeError,
            "null or whatever",
            ConstructorCall(
                Graphics.point,
                Literal("0", JavaType.double),
                NullExpr()))

    def test_passes_deep_expression(self):
        """
        The equivalent Java here is:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(null, null);
        """
        self.assertNoCompileErrors(
            MethodCall(
                Variable("group", Graphics.graphics_group),
                "add",
                ConstructorCall(
                    Graphics.rectangle,
                    NullExpr(),
                    NullExpr())))

    def test_catch_wrong_type_in_deep_expression(self):
        """
        The equivalent Java here is:

            GraphicsGroup group;
            Window window;

            group.add(
                new Rectangle(
                    new Size(null, 0),   // error here
                    window.getSize());
        """
        self.assertCompileError(
            TypeError,
            "Size constructor expects arguments of type (double, double), but got (null, double)",
            MethodCall(
                Variable("group", Graphics.graphics_group),
                "add",
                ConstructorCall(
                    Graphics.rectangle,
                    ConstructorCall(Graphics.size,
                        NullExpr(),
                        Literal("0", JavaType.double)),
                    MethodCall(
                        Variable("window", Graphics.window),
                        "getSize"))))

if __name__ == '__main__':
    unittest.main()
