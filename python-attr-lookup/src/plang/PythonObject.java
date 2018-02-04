package plang;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PythonObject {
    private final Map<String,PythonObject> attrs = new HashMap<>();
    private final PythonType type;
    private List<PythonObject> mro;

    PythonObject(PythonType type) {
        this.type = type;
    }

    public final PythonType getType() {
        return type;
    }

    protected List<PythonObject> buildMRO() {
        List<PythonObject> result = new ArrayList<>();
        result.add(this);
        result.addAll(getType().getMRO());
        return result;
    }

    public List<PythonObject> getMRO() {
        if(mro == null)
            mro = Collections.unmodifiableList(buildMRO());
        return mro;
    }

    public final PythonObject get(String attrName) throws PythonAttributeException {
        for(PythonObject obj : buildMRO())
            if(obj.attrs.containsKey(attrName))
                return obj.attrs.get(attrName);

        throw new PythonAttributeException(this, attrName);
    }

    public final void set(String attrName, PythonObject value) {
        attrs.put(attrName, value);
    }

    @Override
    public String toString() {
        return "PythonObject<" + getType().getName() + ">" + attrs;
    }
}
