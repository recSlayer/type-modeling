# -*- coding: utf-8 -*-

from .context import type_checker
from type_checker import *

import unittest

class TypeCheckerTestSuite(unittest.TestCase):

    def test_type_is_its_own_subtype(self):
        self.assert_subtype(JavaType.linked_list, JavaType.linked_list)

    def test_subtype_includes_direct_supertypes(self):
        self.assert_subtype(JavaType.array_list, JavaType.random_access)
        self.assert_not_subtype(JavaType.random_access, JavaType.array_list)

    def test_subtype_includes_indirect_supertypes(self):
        self.assert_subtype(JavaType.linked_list, JavaType.iterable)
        self.assert_not_subtype(JavaType.iterable, JavaType.linked_list)

    def assert_subtype(self, type0, type1):
        self.assertTrue(type0.is_subtype_of(type1))
        self.assertTrue(type1.is_supertype_of(type0))

    def assert_not_subtype(self, type0, type1):
        self.assertFalse(type0.is_subtype_of(type1))
        self.assertFalse(type1.is_supertype_of(type0))

if __name__ == '__main__':
    unittest.main()
