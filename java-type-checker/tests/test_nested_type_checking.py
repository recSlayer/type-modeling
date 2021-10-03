# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest


class TestNestedTypeChecking(TypeTest):
    def test_00_children_get_type_checked_first(self):
        # Equivalent Java:
        #
        #     Rectangle rect;
        #     Color red;
        #
        #     rect.setFillColor(         // Should not report this “Paint ≠ Point” error...
        #         new Point(red, red));  // ...because it detects this type error first
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Point constructor expects arguments of type (double, double), but got (Color, Color)",
            JavaMethodCall(
                JavaVariable("rect", Graphics.rectangle),
                "setFillColor",
                JavaConstructorCall(
                    Graphics.point,
                    JavaVariable("red", Graphics.color),
                    JavaVariable("red", Graphics.color))))

    def test_01_passes_deep_expression(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     group.add(
        #         new Rectangle(
        #             new Point(0, 0),
        #             window.getSize());
        #
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

    def test_02_catches_wrong_name_in_deep_expression(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     group.add(
        #         new Rectangle(
        #             new Point(0, 0),
        #             window.getFunky());  // error here
        #
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

    def test_03_catches_wrong_type_in_deep_expression(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     group.add(
        #         new Rectangle(        // error in this method call...
        #             new Size(0, 0),   // ...because of this arg
        #             window.getSize());
        #
        self.assertCompileError(
            JavaTypeMismatchError,
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

    def test_04_catches_type_error_in_method_call_receiver(self):
        # Equivalent Java:
        #
        #     GraphicsGroup group;
        #     Window window;
        #
        #     new Rectangle(1, 2)  // error here
        #         .getSize().getWidth();
        #
        self.assertCompileError(
            JavaTypeMismatchError,
            "Rectangle constructor expects arguments of type (Point, Size), but got (double, double)",
            JavaMethodCall(
                JavaMethodCall(
                    JavaConstructorCall(
                        Graphics.rectangle,
                        JavaLiteral("1", JavaBuiltInTypes.DOUBLE),
                        JavaLiteral("2", JavaBuiltInTypes.DOUBLE)),
                    "getSize"),
                "getWidth"))
