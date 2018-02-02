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
class TestTypes:

    void = JavaType("void")

    boolean = JavaType("boolean")
    int = JavaType("int")
    double = JavaType("double")

    object = JavaClassOrInterface("Object",
        methods=[
            JavaMethod("equals", argumentTypes=[object], returnType=boolean),
            JavaMethod("hashCode", returnType=int),
        ])

    point = JavaClassOrInterface("Point",
        direct_supertypes=[object],
        constructors=[
            JavaConstructor([double, double])
        ],
        methods=[
            JavaMethod("getX", returnType=double),
            JavaMethod("getY", returnType=double),
        ]
    )

    size = JavaClassOrInterface("Size",
        direct_supertypes=[object],
        constructors=[
            JavaConstructor([double, double])
        ],
        methods=[
            JavaMethod("getWidth", returnType=double),
            JavaMethod("getHeight", returnType=double),
        ]
    )

    graphics_object = JavaClassOrInterface("GraphicsObject",
        direct_supertypes=[object],
        methods=[
            JavaMethod("getX", returnType=double),
            JavaMethod("getY", returnType=double),
            JavaMethod("getPosition", returnType=point),
            JavaMethod("setPosition", returnType=void, argumentTypes=[double, double]),
        ]
    )

    paint = JavaClassOrInterface("Paint",
        direct_supertypes=[object]
    )

    color = JavaClassOrInterface("Color",
        direct_supertypes=[paint],
        constructors=[
            JavaConstructor([int, int, int]
        )]
    )

    fill_colorable = JavaClassOrInterface("FillColorable",
        direct_supertypes=[object],
        methods=[
            JavaMethod("setFillColor", returnType=void, argumentTypes=[paint]),
            JavaMethod("getFillColor", returnType=paint),
        ]
    )

    stroke_colorable = JavaClassOrInterface("Colorable",
        direct_supertypes=[object],
        methods=[
            JavaMethod("setStrokeColor", returnType=void, argumentTypes=[paint]),
            JavaMethod("getStrokeColor", returnType=paint),
        ]
    )

    rectangle = JavaClassOrInterface("Rectangle",
        direct_supertypes=[graphics_object, stroke_colorable, fill_colorable],
        constructors=[
            JavaConstructor([double, double, double, double]),
            JavaConstructor([point, size])
        ]
    )

    graphics_group = JavaClassOrInterface("GraphicsGroup",
        direct_supertypes=[graphics_object],
        methods=[
            JavaMethod("add", returnType=void, argumentTypes=[graphics_object]),
        ]
    )

    window = JavaClassOrInterface("Window",
        direct_supertypes=[object],
        methods=[
            JavaMethod("getSize", returnType=size),
        ]
    )
