package plang;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;

public class PythonType extends PythonObject {

    private final String name;
    private final PythonObject base;

    public PythonType(String name, PythonObject base) {
        super(null);  // In real Python, the type of a type is “Type”, but that makes this assignment too messy
        this.name = name;
        this.base = base;
    }

    public String getName() {
        return name;
    }

    public PythonObject getBase() {
        return base;
    }

    @Override
    protected List<PythonObject> buildMRO() {
        List<PythonObject> result = new ArrayList<>();
        result.add(this);
        if(getBase() != null)
            result.addAll(getBase().getMRO());
        if(getType() != null)
            result.addAll(getType().getMRO());
        return result;
    }

    public PythonObject instantiate() {
        return new PythonObject(this);
    }

    @Override
    public String toString() {
        return "PythonType<" + name + ">";
    }
}
