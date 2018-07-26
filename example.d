import arsd.simpledisplay;
import arsd.nanovega;
import arsd.color;
import widgets;
import std.stdio: writeln;

/// Function to draw all implimented widgets to the NanoVega context.
void drawWindow(SimpleWindow swnd, NVGContext nvgc) {
    // Draw the background.
    nvgc.drawBackground(PointF(4f, 4f), SizeF(swnd.width - 8f, swnd.height - 8f));

    // Draw all checkbox states.
    nvgc.drawCheckBox(PointF(14f, 14f), SizeF(14f, 14f), UNCHECKED);
    nvgc.drawCheckBox(PointF(42f, 14f), SizeF(14f, 14f), CHECKED);
    nvgc.drawCheckBox(PointF(70f, 14f), SizeF(14f, 14f), HOVERED);
    nvgc.drawCheckBox(PointF(98f, 14f), SizeF(14f, 14f), ACTIVE);

    // Draw all button states.
    nvgc.drawButton("Button", PointF(14f, 54f), SizeF(112f, 26f), CENTER_HORIZONTAL);
    nvgc.drawButton("Button", PointF(14f, 106f), SizeF(112f, 26f), CENTER_HORIZONTAL | HOVERED);
    nvgc.drawButton("Button", PointF(14f, 158f), SizeF(112f, 26f), CENTER_HORIZONTAL | ACTIVE);
}

void main() {
    NVGContext nvgc;

    setOpenGLContextVersion(3, 0);

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

        drawWindow(swnd, nvgc);
    };

    swnd.eventLoop(0, delegate(KeyEvent event) {
        if (event == "Escape") {
            swnd.close();
            return;
        }
    });

    flushGui();
}
