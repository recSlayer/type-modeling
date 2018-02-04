package plang;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import java.util.Arrays;
import java.util.Collections;

import static org.junit.jupiter.api.Assertions.*;

class PythonObjectTest {

    private PythonType fooType;
    private PythonType barType;
    private PythonObject foo;
    private PythonObject bar;

    /**
     * Equivalent Python:
     *
     *   class Foo:
     *     fooish = "definitely"
     *
     *   class Bar:
     *     barriness = "very"
     *
     *   foo = Foo()
     *   bar = Bar()
     *
     *   foo.color = "greenish orange"
     *   bar.flavor = "ineffable"
     */
    @BeforeEach
    void createTestTypeHierarchy() {
        fooType = new PythonType("Foo", null);
        barType = new PythonType("Bar", fooType);
        foo = fooType.instantiate();
        bar = barType.instantiate();
        foo.set("color", new PythonString("greenish orange"));
        bar.set("flavor", new PythonString("ineffable"));
    }

    @Test
    void findAttrsOnSelf() throws Exception {
        assertEqualsPyStr("greenish orange", foo.get("color"));
        assertEqualsPyStr("ineffable", bar.get("flavor"));
    }

    @Test
    void exceptionWhenAttrNotFound() throws Exception {
        PythonAttributeException error = assertThrows(
            PythonAttributeException.class,
            () -> {
                foo.get("flavor");
            } );

        assertSame(foo, error.getPyObject());
        assertEquals("flavor", error.getAttrName());
    }

    @Test
    void typeMroIncludesSelf() throws Exception {
        assertEquals(
            Collections.singletonList(fooType),
            fooType.getMRO());
    }

    @Test
    void typeMroIncludesBaseClass() throws Exception {
        assertEquals(
            Arrays.asList(barType, fooType),
            barType.getMRO());
    }

    @Test
    void objectMroIncludesType() throws Exception {
        assertEquals(
            Arrays.asList(foo, fooType),
            foo.getMRO());
    }

    @Test
    void objectMroIncludesBaseClass() throws Exception {
        assertEquals(
            Arrays.asList(bar, barType, fooType),
            bar.getMRO());
    }

    @Test
    void findInheritedAttrs() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"   # Type attributes...
        //   foo.socks               # ...show up on instances of the type...
        //   Bar.socks               # ...and on subtypes...
        //   bar.socks               # ...and on instances of subtypes too!

        fooType.set("socks", new PythonString("rainbow"));
        assertEqualsPyStr("rainbow", fooType.get("socks"));
        assertEqualsPyStr("rainbow", foo.get("socks"));
        assertEqualsPyStr("rainbow", barType.get("socks"));
        assertEqualsPyStr("rainbow", bar.get("socks"));
    }

    @Test
    void overrideInheritedAttrsInType() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"
        //   Bar.socks = "polka dot"

        fooType.set("socks", new PythonString("rainbow"));
        barType.set("socks", new PythonString("polka dot"));

        assertEqualsPyStr("rainbow",   fooType.get("socks"));
        assertEqualsPyStr("rainbow",   foo.get("socks"));
        assertEqualsPyStr("polka dot", barType.get("socks"));
        assertEqualsPyStr("polka dot", bar.get("socks"));
    }

    @Test
    void overrideInheritedAttrsInInstance() throws Exception {
        // Equivalent Python:
        //
        //   Foo.socks = "rainbow"
        //   foo.socks = "chartreuse"

        fooType.set("socks", new PythonString("rainbow"));
        foo.set("socks", new PythonString("chartreuse"));

        assertEqualsPyStr("rainbow",    fooType.get("socks"));
        assertEqualsPyStr("chartreuse", foo.get("socks"));
        assertEqualsPyStr("rainbow",    barType.get("socks"));
        assertEqualsPyStr("rainbow",    bar.get("socks"));
    }

    // –––––– Helpers ––––––

    private void assertEqualsPyStr(String str, PythonObject pyobj) {
        assertEquals(str, pyobj.toString());
    }
}