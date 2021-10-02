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
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE]),
        methods=[
            JavaMethod("getX", return_type=JavaBuiltInTypes.DOUBLE),
            JavaMethod("getY", return_type=JavaBuiltInTypes.DOUBLE),
        ]
    )

    size = JavaObjectType(
        "Size",
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        constructor=JavaConstructor([JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE]),
        methods=[
            JavaMethod("getWidth", return_type=JavaBuiltInTypes.DOUBLE),
            JavaMethod("getHeight", return_type=JavaBuiltInTypes.DOUBLE),
        ]
    )

    graphics_object = JavaObjectType(
        "GraphicsObject",
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        methods=[
            JavaMethod("getX", return_type=JavaBuiltInTypes.DOUBLE),
            JavaMethod("getY", return_type=JavaBuiltInTypes.DOUBLE),
            JavaMethod("getPosition", return_type=point),
            JavaMethod("setPosition", return_type=JavaBuiltInTypes.VOID,
                       argument_types=[JavaBuiltInTypes.DOUBLE, JavaBuiltInTypes.DOUBLE]),
        ]
    )

    paint = JavaObjectType(
        "Paint",
        direct_supertypes=[JavaBuiltInTypes.OBJECT]
    )

    color = JavaObjectType(
        "Color",
        direct_supertypes=[paint],
        constructor=JavaConstructor([int, int, int])
    )

    fillable = JavaObjectType(
        "Fillable",
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        methods=[
            JavaMethod("setFillColor", return_type=JavaBuiltInTypes.VOID, argument_types=[paint]),
            JavaMethod("getFillColor", return_type=paint),
        ]
    )

    strokable = JavaObjectType(
        "Strokable",
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        methods=[
            JavaMethod("setStrokeColor", return_type=JavaBuiltInTypes.VOID, argument_types=[paint]),
            JavaMethod("getStrokeColor", return_type=paint),
        ]
    )

    rectangle = JavaObjectType(
        "Rectangle",
        direct_supertypes=[graphics_object, strokable, fillable],
        constructor=JavaConstructor([point, size]),
        methods=[
            JavaMethod("getSize", return_type=size)
        ]
    )

    graphics_group = JavaObjectType(
        "GraphicsGroup",
        direct_supertypes=[graphics_object],
        methods=[
            JavaMethod("add", return_type=JavaBuiltInTypes.VOID, argument_types=[graphics_object]),
        ]
    )

    window = JavaObjectType(
        "Window",
        direct_supertypes=[JavaBuiltInTypes.OBJECT],
        methods=[
            JavaMethod("getSize", return_type=size),
        ]
    )
