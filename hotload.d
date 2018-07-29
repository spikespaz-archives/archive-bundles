module hotload;

import core.sys.windows.windows;
import std.stdio;
import std.traits;
import std.string;

struct Symbol(const string symbol, func) {
    static immutable name = symbol;
    extern (Windows) alias FunctionType = ReturnType!(func) function(ParameterTypeTuple!(func));
}

private template MixinMembers(symbol, V...) {
    mixin("alias symbol.FunctionType FP_" ~ symbol.name ~ ";");
    mixin("symbol.FunctionType " ~ symbol.name ~ ";");

    static if (V.length > 0)
        mixin MixinMembers!(V);
}

final class Module(const string path, symbols...) {
    private HMODULE mHandle = null;

    public mixin MixinMembers!(symbols);

    public this() {
        load();
        initSymbols();
    }

    public ~this() {
        free();
    }

    private void initSymbols() {
        foreach (i, symbol; symbols) {
            mixin(symbol.name ~ " = getSymbol!(FP_" ~ symbol.name ~ ")(symbol.name);");
        }
    }

    private void load() {
        mHandle = LoadLibraryA(toStringz(path));
        assert(mHandle);
    }

    private void free() {
        FreeLibrary(mHandle);
    }

    public T getSymbol(T)(const string sym) {
        return cast(T) getSymbolAddress(sym);
    }

    public void* getSymbolAddress(const string sym) {
        return GetProcAddress(mHandle, toStringz(sym));
    }
}
