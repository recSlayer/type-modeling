# -*- coding: utf-8 -*-

from type_checker import *
from tests.fixtures import TestTypes
import unittest


class TestTypeRelationships(unittest.TestCase):

    def test_type_is_its_own_subtype(self):
        self.assert_subtype(TestTypes.rectangle, TestTypes.rectangle)

    def test_subtype_includes_direct_supertypes(self):
        self.assert_subtype(TestTypes.graphics_group, TestTypes.graphics_object)
        self.assert_not_subtype(TestTypes.graphics_object, TestTypes.graphics_group)

    def test_subtype_includes_indirect_supertypes(self):
        self.assert_subtype(TestTypes.color, TestTypes.object)
        self.assert_not_subtype(TestTypes.object, TestTypes.color)

    # ––– Helpers –––

    def assert_subtype(self, type0, type1):
        self.assertTrue(type0.is_subtype_of(type1))
        self.assertTrue(type1.is_supertype_of(type0))

    def assert_not_subtype(self, type0, type1):
        self.assertFalse(type0.is_subtype_of(type1))
        self.assertFalse(type1.is_supertype_of(type0))

if __name__ == '__main__':
    unittest.main()
