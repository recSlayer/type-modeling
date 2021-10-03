# -*- coding: utf-8 -*-

from java_type_checker import *
from tests.fixtures import Graphics
from tests.helpers import TypeTest
import unittest


class TestTypeRelationships(TypeTest):

    def test_00_type_is_its_own_subtype(self):
        self.assertSubtype(Graphics.rectangle, Graphics.rectangle)

    def test_01_subtype_includes_direct_supertypes(self):
        self.assertSubtype(Graphics.graphics_group, Graphics.graphics_object)
        self.assertSubtype(Graphics.rectangle, Graphics.fillable)
        self.assertNotSubtype(Graphics.graphics_object, Graphics.graphics_group)
        self.assertNotSubtype(Graphics.fillable, Graphics.rectangle)

    def test_02_subtype_includes_indirect_supertypes(self):
        self.assertSubtype(Graphics.color, JavaBuiltInTypes.OBJECT)
        self.assertNotSubtype(JavaBuiltInTypes.OBJECT, Graphics.color)

    def test_03_subtype_handles_arbitrary_levels_of_indirection(self):
        deep_subtype = Graphics.rectangle
        for i in range(100):
            unrelated_type = JavaObjectType("UnrelatedType{0}".format(i))
            deep_subtype = JavaObjectType(
                "DeepType{0}".format(i),
                direct_supertypes=[unrelated_type, deep_subtype])
        self.assertSubtype(deep_subtype, Graphics.strokable)

    def test_04_subtype_does_not_include_unrelated_types(self):
        self.assertNotSubtype(Graphics.color, Graphics.point)
        self.assertNotSubtype(Graphics.point, Graphics.color)


if __name__ == '__main__':
    unittest.main()
