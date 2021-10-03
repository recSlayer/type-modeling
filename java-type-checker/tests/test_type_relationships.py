# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
import unittest


class TestTypeRelationships(unittest.TestCase):

    def test_00_type_is_its_own_subtype(self):
        self.assert_subtype(Graphics.rectangle, Graphics.rectangle)

    def test_01_subtype_includes_direct_supertypes(self):
        self.assert_subtype(Graphics.graphics_group, Graphics.graphics_object)
        self.assert_subtype(Graphics.rectangle, Graphics.fillable)
        self.assert_not_subtype(Graphics.graphics_object, Graphics.graphics_group)
        self.assert_not_subtype(Graphics.fillable, Graphics.rectangle)

    def test_02_subtype_includes_indirect_supertypes(self):
        self.assert_subtype(Graphics.color, JavaBuiltInTypes.OBJECT)
        self.assert_not_subtype(JavaBuiltInTypes.OBJECT, Graphics.color)

    def test_03_subtype_handles_arbitrary_levels_of_indirection(self):
        deep_subtype = Graphics.rectangle
        for i in range(100):
            unrelated_type = JavaObjectType("UnrelatedType{0}".format(i))
            deep_subtype = JavaObjectType(
                "DeepType{0}".format(i),
                direct_supertypes=[unrelated_type, deep_subtype])
        self.assert_subtype(deep_subtype, Graphics.strokable)

    def test_04_subtype_does_not_include_unrelated_types(self):
        self.assert_not_subtype(Graphics.color, Graphics.point)
        self.assert_not_subtype(Graphics.point, Graphics.color)

    # ––– Helpers –––

    def assert_subtype(self, type0, type1):
        self.assertTrue(type0.is_subtype_of(type1))
        self.assertTrue(type1.is_supertype_of(type0))

    def assert_not_subtype(self, type0, type1):
        self.assertFalse(type0.is_subtype_of(type1))
        self.assertFalse(type1.is_supertype_of(type0))


if __name__ == '__main__':
    unittest.main()
