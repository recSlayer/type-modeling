# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestNull(TypeTest):
    def test_00_null_is_object_type(self):
        self.assertEqual(True, JavaBuiltInTypes.NULL.is_object_type)

    def test_01_null_is_not_instantiable(self):
        self.assertEqual(False, JavaBuiltInTypes.NULL.is_instantiable)

    def test_02_null_is_subtype_of_all_object_types(self):
        self.assertSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.OBJECT)
        self.assertSubtype(JavaBuiltInTypes.NULL, Graphics.graphics_group)
        self.assertSubtype(JavaBuiltInTypes.NULL, Graphics.fillable)
        self.assertNotSubtype(JavaBuiltInTypes.OBJECT, JavaBuiltInTypes.NULL)
        self.assertNotSubtype(Graphics.graphics_group, JavaBuiltInTypes.NULL)
        self.assertNotSubtype(Graphics.fillable, JavaBuiltInTypes.NULL)

    def test_03_null_is_subtype_of_itself(self):
        self.assertSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.NULL)

    def test_04_null_is_not_subtype_of_primitives(self):
        self.assertNotSubtype(JavaBuiltInTypes.NULL, JavaBuiltInTypes.INT)
        self.assertNotSubtype(JavaBuiltInTypes.INT, JavaBuiltInTypes.NULL)

    def test_05_object_params_accept_null(self):
        # Equivalent Java:
        #
        #     Rectangle rect;
        #
        #     rect.setFillColor(null);
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaNullLiteral()))

    def test_06_cannot_call_method_on_null(self):
        # Equivalent Java:
        #
        #     null.hashCode();
        #
        self.assertCompileError(
            NoSuchJavaMethod,  # Think: why shouldn’t this be NullPointerException?
            "Cannot invoke method hashCode() on null",  # null provides a special error message
            JavaMethodCall(
                JavaNullLiteral(),
                "hashCode"))

    def test_07_cannot_instantiate_null(self):
        # Equivalent Java:
        #
        #     new null();
        #
        self.assertCompileError(
            JavaIllegalInstantiationError,
            "Type null is not instantiable",
            JavaConstructorCall(
                JavaBuiltInTypes.NULL))

    def test_08_cannot_pass_null_for_primitive(self):
        # Equivalent Java:
        #
        #     new Point(0.0, null);
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Point constructor expects arguments of type (double, double), but got (double, null)",
            JavaConstructorCall(
                Graphics.point,
                JavaLiteral("0.0", JavaBuiltInTypes.DOUBLE),
                JavaNullLiteral()))

    def test_09_passes_deep_expression(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     group.add(
        #         new Rectangle(null, null);
        #
        self.assertNoCompileErrors(
            JavaMethodCall(
                JavaVariable("group", Graphics.graphics_group),
                "add",
                JavaConstructorCall(
                    Graphics.rectangle,
                    JavaNullLiteral(),
                    JavaNullLiteral())))

    def test_10_catch_wrong_type_in_deep_expression(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     group.add(
        #         new Rectangle(
        #             new Size(null, 0),   // error here
        #             window.getSize());
        #
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
