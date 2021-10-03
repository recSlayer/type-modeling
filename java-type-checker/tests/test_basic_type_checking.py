# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestBasicTypeChecking(TypeTest):

    def test_00_variables_never_have_type_errors(self):
        self.assertNoCompileErrors(
            JavaVariable("p", Graphics.point))

    def test_01_literals_never_have_type_errors(self):
        self.assertNoCompileErrors(
            JavaLiteral("3.72", JavaBuiltInTypes.DOUBLE))


if __name__ == '__main__':
    unittest.main()
