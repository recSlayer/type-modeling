package plang;

/**
 * Thrown when PythonObject.get() cannot find an attribute.
 */
public class PythonAttributeException extends Exception {
    private final PythonObject pyobject;
    private final String attrName;

    PythonAttributeException(PythonObject pyobject, String attrName) {
        super("AttributeError: '"
            + pyobject.getType().getName()
            + "' object has no attribute '"
            + attrName
            + "'");

        this.pyobject = pyobject;
        this.attrName = attrName;
    }

    public PythonObject getPyObject() {
        return pyobject;
    }

    public String getAttrName() {
        return attrName;
    }
}
