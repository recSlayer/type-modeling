# -*- coding: utf-8 -*-

from type_checker import *

"""
This file contains types declarations used by the unit tests which model the following
Java structure, loosely modeled after Bret Jackson’s graphics library from COMP 124:

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

    interface FillColorable {
        void setFillColor(Paint fillColor);
        Paint getFillColor();
    }

    interface Colorable {
        void setStrokeColor(Paint strokeColor);
        Paint getStrokeColor();
    }

    class Rectangle extends GraphicsObject implements Colorable, FillColorable {
    }

    class GraphicsGroup extends GraphicsObject implements GraphicsObserver {
        void add(GraphicsObject gObject) { ... }
    }

    class Window {
        Size getSize();
    }
"""


class Graphics:

    point = JavaClassOrInterface("Point",
        direct_supertypes=[JavaType.object],
        constructor=JavaConstructor([JavaType.double, JavaType.double]),
        methods=[
            JavaMethod("getX", return_type=JavaType.double),
            JavaMethod("getY", return_type=JavaType.double),
        ]
    )

    size = JavaClassOrInterface("Size",
        direct_supertypes=[JavaType.object],
        constructor=JavaConstructor([JavaType.double, JavaType.double]),
        methods=[
            JavaMethod("getWidth", return_type=JavaType.double),
            JavaMethod("getHeight", return_type=JavaType.double),
        ]
    )

    graphics_object = JavaClassOrInterface("GraphicsObject",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("getX", return_type=JavaType.double),
            JavaMethod("getY", return_type=JavaType.double),
            JavaMethod("getPosition", return_type=point),
            JavaMethod("setPosition", return_type=JavaType.void, argument_types=[JavaType.double, JavaType.double]),
        ]
    )

    paint = JavaClassOrInterface("Paint",
        direct_supertypes=[JavaType.object]
    )

    color = JavaClassOrInterface("Color",
        direct_supertypes=[paint],
        constructor=JavaConstructor([int, int, int])
    )

    fill_colorable = JavaClassOrInterface("FillColorable",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("setFillColor", return_type=JavaType.void, argument_types=[paint]),
            JavaMethod("getFillColor", return_type=paint),
        ]
    )

    stroke_colorable = JavaClassOrInterface("Colorable",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("setStrokeColor", return_type=JavaType.void, argument_types=[paint]),
            JavaMethod("getStrokeColor", return_type=paint),
        ]
    )

    rectangle = JavaClassOrInterface("Rectangle",
        direct_supertypes=[graphics_object, stroke_colorable, fill_colorable],
        constructor=JavaConstructor([point, size]),
    )

    graphics_group = JavaClassOrInterface("GraphicsGroup",
        direct_supertypes=[graphics_object],
        methods=[
            JavaMethod("add", return_type=JavaType.void, argument_types=[graphics_object]),
        ]
    )

    window = JavaClassOrInterface("Window",
        direct_supertypes=[JavaType.object],
        methods=[
            JavaMethod("getSize", return_type=size),
        ]
    )
