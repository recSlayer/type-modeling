package plang;

public class PythonString extends PythonObject {
    public static final PythonType TYPE = new PythonType("str", null);
    private final String value;

    public PythonString(String value) {
        super(PythonString.TYPE);
        this.value = value;
    }

    @Override
    public String toString() {
        return value;
    }

    @Override
    public final boolean equals(Object that) {
        if(!(that instanceof PythonString))
            return false;
        return this.value.equals(((PythonString) that).value);
    }

    @Override
    public int hashCode() {
        return value.hashCode();
    }
}
