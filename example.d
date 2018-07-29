import arsd.simpledisplay;
import arsd.nanovega;
import arsd.color;
import widgets;
import hotload;
import std.stdio: writeln;

void main() {
    NVGContext nvgc;

    setOpenGLContextVersion(3, 0);
    initGlobalThemes();

    auto swnd = new SimpleWindow(1280, 720, "New Style Widgets", OpenGlOptions.yes, Resizability.allowResizing);

    swnd.minWidth = 768;
    swnd.minHeight = 432;

    swnd.onClosing = delegate() { nvgc.kill(); };

    swnd.visibleForTheFirstTime = delegate() {
        nvgc = nvgCreateContext();

        if (nvgc is null)
            assert(0, "Cannot initialize Nanovega context.");
    };

    swnd.redrawOpenGlScene = delegate() {
        glViewport(0, 0, swnd.width, swnd.height);
        glClearColor(0, 0, 0, 0);
        glClear(glNVGClearFlags);

        nvgc.beginFrame(swnd.width, swnd.height);
        scope (exit)
            nvgc.endFrame();

        auto dll = new Module!("example.dll", Symbol!("drawWindow", void function(SimpleWindow, NVGContext)));

        dll.drawWindow(swnd, nvgc);
    };

    swnd.eventLoop(0, delegate(KeyEvent event) {
        if (event == "Escape") {
            swnd.close();
            return;
        }
    });

    flushGui();
}
