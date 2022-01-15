# -*- coding: utf-8 -*-

from java_type_checker import *

"""
This file contains types declarations used by the unit tests which model the following
Java structure, loosely modeled after the kilt-graphics library from COMP 127/128:

    class Point {
        double getX();
        double getY();
        Point(double x, double y);
    }

    class Size {
        double getWidth();
        double getHeight();
        Size(double width, double height);
    }

    class GraphicsObject {
        abstract double getX();
        abstract double getY();
        abstract Point getPosition();
        abstract void setPosition(double x, double y);
    }

    interface Paint {
    }

    class Color implements Paint {
        Color(int r, int g, int b) { ... }
    }

    interface Fillable {
        void setFillColor(Paint fillColor);
        Paint getFillColor();
    }

    interface Strokable {
        void setStrokeColor(Paint strokeColor);
        Paint getStrokeColor();
    }

    class Rectangle extends GraphicsObject implements Strokable, Fillable {
    }

    class GraphicsGroup extends GraphicsObject implements GraphicsObserver {
        void add(GraphicsObject gObject) { ... }
    }

    class Window {
        Size getSize();
    }
"""


class Graphics:
    point = JavaObjectType(
        "Point",
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE])
    )
    point.add_method(JavaMethod("getX", return_type=JavaBuiltInTypes.DOUBLE))
    point.add_method(JavaMethod("getY", return_type=JavaBuiltInTypes.DOUBLE))

    size = JavaObjectType(
        "Size",
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE])
    )
    size.add_method(JavaMethod("getWidth", return_type=JavaBuiltInTypes.DOUBLE))
    size.add_method(JavaMethod("getHeight", return_type=JavaBuiltInTypes.DOUBLE))

    graphics_object = JavaObjectType(
        "GraphicsObject"
    )
    graphics_object.add_method(JavaMethod("getX", return_type=JavaBuiltInTypes.DOUBLE))
    graphics_object.add_method(JavaMethod("getY", return_type=JavaBuiltInTypes.DOUBLE))
    graphics_object.add_method(JavaMethod("getPosition", return_type=point))
    graphics_object.add_method(JavaMethod("setPosition", return_type=JavaBuiltInTypes.VOID,
               argument_types=[JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE]))

    paint = JavaObjectType(
        "Paint"
    )

    color = JavaObjectType(
        "Color",
        direct_supertypes=[paint],
        constructor=JavaConstructor([int, int, int])
    )

    fillable = JavaObjectType(
        "Fillable"
    )
    fillable.add_method(JavaMethod("setFillColor", return_type=JavaBuiltInTypes.VOID, argument_types=[paint]))
    fillable.add_method(JavaMethod("getFillColor", return_type=paint))

    strokable = JavaObjectType(
        "Strokable"
    )
    strokable.add_method(JavaMethod("setStrokeColor", return_type=JavaBuiltInTypes.VOID, argument_types=[paint]))
    strokable.add_method(JavaMethod("getStrokeColor", return_type=paint))

    rectangle = JavaObjectType(
        "Rectangle",
        direct_supertypes=[graphics_object, strokable, fillable],
        constructor=JavaConstructor([point, size])
    )
    rectangle.add_method(JavaMethod("getSize", return_type=size))

    graphics_group = JavaObjectType(
        "GraphicsGroup",
        direct_supertypes=[graphics_object]
    )
    graphics_group.add_method(JavaMethod("add", return_type=JavaBuiltInTypes.VOID, argument_types=[graphics_object]))

    window = JavaObjectType(
        "Window"
    )
    window.add_method(JavaMethod("getSize", return_type=size))
