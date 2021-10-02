# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestStaticTypes(TypeTest):

    def test_variable_static_type_is_its_declared_type(self):
        self.assertEqual(
            Graphics.point,
            JavaVariable("p", Graphics.point).static_type())

    def test_literal_static_type_is_its_type(self):
        self.assertEqual(
            JavaBuiltInTypes.INT,
            JavaLiteral("3", JavaBuiltInTypes.INT).static_type())

    def test_null_literal_static_type_is_null(self):
        self.assertEqual(
            JavaBuiltInTypes.NULL,
            JavaNullLiteral().static_type())

    def test_method_call_static_type_is_method_return_type(self):
        # p.getX() → double
        self.assertEqual(
            JavaBuiltInTypes.DOUBLE,
            JavaMethodCall(JavaVariable("p", Graphics.point), "getX").static_type())

    def test_object_instantiation_static_type_is_the_instantiate_type(self):
        # new Point() → Point
        self.assertEqual(
            Graphics.point,
            JavaConstructorCall(Graphics.point).static_type())

if __name__ == '__main__':
    unittest.main()
