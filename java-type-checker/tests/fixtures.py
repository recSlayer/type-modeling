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
        direct_supertypes=[JavaType.object],
        constructor=JavaConstructor([JavaType.double, JavaType.double]),
        methods=[
            JavaMethod("getX", return_type=JavaType.double),
            JavaMethod("getY", return_type=JavaType.double),
        ]
    )

    size = JavaObjectType(
        "Size",
        direct_supertypes=[JavaType.object],
        constructor=JavaConstructor([JavaType.double, JavaType.double]),
        methods=[
            JavaMethod("getWidth", return_type=JavaType.double),
            JavaMethod("getHeight", return_type=JavaType.double),
        ]
    )

    graphics_object = JavaObjectType(
        "GraphicsObject",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("getX", return_type=JavaType.double),
            JavaMethod("getY", return_type=JavaType.double),
            JavaMethod("getPosition", return_type=point),
            JavaMethod("setPosition", return_type=JavaType.void, argument_types=[JavaType.double, JavaType.double]),
        ]
    )

    paint = JavaObjectType(
        "Paint",
        direct_supertypes=[JavaType.object]
    )

    color = JavaObjectType(
        "Color",
        direct_supertypes=[paint],
        constructor=JavaConstructor([int, int, int])
    )

    fillable = JavaObjectType(
        "Fillable",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("setFillColor", return_type=JavaType.void, argument_types=[paint]),
            JavaMethod("getFillColor", return_type=paint),
        ]
    )

    strokable = JavaObjectType(
        "Strokable",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("setStrokeColor", return_type=JavaType.void, argument_types=[paint]),
            JavaMethod("getStrokeColor", return_type=paint),
        ]
    )

    rectangle = JavaObjectType(
        "Rectangle",
        direct_supertypes=[graphics_object, strokable, fillable],
        constructor=JavaConstructor([point, size]),
    )

    graphics_group = JavaObjectType(
        "GraphicsGroup",
        direct_supertypes=[graphics_object],
        methods=[
            JavaMethod("add", return_type=JavaType.void, argument_types=[graphics_object]),
        ]
    )

    window = JavaObjectType(
        "Window",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("getSize", return_type=size),
        ]
    )
