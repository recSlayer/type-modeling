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

    def test_02_assignments_allow_same_type(self):
        self.assertNoCompileErrors(
            JavaAssignment(
                JavaVariable("x", JavaBuiltInTypes.INT),
                JavaLiteral("1", JavaBuiltInTypes.INT)
            )
        )

    def test_03_assignments_do_not_allow_unrelated_type(self):
        self.assertCompileError(
            JavaTypeMismatchError,
            "Variable x has type int, but right-hand side of assignment has type boolean",
            JavaAssignment(
                JavaVariable("x", JavaBuiltInTypes.INT),
                JavaLiteral("1", JavaBuiltInTypes.BOOLEAN)
            )
        )

    def test_04_assignments_allow_rhs_subtype(self):
        self.assertNoCompileErrors(
            JavaAssignment(
                JavaVariable("f", Graphics.fillable),
                JavaVariable("r", Graphics.rectangle)
            )
        )

    def test_05_assignments_does_not_allow_rhs_supertype(self):
        self.assertCompileError(
            JavaTypeMismatchError,
            "Variable r has type Rectangle, but right-hand side of assignment has type Fillable",
            JavaAssignment(
                JavaVariable("r", Graphics.rectangle),
                JavaVariable("f", Graphics.fillable)
            )
        )


if __name__ == '__main__':
    unittest.main()