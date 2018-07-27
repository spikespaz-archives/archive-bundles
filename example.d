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
    nvgc.drawButton("Button", PointF(14f, 54f), SizeF(112f, 26f));
    nvgc.drawButton("Button", PointF(14f, 106f), SizeF(112f, 26f), CENTER_VERTICAL | HOVERED);
    nvgc.drawButton("Button", PointF(14f, 158f), SizeF(112f, 26f), CENTER_VERTICAL | ALIGN_RIGHT | ACTIVE);

    // Draw boxes to show the alignment of text.
    nvgc.beginPath();
    nvgc.strokeColor = NVGColor.black;
    nvgc.strokeWidth = 1;
    nvgc.rect(350f, 100, 150f, 30f);
    nvgc.rect(500f, 100, 150f, 30f);
    nvgc.rect(350f, 150, 150f, 30f);
    nvgc.rect(500f, 150, 150f, 30f);
    nvgc.rect(350f, 200, 150f, 30f);
    nvgc.rect(500f, 200, 150f, 30f);
    nvgc.rect(350f, 250, 150f, 30f);
    nvgc.rect(500f, 250, 150f, 30f);
    nvgc.rect(425f, 300, 150f, 30f);
    nvgc.stroke();

    // Draw all alignments of text labels.
    nvgc.drawTextLabel("Top Left", PointF(350f, 100), SizeF(150f, 30f), ALIGN_TOP | ALIGN_LEFT);
    nvgc.drawTextLabel("Top Right", PointF(500f, 100), SizeF(150f, 30f), ALIGN_TOP | ALIGN_RIGHT);
    nvgc.drawTextLabel("Middle Left", PointF(350f, 150), SizeF(150f, 30f), CENTER_VERTICAL | ALIGN_LEFT);
    nvgc.drawTextLabel("Middle Right", PointF(500f, 150), SizeF(150f, 30f), CENTER_VERTICAL | ALIGN_RIGHT);
    nvgc.drawTextLabel("Bottom Left", PointF(350f, 200), SizeF(150f, 30f), ALIGN_BOTTOM | ALIGN_LEFT);
    nvgc.drawTextLabel("Bottom Right", PointF(500f, 200), SizeF(150f, 30f), ALIGN_BOTTOM | ALIGN_RIGHT);
    nvgc.drawTextLabel("Top Middle", PointF(350f, 250), SizeF(150f, 30f), ALIGN_TOP | CENTER_HORIZONTAL);
    nvgc.drawTextLabel("Bottom Middle", PointF(500f, 250), SizeF(150f, 30f), ALIGN_BOTTOM | CENTER_HORIZONTAL);
    nvgc.drawTextLabel("Center", PointF(425f, 300), SizeF(150f, 30f), CENTER_VERTICAL | CENTER_HORIZONTAL);

}

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
