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

    point = ClassOrInterface("Point",
        direct_supertypes=[Type.object],
        constructor=Constructor([Type.double, Type.double]),
        methods=[
            Method("getX", return_type=Type.double),
            Method("getY", return_type=Type.double),
        ]
    )

    size = ClassOrInterface("Size",
        direct_supertypes=[Type.object],
        constructor=Constructor([Type.double, Type.double]),
        methods=[
            Method("getWidth", return_type=Type.double),
            Method("getHeight", return_type=Type.double),
        ]
    )

    graphics_object = ClassOrInterface("GraphicsObject",
        direct_supertypes=[Type.object],
        methods=[
            Method("getX", return_type=Type.double),
            Method("getY", return_type=Type.double),
            Method("getPosition", return_type=point),
            Method("setPosition", return_type=Type.void, argument_types=[Type.double, Type.double]),
        ]
    )

    paint = ClassOrInterface("Paint",
        direct_supertypes=[Type.object]
    )

    color = ClassOrInterface("Color",
        direct_supertypes=[paint],
        constructor=Constructor([int, int, int])
    )

    fillable = ClassOrInterface("Fillable",
        direct_supertypes=[Type.object],
        methods=[
            Method("setFillColor", return_type=Type.void, argument_types=[paint]),
            Method("getFillColor", return_type=paint),
        ]
    )

    strokable = ClassOrInterface("Strokable",
        direct_supertypes=[Type.object],
        methods=[
            Method("setStrokeColor", return_type=Type.void, argument_types=[paint]),
            Method("getStrokeColor", return_type=paint),
        ]
    )

    rectangle = ClassOrInterface("Rectangle",
        direct_supertypes=[graphics_object, strokable, fillable],
        constructor=Constructor([point, size]),
    )

    graphics_group = ClassOrInterface("GraphicsGroup",
        direct_supertypes=[graphics_object],
        methods=[
            Method("add", return_type=Type.void, argument_types=[graphics_object]),
        ]
    )

    window = ClassOrInterface("Window",
        direct_supertypes=[Type.object],
        methods=[
            Method("getSize", return_type=size),
        ]
    )
